#!/usr/bin/env python3
"""Spike 0.14 (plan 11.1): lane tools headless, as the lane identity.

Published as probe/tools_probe.py in GetAI-IP/export-probe (private, scratch),
run by .github/workflows/tools.yml. One subcommand per step:

  flow       a solution-aware cloud flow by the Web API, as getai-fl1-exec:
             make a flow with no connector (a schedule trigger and one Compose
             step) in FactorySpike, update it, turn it on, see it run, turn it
             off. Then try to turn on the existing Dataverse flow and run it.
             Then export and unpack, compare with the reset commit, and pack the
             tree again signed out and with no network
  flow-undo  delete the timer flow and make sure the Dataverse flow is off. A
             safety net only
  summary    write the result table; exit 1 if the step failed

Not a gate script. Never prints a token. Standard library only (python3 -I).
"""

import base64
import difflib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

LOGIN_BASE = "https://login.microsoftonline.com"
API = "/api/data/v9.2"
FLOW_SERVICE = "https://service.flow.microsoft.com"
FLOW_RP = "https://api.flow.microsoft.com"


class ProbeError(Exception):
    pass


def env(name, default=""):
    return os.environ.get(name, default)


SOLUTION = env("SOLUTION", "FactorySpike")
RESET_COMMIT = env("RESET_COMMIT", "reset-commit/FactorySpike")

TIMER_FLOW = "Factory spike timer flow"
MAIN_FLOW = "Factory spike flow"
NOTE = "Spike 0.14 scratch. A flow with no connector, made by the tools probe. Remove after spike 0.14."
WAIT_FOR_RUN_SECONDS = int(env("WAIT_FOR_RUN_SECONDS", "420"))
POLL_SECONDS = 20


def resource():
    return env("ENV_URL").rstrip("/")


def work_dir():
    path = os.path.join(env("RUNNER_TEMP", "/tmp"), "tools-probe", env("MODE", "local"))
    os.makedirs(path, exist_ok=True)
    return path


def clip(text, limit=800):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit] + " ...[cut]"


def summary_write(markdown):
    path = env("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(markdown + "\n")


def save(name, data):
    with open(os.path.join(work_dir(), name), "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, default=str, sort_keys=True)


def bare(guid):
    return (guid or "").strip("{}").lower()


def quote(value):
    return value.replace("'", "''")


# ---------- tokens (never printed) ----------

def github_oidc_token():
    url = env("ACTIONS_ID_TOKEN_REQUEST_URL")
    if not url:
        raise ProbeError("no ACTIONS_ID_TOKEN_REQUEST_URL: the job needs id-token: write")
    url += ("&" if "?" in url else "?") + "audience=" + urllib.parse.quote("api://AzureADTokenExchange", safe="")
    request = urllib.request.Request(url, headers={"Authorization": "Bearer " + env("ACTIONS_ID_TOKEN_REQUEST_TOKEN")})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["value"]


def app_token(audience):
    """Client credentials for one resource, with the GitHub OIDC token as the client assertion."""
    form = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": env("APP_ID"),
        "scope": audience.rstrip("/") + "/.default",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": github_oidc_token(),
    }).encode()
    request = urllib.request.Request(
        f"{LOGIN_BASE}/{env('TENANT_ID')}/oauth2/v2.0/token", data=form,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)["access_token"]
    except urllib.error.HTTPError as error:
        try:
            detail = json.loads(error.read() or b"{}")
        except ValueError:
            detail = {}
        raise ProbeError(f"token request for {audience} failed: HTTP {error.code} {detail.get('error')}: "
                         f"{clip(detail.get('error_description', ''), 400)}") from None


def claim_names(jwt):
    """Which claims the token carries, and the few that say who and what, never the token itself."""
    part = jwt.split(".")[1]
    claims = json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))
    keep = {k: claims.get(k) for k in ("aud", "appid", "idtyp", "roles", "scp") if k in claims}
    return keep


# ---------- HTTP ----------

