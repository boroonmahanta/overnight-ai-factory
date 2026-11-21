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
  part2      Microsoft's plugins as the lane identity (pinned, telemetry off):
             az login with the job's GitHub OIDC token, then the model-apps
             build engine on a tiny App Spec (lint, dry run, apply, never
             --allow-destructive), then FlowAgent's MCP server called by a small
             client (list, get, update, run the timer flow, read its runs), on
             the Power Platform API path and on the classic fallback. Then
             export and unpack, compare, and pack again signed out and offline
  part3      the MCP count-and-retry shim (mcp_shim.py) in front of the Dataverse
             CLI's local proxy, signed in as the lane identity: three short
             sessions of a scripted client against FactorySpike (reads, one create
             on the spike table, a bad query, a create on a table that does not
             exist, a call past the cap, and creates whose answer the shim drops
             before it retries). Every row it makes is named "spike-0.14 part3
             (...)" and is deleted by the Web API at the end
  part4      the skills in `copilot -p` (Copilot CLI pinned, Microsoft's plugins pinned,
             unattended, telemetry off), with the shim in front of Dataverse MCP: two
             tiny stories in FactorySpike, one session each (an App Spec change to the
             existing app; a change to the timer flow's Compose step, the flow left off).
             Then export and unpack, compare, and pack again signed out and offline
  part4b     option (b) for part 4's App Spec story (Session 29): the same additive change to the existing
             app without the App Spec build engine, in one `copilot -p` session: the column by Dataverse
             MCP update_table (through the shim), the form and view by the Web API through the trusted
             helper webapi.py, then PublishXml. Export before and after, compare, pack again offline
  part4b-undo  take part 4b's change out of the lane by the Web API: the column off the table's forms
             and views (published), then the column. Deletes nothing if any row holds a value in it
  scan       delete any output file that holds a token-shaped string (before upload)
  summary    write the result table; exit 1 if the step failed

Not a gate script. Never prints a token. Standard library only (python3 -I).
"""

import base64
import difflib
import hashlib
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
from xml.etree import ElementTree

LOGIN_BASE = os.environ.get("LOGIN_BASE", "https://login.microsoftonline.com")   # local checks point it at a fake
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
JWT = re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]*")


def redact(text):
    """Belt and braces: no token-shaped string reaches a log, the summary or the artifact."""
    return JWT.sub("[token removed]", text or "")


def log_path_for(name, suffix=".log"):
    logs = os.path.join(work_dir(), "logs")
    os.makedirs(logs, exist_ok=True)
    return os.path.join(logs, re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") + suffix)


def run(name, argv, cwd=None, allow_fail=True, extra_env=None, timeout=None, shown=None):
    """Run a command, keep its output in a log file, record the step. `shown` replaces the command in the record."""
    started = time.time()
    shown = shown or " ".join(argv)
    print(f"\n::group::{name}: {shown}")
    child_env = dict(os.environ, **(extra_env or {}))
    try:
        process = subprocess.run(argv, cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, text=True, env=child_env, timeout=timeout)
        code, output = process.returncode, redact(process.stdout)
    except subprocess.TimeoutExpired as error:
        code, output = 124, redact((error.stdout or b"").decode("utf-8", "replace") if isinstance(error.stdout, bytes)
                                   else (error.stdout or "")) + f"\n[timed out after {timeout} s]"
    seconds = round(time.time() - started, 1)
    with open(log_path_for(name), "w", encoding="utf-8") as handle:
        handle.write(output)
    print(output[-6000:])
    print(f"::endgroup::\n{name}: exit {code} in {seconds} s")
    STEPS.append({"name": name, "command": shown, "exit": code, "seconds": seconds, "tail": clip(output[-1500:], 1500)})
    if code != 0 and not allow_fail:
        raise ProbeError(f"{name} failed with exit {code}")
    return code == 0


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


# ---------- part 2: Microsoft's plugins as the lane identity ----------
#
# Microsoft's power-platform-skills, pinned by the workflow and run unread for this spike only
# (Boroon, 18 November 2026). Both plugins take every token from `az account get-access-token`, so
# the Azure CLI is signed in as getai-fl1-exec with the job's GitHub OIDC token, the same federated
# credential pac uses.

PPS_ROOT = env("PPS_ROOT")
MODEL_APPS = os.path.join(PPS_ROOT, "plugins", "model-apps")
POWER_AUTOMATE = os.path.join(PPS_ROOT, "plugins", "power-automate")
APP_TABLE = "fspk_spikeapprow"
APP_NAME = "Factory spike app"
SCRATCH = "Spike 0.14 scratch, made by the App Spec build engine as the lane identity. Remove after spike 0.14."
# A host that never resolves (.invalid): FlowAgent falls back to the classic flow service on ENOTFOUND.
FALLBACK_TEMPLATE = "https://{prefix}.{shard}.spike-fallback.invalid"

APP_SPEC = {
    "solution": {"uniqueName": SOLUTION, "displayName": "Factory spike", "publisherPrefix": "fspk"},
    "app": {"name": APP_NAME, "description": SCRATCH},
    "entities": [{
        "schemaName": APP_TABLE, "displayName": "Spike app row", "pluralName": "Spike app rows",
        "description": SCRATCH,
        "primaryAttribute": {"schemaName": "fspk_name", "displayName": "Name"},
        "columns": [{"schemaName": "fspk_note", "displayName": "Note", "type": "Text",
                     "description": "A free-text note on a spike app row."}],
    }],
    "relationships": [],
    "forms": [{"entity": APP_TABLE, "type": "main", "name": "Spike app row", "layout": "auto",
               "description": "The main form for a spike app row."}],
    "views": [{"entity": APP_TABLE, "name": "Active spike app rows", "columns": ["fspk_name", "fspk_note"],
               "sort": [{"attr": "fspk_name", "dir": "asc"}], "activeOnly": True,
               "description": "Active spike app rows, by name."}],
    "appShell": {"areas": [{"label": "Spike", "groups": [{"label": "Rows", "subAreas": [{"entity": APP_TABLE}]}]}]},
}

COMPONENT_TYPES = {1: "table", 2: "column", 3: "relationship", 9: "choice", 10: "table relationship", 20: "security role",
                   26: "view", 29: "process or flow", 59: "chart", 60: "form", 61: "web resource", 62: "site map",
                   80: "model-driven app", 372: "connection reference", 380: "environment variable definition",
                   381: "environment variable value"}


def node_env():
    """What every plugin process gets: no user waiting, telemetry off. The job sets the same."""
    return {"POWER_PLATFORM_SKILLS_NONINTERACTIVE": "1",
            "POWER_PLATFORM_SKILLS_TELEMETRY": "0",
            "POWER_PLATFORM_SKILLS_TELEMETRY_MODEL_APPS_OPTOUT": "1",
            "POWER_PLATFORM_SKILLS_TELEMETRY_POWER_AUTOMATE_OPTOUT": "1",
            "FLOWAGENT_TELEMETRY": "0",
            "FLOWAGENT_DISABLE_DISK_CACHE": "1",
            "PA_CLOUD": "commercial"}


def jwt_claims(token):
    part = token.split(".")[1]
    return json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))


def as_text(value):
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    return value or ""


def tool_versions():
    found = {}
    for name, argv in (("node", ["node", "--version"]), ("az", ["az", "version", "--output", "json"])):
        try:
            process = subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired) as error:
            found[name] = f"not run: {error}"
            continue
        if name == "az":
            try:
                found[name] = json.loads(process.stdout or "{}").get("azure-cli")
            except ValueError:
                found[name] = None
        else:
            found[name] = process.stdout.strip()
    for plugin, folder in (("model-apps", MODEL_APPS), ("power-automate", POWER_AUTOMATE)):
        try:
            with open(os.path.join(folder, ".claude-plugin", "plugin.json"), encoding="utf-8") as handle:
                found[plugin] = json.load(handle).get("version")
        except (OSError, ValueError):
            found[plugin] = None
        try:
            with open(os.path.join(folder, "scripts", "lib", "telemetry", "ikey.json"), encoding="utf-8") as handle:
                found[plugin + " telemetry disabled"] = json.load(handle).get("disabled") is True
        except (OSError, ValueError):
            found[plugin + " telemetry disabled"] = None
    process = subprocess.run(["git", "-C", PPS_ROOT, "rev-parse", "HEAD"], capture_output=True, text=True)
    found["power-platform-skills head"] = process.stdout.strip()
    found["head is the pin"] = bool(env("PPS_COMMIT")) and process.stdout.strip() == env("PPS_COMMIT")
    return found


def az_login(label):
    """Sign the Azure CLI in as the lane identity with a fresh GitHub OIDC token. The token is never shown."""
    try:
        assertion = github_oidc_token()
    except (ProbeError, OSError, ValueError) as error:
        note(f"az login ({label})", False, 0, f"no GitHub OIDC token: {error}")
        return {"ok": False, "error": clip(error, 300)}
    claims = jwt_claims(assertion)
    ok = run(f"az login ({label})",
             ["az", "login", "--service-principal", "--username", env("APP_ID"), "--tenant", env("TENANT_ID"),
              "--federated-token", assertion, "--allow-no-subscriptions", "--output", "none"],
             shown="az login --service-principal --username <app id> --tenant <tenant id> "
                   "--federated-token <GitHub OIDC token> --allow-no-subscriptions --output none", timeout=180)
    return {"ok": ok, "oidc_token_lifetime_seconds": claims.get("exp", 0) - claims.get("iat", 0)}


def az_account():
    process = subprocess.run(["az", "account", "show", "--output", "json"], stdin=subprocess.DEVNULL,
                             capture_output=True, text=True, timeout=120)
    if process.returncode != 0:
        return {"ok": False, "error": clip(redact(process.stderr), 400)}
    data = json.loads(process.stdout)
    user = data.get("user") or {}
    return {"ok": True, "user_type": user.get("type"), "user_is_lane_app": user.get("name") == env("APP_ID"),
            "tenant_matches": data.get("tenantId") == env("TENANT_ID"), "account_name": data.get("name")}


def az_token(resource_url):
    """One `az account get-access-token`, as both plugins call it. Keeps whether it worked and which claims, never the token."""
    started = time.time()
    process = subprocess.run(["az", "account", "get-access-token", "--resource", resource_url, "--output", "json"],
                             stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=120)
    result = {"seconds": round(time.time() - started, 1)}
    if process.returncode != 0:
        result.update(ok=False, error=clip(redact(process.stderr), 500))
        return result
    data = json.loads(process.stdout)
    token = data.get("accessToken") or ""
    result.update(ok=bool(token), expires_on=data.get("expiresOn"))
    try:
        result["claims"] = claim_names(token)
    except (IndexError, ValueError):
        result["claims"] = "not a JWT"
    return result


def az_tokens():
    return {name: az_token(url) for name, url in (
        ("dataverse", resource()), ("dataverse with slash", resource() + "/"),
        ("power apps service", "https://service.powerapps.com/"), ("flow service", FLOW_SERVICE),
        ("power platform api", "https://api.powerplatform.com"))}


def last_json(text):
    """The JSON result a plugin script prints last on stdout."""
    text = (text or "").strip()
    try:
        return json.loads(text)
    except ValueError:
        pass
    lines = text.split("\n")
    for start in range(len(lines) - 1, -1, -1):
        if lines[start].startswith("{") or lines[start].startswith("["):
            try:
                return json.loads("\n".join(lines[start:]))
            except ValueError:
                continue
    return None


def node_run(name, argv, cwd, timeout):
    """Run one plugin script with its stdout (its JSON result) and stderr (its progress) kept apart."""
    shown = " ".join(argv).replace(MODEL_APPS, "<model-apps>").replace(work_dir(), "<work>")
    started = time.time()
    print(f"\n::group::{name}: {shown}")
    try:
        process = subprocess.run(argv, cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                                 env=dict(os.environ, **node_env()), timeout=timeout)
        code, out, err = process.returncode, redact(process.stdout), redact(process.stderr)
    except subprocess.TimeoutExpired as error:
        code, out = 124, redact(as_text(error.stdout))
        err = redact(as_text(error.stderr)) + f"\n[timed out after {timeout} s]"
    seconds = round(time.time() - started, 1)
    with open(log_path_for(name, ".stdout.log"), "w", encoding="utf-8") as handle:
        handle.write(out)
    with open(log_path_for(name, ".stderr.log"), "w", encoding="utf-8") as handle:
        handle.write(err)
    print(err[-6000:])
    print(out[-3000:])
    print(f"::endgroup::\n{name}: exit {code} in {seconds} s")
    STEPS.append({"name": name, "command": shown, "exit": code, "seconds": seconds,
                  "tail": clip((err + "\n" + out)[-1500:], 1500)})
    result = last_json(out)
    return {"exit": code, "seconds": seconds, "result": clip(json.dumps(result, default=str), 3000) if result else None,
            "stderr_tail": clip(err[-3000:], 3000)}


def solution_parts(dv, solution_id):
    rows = dv.rows(f"/solutioncomponents?$select=objectid,componenttype&$filter=_solutionid_value eq {solution_id}")
    return sorted({(row["componenttype"], bare(row["objectid"])) for row in rows})


def app_spec_part(dv, solution_id):
    """Lint, dry run, then apply the tiny App Spec, as /app-builder's unattended mode does. Never --allow-destructive."""
    out = {}
    folder = os.path.join(work_dir(), "app-spec")
    os.makedirs(folder, exist_ok=True)
    spec_path = os.path.join(folder, "app-spec.json")
    with open(spec_path, "w", encoding="utf-8") as handle:
        json.dump(APP_SPEC, handle, indent=2)
    scripts = os.path.join(MODEL_APPS, "scripts")
    build = ["node", os.path.join(scripts, "build-model-app.js"), "--env", resource(), "--spec", "@" + spec_path]
    before = solution_parts(dv, solution_id)
    try:
        out["lint"] = node_run("App Spec lint", ["node", os.path.join(scripts, "lint-app-spec.js"), "--spec",
                                                 "@" + spec_path, "--json"], folder, 300)
        if out["lint"]["exit"] != 0:
            out["stopped_at"] = "lint"           # lint errors block, as in the skill
            return out
        out["dry_run"] = node_run("App Spec build, dry run", build + ["--non-interactive"], folder, 900)
        if out["dry_run"]["exit"] != 0:
            out["stopped_at"] = "dry run"        # the dry run is the unattended approval
            return out
        out["apply"] = node_run("App Spec build, apply", build + ["--apply", "--verify", "--publish", "--non-interactive"],
                                folder, 1800)
        if out["apply"]["exit"] != 0:
            out["stopped_at"] = "apply"
    finally:
        try:
            after = solution_parts(dv, solution_id)
            out["solution_parts_added"] = [{"type": COMPONENT_TYPES.get(t, str(t)), "id": i} for t, i in after if (t, i) not in before]
            out["solution_parts_removed"] = [{"type": COMPONENT_TYPES.get(t, str(t)), "id": i} for t, i in before if (t, i) not in after]
            status, _, table = dv.call("GET", f"/EntityDefinitions(LogicalName='{APP_TABLE}')?$select=LogicalName,SchemaName,IsManaged",
                                       ok=(200, 404))
            out["table_exists"] = status == 200
            apps = dv.rows(f"/appmodules?$select=appmoduleid,uniquename,name,publishedon&$filter=name eq '{quote(APP_NAME)}'")
            out["apps_found"] = [{"uniquename": a.get("uniquename"), "published_on": a.get("publishedon")} for a in apps]
        except ProbeError as error:
            out["read_back_error"] = str(error)
    return out


class McpClient:
    """A small stdio MCP client: newline-delimited JSON-RPC, one request at a time, every tools/call counted."""

    def __init__(self, label, argv, cwd, extra_env, log_name=None):
        self.label = label
        self.stderr_path = log_path_for(log_name or f"flowagent {label}", ".stderr.log")
        self.stderr_file = open(self.stderr_path, "w", encoding="utf-8")
        self.process = subprocess.Popen(argv, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=self.stderr_file, text=True, bufsize=1,
                                        env=dict(os.environ, **extra_env))
        self.lines = queue.Queue()
        threading.Thread(target=self._read, daemon=True).start()
        self.next_id = 0
        self.calls = []
        self.server_requests = []

    def _read(self):
        for line in self.process.stdout:
            self.lines.put(line)
        self.lines.put(None)

    def send(self, message):
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

    def request(self, method, params=None, timeout=120):
        self.next_id += 1
        request_id = self.next_id
        message = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            message["params"] = params
        self.send(message)
        deadline = time.time() + timeout
        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                raise ProbeError(f"{method}: no answer in {timeout} s")
            try:
                line = self.lines.get(timeout=remaining)
            except queue.Empty:
                continue
            if line is None:
                raise ProbeError(f"{method}: the server closed its output (exit {self.process.poll()})")
            try:
                answer = json.loads(line)
            except ValueError:
                continue
            if not isinstance(answer, dict):
                continue
            if "method" in answer and "id" in answer:
                # A request from the server (sampling, roots, elicitation): the spike client offers none.
                self.server_requests.append(answer.get("method"))
                self.send({"jsonrpc": "2.0", "id": answer["id"],
                           "error": {"code": -32601, "message": "not offered by the spike client"}})
                continue
            if answer.get("id") == request_id:
                if "error" in answer:
                    raise ProbeError(f"{method}: JSON-RPC error {clip(json.dumps(answer['error']), 400)}")
                return answer.get("result") or {}

    def notify(self, method, params=None):
        message = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            message["params"] = params
        self.send(message)

    def start(self):
        init = self.request("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                           "clientInfo": {"name": "spike-0.14-probe", "version": "0.1"}}, timeout=180)
        self.notify("notifications/initialized")
        tools = self.request("tools/list", {}, timeout=120)
        return init, tools

    def call(self, tool, arguments, timeout=180):
        started = time.time()
        shown = {k: ("<definition>" if k == "definition" else v) for k, v in arguments.items() if k != "env"}
        entry = {"tool": tool, "arguments": shown}
        data = None
        try:
            result = self.request("tools/call", {"name": tool, "arguments": arguments}, timeout)
            text = "\n".join(part.get("text", "") for part in result.get("content", []) if part.get("type") == "text")
            entry["is_error"] = bool(result.get("isError"))
            entry["text"] = clip(redact(text), 1500)
            try:
                data = json.loads(text)
            except ValueError:
                data = None
        except ProbeError as error:
            entry["is_error"] = True
            entry["text"] = str(error)
        except (BrokenPipeError, OSError) as error:
            entry["is_error"] = True
            entry["text"] = f"the server is gone: {error}"
        entry["seconds"] = round(time.time() - started, 1)
        self.calls.append(entry)
        print(f"{self.label}: {tool} -> {'ERROR' if entry['is_error'] else 'ok'} in {entry['seconds']} s: {entry['text'][:400]}")
        return entry, data

    def close(self):
        try:
            self.process.stdin.close()
        except OSError:
            pass
        try:
            self.process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
        self.stderr_file.close()
        with open(self.stderr_path, encoding="utf-8", errors="replace") as handle:
            text = redact(handle.read())
        with open(self.stderr_path, "w", encoding="utf-8") as handle:
            handle.write(text)
        return text


def flowagent_session(label, extra_env, env_id, dv, compose, run_while_off=False):
    """Start FlowAgent's MCP server as its .mcp.json does, and work the timer flow through it."""
    with open(os.path.join(POWER_AUTOMATE, ".mcp.json"), encoding="utf-8") as handle:
        server = json.load(handle)["mcpServers"]["flowagent"]
    session = {"label": label}
    started = time.time()
    client = McpClient(label, [server["command"], *server.get("args", [])], POWER_AUTOMATE,
                       dict(node_env(), PLUGIN_ROOT=POWER_AUTOMATE, PA_DEFAULT_ENVIRONMENT=env_id, **extra_env))
    try:
        init, tools = client.start()
        session["server"] = init.get("serverInfo")
        session["protocol"] = init.get("protocolVersion")
        names = sorted(t.get("name", "") for t in tools.get("tools", []))
        session["tools_listed"] = len(names)
        timer = find_flow(dv, TIMER_FLOW)
        if not timer:
            raise ProbeError("the timer flow from part 1 is not in the lane")
        if run_while_off:
            client.call("whoami", {})
            client.call("doctor", {}, timeout=300)

        entry, listed = client.call("list_flows", {"env": env_id, "name": TIMER_FLOW, "top": 50})
        rows = listed if isinstance(listed, list) else (listed or {}).get("flows", []) if isinstance(listed, dict) else []
        flow_id = next((r.get("name") for r in rows if isinstance(r, dict) and r.get("displayName") == TIMER_FLOW), None)
        session["listed_timer_flow"] = bool(flow_id)
        if flow_id:
            session["flow_id_is"] = ("workflowidunique" if bare(flow_id) == bare(timer["workflowidunique"]) else
                                     "workflowid" if bare(flow_id) == bare(timer["workflowid"]) else "something else")
        flow_id = flow_id or timer["workflowidunique"]

        entry, flow = client.call("get_flow", {"env": env_id, "flow": flow_id})
        session["got_flow"] = isinstance(flow, dict) and isinstance(flow.get("properties"), dict)
        client.call("get_flow_context", {"env": env_id, "flow": flow_id})

        if session["got_flow"]:
            definition = flow["properties"].get("definition") or {}
            definition.setdefault("actions", {}).setdefault("Compose", {})["inputs"] = compose
            entry, _ = client.call("update_flow", {"env": env_id, "flow": flow_id, "definition": definition}, timeout=240)
            after = find_flow(dv, TIMER_FLOW)
            session["updated"] = not entry["is_error"] and compose_text(after) == compose
        if run_while_off:
            entry, _ = client.call("run_flow", {"env": env_id, "flow": flow_id}, timeout=120)
            session["ran_while_off"] = not entry["is_error"]

        entry, _ = client.call("publish_flow", {"env": env_id, "flow": flow_id})
        session["turned_on"] = not entry["is_error"]
        state = find_flow(dv, TIMER_FLOW)
        session["state_after_on"] = [state.get("statecode"), state.get("statuscode")]
        entry, ran = client.call("run_flow", {"env": env_id, "flow": flow_id, "wait": True, "timeout": 90}, timeout=180)
        session["run"] = {"ok": not entry["is_error"]}
        if isinstance(ran, dict):
            session["run"].update({k: ran.get(k) for k in ("status", "invocationPath", "triggerName", "errorCode")})
        entry, runs = client.call("get_run_history", {"env": env_id, "flow": flow_id, "top": 10})
        run_rows = runs if isinstance(runs, list) else (runs or {}).get("runs", []) if isinstance(runs, dict) else []
        session["runs_read"] = [r.get("status") for r in run_rows if isinstance(r, dict)]
        entry, _ = client.call("disable_flow", {"env": env_id, "flow": flow_id})
        session["turned_off"] = not entry["is_error"]
    except ProbeError as error:
        session["error"] = str(error)
    finally:
        stderr = client.close()
        session["calls"] = client.calls
        session["tool_calls"] = len(client.calls)
        session["server_requests"] = client.server_requests
        session["seconds"] = round(time.time() - started, 1)
        session["fell_back"] = "Falling back to classic Flow RP API" in stderr
        session["stderr_tail"] = clip(stderr[-2500:], 2500)
        timer = find_flow(dv, TIMER_FLOW)
        if timer and timer.get("statecode") == 1:   # never leave the timer flow on
            session["backstop_turned_off"] = set_state(dv, timer["workflowid"], False)
    return session


def cmd_part2():
    results = {"mode": "part2", "run_id": env("GITHUB_RUN_ID"), "steps": STEPS}
    try:
        results["tools"] = tool_versions()
        dv = Dataverse()
        org = dv.get("/RetrieveCurrentOrganization(AccessType=Microsoft.Dynamics.CRM.EndpointAccessType'Default')")
        env_id = (org.get("Detail") or {}).get("EnvironmentId")
        if not env_id:
            raise ProbeError("no environment ID from RetrieveCurrentOrganization")
        solution_id = dv.rows(f"/solutions?$select=solutionid&$filter=uniquename eq '{SOLUTION}'")[0]["solutionid"]

        # 1. Sign the Azure CLI in as the lane identity; see which tokens it can get.
        results["az_login_app_spec"] = az_login("App Spec")
        results["az_account"] = az_account()
        results["az_tokens"] = az_tokens()

        # 2. The App Spec: lint, dry run, apply (unattended, never --allow-destructive).
        try:
            results["app_spec"] = app_spec_part(dv, solution_id)
        except (ProbeError, OSError) as error:
            results["app_spec"] = {"error": str(error)}

        # 3. FlowAgent, on the Power Platform API and then on the classic fallback.
        results["az_login_flowagent"] = az_login("FlowAgent")
        for key, label, extra, compose, first in (
                ("flowagent_ppapi", "power platform api", {}, "factory spike timer v3 (FlowAgent, Power Platform API)", True),
                ("flowagent_fallback", "classic fallback", {"PA_PPAPI_BASE_URL": FALLBACK_TEMPLATE},
                 "factory spike timer v4 (FlowAgent, classic fallback)", False)):
            try:
                results[key] = flowagent_session(label, extra, env_id, dv, compose, run_while_off=first)
            except Exception as error:  # a session that cannot start is a finding, not the end of the mode
                results[key] = {"label": label, "error": f"{type(error).__name__}: {clip(error, 400)}"}

        # 4. Export, see what landed, pack again signed out and offline.
        zip_path, folder = export_unpack("after-part2")
        results["vs_reset_commit"] = compare(RESET_COMMIT, folder, "reset-commit", "export")
        files = sorted(tree(folder))
        results["app_files_in_export"] = [n for n in files if APP_TABLE in n.lower() or n.lower().startswith(
            ("appmodules/", "appmodulesitemaps/", "webresources/"))]
        timer_json = [n for n in files if n.lower().startswith("workflows/factoryspiketimerflow") and n.endswith(".json")]
        if timer_json:
            with open(os.path.join(folder, timer_json[0]), encoding="utf-8-sig") as handle:
                results["exported_compose"] = json.load(handle)["properties"]["definition"]["actions"]["Compose"]["inputs"]
        results["pack"] = pack_offline(zip_path, folder)
        results["writes"] = dv.writes
    except ProbeError as error:
        results["error"] = str(error)
    finally:
        subprocess.run(["az", "logout"], stdin=subprocess.DEVNULL, capture_output=True)
        spec = results.get("app_spec", {})
        fa, fb = results.get("flowagent_ppapi", {}), results.get("flowagent_fallback", {})
        exported = results.get("app_files_in_export", [])
        results["exit_test"] = {
            "az_login_as_lane_identity": bool(results.get("az_login_app_spec", {}).get("ok"))
                                         and bool(results.get("az_account", {}).get("user_is_lane_app")),
            "app_spec_lint": spec.get("lint", {}).get("exit") == 0,
            "app_spec_dry_run": spec.get("dry_run", {}).get("exit") == 0,
            "app_spec_apply": spec.get("apply", {}).get("exit") == 0,
            "app_table_exported": any(n.lower().startswith("entities/" + APP_TABLE) for n in exported),
            "app_exported": any(n.lower().startswith("appmodules/") for n in exported),
            "flowagent_ppapi_listed": bool(fa.get("listed_timer_flow")),
            "flowagent_ppapi_updated": bool(fa.get("updated")),
            "flowagent_ppapi_ran": bool(fa.get("run", {}).get("ok")) and fa.get("run", {}).get("status") == "Succeeded",
            "flowagent_ppapi_runs_read": bool(fa.get("runs_read")),
            "flowagent_fallback_used": bool(fb.get("fell_back")),
            "flowagent_fallback_updated": bool(fb.get("updated")),
            "flowagent_fallback_ran": bool(fb.get("run", {}).get("ok")) and fb.get("run", {}).get("status") == "Succeeded",
            "flowagent_fallback_runs_read": bool(fb.get("runs_read")),
            "exported_with_flowagent_update": results.get("exported_compose") == "factory spike timer v4 (FlowAgent, classic fallback)",
            "packs_signed_out": bool(results.get("pack", {}).get("pack"))
                                and results.get("pack", {}).get("repack_vs_export", {}).get("same_root_components", False),
            "packs_with_no_network": bool(results.get("pack", {}).get("pack_no_network")),
        }
        results["exit_test"]["pass"] = all(results["exit_test"].values())
        save("results.json", results)
        print(json.dumps(results["exit_test"], indent=2))


# ---------- part 3: the MCP count-and-retry shim ----------

SHIM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_shim.py")
SPIKE_TABLE = "fspk_spikeitem"     # spike 0.18's table in FactorySpike: fspk_name (text), fspk_quantity (whole number)
MISSING_TABLE = "fspk_nosuchtable"
ROW_PREFIX = "spike-0.14 part3"    # every row part 3 makes starts with this, so the clean-up finds them all
SHIM_TIMEOUT = int(env("SHIM_TIMEOUT", "120"))
CALL_TIMEOUT = SHIM_TIMEOUT * 4 + 60
QUERY_ARGS = ("querytext", "query", "sql", "statement")
TABLE_ARGS = ("tablename", "table", "entityname", "entity", "logicalname")
ITEM_ARGS = ("item", "record", "data", "fields", "columns", "attributes", "values", "row")


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def row_name(label):
    return f"{ROW_PREFIX} ({label})"


def pick(schema, wanted):
    """An argument name from a tool's own inputSchema: exact names first, then substrings (spike 0.3)."""
    properties = (schema or {}).get("properties") or {}
    for name in wanted:
        for key in properties:
            if key.lower() == name:
                return key, properties[key]
    for name in wanted:
        for key in properties:
            if name in key.lower():
                return key, properties[key]
    return None, None


def read_json(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


def read_jsonl(path):
    found = []
    try:
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                try:
                    found.append(json.loads(line))
                except ValueError:
                    pass
    except OSError:
        pass
    return found


class Calls:
    """The scripted client's side of one shim session. Names each call; the shim numbers them in the order sent."""

    def __init__(self, client, listed, session):
        self.client, self.session = client, session
        session["order"] = []
        reader, creator = listed.get("read_query"), listed.get("create_record")
        if not (reader and creator):
            raise ProbeError("tools/list has no read_query or create_record")
        session["schemas"] = {"read_query": reader.get("inputSchema"), "create_record": creator.get("inputSchema")}
        self.query_arg = pick(reader.get("inputSchema"), QUERY_ARGS)[0]
        self.table_arg = pick(creator.get("inputSchema"), TABLE_ARGS)[0]
        self.item_arg, item_schema = pick(creator.get("inputSchema"), ITEM_ARGS)
        if not (self.query_arg and self.table_arg and self.item_arg):
            raise ProbeError("cannot tell read_query's or create_record's argument names from their inputSchema")
        self.item_is_text = (item_schema or {}).get("type") == "string"

    def call(self, name, tool, arguments):
        self.session["order"].append(name)
        entry, _ = self.client.call(tool, arguments, timeout=CALL_TIMEOUT)
        entry["step"] = name
        return entry

    def read(self, name, sql):
        return self.call(name, "read_query", {self.query_arg: sql})

    def create(self, name, table, item):
        return self.call(name, "create_record", {self.table_arg: table,
                                                 self.item_arg: json.dumps(item) if self.item_is_text else item})


def session_a(calls, session):
    """Reads and one create on the spike table, then two forced failures: a bad query, a table that does not exist."""
    by_name = (f"SELECT {SPIKE_TABLE}id, fspk_name, fspk_quantity FROM {SPIKE_TABLE} "
               f"WHERE fspk_name = '{row_name('create')}'")
    calls.read("read organization", "SELECT TOP 1 name FROM organization")
    calls.read("read the spike table", f"SELECT TOP 5 fspk_name, fspk_quantity FROM {SPIKE_TABLE}")
    calls.create("create", SPIKE_TABLE, {"fspk_name": row_name("create"), "fspk_quantity": 1})
    entry = calls.read("read back", by_name)
    session["read_back_found_row"] = not entry["is_error"] and row_name("create") in entry.get("text", "")
    calls.read("bad query", f"SELEKT fspk_name FROM {SPIKE_TABLE}")
    calls.create("missing table", MISSING_TABLE, {"fspk_name": row_name("missing table")})


def session_b(calls, session):
    """A cap of 2: a read, then a bad query whose retry would pass the cap, then one more read."""
    calls.read("read organization", "SELECT TOP 1 name FROM organization")
    calls.read("bad query at the cap", f"SELEKT fspk_name FROM {SPIKE_TABLE}")
    calls.read("read after the cap", "SELECT TOP 1 name FROM organization")


def session_c(calls, session):
    """The shim drops the answer to each create's first attempt, then retries: does the create land twice?"""
    calls.create("create, answer dropped", SPIKE_TABLE, {"fspk_name": row_name("answer dropped"), "fspk_quantity": 2})
    session["own_id"] = str(uuid.uuid4())
    calls.create("create with its own ID, answer dropped", SPIKE_TABLE,
                 {f"{SPIKE_TABLE}id": session["own_id"], "fspk_name": row_name("own ID, answer dropped"),
                  "fspk_quantity": 3})


def per_call(session):
    """The shim's record of each call, under the name the script gave it."""
    by_number = {}
    for event in session.get("events", []):
        number = event.get("call")
        if number is None:
            continue
        entry = by_number.setdefault(number, {"tool": event.get("tool"), "attempts": [], "final": None})
        kind = event.get("event")
        if kind == "answer":
            entry["attempts"].append({k: event.get(k) for k in ("attempt", "kind", "seconds", "text", "proxy_stderr",
                                                                 "status_hint")})
        elif kind == "final":
            entry["final"] = event.get("kind")
        elif kind == "refused":
            entry["final"] = "refused"
            entry["refused"] = event.get("message")
        elif kind == "fault-dropped-answer":
            entry["dropped"] = {"kind": event.get("kind_dropped"), "text": event.get("text")}
        elif kind in ("stop", "stop-again"):
            entry.setdefault("stops", []).append({"reason": event.get("reason"), "park": event.get("park")})
    return {name: by_number.get(index, {}) for index, name in enumerate(session.get("order", []), start=1)}


def shim_session(label, cap, shim_args, script):
    """Start the shim in front of `dataverse mcp`, drive it with `script`, then read the shim's own records."""
    folder = os.path.join(work_dir(), "shim-" + re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-"))
    os.makedirs(folder, exist_ok=True)
    paths = {"log": os.path.join(folder, "calls.jsonl"), "proxy_log": os.path.join(folder, "proxy-stderr.log"),
             "summary": os.path.join(folder, "summary.json"), "stop": os.path.join(folder, "stop.json")}
    argv = [sys.executable, "-I", SHIM, "--cap", str(cap), "--retries", "3", "--timeout", str(SHIM_TIMEOUT),
            "--log", paths["log"], "--proxy-log", paths["proxy_log"], "--summary", paths["summary"],
            "--stop-file", paths["stop"], *shim_args, "--", env("DATAVERSE_BIN", "dataverse"), "mcp", resource()]
    session = {"label": label, "cap": cap, "shim_args": shim_args}
    started = time.time()
    print(f"\n::group::shim session {label} (cap {cap})")
    client = McpClient(label, argv, work_dir(), {}, log_name=f"shim {label}")
    try:
        init, tools = client.start()
        session["server"] = init.get("serverInfo")
        session["protocol"] = init.get("protocolVersion")
        listed = {tool.get("name"): tool for tool in tools.get("tools", [])}
        session["tools_listed"] = sorted(name for name in listed if name)
        script(Calls(client, listed, session), session)
    except ProbeError as error:
        session["error"] = str(error)
    finally:
        session["shim_stderr"] = clip(client.close()[-1500:], 1500)
        session["seconds"] = round(time.time() - started, 1)
        session["client_calls"] = client.calls
        session["shim_summary"] = read_json(paths["summary"])
        session["stop"] = read_json(paths["stop"])
        session["events"] = read_jsonl(paths["log"])
        session["per_call"] = per_call(session)
        print(f"::endgroup::\nshim session {label}: {session['seconds']} s, "
              f"counts {json.dumps({k: (session['shim_summary'] or {}).get(k) for k in ('calls', 'attempts', 'refused')})}")
    return session


def part3_rows(dv, me, entity_set):
    return dv.rows(f"/{entity_set}?$select={SPIKE_TABLE}id,fspk_name,fspk_quantity,createdon"
                   f"&$filter=startswith(fspk_name,'{ROW_PREFIX}') and _createdby_value eq {me}")


def part3_clean(dv, me, entity_set):
    """Delete, by the Web API, every row part 3 made: its name starts with ROW_PREFIX and this app user made it."""
    rows = part3_rows(dv, me, entity_set)
    deleted = []
    for row in rows:
        status, _, _ = dv.call("DELETE", f"/{entity_set}({row[SPIKE_TABLE + 'id']})", ok=(204, 404))
        deleted.append({"name": row.get("fspk_name"), "status": status})
    left = part3_rows(dv, me, entity_set)
    return {"found": len(rows), "deleted": deleted, "left": len(left)}


def part3_billing(sessions):
    """What the admin centre should show for this run, under each reading of what is billed (0.1 credit a call)."""
    totals = {"client_calls": 0, "attempts_sent": 0, "refused": 0, "retries": 0, "late_answers": 0, "by_kind": {}}
    for session in sessions.values():
        summary = session.get("shim_summary") or {}
        for key, total in (("calls", "client_calls"), ("attempts", "attempts_sent"), ("refused", "refused"),
                           ("retries", "retries"), ("late_answers", "late_answers")):
            totals[total] += summary.get(key, 0)
        for kind, count in (summary.get("outcomes") or {}).items():
            totals["by_kind"][kind] = totals["by_kind"].get(kind, 0) + count
    kinds = totals["by_kind"]
    answered = kinds.get("ok", 0) + kinds.get("dropped", 0)
    totals["rows_if_every_attempt_sent_bills"] = totals["attempts_sent"]
    totals["rows_if_tool_errors_bill_but_rpc_errors_do_not"] = answered + kinds.get("tool_error", 0)
    totals["rows_if_only_answers_without_error_bill"] = answered
    totals["credits_if_every_attempt_sent_bills"] = round(0.1 * totals["attempts_sent"], 1)
    return totals


def part3_exit_test(results):
    sessions = results.get("sessions", {})
    a, b, c = (sessions.get(key, {}) for key in ("a", "b", "c"))
    pa, pb, pc = (session.get("per_call", {}) for session in (a, b, c))

    def kinds(per, name):
        return [attempt.get("kind") for attempt in per.get(name, {}).get("attempts", [])]

    def final(per, name):
        return per.get(name, {}).get("final")

    def counts_match(session):
        summary = session.get("shim_summary") or {}
        events = session.get("events", [])
        return (summary.get("final") is True
                and summary.get("attempts") == sum(1 for e in events if e.get("event") == "attempt")
                and summary.get("calls") == sum(1 for e in events if e.get("event") == "call")
                and summary.get("calls") == len(session.get("order", [])))

    test = {
        "initialize_and_tools_list_pass_through": "read_query" in a.get("tools_listed", []),
        "reads_pass_through": final(pa, "read organization") == "ok" and final(pa, "read the spike table") == "ok",
        "create_passes_through": final(pa, "create") == "ok" and bool(a.get("read_back_found_row")),
        "bad_query_tried_four_times": len(kinds(pa, "bad query")) == 4 and final(pa, "bad query") != "ok",
        "missing_table_tried_four_times": len(kinds(pa, "missing table")) == 4 and final(pa, "missing table") != "ok",
        "cap_never_passed": (b.get("shim_summary") or {}).get("attempts") == 2,
        "past_the_cap_refused_with_park_budget": final(pb, "bad query at the cap") == "refused"
                                                 and final(pb, "read after the cap") == "refused"
                                                 and (b.get("stop") or {}).get("park") == "budget",
        "dropped_answer_retried": kinds(pc, "create, answer dropped")[:1] == ["dropped"]
                                  and final(pc, "create, answer dropped") == "ok",
        "counts_match_the_log": all(counts_match(session) for session in (a, b, c)),
        "rows_cleaned_up": (results.get("cleanup") or {}).get("left") == 0,
    }
    test["pass"] = all(test.values())
    return test


def cmd_part3():
    results = {"mode": "part3", "run_id": env("GITHUB_RUN_ID"), "steps": STEPS, "started_utc": utc_now()}
    dv = me = entity_set = None
    try:
        dv = Dataverse()
        me = dv.get("/WhoAmI")["UserId"]
        meta = dv.get(f"/EntityDefinitions(LogicalName='{SPIKE_TABLE}')"
                      "?$select=EntitySetName,PrimaryIdAttribute,PrimaryNameAttribute")
        entity_set = meta["EntitySetName"]
        results["spike_table"] = {k: meta.get(k) for k in ("EntitySetName", "PrimaryIdAttribute", "PrimaryNameAttribute")}
        results["leftovers_before"] = part3_clean(dv, me, entity_set)
        sessions = results["sessions"] = {}
        sessions["a"] = shim_session("a reads, create, failures", 16, ["--keep-going"], session_a)
        sessions["b"] = shim_session("b cap of 2", 2, [], session_b)
        sessions["c"] = shim_session("c dropped answers", 8, ["--fault", "drop-answer:create_record:1",
                                                              "--fault", "drop-answer:create_record:2"], session_c)
        by_name = {}
        for row in part3_rows(dv, me, entity_set):
            by_name[row.get("fspk_name")] = by_name.get(row.get("fspk_name"), 0) + 1
        results["rows_by_name"] = by_name
        results["writes_twice"] = {label: by_name.get(row_name(label), 0)
                                   for label in ("answer dropped", "own ID, answer dropped")}
    except ProbeError as error:
        results["error"] = str(error)
    finally:
        if dv and me and entity_set:
            try:
                results["cleanup"] = part3_clean(dv, me, entity_set)
            except ProbeError as error:
                results["cleanup"] = {"error": str(error)}
        results["ended_utc"] = utc_now()
        results["billing"] = part3_billing(results.get("sessions", {}))
        results["exit_test"] = part3_exit_test(results)
        for session in results.get("sessions", {}).values():
            session.pop("events", None)   # the whole log is calls.jsonl in the artifact
        save("results.json", results)
        print(json.dumps({"exit_test": results["exit_test"], "billing": results["billing"],
                          "writes_twice": results.get("writes_twice")}, indent=2))


# ---------- part 4: the skills in copilot -p ----------
#
# Copilot CLI 1.0.113 (probe/copilot/package-lock.json) with Microsoft's plugins loaded from
# their pinned folders (--plugin-dir), run unread for this spike only (Boroon, 18 November
# 2026). The Dataverse MCP server is the shim in front of `dataverse mcp`, named "dataverse"
# (the Dataverse skills look for any tool whose name holds "dataverse"). FlowAgent is defined
# again in the session's MCP config, so its folder and settings are known. One session per
# story; the lane's sign-ins (pac, az, the Dataverse CLI) are made fresh before each.

DVS_ROOT = env("DVS_ROOT")
DV_PLUGIN = os.path.join(DVS_ROOT, ".github", "plugins", "dataverse")
COPILOT = env("COPILOT_BIN", "copilot")
PLAN_MODEL = env("COPILOT_PLAN_MODEL", "claude-sonnet-5.5")   # plan 5.2's default; checked before use
MAX_AI_CREDITS = env("COPILOT_MAX_AI_CREDITS", "150")          # per story; the CLI's minimum is 30
STORY_SECONDS = int(env("STORY_SECONDS", "1800"))
MCP_CAP = int(env("MCP_CAP", "60"))                            # well above a small story's calls
NEW_COLUMN = "fspk_category"
APP_VIEW = "Active spike app rows"
COMPOSE_V5 = "factory spike timer v5 (Copilot CLI, part 4)"
OIDC_VARS = ("ACTIONS_ID_TOKEN_REQUEST_TOKEN", "ACTIONS_ID_TOKEN_REQUEST_URL")

# What the session may do without asking. In -p and autopilot runs, anything else is denied.
ALLOW_TOOLS = ["shell(node:*)", "shell(pac:*)", "shell(az:*)", "shell(dataverse:*)", "shell(python3:*)",
               "shell(mkdir:*)", "write", "dataverse", "flowagent", "microsoft-learn"]
# Denied even where an allow rule matches (deny wins): the driver's jobs, sign-ins, installs, deletes.
DENY_TOOLS = ["shell(pac solution export:*)", "shell(pac solution import:*)", "shell(pac solution delete:*)",
              "shell(pac solution pack:*)", "shell(pac auth create:*)", "shell(pac auth clear:*)",
              "shell(pac auth delete:*)", "shell(pac auth select:*)", "shell(az login:*)", "shell(az logout:*)",
              "shell(az account get-access-token:*)", "shell(dataverse auth:*)", "shell(dataverse mcp:*)",
              "shell(git push:*)", "shell(curl:*)", "shell(wget:*)", "shell(sudo:*)", "shell(npm:*)",
              "shell(npx:*)", "shell(pip:*)", "shell(pip3:*)", "shell(rm:*)"]

UNATTENDED = """You are working unattended, as part of a night run: nobody will answer questions and nobody
can approve anything until morning.

Environment: {url} (Dataverse). pac, az and the dataverse CLI are already signed in to it, as an
application user. Solution: FactorySpike (publisher prefix fspk).

{story}

Rules for this run:
- Build in the environment. Do not export, import, pack or delete any solution: another step exports
  the solution after you.
- Never pass --allow-destructive. If the change would need it, stop and say so.
- If a tool or command is refused, do not try to get round it. Note it, and carry on if you can, or stop.
- Before you finish, write handoff.md in the working directory: what you changed; each point where you
  stopped, or would have asked a person for approval; each tool or command that was refused and what you
  did then; anything left undone."""

STORIES = [
    {"key": "app_spec", "plugin": "model-apps", "story": (
        "In it, the model-driven app \"Factory spike app\" (fspk_factoryspikeapp) shows the table \"Spike app row\"\n"
        "(fspk_spikeapprow), which has the columns fspk_name and fspk_note.\n\n"
        "Story: add one text column to that table, display name \"Category\", logical name fspk_category, at most 100\n"
        "characters, and show it on the table's main form \"Spike app row\" and in the view \"Active spike app rows\".\n"
        "Change nothing else. Use the app-builder skill of the model-apps plugin.")},
    {"key": "flow", "plugin": "power-automate", "story": (
        "In it, the cloud flow \"Factory spike timer flow\" (a schedule trigger and one Compose step) is turned off.\n\n"
        f"Story: change the input of its Compose step to exactly \"{COMPOSE_V5}\".\n"
        "Leave the flow turned off: do not turn it on and do not run it. Change nothing else. Use the Power Automate\n"
        "plugin's skills and its FlowAgent tools.")},
]


def redact_tree(folder):
    """Rewrite every text file under `folder` with token-shaped strings removed (Copilot writes some files itself)."""
    changed = []
    for here, _, names in os.walk(folder):
        for name in names:
            path = os.path.join(here, name)
            try:
                with open(path, "rb") as handle:
                    data = handle.read()
            except OSError:
                continue
            if not re.search(JWT.pattern.encode(), data):
                continue
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                os.remove(path)
                changed.append(os.path.relpath(path, folder) + " (deleted, not text)")
                continue
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(redact(text))
            changed.append(os.path.relpath(path, folder))
    return changed


def quiet(argv, extra_env=None, drop=(), timeout=180):
    """Run a command, keep only whether it worked and a redacted tail."""
    child_env = {k: v for k, v in dict(os.environ, **(extra_env or {})).items() if k not in drop}
    try:
        process = subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True, text=True, env=child_env,
                                 timeout=timeout)
        return {"ok": process.returncode == 0, "exit": process.returncode,
                "tail": clip(redact(process.stdout + process.stderr)[-600:], 600)}
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"ok": False, "exit": None, "tail": clip(error, 300)}


def lane_sign_in(label):
    """Fresh sign-ins for one story: pac, the Dataverse CLI and az, each with a new GitHub OIDC token."""
    tenant, app, url = env("TENANT_ID"), env("APP_ID"), env("ENV_URL")
    out = {"pac_clear": quiet(["pac", "auth", "clear"])}
    out["pac"] = quiet(["pac", "auth", "create", "--name", "lane", "--githubFederated", "--tenant", tenant,
                        "--applicationId", app, "--environment", url])
    out["pac_who"] = quiet(["pac", "org", "who"])
    out["dataverse_clear"] = quiet(["dataverse", "auth", "remove", "--all"])
    out["dataverse"] = quiet(["dataverse", "auth", "create", "--name", "lane-dv", "--githubFederated", "--tenant",
                              tenant, "--applicationId", app, "--environment", url, "--accept-cleartext-caching"])
    out["dataverse_who"] = quiet(["dataverse", "org", "who"])
    out["az"] = az_login(f"az, {label}")
    out["az_tokens"] = az_tokens()   # every token at once, while the OIDC token is fresh (part 2 finding 9)
    out["ok"] = all(out[k]["ok"] for k in ("pac", "pac_who", "dataverse", "dataverse_who", "az"))
    note(f"sign in for {label} (pac, dataverse, az)", out["ok"], 0, json.dumps({k: v.get("ok") for k, v in out.items()
                                                                                if isinstance(v, dict) and "ok" in v}))
    return out


def without_oidc_check():
    """Do the lane's sign-ins still work with the OIDC variables gone, as --secret-env-vars would leave them?"""
    url = env("ENV_URL")
    out = {"pac_org_who": quiet(["pac", "org", "who"], drop=OIDC_VARS),
           "dataverse_org_who": quiet(["dataverse", "org", "who"], drop=OIDC_VARS),
           "az_dataverse_token": az_token_without_oidc(url)}
    out["all_ok"] = all(v["ok"] for v in out.values())
    return out


def az_token_without_oidc(url):
    process = subprocess.run(["az", "account", "get-access-token", "--resource", url, "--query", "expiresOn",
                              "--output", "tsv"], stdin=subprocess.DEVNULL, capture_output=True, text=True,
                             env={k: v for k, v in os.environ.items() if k not in OIDC_VARS}, timeout=120)
    return {"ok": process.returncode == 0, "exit": process.returncode,
            "tail": clip(redact(process.stdout + process.stderr)[-300:], 300)}


def copilot_env(extra=None):
    base = dict(os.environ, **node_env(), COPILOT_AUTO_UPDATE="false", COPILOT_TELEMETRY_DISABLED="true",
                COPILOT_PLUGIN_DIR_ONLY="true", DATAVERSE_TELEMETRY_OPT_OUT="1", NO_COLOR="1")
    base.update(extra or {})
    return base


def model_check():
    """One tiny prompt with plan 5.2's model. If the CLI refuses the name, the stories use its default."""
    folder = os.path.join(work_dir(), "model-check")
    os.makedirs(folder, exist_ok=True)
    usage = os.path.join(folder, "usage.json")
    argv = [COPILOT, "-p", "Reply with the single word: ready", "-s", "--no-ask-user", "--disable-builtin-mcps",
            f"--model={PLAN_MODEL}", f"--max-ai-credits={30}", f"--usage-output-file={usage}", "-C", folder]
    started = time.time()
    try:
        process = subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=300,
                                 env=copilot_env())
        code, out = process.returncode, redact(process.stdout + "\n" + process.stderr)
    except subprocess.TimeoutExpired:
        code, out = 124, "timed out"
    result = {"model": PLAN_MODEL, "exit": code, "seconds": round(time.time() - started, 1),
              "answer": clip(out, 1200), "usage": read_json(usage)}
    result["use_model"] = code == 0 and "ready" in out.lower()
    note(f"model check ({PLAN_MODEL})", result["use_model"], result["seconds"], result["answer"])
    return result


def mcp_config(folder, env_id, keys_path, with_flowagent=True):
    """The session's MCP servers: the shim in front of `dataverse mcp`, and FlowAgent from its pinned folder
    (part 4b leaves FlowAgent out)."""
    shim_dir = os.path.join(folder, "shim")
    os.makedirs(shim_dir, exist_ok=True)
    paths = {k: os.path.join(shim_dir, f) for k, f in (("log", "calls.jsonl"), ("proxy_log", "proxy-stderr.log"),
                                                       ("summary", "summary.json"), ("stop", "stop.json"))}
    config = {"mcpServers": {
        "dataverse": {"type": "local", "command": sys.executable, "tools": ["*"],
                      "args": ["-I", SHIM, "--cap", str(MCP_CAP), "--timeout", "60", "--keys-file", keys_path,
                               "--webapi", resource(), "--log", paths["log"], "--proxy-log", paths["proxy_log"],
                               "--summary", paths["summary"], "--stop-file", paths["stop"], "--",
                               env("DATAVERSE_BIN", "dataverse"), "mcp", resource()],
                      "env": {"DATAVERSE_TELEMETRY_OPT_OUT": "1"}}}}
    if with_flowagent:
        with open(os.path.join(POWER_AUTOMATE, ".mcp.json"), encoding="utf-8") as handle:
            flowagent = json.load(handle)["mcpServers"]["flowagent"]
        config["mcpServers"]["flowagent"] = {
            "type": "local", "command": flowagent["command"], "args": flowagent.get("args", []),
            "cwd": POWER_AUTOMATE, "tools": ["*"],
            "env": dict(node_env(), PLUGIN_ROOT=POWER_AUTOMATE, PA_DEFAULT_ENVIRONMENT=env_id)}
    path = os.path.join(folder, "mcp-config.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(config, handle, indent=2)
    return path, paths


def walk_strings(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)
    elif isinstance(value, str):
        yield value


def first_key(value, names):
    """The first value under any of `names`, searching nested objects."""
    if isinstance(value, dict):
        for name in names:
            if isinstance(value.get(name), (str, int, float)):
                return value[name]
        for item in value.values():
            found = first_key(item, names)
            if found is not None:
                return found
    elif isinstance(value, list):
        for item in value:
            found = first_key(item, names)
            if found is not None:
                return found
    return None


DENIED = re.compile(r"denied|not permitted|permission|was refused|not allowed", re.I)


def read_events(path):
    """Copilot's --output-format json lines: event types, tool calls by name, anything that reads as a denial."""
    events = read_jsonl(path)
    types, tools, denials, messages = {}, {}, [], []
    for event in events:
        kind = str(event.get("type") or event.get("event") or "?")
        types[kind] = types.get(kind, 0) + 1
        if "tool" in kind.lower():
            name = first_key(event, ("toolName", "tool_name", "mcpToolName", "name"))
            if name:
                tools.setdefault(str(name), {}).setdefault(kind, 0)
                tools[str(name)][kind] += 1
        joined = " ".join(walk_strings(event))
        data = event.get("data") or {}
        # A denial is a tool call that did not succeed with a permission message, or a permission event. Matching any
        # event text (as run 40121696 did) also caught ordinary words in handoffs and summaries.
        failed = kind == "tool.execution_complete" and data.get("success") is False
        if (failed and DENIED.search(json.dumps(data.get("error")))) or "permission" in kind.lower():
            denials.append({"type": kind, "tool": first_key(event, ("toolName", "tool_name", "name")),
                            "text": clip(joined, 700)})
        if failed:
            bucket = tools.setdefault("(failed)", {})
            reason = clip(json.dumps(data.get("error")), 160)
            bucket[reason] = bucket.get(reason, 0) + 1
        if "message" in kind.lower() and "assistant" in kind.lower():
            messages.append(clip(first_key(event, ("content", "text", "message")) or joined, 1500))
    return {"events": len(events), "types": types, "tools": tools, "denials": denials,
            "last_messages": messages[-3:]}


PLUGIN_FOLDERS = {"model-apps": lambda: MODEL_APPS, "power-automate": lambda: POWER_AUTOMATE, "dataverse": lambda: DV_PLUGIN}


def started_commands(path):
    """The shell commands the session started (tool.execution_start), redacted and clipped."""
    found = []
    for event in read_jsonl(path):
        if event.get("type") != "tool.execution_start":
            continue
        command = ((event.get("data") or {}).get("arguments") or {}).get("command")
        if command:
            found.append(clip(redact(str(command)), 400))
    return found


def run_story(story, model_ok, secrets, env_id, keys_path):
    """One `copilot -p` session. A story may name its own plugins, extra allow and deny rules, extra
    folders, environment, and whether FlowAgent is served (part 4b uses these; part 4 used the defaults)."""
    folder = os.path.join(work_dir(), "story-" + story["key"])
    os.makedirs(folder, exist_ok=True)
    config_path, shim = mcp_config(folder, env_id, keys_path, story.get("flowagent", True))
    files = {k: os.path.join(folder, f) for k, f in (("events", "events.jsonl"), ("stderr", "copilot-stderr.log"),
                                                     ("usage", "usage.json"), ("share", "transcript.md"),
                                                     ("otel", "otel.jsonl"), ("handoff", "handoff.md"),
                                                     ("webapi", "webapi-calls.jsonl"))}
    plugins = [PLUGIN_FOLDERS[name]() for name in story.get("plugins", ("model-apps", "power-automate", "dataverse"))]
    prompt = UNATTENDED.format(url=resource() + "/", story=story["story"])
    argv = [COPILOT, "-p", prompt, "--autopilot", "--max-autopilot-continues=10", f"--max-ai-credits={MAX_AI_CREDITS}",
            "--no-ask-user", "--output-format=json", f"--share={files['share']}",
            f"--usage-output-file={files['usage']}", f"--log-dir={os.path.join(folder, 'copilot-logs')}",
            "--log-level=info", "--disable-client-telemetry", "--disable-builtin-mcps",
            "--disable-mcp-server=playwright", f"--additional-mcp-config=@{config_path}", "-C", folder]
    for plugin in plugins:
        argv += [f"--plugin-dir={plugin}", f"--add-dir={plugin}"]
    argv += [f"--add-dir={extra}" for extra in story.get("add_dirs", [])]
    argv += [f"--allow-tool={rule}" for rule in ALLOW_TOOLS] + [f"--deny-tool={rule}" for rule in DENY_TOOLS]
    argv += [f"--deny-tool={rule}" for rule in story.get("deny_extra", [])]
    if model_ok:
        argv.append(f"--model={PLAN_MODEL}")
    argv.append("--secret-env-vars=" + ",".join(secrets))
    extra_env = {"COPILOT_OTEL_FILE_EXPORTER_PATH": files["otel"], "WEBAPI_LOG": files["webapi"]}
    if story.get("plugin"):
        extra_env["PLUGIN_ROOT"] = PLUGIN_FOLDERS[story["plugin"]]()
    extra_env.update(story.get("env", {}))
    child_env = copilot_env(extra_env)
    shown = list(argv)
    shown[2] = f"<the {story['key']} prompt>"
    with open(os.path.join(folder, "command.json"), "w", encoding="utf-8") as handle:
        json.dump({"argv": shown, "prompt": prompt}, handle, indent=2)
    result = {"key": story["key"], "prompt": prompt, "ended_by": "copilot"}
    print(f"\n::group::story {story['key']}")
    started = time.time()
    with open(files["events"], "w", encoding="utf-8") as out, open(files["stderr"], "w", encoding="utf-8") as err:
        process = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=err, text=True,
                                   env=child_env, bufsize=1)
        lines = queue.Queue()
        threading.Thread(target=lambda: [lines.put(line) for line in process.stdout] + [lines.put(None)],
                         daemon=True).start()
        while True:
            try:
                line = lines.get(timeout=2)
            except queue.Empty:
                line = ""
            if line is None:
                break
            if line:
                out.write(redact(line))
                out.flush()
            stop = read_json(shim["stop"])
            if stop and result["ended_by"] == "copilot":
                result["ended_by"] = f"driver: shim stop, PARK {stop.get('park')}"
                process.terminate()
            if time.time() - started > STORY_SECONDS and result["ended_by"] == "copilot":
                result["ended_by"] = f"driver: past {STORY_SECONDS} s"
                process.terminate()
        try:
            process.wait(timeout=60)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
    result["exit"] = process.returncode
    result["seconds"] = round(time.time() - started, 1)
    print(f"::endgroup::\nstory {story['key']}: exit {result['exit']} in {result['seconds']} s, {result['ended_by']}")
    result["redacted_files"] = redact_tree(folder)
    result["events"] = read_events(files["events"])
    usage = read_json(files["usage"]) or {}
    result["usage"] = usage
    nano = first_key(usage, ("totalNanoAiu",))
    result["ai_credits"] = round(float(nano) / 1e9, 2) if isinstance(nano, (int, float)) else None
    result["shim"] = read_json(shim["summary"])
    result["shim_stop"] = read_json(shim["stop"])
    result["mcp_calls"] = (result["shim"] or {}).get("attempts")
    shim_events = read_jsonl(shim["log"])
    result["mcp_tools_listed"] = next((e.get("names") for e in shim_events if e.get("event") == "tools-list"), None)
    result["mcp_call_list"] = [{k: e.get(k) for k in ("call", "tool", "kind", "attempt", "text", "correlation_id")}
                               for e in shim_events if e.get("event") == "answer"]
    for e in result["mcp_call_list"]:
        e["text"] = clip(e.get("text"), 400)
    with open(files["stderr"], encoding="utf-8", errors="replace") as handle:
        result["stderr_tail"] = clip(redact(handle.read())[-2500:], 2500)
    try:
        with open(files["handoff"], encoding="utf-8") as handle:
            result["handoff"] = redact(handle.read())[:6000]
    except OSError:
        result["handoff"] = None
    # A command the session ran with --allow-destructive. Only the commands it started count: the prompt's own rule
    # and the build engine's refusal both name the flag (run 40121696 flagged the refusal by mistake).
    result["destructive_flag_seen"] = any(
        "--allow-destructive" in str(((event.get("data") or {}).get("arguments") or {}).get("command", ""))
        for event in read_jsonl(files["events"]) if event.get("type") == "tool.execution_start")
    # Part 4b: did the session start the App Spec build engine at all, or apply with it? Again only the commands
    # the session started count, not the prompt that names the engine.
    result["commands"] = started_commands(files["events"])
    result["engine_runs"] = [c for c in result["commands"] if "build-model-app" in c]
    result["engine_applied"] = any("--apply" in c for c in result["engine_runs"])
    result["webapi_calls"] = read_jsonl(files["webapi"])
    result["workflow_log"] = None
    for here, _, names in os.walk(folder):
        if "workflow-log.md" in names:
            with open(os.path.join(here, "workflow-log.md"), encoding="utf-8", errors="replace") as handle:
                result["workflow_log"] = clip(redact(handle.read()), 4000)
            break
    note(f"story {story['key']}", result["exit"] == 0 and result["ended_by"] == "copilot", result["seconds"],
         result["stderr_tail"][-800:])
    return result


def app_state(dv):
    """The spike app table's columns, and whether the new column is on its main form and in the view."""
    out = {}
    attributes = dv.rows(f"/EntityDefinitions(LogicalName='{APP_TABLE}')/Attributes?$select=LogicalName")
    out["columns"] = sorted(a["LogicalName"] for a in attributes)
    forms = dv.rows(f"/systemforms?$select=name,type,formxml&$filter=objecttypecode eq '{APP_TABLE}' and type eq 2")
    out["main_forms"] = {f["name"]: NEW_COLUMN in (f.get("formxml") or "") for f in forms}
    views = dv.rows(f"/savedqueries?$select=name,layoutxml,fetchxml&$filter=returnedtypecode eq '{APP_TABLE}'")
    out["views_with_column"] = sorted(v["name"] for v in views if NEW_COLUMN in (v.get("layoutxml") or ""))
    out["view_named"] = {v["name"]: NEW_COLUMN in (v.get("layoutxml") or "") for v in views if v["name"] == APP_VIEW}
    return out


def cmd_part4():
    results = {"mode": "part4", "run_id": env("GITHUB_RUN_ID"), "steps": STEPS, "started_utc": utc_now(),
               "settings": {"max_ai_credits_per_story": MAX_AI_CREDITS, "mcp_cap": MCP_CAP, "allow": ALLOW_TOOLS,
                            "deny": DENY_TOOLS, "plan_model": PLAN_MODEL, "story_seconds": STORY_SECONDS}}
    try:
        results["tools"] = tool_versions()
        results["tools"]["copilot"] = quiet([COPILOT, "--version"], extra_env={"COPILOT_AUTO_UPDATE": "false"})["tail"]
        process = subprocess.run(["git", "-C", DVS_ROOT, "rev-parse", "HEAD"], capture_output=True, text=True)
        results["tools"]["dataverse-skills head"] = process.stdout.strip()
        results["tools"]["dataverse-skills head is the pin"] = process.stdout.strip() == env("DVS_COMMIT")
        dv = Dataverse()
        org = dv.get("/RetrieveCurrentOrganization(AccessType=Microsoft.Dynamics.CRM.EndpointAccessType'Default')")
        env_id = (org.get("Detail") or {}).get("EnvironmentId")
        if not env_id:
            raise ProbeError("no environment ID from RetrieveCurrentOrganization")
        solution_id = dv.rows(f"/solutions?$select=solutionid&$filter=uniquename eq '{SOLUTION}'")[0]["solutionid"]
        keys = {row["LogicalName"]: row["PrimaryIdAttribute"]
                for row in dv.rows("/EntityDefinitions?$select=LogicalName,PrimaryIdAttribute") if row.get("PrimaryIdAttribute")}
        keys_path = os.path.join(work_dir(), "primary-keys.json")
        with open(keys_path, "w", encoding="utf-8") as handle:
            json.dump(keys, handle)
        results["primary_keys_read"] = len(keys)
        before_parts = solution_parts(dv, solution_id)
        results["app_before"] = app_state(dv)
        timer = find_flow(dv, TIMER_FLOW)
        results["flow_before"] = {"compose": compose_text(timer), "state": [timer.get("statecode"), timer.get("statuscode")]}

        results["model_check"] = model_check()
        stories = results["stories"] = {}
        for story in STORIES:
            sign_in = lane_sign_in(story["key"])
            results.setdefault("sign_ins", {})[story["key"]] = sign_in
            if "without_oidc" not in results:
                results["without_oidc"] = without_oidc_check()
            secrets = ["GITHUB_TOKEN", "GH_TOKEN", "COPILOT_GITHUB_TOKEN"]
            if results["without_oidc"]["all_ok"]:
                secrets += list(OIDC_VARS)
            results.setdefault("secret_env_vars", {})[story["key"]] = secrets
            try:
                stories[story["key"]] = run_story(story, results["model_check"]["use_model"], secrets, env_id, keys_path)
            except (OSError, ProbeError) as error:
                stories[story["key"]] = {"key": story["key"], "error": f"{type(error).__name__}: {clip(error, 400)}"}

        # What the stories changed, read by the Web API with a fresh token.
        dv = Dataverse()
        after_parts = solution_parts(dv, solution_id)
        results["solution_parts_added"] = [{"type": COMPONENT_TYPES.get(t, str(t)), "id": i}
                                           for t, i in after_parts if (t, i) not in before_parts]
        results["solution_parts_removed"] = [{"type": COMPONENT_TYPES.get(t, str(t)), "id": i}
                                             for t, i in before_parts if (t, i) not in after_parts]
        results["app_after"] = app_state(dv)
        timer = find_flow(dv, TIMER_FLOW)
        results["flow_after"] = {"compose": compose_text(timer), "state": [timer.get("statecode"), timer.get("statuscode")]}
        if timer.get("statecode") == 1:   # never leave the timer flow on
            results["flow_backstop_off"] = set_state(dv, timer["workflowid"], False)

        # The driver's part: export, compare, pack again signed out and offline.
        lane_sign_in("export")
        zip_path, folder = export_unpack("after-part4")
        results["vs_reset_commit"] = compare(RESET_COMMIT, folder, "reset-commit", "export")
        files = sorted(tree(folder))
        results["column_in_export"] = []
        for name in files:
            if name.lower().startswith(("entities/" + APP_TABLE, "appmodules/")):
                with open(os.path.join(folder, name), encoding="utf-8-sig", errors="replace") as handle:
                    if NEW_COLUMN in handle.read():
                        results["column_in_export"].append(name)
        timer_json = [n for n in files if n.lower().startswith("workflows/factoryspiketimerflow") and n.endswith(".json")]
        if timer_json:
            with open(os.path.join(folder, timer_json[0]), encoding="utf-8-sig") as handle:
                results["exported_compose"] = json.load(handle)["properties"]["definition"]["actions"]["Compose"]["inputs"]
        results["pack"] = pack_offline(zip_path, folder)
        results["writes"] = dv.writes
    except ProbeError as error:
        results["error"] = str(error)
    finally:
        subprocess.run(["az", "logout"], stdin=subprocess.DEVNULL, capture_output=True)
        results["ended_utc"] = utc_now()
        app_story = results.get("stories", {}).get("app_spec", {})
        flow_story = results.get("stories", {}).get("flow", {})
        app_after = results.get("app_after", {})
        results["exit_test"] = {
            "sessions_ran": bool(app_story.get("events", {}).get("events")) and bool(flow_story.get("events", {}).get("events")),
            "app_column_made": NEW_COLUMN in app_after.get("columns", []),
            "app_column_on_main_form": any(app_after.get("main_forms", {}).values()),
            "app_column_in_view": any(app_after.get("view_named", {}).values()),
            "flow_compose_changed": results.get("flow_after", {}).get("compose") == COMPOSE_V5,
            "flow_left_off": results.get("flow_after", {}).get("state", [None])[0] == 0,
            "no_allow_destructive": not app_story.get("destructive_flag_seen") and not flow_story.get("destructive_flag_seen"),
            "nothing_left_the_solution": not results.get("solution_parts_removed"),
            "column_exported": any(n.lower().startswith("entities/") for n in results.get("column_in_export", [])),
            "flow_change_exported": results.get("exported_compose") == COMPOSE_V5,
            "packs_signed_out": bool(results.get("pack", {}).get("pack"))
                                and results.get("pack", {}).get("repack_vs_export", {}).get("same_root_components", False),
            "packs_with_no_network": bool(results.get("pack", {}).get("pack_no_network")),
        }
        results["exit_test"]["pass"] = all(results["exit_test"].values())
        save("results.json", results)
        print(json.dumps(results["exit_test"], indent=2))


# ---------- part 4b: option (b), an additive change to the existing app without the App Spec engine ----------
#
# Part 4's App Spec story again (a column on the existing table, shown on the main form "Spike app row" and in
# the view "Active Spike app rows"), but by another route: the column by Dataverse MCP `update_table` (through the
# shim), the form's formxml and the view's layoutxml and fetchxml by the Web API, then PublishXml. The Web API goes
# through a trusted helper (probe/webapi.py): it signs in from the Azure CLI's cache, adds the solution header to
# every write, and refuses DELETE, PUT and the driver's solution actions. The model-apps plugin stays loaded, so
# the session could reach for the build engine; the prompt says not to, and the probe checks the commands it ran.

APP_FORM = "Spike app row"
OTHER_MAIN_FORM = "Information"
APP_VIEW_EXACT = "Active Spike app rows"   # the stock default view's name (part 4's APP_VIEW had the case wrong)
PROBE_DIR = os.path.dirname(os.path.abspath(__file__))
WEBAPI_HELPER = os.path.join(PROBE_DIR, "webapi.py")

STORY_4B = {"key": "app_additive", "plugin": None, "plugins": ("model-apps", "dataverse"), "flowagent": False,
            "add_dirs": [PROBE_DIR], "deny_extra": [f"write({PROBE_DIR}/**)"], "story": (
    "In it, the model-driven app \"Factory spike app\" (fspk_factoryspikeapp) shows the table \"Spike app row\"\n"
    "(fspk_spikeapprow), which has the columns fspk_name and fspk_note. The table has two main forms, \"Spike app\n"
    "row\" and \"Information\", and its views include \"Active Spike app rows\".\n\n"
    "Story: add one text column to that table, display name \"Category\", logical name fspk_category, at most 100\n"
    "characters, and show it on the main form \"Spike app row\" (only that form) and in the view \"Active Spike app\n"
    "rows\". Change nothing else.\n\n"
    "How, because the app already exists:\n"
    "- Do not run the model-apps build engine (build-model-app.js) at all, not even a dry run, and do not use the\n"
    "  app-builder skill: at night it cannot apply a change to an existing app.\n"
    "- Add the column with the dataverse MCP server's update_table tool.\n"
    "- Change the form and the view through the Dataverse Web API, with the trusted helper\n"
    f"    python3 {WEBAPI_HELPER} METHOD PATH [--body JSON|@FILE] [--out FILE]\n"
    "  where PATH has no leading slash, for example systemforms(<formid>). Run it with --help first.\n"
    "  The form is a row in systemforms (column formxml), the view a row in savedqueries (columns layoutxml\n"
    "  and fetchxml). Read the existing row, add the new column to its XML, and PATCH that row.\n"
    "  Do not create a new form or view. The helper signs in and adds the solution header itself; it refuses deletes.\n"
    "- Then publish the table's customisations with the helper (POST PublishXml), and read the column, the form\n"
    "  and the view back to check.\n"
    "- The Dataverse skills' Python SDK is not installed and pip is not allowed: use the helper and the MCP tools.")}


def sha(text):
    return hashlib.sha256((text or "").encode()).hexdigest()[:16]


def label_text(label):
    return ((label or {}).get("UserLocalizedLabel") or {}).get("Label")


def app_detail(dv):
    """The spike app table's columns, every form and view on it (hashed), and the new column's definition."""
    out = {}
    attributes = dv.rows(f"/EntityDefinitions(LogicalName='{APP_TABLE}')/Attributes?$select=LogicalName,AttributeType")
    out["columns"] = sorted(a["LogicalName"] for a in attributes)
    if NEW_COLUMN in out["columns"]:
        status, _, column = dv.call(
            "GET", f"/EntityDefinitions(LogicalName='{APP_TABLE}')/Attributes(LogicalName='{NEW_COLUMN}')"
                   "/Microsoft.Dynamics.CRM.StringAttributeMetadata?$select=LogicalName,AttributeType,MaxLength,"
                   "DisplayName,RequiredLevel,MetadataId", ok=(200, 400, 404))
        out["new_column"] = ({"type": column.get("AttributeType"), "max_length": column.get("MaxLength"),
                              "display_name": label_text(column.get("DisplayName")),
                              "required": (column.get("RequiredLevel") or {}).get("Value"),
                              "metadata_id": column.get("MetadataId")} if status == 200 else {"status": status})
    forms = dv.rows(f"/systemforms?$select=formid,name,type,formxml,publishedon&$filter=objecttypecode eq '{APP_TABLE}'")
    out["forms"] = {bare(f["formid"]): {"name": f.get("name"), "type": f.get("type"), "sha": sha(f.get("formxml")),
                                        "has_column": NEW_COLUMN in (f.get("formxml") or ""),
                                        "published_on": f.get("publishedon")} for f in forms}
    views = dv.rows(f"/savedqueries?$select=savedqueryid,name,querytype,layoutxml,fetchxml"
                    f"&$filter=returnedtypecode eq '{APP_TABLE}'")
    out["views"] = {bare(v["savedqueryid"]): {"name": v.get("name"), "querytype": v.get("querytype"),
                                              "sha_layout": sha(v.get("layoutxml")), "sha_fetch": sha(v.get("fetchxml")),
                                              "in_layout": NEW_COLUMN in (v.get("layoutxml") or ""),
                                              "in_fetch": NEW_COLUMN in (v.get("fetchxml") or "")} for v in views}
    return out


def outside_state(dv):
    """What could be made outside the solution: every form and view in the environment by ID (systemform has no
    createdon to filter on, run 40125881; spike 0.19 found forms keep no maker), the fspk_ tables, and the other
    spike table's columns."""
    forms = {bare(f["formid"]): [f.get("name"), f.get("objecttypecode")]
             for f in dv.rows("/systemforms?$select=formid,name,objecttypecode")}
    views = {bare(v["savedqueryid"]): [v.get("name"), v.get("returnedtypecode")]
             for v in dv.rows("/savedqueries?$select=savedqueryid,name,returnedtypecode")}
    tables = sorted(row["LogicalName"] for row in dv.rows("/EntityDefinitions?$select=LogicalName")
                    if row["LogicalName"].startswith("fspk_"))
    item_columns = sorted(a["LogicalName"] for a in dv.rows(
        f"/EntityDefinitions(LogicalName='{SPIKE_TABLE}')/Attributes?$select=LogicalName"))
    return {"forms": forms, "views": views, "fspk_tables": tables, "spikeitem_columns": item_columns}


def outside_change(before, after):
    """New or gone forms and views anywhere, and any change to the fspk_ tables or the other spike table."""
    return {"forms_new": [dict(id=i, name=after["forms"][i][0], table=after["forms"][i][1])
                          for i in sorted(set(after["forms"]) - set(before["forms"]))],
            "forms_gone": sorted(set(before["forms"]) - set(after["forms"])),
            "views_new": [dict(id=i, name=after["views"][i][0], table=after["views"][i][1])
                          for i in sorted(set(after["views"]) - set(before["views"]))],
            "views_gone": sorted(set(before["views"]) - set(after["views"])),
            "fspk_tables_before": before["fspk_tables"], "fspk_tables_after": after["fspk_tables"],
            "spikeitem_columns_same": before["spikeitem_columns"] == after["spikeitem_columns"],
            "forms_counted": [len(before["forms"]), len(after["forms"])],
            "views_counted": [len(before["views"]), len(after["views"])]}


def file_sha(path):
    try:
        with open(path, "rb") as handle:
            return hashlib.sha256(handle.read()).hexdigest()[:16]
    except OSError:
        return None


def cmd_part4b():
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    results = {"mode": "part4b", "run_id": env("GITHUB_RUN_ID"), "steps": STEPS, "started_utc": started,
               "settings": {"max_ai_credits_per_story": MAX_AI_CREDITS, "mcp_cap": MCP_CAP, "allow": ALLOW_TOOLS,
                            "deny": DENY_TOOLS + STORY_4B["deny_extra"], "plan_model": PLAN_MODEL,
                            "story_seconds": STORY_SECONDS, "plugins": list(STORY_4B["plugins"])}}
    trusted = {name: file_sha(os.path.join(PROBE_DIR, name)) for name in ("webapi.py", "mcp_shim.py")}
    results["trusted_files_before"] = trusted
    try:
        results["tools"] = tool_versions()
        results["tools"]["copilot"] = quiet([COPILOT, "--version"], extra_env={"COPILOT_AUTO_UPDATE": "false"})["tail"]
        process = subprocess.run(["git", "-C", DVS_ROOT, "rev-parse", "HEAD"], capture_output=True, text=True)
        results["tools"]["dataverse-skills head is the pin"] = process.stdout.strip() == env("DVS_COMMIT")
        dv = Dataverse()
        org = dv.get("/RetrieveCurrentOrganization(AccessType=Microsoft.Dynamics.CRM.EndpointAccessType'Default')")
        env_id = (org.get("Detail") or {}).get("EnvironmentId")
        if not env_id:
            raise ProbeError("no environment ID from RetrieveCurrentOrganization")
        solution_id = dv.rows(f"/solutions?$select=solutionid&$filter=uniquename eq '{SOLUTION}'")[0]["solutionid"]
        keys = {row["LogicalName"]: row["PrimaryIdAttribute"]
                for row in dv.rows("/EntityDefinitions?$select=LogicalName,PrimaryIdAttribute") if row.get("PrimaryIdAttribute")}
        keys_path = os.path.join(work_dir(), "primary-keys.json")
        with open(keys_path, "w", encoding="utf-8") as handle:
            json.dump(keys, handle)
        before_parts = solution_parts(dv, solution_id)
        results["app_before"] = app_detail(dv)
        outside_before = outside_state(dv)
        if NEW_COLUMN in results["app_before"]["columns"]:
            raise ProbeError(f"{NEW_COLUMN} already exists: this story needs the table as part 4 left it")

        # The driver's export before the story, so the story's own change shows file by file.
        lane_sign_in("export before")
        _, before_folder = export_unpack("before-part4b")

        results["model_check"] = model_check()
        sign_in = results["sign_in"] = lane_sign_in(STORY_4B["key"])
        results["without_oidc"] = without_oidc_check()
        secrets = ["GITHUB_TOKEN", "GH_TOKEN", "COPILOT_GITHUB_TOKEN"]
        if results["without_oidc"]["all_ok"]:
            secrets += list(OIDC_VARS)
        results["secret_env_vars"] = secrets
        if not sign_in["ok"]:
            raise ProbeError("the lane's sign-ins failed before the story")
        try:
            results["story"] = run_story(STORY_4B, results["model_check"]["use_model"], secrets, env_id, keys_path)
        except (OSError, ProbeError) as error:
            results["story"] = {"key": STORY_4B["key"], "error": f"{type(error).__name__}: {clip(error, 400)}"}
        results["trusted_files_after"] = {name: file_sha(os.path.join(PROBE_DIR, name)) for name in trusted}

        # What the story changed, read by the Web API with a fresh token.
        dv = Dataverse()
        after_parts = solution_parts(dv, solution_id)
        results["solution_parts_added"] = [{"type": COMPONENT_TYPES.get(t, str(t)), "id": i}
                                           for t, i in after_parts if (t, i) not in before_parts]
        results["solution_parts_removed"] = [{"type": COMPONENT_TYPES.get(t, str(t)), "id": i}
                                             for t, i in before_parts if (t, i) not in after_parts]
        results["app_after"] = app_detail(dv)
        results["outside"] = outside_change(outside_before, outside_state(dv))
        column_id = bare((results["app_after"].get("new_column") or {}).get("metadata_id"))
        results["column_is_solution_component"] = bool(column_id) and (2, column_id) in after_parts

        # The driver's part: export, compare with the export before, pack again signed out and offline.
        lane_sign_in("export")
        zip_path, folder = export_unpack("after-part4b")
        results["vs_before"] = compare(before_folder, folder, "before", "after")
        form_ids = {i for i, f in results["app_after"]["forms"].items() if f["name"] == APP_FORM and f["type"] == 2}
        view_ids = {i for i, v in results["app_after"]["views"].items() if (v["name"] or "").lower() == APP_VIEW_EXACT.lower()}
        expected = {f"Entities/{APP_TABLE}/Entity.xml"}
        expected |= {f"Entities/{APP_TABLE}/FormXml/main/{{{i}}}.xml" for i in form_ids}
        expected |= {f"Entities/{APP_TABLE}/SavedQueries/{{{i}}}.xml" for i in view_ids}
        changed = set(results["vs_before"].get("only_in_first", []) + results["vs_before"].get("only_in_second", [])
                      + results["vs_before"].get("raw_differ", []))
        results["export_expected_files"] = sorted(expected)
        results["export_changed_files"] = sorted(changed)
        results["export_unexpected_changes"] = sorted(n for n in changed if n.lower() not in {e.lower() for e in expected})
        results["column_in_export"] = []
        for name in sorted(tree(folder)):
            if name.lower().startswith("entities/" + APP_TABLE):
                with open(os.path.join(folder, name), encoding="utf-8-sig", errors="replace") as handle:
                    if NEW_COLUMN in handle.read():
                        results["column_in_export"].append(name)
        results["pack"] = pack_offline(zip_path, folder)
        results["writes"] = dv.writes
    except ProbeError as error:
        results["error"] = str(error)
    finally:
        subprocess.run(["az", "logout"], stdin=subprocess.DEVNULL, capture_output=True)
        results["ended_utc"] = utc_now()
        story = results.get("story", {})
        before, after = results.get("app_before", {}), results.get("app_after", {})
        column = after.get("new_column") or {}
        target_forms = [i for i, f in after.get("forms", {}).items() if f["name"] == APP_FORM and f["type"] == 2]
        target_views = [i for i, v in after.get("views", {}).items() if (v["name"] or "").lower() == APP_VIEW_EXACT.lower()]
        others_same = lambda kind, targets, keys: all(
            {k: before.get(kind, {}).get(i, {}).get(k) for k in keys} == {k: item.get(k) for k in keys}
            for i, item in after.get(kind, {}).items() if i not in targets)
        out = results.get("outside", {})
        results["exit_test"] = {
            "session_ran": bool(story.get("events", {}).get("events")) and story.get("ended_by") == "copilot",
            "engine_not_run": not story.get("engine_runs") and "events" in story,
            "no_allow_destructive": not story.get("destructive_flag_seen") and "events" in story,
            "column_made": column.get("type") == "String" and column.get("max_length") == 100
                           and column.get("display_name") == "Category",
            "column_on_the_form": bool(target_forms) and all(after["forms"][i]["has_column"] for i in target_forms),
            "other_forms_unchanged": bool(after.get("forms")) and others_same("forms", target_forms, ("sha",)),
            "column_in_the_view": bool(target_views) and all(after["views"][i]["in_layout"] and after["views"][i]["in_fetch"]
                                                             for i in target_views),
            "other_views_unchanged": bool(after.get("views")) and others_same("views", target_views,
                                                                                ("sha_layout", "sha_fetch")),
            "no_new_forms_or_views": set(before.get("forms", {})) == set(after.get("forms", {}))
                                     and set(before.get("views", {})) == set(after.get("views", {})) and bool(after),
            "nothing_made_outside": bool(out) and not out.get("forms_new") and not out.get("views_new")
                                    and not out.get("forms_gone") and not out.get("views_gone")
                                    and out.get("fspk_tables_after") == out.get("fspk_tables_before")
                                    and bool(out.get("spikeitem_columns_same")),
            "nothing_left_the_solution": "solution_parts_removed" in results and not results["solution_parts_removed"],
            "column_exported": f"Entities/{APP_TABLE}/Entity.xml" in results.get("column_in_export", []),
            "form_change_exported": any("/formxml/main/" in n.lower() for n in results.get("column_in_export", [])),
            "view_change_exported": any("/savedqueries/" in n.lower() for n in results.get("column_in_export", [])),
            "only_the_expected_files_changed": "export_unexpected_changes" in results
                                               and not results["export_unexpected_changes"],
            "trusted_files_unchanged": results.get("trusted_files_after") == trusted,
            "packs_signed_out": bool(results.get("pack", {}).get("pack"))
                                and results.get("pack", {}).get("repack_vs_export", {}).get("same_root_components", False),
            "packs_with_no_network": bool(results.get("pack", {}).get("pack_no_network")),
        }
        results["exit_test"]["pass"] = all(results["exit_test"].values())
        save("results.json", results)
        print(json.dumps(results["exit_test"], indent=2))


def strip_form_column(formxml):
    """The form XML with every cell bound to NEW_COLUMN removed, and any row that only held such a cell."""
    root = ElementTree.fromstring(formxml)
    removed = 0
    for rows in root.iter("rows"):
        for row in list(rows.findall("row")):
            cells = row.findall("cell")
            hits = [c for c in cells if any(ctl.get("datafieldname") == NEW_COLUMN for ctl in c.iter("control"))]
            for cell in hits:
                row.remove(cell)
                removed += 1
            if hits and len(hits) == len(cells):
                rows.remove(row)
    return ElementTree.tostring(root, encoding="unicode"), removed


def strip_view_column(layoutxml, fetchxml):
    """The view's layout and fetch with NEW_COLUMN's cell, attribute, order and conditions removed."""
    layout, fetch, removed = ElementTree.fromstring(layoutxml), ElementTree.fromstring(fetchxml), 0
    for row in layout.iter("row"):
        for cell in [c for c in row.findall("cell") if c.get("name") == NEW_COLUMN]:
            row.remove(cell)
            removed += 1
    for parent in list(fetch.iter()):
        for child in [c for c in list(parent) if c.tag in ("attribute", "order", "condition")
                      and NEW_COLUMN in (c.get("name"), c.get("attribute"))]:
            parent.remove(child)
            removed += 1
    return ElementTree.tostring(layout, encoding="unicode"), ElementTree.tostring(fetch, encoding="unicode"), removed


def cmd_part4b_undo():
    """Take part 4b's change back out of the lane: the column off the table's forms and views (published), then the
    column itself. Stops, deleting nothing, if any row holds a value in the column."""
    results = {"mode": "part4b-undo", "run_id": env("GITHUB_RUN_ID"), "steps": STEPS, "started_utc": utc_now()}
    try:
        dv = Dataverse()
        solution_header = {"MSCRM.SolutionUniqueName": SOLUTION}
        status, _, _ = dv.call("GET", f"/EntityDefinitions(LogicalName='{APP_TABLE}')/Attributes(LogicalName='{NEW_COLUMN}')"
                                      "?$select=LogicalName", ok=(200, 404))
        results["column_found"] = status == 200
        if status == 200:
            entity_set = dv.get(f"/EntityDefinitions(LogicalName='{APP_TABLE}')?$select=EntitySetName")["EntitySetName"]
            held = dv.get(f"/{entity_set}?$select={NEW_COLUMN}&$filter={NEW_COLUMN} ne null&$top=1").get("value", [])
            results["rows_with_a_value"] = len(held)
            if held:
                raise ProbeError(f"a row holds a value in {NEW_COLUMN}: nothing deleted, a person decides")
            changed = []
            for form in dv.rows(f"/systemforms?$select=formid,name,formxml&$filter=objecttypecode eq '{APP_TABLE}'"):
                if NEW_COLUMN in (form.get("formxml") or ""):
                    xml, removed = strip_form_column(form["formxml"])
                    dv.call("PATCH", f"/systemforms({form['formid']})", {"formxml": xml}, dict(solution_header, **{"If-Match": "*"}))
                    changed.append({"form": form["name"], "cells_removed": removed})
            for view in dv.rows(f"/savedqueries?$select=savedqueryid,name,layoutxml,fetchxml"
                                f"&$filter=returnedtypecode eq '{APP_TABLE}'"):
                if NEW_COLUMN in (view.get("layoutxml") or "") + (view.get("fetchxml") or ""):
                    layout, fetch, removed = strip_view_column(view["layoutxml"], view["fetchxml"])
                    dv.call("PATCH", f"/savedqueries({view['savedqueryid']})", {"layoutxml": layout, "fetchxml": fetch},
                            dict(solution_header, **{"If-Match": "*"}))
                    changed.append({"view": view["name"], "parts_removed": removed})
            results["forms_and_views_changed"] = changed
            if changed:
                dv.call("POST", "/PublishXml", {"ParameterXml": f"<importexportxml><entities><entity>{APP_TABLE}</entity>"
                                                                "</entities></importexportxml>"})
            dv.call("DELETE", f"/EntityDefinitions(LogicalName='{APP_TABLE}')/Attributes(LogicalName='{NEW_COLUMN}')")
            status, _, _ = dv.call("GET", f"/EntityDefinitions(LogicalName='{APP_TABLE}')/Attributes(LogicalName='{NEW_COLUMN}')"
                                          "?$select=LogicalName", ok=(200, 404))
            results["column_gone"] = status == 404
        results["app_after"] = {k: v for k, v in app_detail(dv).items() if k != "views"}
        results["writes"] = dv.writes
    except ProbeError as error:
        results["error"] = str(error)
    finally:
        results["ended_utc"] = utc_now()
        save("results.json", results)
        print(json.dumps({k: results.get(k) for k in ("column_found", "rows_with_a_value", "forms_and_views_changed",
                                                      "column_gone", "writes", "error")}, indent=2, default=str))
    return 1 if results.get("error") or (results.get("column_found") and not results.get("column_gone")) else 0


# ---------- deleting the scratch of spikes 0.14, 0.18 and 0.19 (Boroon, 21 November 2026) ----------
#
# Everything the spikes made in factory-lane-1 carries the publisher prefix fspk_, the names "Factory spike ...",
# or the solution FactorySpike and publisher factoryspike. scratch-list reads them; scratch-delete deletes them,
# children first, then lists again and fails if anything is left. Kept: getai-fl1-exec, its application user,
# factory-lane-1 and the allowed MCP client new_getaifl1exec (plan, Stage 3).

PREFIX = "fspk_"


def scratch_query(dv, label, path, id_field, name_field, keep=None):
    try:
        rows = dv.rows(path)
    except ProbeError as error:
        return {"label": label, "error": str(error), "rows": []}
    rows = [r for r in rows if keep is None or keep(r)]
    return {"label": label, "rows": [{"id": r.get(id_field), "name": r.get(name_field),
                                      **({"parent": r.get("_parentroleid_value")} if "_parentroleid_value" in r else {}),
                                      **({"state": r.get("statecode")} if label == "cloud flows" else {})}
                                     for r in rows]}


def scratch_parts(dv):
    """Every scratch part in the lane, found by its scratch names. Read only."""
    tables = scratch_query(dv, "tables", "/EntityDefinitions?$select=LogicalName,MetadataId,IsCustomEntity",
                           "LogicalName", "LogicalName", keep=lambda r: str(r.get("LogicalName", "")).startswith(PREFIX))
    parts = [
        scratch_query(dv, "cloud flows", "/workflows?$select=workflowid,name,statecode,category"
                      "&$filter=startswith(name,'Factory spike')", "workflowid", "name"),
        scratch_query(dv, "security roles", "/roles?$select=roleid,name,_parentroleid_value"
                      "&$filter=startswith(name,'Factory spike')", "roleid", "name"),
        scratch_query(dv, "environment variable values", "/environmentvariablevalues?$select=environmentvariablevalueid,"
                      f"schemaname&$filter=startswith(schemaname,'{PREFIX}')", "environmentvariablevalueid", "schemaname"),
        scratch_query(dv, "environment variable definitions", "/environmentvariabledefinitions?$select="
                      f"environmentvariabledefinitionid,schemaname&$filter=startswith(schemaname,'{PREFIX}')",
                      "environmentvariabledefinitionid", "schemaname"),
        scratch_query(dv, "connection references", "/connectionreferences?$select=connectionreferenceid,"
                      f"connectionreferencelogicalname&$filter=startswith(connectionreferencelogicalname,'{PREFIX}')",
                      "connectionreferenceid", "connectionreferencelogicalname"),
        scratch_query(dv, "model-driven apps", f"/appmodules?$select=appmoduleid,uniquename&$filter=startswith(uniquename,'{PREFIX}')",
                      "appmoduleid", "uniquename"),
        scratch_query(dv, "site maps", "/sitemaps?$select=sitemapid,sitemapnameunique"
                      f"&$filter=startswith(sitemapnameunique,'{PREFIX}')", "sitemapid", "sitemapnameunique"),
        scratch_query(dv, "web resources", f"/webresourceset?$select=webresourceid,name&$filter=startswith(name,'{PREFIX}')",
                      "webresourceid", "name"),
        tables,
        scratch_query(dv, "solutions", "/solutions?$select=solutionid,uniquename&$filter=uniquename eq 'FactorySpike'",
                      "solutionid", "uniquename"),
        scratch_query(dv, "publishers", "/publishers?$select=publisherid,uniquename&$filter=uniquename eq 'factoryspike'",
                      "publisherid", "uniquename"),
    ]
    for app in parts[5]["rows"]:
        settings = scratch_query(dv, "app settings", "/appsettings?$select=appsettingid,uniquename"
                                 f"&$filter=_parentappmoduleid_value eq {app['id']}", "appsettingid", "uniquename")
        settings["label"] = f"app settings of {app['name']}"
        parts.insert(5, settings)
    return parts


def scratch_table(parts):
    lines = ["| Part | Found | Names |", "|---|---|---|"]
    for part in parts:
        names = ", ".join(str(r["name"]) for r in part["rows"]) or ("(read failed: " + part["error"][:200] + ")"
                                                                    if part.get("error") else "")
        lines.append(f"| {part['label']} | {len(part['rows'])} | {names} |")
    return lines


def cmd_scratch_list():
    dv = Dataverse()
    parts = scratch_parts(dv)
    save("results.json", {"mode": "scratch-list", "parts": parts})
    lines = ["### Scratch in the lane (read only)", ""] + scratch_table(parts)
    summary_write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 1 if any(p.get("error") for p in parts) else 0


SET_FOR = {"cloud flows": "workflows", "security roles": "roles", "environment variable values": "environmentvariablevalues",
           "environment variable definitions": "environmentvariabledefinitions",
           "connection references": "connectionreferences", "model-driven apps": "appmodules", "site maps": "sitemaps",
           "web resources": "webresourceset", "solutions": "solutions", "publishers": "publishers"}


def cmd_scratch_delete():
    """Delete every scratch part, children first; then list again. Only at Boroon's word (21 November 2026)."""
    dv = Dataverse()
    before = scratch_parts(dv)
    done = []
    for part in before:
        label = part["label"]
        for row in part["rows"]:
            if label == "cloud flows" and row.get("state") == 1:
                done.append({"part": label, "name": row["name"], "turned_off": set_state(dv, row["id"], False)["status"]})
            if label == "security roles" and row.get("parent"):
                continue   # a business unit's copy goes with its root role
            if label == "tables":
                path = f"/EntityDefinitions(LogicalName='{row['id']}')"
            elif label.startswith("app settings"):
                path = f"/appsettings({row['id']})"
            else:
                path = f"/{SET_FOR[label]}({row['id']})"
            status, _, parsed = http("DELETE", dv.base + path, dv.token,
                                     headers={"OData-MaxVersion": "4.0", "OData-Version": "4.0"}, timeout=600)
            done.append({"part": label, "name": row["name"], "status": status,
                         **({"error": error_text(parsed)} if status not in (200, 204, 404) else {})})
            print(f"DELETE {label} {row['name']}: HTTP {status}")
    after = scratch_parts(dv)
    left = [{"part": p["label"], "names": [r["name"] for r in p["rows"]]} for p in after if p["rows"]]
    save("results.json", {"mode": "scratch-delete", "before": before, "deleted": done, "after": after, "left": left})
    lines = ["### Scratch deleted", "", "Before:", ""] + scratch_table(before) + ["", "Deletes:", ""]
    lines += [f"- {d['part']}: {d['name']}: HTTP {d.get('status')}" + (f" ({d['error']})" if d.get("error") else "")
              for d in done]
    lines += ["", "After:", ""] + scratch_table(after)
    lines += ["", f"## Result: **{'nothing left' if not left else 'LEFT: ' + json.dumps(left)}**"]
    summary_write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 1 if left or any(p.get("error") for p in after) else 0


def cmd_scan():
    """Delete any output file that holds a token-shaped string, before the artifact upload."""
    root = os.path.join(env("RUNNER_TEMP", "/tmp"), "tools-probe")
    pattern = re.compile(JWT.pattern.encode())
    removed = []
    for here, _, names in os.walk(root):
        for name in names:
            path = os.path.join(here, name)
            try:
                with open(path, "rb") as handle:
                    data = handle.read()
            except OSError:
                continue
            if pattern.search(data):
                os.remove(path)
                removed.append(os.path.relpath(path, root))
    line = "Token scan: removed " + (", ".join(removed) if removed else "nothing")
    print(line)
    summary_write(f"### scan\n\n{line}\n")


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
    if results["mode"] in ("part2", "part3", "part4", "part4b"):
        lines += {"part2": summary_part2, "part3": summary_part3, "part4": summary_part4,
                  "part4b": summary_part4b}[results["mode"]](results)
        summary_write("\n".join(lines) + "\n")
        print("\n".join(lines))
        return 0 if results.get("exit_test", {}).get("pass") else 1
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


def summary_part2(results):
    def short(value, limit=900):
        return json.dumps(value, default=str)[:limit]
    lines = []
    if results.get("error"):
        lines += ["", f"**error**: {results['error']}"]
    for key in ("tools", "az_login_app_spec", "az_account", "az_tokens", "az_login_flowagent"):
        if key in results:
            lines += ["", f"**{key}**: `{short(results[key], 1500)}`"]
    spec = results.get("app_spec", {})
    lines += ["", "#### App Spec", ""]
    for step in ("lint", "dry_run", "apply"):
        if step in spec:
            lines += [f"**{step}**: exit {spec[step]['exit']} in {spec[step]['seconds']} s; result `{(spec[step]['result'] or '')[:700]}`",
                      "", "```", spec[step]["stderr_tail"][-1500:], "```"]
    for key in ("stopped_at", "error", "table_exists", "apps_found", "solution_parts_added", "solution_parts_removed",
                "read_back_error"):
        if key in spec:
            lines += [f"**{key}**: `{short(spec[key])}`"]
    for key in ("flowagent_ppapi", "flowagent_fallback"):
        session = results.get(key, {})
        lines += ["", f"#### FlowAgent, {session.get('label', key)}", ""]
        lines += [f"**{k}**: `{short(session[k], 400)}`" for k in (
            "server", "protocol", "tools_listed", "listed_timer_flow", "flow_id_is", "got_flow", "updated", "ran_while_off",
            "turned_on", "state_after_on", "run", "runs_read", "turned_off", "fell_back", "tool_calls", "server_requests",
            "seconds", "backstop_turned_off", "error") if k in session]
        lines += ["", "| Tool | Arguments | Result | Seconds | Answer |", "|---|---|---|---|---|"]
        lines += [f"| {c['tool']} | `{short(c['arguments'], 120)}` | {'ERROR' if c['is_error'] else 'ok'} | {c['seconds']} | "
                  f"{c['text'][:300].replace('|', '/')} |" for c in session.get("calls", [])]
        if session.get("stderr_tail"):
            lines += ["", "```", session["stderr_tail"][-1500:], "```"]
    c = results.get("vs_reset_commit", {})
    lines += ["", f"**vs_reset_commit**: only in the commit {c.get('only_in_first')}; only in the export "
              f"{c.get('only_in_second')}; files that differ {c.get('raw_differ')}",
              f"**app_files_in_export**: `{short(results.get('app_files_in_export'))}`",
              f"**exported_compose**: `{results.get('exported_compose')}`",
              f"**pack**: `{short(results.get('pack'), 1200)}`", f"**writes**: `{short(results.get('writes'))}`",
              "", f"## Part 2 result: **{mark(results.get('exit_test', {}).get('pass'))}**"]
    return lines


def summary_part3(results):
    def short(value, limit=900):
        return json.dumps(value, default=str)[:limit]

    def cell(text, limit=300):
        return " ".join(str(text or "").split())[:limit].replace("|", "/")
    lines = []
    if results.get("error"):
        lines += ["", f"**error**: {results['error']}"]
    for key in ("started_utc", "ended_utc", "spike_table", "leftovers_before", "rows_by_name", "writes_twice",
                "cleanup", "billing"):
        if key in results:
            lines += ["", f"**{key}**: `{short(results[key], 1500)}`"]
    for key, session in results.get("sessions", {}).items():
        summary = session.get("shim_summary") or {}
        lines += ["", f"#### Session {session.get('label', key)} (cap {session.get('cap')}, {short(session.get('shim_args'))})", ""]
        lines += [f"**{k}**: `{short(session[k], 600)}`" for k in ("server", "protocol", "tools_listed", "seconds", "stop",
                                                                 "error", "own_id") if session.get(k) is not None]
        lines += [f"**shim counts**: `{short({k: summary.get(k) for k in ('calls', 'attempts', 'refused', 'retries', 'late_answers', 'outcomes', 'stops')}, 1500)}`",
                  "", "| Step | Tool | Attempts | Final | The client saw | Proxy stderr, last failed attempt |",
                  "|---|---|---|---|---|---|"]
        seen = {entry.get("step"): entry for entry in session.get("client_calls", [])}
        for name in session.get("order", []):   # results.json sorts its keys; the order list keeps the call order
            call = session.get("per_call", {}).get(name, {})
            attempts = call.get("attempts", [])
            failed = [attempt for attempt in attempts if attempt.get("kind") != "ok"]
            stderr = " / ".join((failed[-1].get("proxy_stderr") or [])[-3:]) if failed else ""
            lines.append(f"| {name} | {call.get('tool')} | {', '.join(a.get('kind') or '?' for a in attempts) or '-'} | "
                         f"{call.get('final')} | {cell(seen.get(name, {}).get('text'))} | {cell(stderr)} |")
    lines += ["", f"## Part 3 result: **{mark(results.get('exit_test', {}).get('pass'))}**"]
    return lines


def summary_part4(results):
    def short(value, limit=900):
        return json.dumps(value, default=str)[:limit]
    lines = []
    if results.get("error"):
        lines += ["", f"**error**: {results['error']}"]
    for key in ("started_utc", "ended_utc", "tools", "settings", "model_check", "without_oidc", "secret_env_vars",
                "primary_keys_read", "app_before", "app_after", "flow_before", "flow_after", "solution_parts_added",
                "solution_parts_removed", "column_in_export", "exported_compose"):
        if key in results:
            lines += ["", f"**{key}**: `{short(results[key], 1500)}`"]
    for key, story in results.get("stories", {}).items():
        lines += ["", f"#### Story {key}", ""]
        lines += [f"**{k}**: `{short(story[k], 1500)}`" for k in (
            "exit", "seconds", "ended_by", "ai_credits", "mcp_calls", "shim_stop", "destructive_flag_seen", "error",
            "redacted_files") if k in story]
        events = story.get("events", {})
        lines += [f"**event types**: `{short(events.get('types'), 1200)}`", f"**tools**: `{short(events.get('tools'), 2000)}`",
                  f"**denials** ({len(events.get('denials', []))}):"]
        lines += [f"- `{short(d, 500)}`" for d in events.get("denials", [])[:25]]
        lines += ["", "| MCP call | Tool | Kind | Attempt | Answer |", "|---|---|---|---|---|"]
        lines += [f"| {c.get('call')} | {c.get('tool')} | {c.get('kind')} | {c.get('attempt')} | "
                  f"{str(c.get('text') or '')[:200].replace('|', '/')} |" for c in story.get("mcp_call_list", [])]
        lines += ["", "**usage**: `" + short(story.get("usage"), 1500) + "`", "", "**handoff.md**:", "", "```",
                  (story.get("handoff") or "(none)")[:3000], "```", "", "**copilot stderr tail**:", "", "```",
                  (story.get("stderr_tail") or "")[-1500:], "```"]
    c = results.get("vs_reset_commit", {})
    lines += ["", f"**vs_reset_commit**: only in the commit {c.get('only_in_first')}; only in the export "
              f"{c.get('only_in_second')}; files that differ {c.get('raw_differ')}",
              f"**pack**: `{short(results.get('pack'), 1200)}`", f"**writes**: `{short(results.get('writes'))}`",
              "", f"## Part 4 result: **{mark(results.get('exit_test', {}).get('pass'))}**"]
    return lines


def summary_part4b(results):
    def short(value, limit=900):
        return json.dumps(value, default=str)[:limit]
    lines = []
    if results.get("error"):
        lines += ["", f"**error**: {results['error']}"]
    for key in ("started_utc", "ended_utc", "tools", "settings", "model_check", "without_oidc", "secret_env_vars",
                "trusted_files_before", "trusted_files_after", "app_before", "app_after", "outside",
                "solution_parts_added", "solution_parts_removed", "column_is_solution_component",
                "export_expected_files", "export_changed_files", "export_unexpected_changes", "column_in_export"):
        if key in results:
            lines += ["", f"**{key}**: `{short(results[key], 2000)}`"]
    story = results.get("story", {})
    lines += ["", f"#### Story {story.get('key')}", ""]
    lines += [f"**{k}**: `{short(story[k], 1500)}`" for k in (
        "exit", "seconds", "ended_by", "ai_credits", "mcp_calls", "shim_stop", "destructive_flag_seen", "engine_runs",
        "engine_applied", "error", "redacted_files") if k in story]
    events = story.get("events", {})
    lines += [f"**event types**: `{short(events.get('types'), 1200)}`", f"**tools**: `{short(events.get('tools'), 2000)}`",
              f"**denials** ({len(events.get('denials', []))}):"]
    lines += [f"- `{short(d, 500)}`" for d in events.get("denials", [])[:25]]
    lines += ["", "| MCP call | Tool | Kind | Attempt | Answer |", "|---|---|---|---|---|"]
    lines += [f"| {c.get('call')} | {c.get('tool')} | {c.get('kind')} | {c.get('attempt')} | "
              f"{str(c.get('text') or '')[:200].replace('|', '/')} |" for c in story.get("mcp_call_list", [])]
    lines += ["", "| Web API call | Status | Seconds | Error |", "|---|---|---|---|"]
    lines += [f"| {c.get('method')} {str(c.get('path'))[:140].replace('|', '/')} | {c.get('status', c.get('refused'))} | "
              f"{c.get('seconds')} | {str(c.get('error') or '')[:160].replace('|', '/')} |" for c in story.get("webapi_calls", [])]
    lines += ["", "**commands started**:", ""] + [f"- `{c[:300]}`" for c in story.get("commands", [])[:60]]
    lines += ["", "**usage**: `" + short(story.get("usage"), 1500) + "`", "", "**handoff.md**:", "", "```",
              (story.get("handoff") or "(none)")[:3000], "```", "", "**copilot stderr tail**:", "", "```",
              (story.get("stderr_tail") or "")[-1500:], "```"]
    c = results.get("vs_before", {})
    lines += ["", f"**vs_before**: only before {c.get('only_in_first')}; only after {c.get('only_in_second')}; "
              f"files that differ {c.get('raw_differ')}"]
    for name, sample in list(c.get("samples", {}).items())[:6]:
        lines += [f"`{name}`:", "```diff", *sample, "```"]
    lines += [f"**pack**: `{short(results.get('pack'), 1200)}`", f"**writes**: `{short(results.get('writes'))}`",
              "", f"## Part 4b result: **{mark(results.get('exit_test', {}).get('pass'))}**"]
    return lines


COMMANDS = {"flow": cmd_flow, "flow-undo": cmd_flow_undo, "part2": cmd_part2, "part3": cmd_part3, "part4": cmd_part4,
            "part4b": cmd_part4b, "part4b-undo": cmd_part4b_undo, "scratch-list": cmd_scratch_list,
            "scratch-delete": cmd_scratch_delete, "scan": cmd_scan, "summary": cmd_summary}


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