def http(method, url, token, body=None, headers=None, timeout=300):
    """One call. Returns (status, headers, parsed body or text). Never raises on an HTTP status."""
    url = urllib.parse.quote(url, safe="/:?&=$(),'@*!-._~%+;")
    data = None if body is None else json.dumps(body).encode()
    all_headers = {"Authorization": "Bearer " + token, "Accept": "application/json"}
    if body is not None:
        all_headers["Content-Type"] = "application/json; charset=utf-8"
    all_headers.update(headers or {})
    request = urllib.request.Request(url, data=data, method=method, headers=all_headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status, response_headers, text = response.status, response.headers, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        status, response_headers, text = error.code, error.headers, error.read().decode("utf-8", "replace")
    try:
        parsed = json.loads(text) if text.strip() else {}
    except ValueError:
        parsed = text
    return status, response_headers, parsed


def error_text(parsed):
    if isinstance(parsed, dict):
        err = parsed.get("error") or {}
        if isinstance(err, dict):
            return clip(f"{err.get('code', '')}: {err.get('message', '')}", 600)
    return clip(parsed, 600)


class Dataverse:
    def __init__(self):
        self.token = app_token(resource())
        self.base = resource() + API
        self.writes = []

    def call(self, method, path, body=None, headers=None, ok=(200, 201, 204), timeout=300):
        url = path if path.startswith("http") else self.base + path
        all_headers = {"OData-MaxVersion": "4.0", "OData-Version": "4.0"}
        all_headers.update(headers or {})
        status, response_headers, parsed = http(method, url, self.token, body, all_headers, timeout)
        if method != "GET":
            self.writes.append(f"{method} {path.split('?')[0]} -> {status}")
        if status not in ok:
            raise ProbeError(f"{method} {path.split('?')[0]}: HTTP {status}: {error_text(parsed)}")
        return status, response_headers, parsed

    def get(self, path, ok=(200,)):
        return self.call("GET", path, ok=ok)[2]

    def rows(self, path):
        found = []
        _, _, body = self.call("GET", path, headers={"Prefer": "odata.maxpagesize=5000"})
        found += body.get("value", [])
        while body.get("@odata.nextLink"):
            _, _, body = self.call("GET", body["@odata.nextLink"], headers={"Prefer": "odata.maxpagesize=5000"})
            found += body.get("value", [])
        return found

    def create(self, entity_set, body, solution=None):
        headers = {"MSCRM.SolutionUniqueName": solution} if solution else {}
        _, response_headers, _ = self.call("POST", "/" + entity_set, body, headers)
        entity_id = response_headers.get("OData-EntityId", "")
        match = re.search(r"\(([0-9a-fA-F-]{36})\)\s*$", entity_id)
        return match.group(1) if match else entity_id


# ---------- trees and zips ----------

def tree(folder):
    files = {}
    for here, dirs, names in os.walk(folder):
        dirs[:] = sorted(d for d in dirs if d not in ("bin", "obj", ".git"))
        for name in names:
            path = os.path.join(here, name)
            files[os.path.relpath(path, folder).replace(os.sep, "/")] = path
    return files


def canonical(path):
    with open(path, "rb") as handle:
        data = handle.read()
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return data
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    return "\n".join(lines).strip("\n").encode()


def compare(a, b, label_a, label_b):
    """Compare two trees file by file: raw bytes, then the canonical form."""
    if not (a and b and os.path.isdir(a) and os.path.isdir(b)):
        return {"compared": False, "why": "a tree is missing"}
    left, right = tree(a), tree(b)
    only_a = sorted(set(left) - set(right))
    only_b = sorted(set(right) - set(left))
    raw_diff, canonical_diff, samples = [], [], {}
    for name in sorted(set(left) & set(right)):
        with open(left[name], "rb") as h1, open(right[name], "rb") as h2:
            if h1.read() == h2.read():
                continue
        raw_diff.append(name)
        c1, c2 = canonical(left[name]), canonical(right[name])
        if c1 != c2:
            canonical_diff.append(name)
        if len(samples) < 12:
            try:
                lines = list(difflib.unified_diff(c1.decode().split("\n"), c2.decode().split("\n"),
                                                  label_a, label_b, n=0, lineterm=""))
                samples[name] = [clip(line, 300) for line in lines[2:22]] or ["(differs only in bytes the canonical form drops)"]
            except UnicodeDecodeError:
                samples[name] = ["(binary file differs)"]
    return {"compared": True, "files": len(set(left) | set(right)), "only_in_first": only_a,
            "only_in_second": only_b, "raw_differ": raw_diff, "canonical_differ": canonical_diff,
            "samples": samples,
            "equal_raw": not (only_a or only_b or raw_diff),
            "equal_canonical": not (only_a or only_b or canonical_diff)}


def zip_parts(path):
    if not (path and os.path.isfile(path)):
        return None
    with zipfile.ZipFile(path) as archive:
        names = sorted(archive.namelist())
        roots_found = []
        if "solution.xml" in names:
            text = archive.read("solution.xml").decode("utf-8-sig", "replace")
            roots_found = sorted(re.findall(r"<RootComponent\b[^>]*/>", text))
    return {"names": names, "root_components": roots_found}


def compare_zips(a, b):
    first, second = zip_parts(a), zip_parts(b)
    if not (first and second):
        return {"compared": False}
    return {"compared": True, "same_member_names": first["names"] == second["names"],
            "only_in_first": sorted(set(first["names"]) - set(second["names"])),
            "only_in_second": sorted(set(second["names"]) - set(first["names"])),
            "same_root_components": first["root_components"] == second["root_components"]}


# ---------- pac ----------

STEPS = []


def run(name, argv, cwd=None, allow_fail=True):
    """Run a command, keep its output in a log file, record the step."""
    logs = os.path.join(work_dir(), "logs")
    os.makedirs(logs, exist_ok=True)
    log_path = os.path.join(logs, re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") + ".log")
    started = time.time()
    print(f"\n::group::{name}: {' '.join(argv)}")
    process = subprocess.run(argv, cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, text=True)
    seconds = round(time.time() - started, 1)
    with open(log_path, "w", encoding="utf-8") as handle:
        handle.write(process.stdout)
    print(process.stdout[-6000:])
    print(f"::endgroup::\n{name}: exit {process.returncode} in {seconds} s")
    STEPS.append({"name": name, "command": " ".join(argv), "exit": process.returncode, "seconds": seconds,
                  "tail": clip(process.stdout[-1500:], 1500)})
    if process.returncode != 0 and not allow_fail:
        raise ProbeError(f"{name} failed with exit {process.returncode}")
    return process.returncode == 0


def note(name, ok, seconds=0.0, tail=""):
    STEPS.append({"name": name, "command": "(Web API)", "exit": 0 if ok else 1, "seconds": round(seconds, 1),
                  "tail": clip(tail, 1500)})


def export_unpack(label):
    w = work_dir()
    zip_path = os.path.join(w, f"{label}.zip")
    folder = os.path.join(w, label)
    run(f"export ({label})", ["pac", "solution", "export", "--name", SOLUTION, "--path", zip_path, "--overwrite"],
        allow_fail=False)
    run(f"unpack ({label})", ["pac", "solution", "unpack", "--zipfile", zip_path, "--folder", folder,
                              "--packagetype", "Unmanaged"], allow_fail=False)
    return zip_path, folder


def pack_offline(export_zip, root):
    """Sign out, then pack the tree normally and inside a sandbox with no network (spike 0.18's test)."""
    w = work_dir()
    pack = {}
    run("sign out before pack", ["pac", "auth", "clear"])
    user = env("USER") or subprocess.run(["id", "-un"], capture_output=True, text=True).stdout.strip()
    keep = [f"{k}={env(k)}" for k in ("PATH", "HOME", "DOTNET_ROOT", "DOTNET_CLI_TELEMETRY_OPTOUT", "DOTNET_NOLOGO") if env(k)]
    sandbox = ["sudo", "-n", "unshare", "--net", "--"]
    sandbox_ok = run("no-network sandbox starts", sandbox + ["true"])
    net_down = sandbox_ok and not run("network is down in the sandbox", sandbox + [
        "curl", "-sS", "--max-time", "5", "-o", "/dev/null", LOGIN_BASE])
    pack["no_network_sandbox"] = net_down
    repack = os.path.join(w, "repack.zip")
    pack["pack"] = run("pack the tree, signed out", ["pac", "solution", "pack", "--zipfile", repack, "--folder", root,
                                                      "--packagetype", "Unmanaged"])
    pack["repack_vs_export"] = compare_zips(export_zip, repack)
    run("unpack the repacked zip", ["pac", "solution", "unpack", "--zipfile", repack, "--folder",
                                    os.path.join(w, "repack-unpack"), "--packagetype", "Unmanaged"])
    pack["round_trip"] = compare(root, os.path.join(w, "repack-unpack"), "unpack(export)", "unpack(repack)")
    if net_down:
        nonet = os.path.join(w, "repack-nonet.zip")
        pack["pack_no_network"] = run("pack the tree with no network", sandbox + [
            "sudo", "-n", "-u", user, "env", *keep,
            "pac", "solution", "pack", "--zipfile", nonet, "--folder", root, "--packagetype", "Unmanaged"])
        pack["nonet_vs_export"] = compare_zips(export_zip, nonet)
    return pack


# ---------- flows ----------

def timer_clientdata(text):
    """A cloud flow with no connector: a schedule trigger every minute and one Compose step."""
    return json.dumps({"properties": {"connectionReferences": {}, "definition": {
        "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {"$connections": {"defaultValue": {}, "type": "Object"},
                       "$authentication": {"defaultValue": {}, "type": "SecureObject"}},
        "triggers": {"Recurrence": {"recurrence": {"frequency": "Minute", "interval": 1}, "type": "Recurrence"}},
        "actions": {"Compose": {"runAfter": {}, "metadata": {}, "type": "Compose", "inputs": text}}}},
        "schemaVersion": "1.0.0.0"})


FLOW_FIELDS = "workflowid,workflowidunique,name,statecode,statuscode,clientdata,_ownerid_value,createdon,modifiedon"


def find_flow(dv, name):
    rows = dv.rows(f"/workflows?$select={FLOW_FIELDS}&$filter=name eq '{quote(name)}' and category eq 5")
    return rows[0] if rows else None


def compose_text(flow):
    return json.loads(flow["clientdata"])["properties"]["definition"]["actions"]["Compose"]["inputs"]


def set_state(dv, flow_id, on):
    """Turn a cloud flow on (statecode 1, statuscode 2) or off (0, 1), as FlowAgent's publish does."""
    body = {"statecode": 1, "statuscode": 2} if on else {"statecode": 0, "statuscode": 1}
    started = time.time()
    status, _, parsed = http("PATCH", f"{dv.base}/workflows({flow_id})", dv.token, body,
                             {"If-Match": "*", "OData-MaxVersion": "4.0", "OData-Version": "4.0"})
    dv.writes.append(f"PATCH /workflows({flow_id}) state {'on' if on else 'off'} -> {status}")
    return {"status": status, "ok": status in (200, 204), "seconds": round(time.time() - started, 1),
            "error": None if status in (200, 204) else error_text(parsed)}


def dataverse_runs(dv, flow_id):
    """Runs from the FlowRun elastic table (solution flows only)."""
    fields = "name,status,starttime,endtime,triggertype,errorcode,errormessage,workflowid"
    status, _, parsed = http("GET", f"{dv.base}/flowruns?$select={fields}&$filter=workflowid eq '{flow_id}'",
                             dv.token, headers={"OData-MaxVersion": "4.0", "OData-Version": "4.0"})
    if status == 200:
        return {"status": status, "runs": parsed.get("value", [])}
    return {"status": status, "runs": [], "error": error_text(parsed)}


class FlowService:
    """The Power Automate service API (the classic Flow RP), as FlowAgent's fallback calls it."""

    def __init__(self, env_id):
        self.env_id = env_id
        self.error = None if env_id else "no environment ID"
        self.token = None
        self.claims = {}
        if not env_id:
            return
        try:
            self.token = app_token(FLOW_SERVICE)
            self.claims = claim_names(self.token)
        except ProbeError as error:
            self.error = str(error)

    def call(self, method, path, body=None):
        if not self.token:
            return {"status": None, "error": self.error}
        url = f"{FLOW_RP}/providers/Microsoft.ProcessSimple/environments/{self.env_id}{path}"
        url += ("&" if "?" in url else "?") + "api-version=2016-11-01"
        status, _, parsed = http(method, url, self.token, body)
        result = {"status": status}
        if status not in (200, 201, 202, 204):
            result["error"] = error_text(parsed)
        else:
            result["body"] = parsed
        return result

    def runs(self, flow_name):
        result = self.call("GET", f"/flows/{flow_name}/runs")
        body = result.pop("body", None)
        if isinstance(body, dict):
            result["runs"] = [{"name": r.get("name"), "status": (r.get("properties") or {}).get("status"),
                               "startTime": (r.get("properties") or {}).get("startTime")}
                              for r in body.get("value", [])]
        return result


def wait_for_run(dv, service, flow, seconds):
    """Poll the FlowRun table and the flow service until a run has finished, or time runs out."""
    started = time.time()
    polls = []
    while True:
        from_dv = dataverse_runs(dv, flow["workflowid"])
        from_service = service.runs(flow["workflowidunique"]) if service.token else {"status": None}
        finished = [r for r in from_dv["runs"] if r.get("endtime")] + \
                   [r for r in from_service.get("runs", []) if r.get("status") not in (None, "Running", "Waiting")]
        polls.append({"after_seconds": round(time.time() - started), "dataverse_status": from_dv["status"],
                      "dataverse_runs": len(from_dv["runs"]), "service_status": from_service.get("status"),
                      "service_runs": len(from_service.get("runs", []))})
        if finished or time.time() - started >= seconds:
            return {"finished": bool(finished), "waited_seconds": round(time.time() - started),
                    "dataverse": from_dv, "service": from_service, "polls": polls}
        time.sleep(POLL_SECONDS)


def cmd_flow():
    results = {"mode": "flow", "run_id": env("GITHUB_RUN_ID"), "steps": STEPS}
    dv = Dataverse()
    org = dv.get("/RetrieveCurrentOrganization(AccessType=Microsoft.Dynamics.CRM.EndpointAccessType'Default')")
    env_id = (org.get("Detail") or {}).get("EnvironmentId")
    me = dv.get("/WhoAmI")["UserId"]
    ttl = dv.rows("/organizations?$select=flowruntimetoliveinseconds")[0].get("flowruntimetoliveinseconds")
    results["environment"] = {"environment_id_found": bool(env_id), "flowrun_ttl_seconds": ttl}

    # 1. Make the timer flow in the solution (off), as an agent would build live.
    flow = find_flow(dv, TIMER_FLOW)
    started = time.time()
    if not flow:
        dv.create("workflows", {"category": 5, "type": 1, "primaryentity": "none", "name": TIMER_FLOW,
                                "description": NOTE, "clientdata": timer_clientdata("factory spike timer v1")},
                  solution=SOLUTION)
        flow = find_flow(dv, TIMER_FLOW)
        results["created"] = True
    else:
        results["created"] = False
    note("create the timer flow (Web API, solution header)", bool(flow), time.time() - started)
    if not flow:
        raise ProbeError("the timer flow was not made")
    results["timer_owner_is_lane_identity"] = bare(flow.get("_ownerid_value")) == bare(me)
    solution_id = dv.rows(f"/solutions?$select=solutionid&$filter=uniquename eq '{SOLUTION}'")[0]["solutionid"]
    in_solution = dv.rows(f"/solutioncomponents?$select=objectid&$filter=objectid eq {flow['workflowid']} "
                          f"and _solutionid_value eq {solution_id}")
    results["timer_in_solution"] = bool(in_solution)

    # 2. Update it through the Web API: a changed Compose step.
    started = time.time()
    data = json.loads(flow["clientdata"])
    data["properties"]["definition"]["actions"]["Compose"]["inputs"] = "factory spike timer v2"
    dv.call("PATCH", f"/workflows({flow['workflowid']})", {"clientdata": json.dumps(data)}, {"If-Match": "*"})
    flow = find_flow(dv, TIMER_FLOW)
    results["timer_updated"] = compose_text(flow) == "factory spike timer v2"
    note("update the timer flow (Web API)", results["timer_updated"], time.time() - started)

    # 3. Turn it on, see it run, turn it off.
    service = FlowService(env_id)
    results["flow_service_token"] = {"ok": bool(service.token), "error": service.error, "claims": service.claims}
    results["timer_on"] = set_state(dv, flow["workflowid"], True)
    note("turn the timer flow on", results["timer_on"]["ok"], results["timer_on"]["seconds"], results["timer_on"]["error"] or "")
    flow = find_flow(dv, TIMER_FLOW)
    results["timer_state_after_on"] = [flow.get("statecode"), flow.get("statuscode")]
    if results["timer_on"]["ok"]:
        started = time.time()
        results["timer_run"] = wait_for_run(dv, service, flow, WAIT_FOR_RUN_SECONDS)
        note("wait for the timer flow to run", results["timer_run"]["finished"], time.time() - started)
    results["timer_off"] = set_state(dv, flow["workflowid"], False)
    note("turn the timer flow off", results["timer_off"]["ok"], results["timer_off"]["seconds"], results["timer_off"]["error"] or "")

    # 4. The Dataverse flow: its connection reference has no connection, and the connector is premium.
    main = find_flow(dv, MAIN_FLOW)
    if main:
        results["main_state_before"] = [main.get("statecode"), main.get("statuscode")]
        results["main_on"] = set_state(dv, main["workflowid"], True)
        note("try to turn the Dataverse flow on", results["main_on"]["ok"], results["main_on"]["seconds"],
             results["main_on"]["error"] or "")
        main = find_flow(dv, MAIN_FLOW)
        results["main_state_after_on"] = [main.get("statecode"), main.get("statuscode")]
        if results["main_on"]["ok"] and service.token:
            results["main_manual_run"] = service.call("POST", f"/flows/{main['workflowidunique']}/triggers/manual/run", {})
            results["main_manual_run"].pop("body", None)
            results["main_run"] = wait_for_run(dv, service, main, 180)
        if main.get("statecode") == 1:
            results["main_off"] = set_state(dv, main["workflowid"], False)

    # 5. Export, compare with the reset commit, and pack again signed out and offline.
    zip_path, folder = export_unpack("after")
    results["vs_reset_commit"] = compare(RESET_COMMIT, folder, "reset-commit", "export")
    timer_files = [name for name in tree(folder) if name.lower().startswith("workflows/factoryspiketimerflow")]
    results["timer_files_in_export"] = timer_files
    if timer_files:
        json_file = [n for n in timer_files if n.endswith(".json")]
        if json_file:
            with open(os.path.join(folder, json_file[0]), encoding="utf-8-sig") as handle:
                exported = json.load(handle)
            results["exported_compose"] = exported["properties"]["definition"]["actions"]["Compose"]["inputs"]
    results["pack"] = pack_offline(zip_path, folder)
    results["writes"] = dv.writes

    ran = results.get("timer_run", {}).get("finished", False)
    packs = bool(results["pack"].get("pack")) and results["pack"].get("repack_vs_export", {}).get("same_root_components", False)
    results["exit_test"] = {
        "made_in_solution": results["timer_in_solution"],
        "updated": results["timer_updated"],
        "turned_on": results["timer_on"]["ok"],
        "ran": ran,
        "exported_with_update": results.get("exported_compose") == "factory spike timer v2",
        "packs_signed_out": packs,
        "packs_with_no_network": bool(results["pack"].get("pack_no_network")),
        "round_trip_same": results["pack"].get("round_trip", {}).get("equal_raw", False),
    }
    results["exit_test"]["pass"] = all(results["exit_test"].values())
    save("results.json", results)
    print(json.dumps(results["exit_test"], indent=2))


def cmd_flow_undo():
    dv = Dataverse()
    done = []
    flow = find_flow(dv, TIMER_FLOW)
    if flow:
        if flow.get("statecode") == 1:
            set_state(dv, flow["workflowid"], False)
        dv.call("DELETE", f"/workflows({flow['workflowid']})")
        done.append(f"deleted {TIMER_FLOW}")
    main = find_flow(dv, MAIN_FLOW)
    if main and main.get("statecode") == 1:
        set_state(dv, main["workflowid"], False)
        done.append(f"turned {MAIN_FLOW} off")
    print("Undone: " + (", ".join(done) or "nothing"))
    summary_write("### flow-undo\n\nUndone: " + (", ".join(done) or "nothing") + "\n")


def mark(value):
    return "pass" if value else "FAIL"


def cmd_summary():
    path = os.path.join(work_dir(), "results.json")
    if not os.path.isfile(path):
        summary_write(f"### {env('MODE')}\n\nNo results.json: the step did not finish.\n")
        return 1
    with open(path, encoding="utf-8") as handle:
        results = json.load(handle)
    lines = [f"### {results['mode']}: steps", "", "| Step | Exit | Seconds |", "|---|---|---|"]
    lines += [f"| {s['name']} | {s['exit']} | {s['seconds']} |" for s in results["steps"]]
    lines += ["", "| Check | Result |", "|---|---|"]
    lines += [f"| {k} | {mark(v)} |" for k, v in results.get("exit_test", {}).items()]
    for key in ("flow_service_token", "timer_on", "timer_state_after_on", "main_state_before", "main_on",
                "main_state_after_on", "main_manual_run", "environment"):
        if key in results:
            lines += ["", f"**{key}**: `{json.dumps(results[key], default=str)[:900]}`"]
    for key in ("timer_run", "main_run"):
        if key in results:
            r = results[key]
            lines += ["", f"**{key}**: finished {r['finished']} after {r['waited_seconds']} s; "
                      f"Dataverse {r['dataverse'].get('status')} {json.dumps(r['dataverse'].get('runs'), default=str)[:600]}; "
                      f"service {r['service'].get('status')} {json.dumps(r['service'].get('runs', r['service'].get('error')), default=str)[:600]}"]
    c = results.get("vs_reset_commit", {})
    lines += ["", f"**vs_reset_commit**: only in the commit {c.get('only_in_first')}; only in the export "
              f"{c.get('only_in_second')}; files that differ {c.get('raw_differ')}"]
    for name, sample in list(c.get("samples", {}).items())[:4]:
        lines += [f"`{name}`:", "```diff", *sample, "```"]
    lines += ["", f"## Flow result: **{mark(results.get('exit_test', {}).get('pass'))}**"]
    summary_write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if results.get("exit_test", {}).get("pass") else 1


COMMANDS = {"flow": cmd_flow, "flow-undo": cmd_flow_undo, "summary": cmd_summary}


def main(argv):
    if len(argv) != 2 or argv[1] not in COMMANDS:
        print("usage: tools_probe.py " + "|".join(COMMANDS), file=sys.stderr)
        return 2
    try:
        return COMMANDS[argv[1]]() or 0
    except ProbeError as error:
        print(f"::error::{error}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
