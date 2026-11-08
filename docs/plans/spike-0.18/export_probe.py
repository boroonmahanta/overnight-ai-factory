#!/usr/bin/env python3
"""Spike 0.18 (plan 11.1): headless YAML export as the lane identity.

Published as probe/export_probe.py in GetAI-IP/export-probe (private, scratch).
Run by .github/workflows/probe.yml, one subcommand per step:

  claims    print the GitHub OIDC token's claims (never the token)
  setup     make the test solution in the lane through the Web API, as the
            lane's app user: a publisher, a solution, a table with one extra
            column, a connection reference, an environment variable, a cloud
            flow that uses both, and a security role. Safe to run again
  probe     with pac already signed in: export and unpack, clone, a second
            export and clone, unpack into a YAML tree, sync after a change,
            then sign out and pack offline. Writes results.json
  teardown  delete what setup made, and only that. Run only at Boroon's word
  summary   write the result table; exit 1 if the exit test failed

Never prints a token. Standard library only, so it runs under python3 -I.
"""

import base64
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

LOGIN_BASE = "https://login.microsoftonline.com"
API = "/api/data/v9.2"

# Scratch names. Machine-read names stay product-neutral (rule 18).
PUBLISHER = "factoryspike"
PREFIX = "fspk"
OPTION_PREFIX = 74180
SOLUTION = "FactorySpike"
TABLE_SCHEMA = "fspk_SpikeItem"
TABLE = TABLE_SCHEMA.lower()
TABLE_SET = TABLE + "s"
EXTRA_COLUMN = "fspk_Quantity"
CONNREF = "fspk_spikedataverse"
CONNECTOR = "/providers/Microsoft.PowerApps/apis/shared_commondataserviceforapps"
ENVVAR = "fspk_SpikeSetting"
ENVVAR_DESCRIPTION = "Spike 0.18 scratch setting."
FLOW_NAME = "Factory spike flow"
ROLE_NAME = "Factory spike role"
DESCRIPTION = "Spike 0.18 scratch. Made by the export probe. Remove after spikes 0.18 and 0.19."

# Fixed solution component types. Connection reference has an org-specific
# type code, read from its table's ObjectTypeCode.
TYPE_ENTITY, TYPE_ROLE, TYPE_WORKFLOW, TYPE_ENVVAR = 1, 20, 29, 380

# What the exit test needs to find in the extracted tree: a marker string each.
EXPECTED = {
    "table": TABLE,
    "flow": FLOW_NAME,
    "security role": ROLE_NAME,
    "environment variable": ENVVAR,
    "connection reference": CONNREF,
}

OIDC_KEYS = ("iss", "aud", "sub", "job_workflow_ref", "job_workflow_sha", "workflow_ref",
             "event_name", "ref", "environment", "repository", "repository_id",
             "repository_owner", "repository_owner_id", "runner_environment")


class ProbeError(Exception):
    pass


def env(name, default=""):
    return os.environ.get(name, default)


def resource():
    return env("ENV_URL").rstrip("/")


def work_dir():
    path = os.path.join(env("RUNNER_TEMP", "/tmp"), "export-probe", "pac-" + env("PAC_VERSION", "unknown"))
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


# ---------- tokens (never printed) ----------

def claims_of(jwt):
    part = jwt.split(".")[1]
    return json.loads(base64.urlsafe_b64decode(part + "=" * (-len(part) % 4)))


def github_oidc_token():
    url = env("ACTIONS_ID_TOKEN_REQUEST_URL")
    if not url:
        raise ProbeError("no ACTIONS_ID_TOKEN_REQUEST_URL: the job needs id-token: write")
    url += ("&" if "?" in url else "?") + "audience=" + urllib.parse.quote("api://AzureADTokenExchange", safe="")
    request = urllib.request.Request(url, headers={"Authorization": "Bearer " + env("ACTIONS_ID_TOKEN_REQUEST_TOKEN")})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["value"]


def app_token():
    """Client credentials, with the GitHub OIDC token as the client assertion."""
    form = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": env("APP_ID"),
        "scope": resource() + "/.default",
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
        raise ProbeError(f"token request failed: HTTP {error.code} {detail.get('error')}: "
                         f"{clip(detail.get('error_description', ''), 400)}") from None


# ---------- Web API ----------

class Dataverse:
    def __init__(self):
        self.token = app_token()
        self.base = resource() + API

    def call(self, method, path, body=None, headers=None, ok=(200, 201, 204), timeout=300):
        url = path if path.startswith("http") else self.base + path
        # OData filters hold spaces and quotes; encode what HTTP refuses, keep what OData needs.
        url = urllib.parse.quote(url, safe="/:?&=$(),'@*!-._~%+")
        data = None if body is None else json.dumps(body).encode()
        all_headers = {"Authorization": "Bearer " + self.token, "Accept": "application/json",
                       "OData-MaxVersion": "4.0", "OData-Version": "4.0"}
        if body is not None:
            all_headers["Content-Type"] = "application/json; charset=utf-8"
        all_headers.update(headers or {})
        request = urllib.request.Request(url, data=data, method=method, headers=all_headers)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                status, response_headers, text = response.status, response.headers, response.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as error:
            status, response_headers, text = error.code, error.headers, error.read().decode("utf-8", "replace")
        if status not in ok:
            raise ProbeError(f"{method} {path.split('?')[0]}: HTTP {status}: {clip(text, 600)}")
        return status, response_headers, (json.loads(text) if text.strip() else {})

    def get(self, path, ok=(200,)):
        return self.call("GET", path, ok=ok)[2]

    def rows(self, path):
        return self.get(path).get("value", [])

    def create(self, entity_set, body, in_solution=True):
        headers = {"MSCRM.SolutionUniqueName": SOLUTION} if in_solution else {}
        _, response_headers, _ = self.call("POST", "/" + entity_set, body, headers)
        entity_id = response_headers.get("OData-EntityId", "")
        match = re.search(r"\(([0-9a-fA-F-]{36})\)\s*$", entity_id)
        return match.group(1) if match else entity_id


def label(text, language):
    return {"@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [{"@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                                 "Label": text, "LanguageCode": language}]}


def quote(value):
    return value.replace("'", "''")


def flow_clientdata():
    """A manual-trigger flow that lists rows of the spike table through the connection reference."""
    return json.dumps({
        "properties": {
            "connectionReferences": {
                "shared_commondataserviceforapps": {
                    "runtimeSource": "embedded",
                    "connection": {"connectionReferenceLogicalName": CONNREF},
                    "api": {"name": "shared_commondataserviceforapps"},
                }
            },
            "definition": {
                "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
                "contentVersion": "1.0.0.0",
                "parameters": {
                    "$connections": {"defaultValue": {}, "type": "Object"},
                    "$authentication": {"defaultValue": {}, "type": "SecureObject"},
                },
                "triggers": {
                    "manual": {"metadata": {}, "type": "Request", "kind": "Button",
                               "inputs": {"schema": {"type": "object", "properties": {}, "required": []}}}
                },
                "actions": {
                    "List_rows": {
                        "runAfter": {}, "metadata": {}, "type": "OpenApiConnection",
                        "inputs": {
                            "host": {"apiId": CONNECTOR, "connectionName": "shared_commondataserviceforapps",
                                     "operationId": "ListRecords"},
                            "parameters": {"entityName": TABLE_SET, "$top": 1},
                            "authentication": "@parameters('$authentication')",
                        },
                    }
                },
            },
        },
        "schemaVersion": "1.0.0.0",
    })


def find_parts(dv):
    """Look up each scratch part by its unique name. Returns {name: id or None}."""
    found = {}
    rows = dv.rows(f"/publishers?$select=publisherid&$filter=uniquename eq '{PUBLISHER}'")
    found["publisher"] = rows[0]["publisherid"] if rows else None
    rows = dv.rows(f"/solutions?$select=solutionid&$filter=uniquename eq '{SOLUTION}'")
    found["solution"] = rows[0]["solutionid"] if rows else None
    status, _, body = dv.call("GET", f"/EntityDefinitions(LogicalName='{TABLE}')?$select=MetadataId", ok=(200, 404))
    found["table"] = body.get("MetadataId") if status == 200 else None
    rows = dv.rows(f"/connectionreferences?$select=connectionreferenceid&$filter=connectionreferencelogicalname eq '{CONNREF}'")
    found["connection reference"] = rows[0]["connectionreferenceid"] if rows else None
    rows = dv.rows(f"/environmentvariabledefinitions?$select=environmentvariabledefinitionid&$filter=schemaname eq '{ENVVAR}'")
    found["environment variable"] = rows[0]["environmentvariabledefinitionid"] if rows else None
    rows = dv.rows(f"/workflows?$select=workflowid&$filter=name eq '{quote(FLOW_NAME)}' and category eq 5")
    found["flow"] = rows[0]["workflowid"] if rows else None
    rows = dv.rows(f"/roles?$select=roleid&$filter=name eq '{quote(ROLE_NAME)}'")
    found["security role"] = rows[0]["roleid"] if rows else None
    return found


def cmd_claims():
    claims = claims_of(github_oidc_token())
    lines = [f"{key}: {claims.get(key)}" for key in OIDC_KEYS]
    print("OIDC claims (not the token):\n  " + "\n  ".join(lines))
    summary_write("OIDC claims (not the token):\n\n```\n" + "\n".join(lines) + "\n```\n")


def cmd_setup():
    dv = Dataverse()
    me = dv.get("/WhoAmI")
    org = dv.rows("/organizations?$select=languagecode,name")[0]
    language = org["languagecode"]
    print(f"Signed in as user {me['UserId']}, business unit {me['BusinessUnitId']}; org {org['name']}, language {language}")
    found = find_parts(dv)
    made = []

    if not found["publisher"]:
        found["publisher"] = dv.create("publishers", {
            "uniquename": PUBLISHER, "friendlyname": "Factory spike", "description": DESCRIPTION,
            "customizationprefix": PREFIX, "customizationoptionvalueprefix": OPTION_PREFIX}, in_solution=False)
        made.append("publisher")
    if not found["solution"]:
        found["solution"] = dv.create("solutions", {
            "uniquename": SOLUTION, "friendlyname": "Factory spike", "version": "1.0.0.0",
            "description": DESCRIPTION, "publisherid@odata.bind": f"/publishers({found['publisher']})"}, in_solution=False)
        made.append("solution")

    if not found["table"]:
        print("Creating the table (this can take a minute)")
        dv.call("POST", "/EntityDefinitions", {
            "@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata",
            "SchemaName": TABLE_SCHEMA,
            "DisplayName": label("Spike item", language),
            "DisplayCollectionName": label("Spike items", language),
            "Description": label(DESCRIPTION, language),
            "OwnershipType": "UserOwned", "IsActivity": False, "HasActivities": False, "HasNotes": False,
            "Attributes": [{
                "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
                "AttributeType": "String", "AttributeTypeName": {"Value": "StringType"},
                "SchemaName": "fspk_Name", "IsPrimaryName": True, "MaxLength": 100,
                "FormatName": {"Value": "Text"},
                "RequiredLevel": {"Value": "None", "CanBeChanged": True,
                                  "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings"},
                "DisplayName": label("Name", language), "Description": label("Primary name.", language),
            }],
        }, {"MSCRM.SolutionUniqueName": SOLUTION})
        dv.call("POST", f"/EntityDefinitions(LogicalName='{TABLE}')/Attributes", {
            "@odata.type": "Microsoft.Dynamics.CRM.IntegerAttributeMetadata",
            "AttributeType": "Integer", "AttributeTypeName": {"Value": "IntegerType"},
            "SchemaName": EXTRA_COLUMN, "MinValue": 0, "MaxValue": 1000000, "Format": "None",
            "RequiredLevel": {"Value": "None", "CanBeChanged": True,
                              "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings"},
            "DisplayName": label("Quantity", language), "Description": label("A whole number.", language),
        }, {"MSCRM.SolutionUniqueName": SOLUTION})
        found["table"] = find_parts(dv)["table"]
        made.append("table")

    if not found["connection reference"]:
        found["connection reference"] = dv.create("connectionreferences", {
            "connectionreferencelogicalname": CONNREF, "connectionreferencedisplayname": "Spike Dataverse",
            "connectorid": CONNECTOR, "description": DESCRIPTION})
        made.append("connection reference")
    if not found["environment variable"]:
        found["environment variable"] = dv.create("environmentvariabledefinitions", {
            "schemaname": ENVVAR, "displayname": "Spike setting", "description": ENVVAR_DESCRIPTION,
            "type": 100000000, "defaultvalue": "spike-default"})
        made.append("environment variable")
    if not found["flow"]:
        found["flow"] = dv.create("workflows", {
            "category": 5, "type": 1, "primaryentity": "none", "name": FLOW_NAME,
            "description": DESCRIPTION, "clientdata": flow_clientdata()})
        made.append("flow")
    if not found["security role"]:
        found["security role"] = dv.create("roles", {
            "name": ROLE_NAME, "description": DESCRIPTION,
            "businessunitid@odata.bind": f"/businessunits({me['BusinessUnitId']})"})
        made.append("security role")
        privileges = dv.rows("/privileges?$select=privilegeid,name&$filter=" + urllib.parse.quote(
            f"name eq 'prvRead{TABLE}' or name eq 'prvWrite{TABLE}' or name eq 'prvCreate{TABLE}'"))
        if privileges:
            dv.call("POST", f"/roles({found['security role']})/Microsoft.Dynamics.CRM.AddPrivilegesRole", {
                "Privileges": [{"PrivilegeId": p["privilegeid"], "BusinessUnitId": me["BusinessUnitId"],
                                "Depth": "Basic"} for p in privileges]})
            print("Role privileges added: " + ", ".join(sorted(p["name"] for p in privileges)))
        else:
            print("Finding: no privileges found for the table yet; the role has only its defaults")

    # Every part must be in the solution. Add any the create header missed.
    connref_type = dv.get("/EntityDefinitions(LogicalName='connectionreference')?$select=ObjectTypeCode")["ObjectTypeCode"]
    wanted = {"table": TYPE_ENTITY, "security role": TYPE_ROLE, "flow": TYPE_WORKFLOW,
              "environment variable": TYPE_ENVVAR, "connection reference": connref_type}
    members = {row["objectid"].lower(): row["componenttype"] for row in dv.rows(
        f"/solutioncomponents?$select=objectid,componenttype&$filter=_solutionid_value eq {found['solution']}")}
    for part, component_type in wanted.items():
        object_id = found[part]
        if object_id and object_id.lower() not in members:
            print(f"Finding: the create header did not put the {part} in the solution; adding it")
            dv.call("POST", "/AddSolutionComponent", {
                "ComponentId": object_id, "ComponentType": component_type, "SolutionUniqueName": SOLUTION,
                "AddRequiredComponents": False, "DoNotIncludeSubcomponents": False})
    members = dv.rows(f"/solutioncomponents?$select=objectid,componenttype,rootcomponentbehavior&$filter=_solutionid_value eq {found['solution']}")

    print("Publishing all customisations")
    dv.call("POST", "/PublishAllXml", {})

    lines = [f"| {part} | `{found[part]}` | {'made now' if part in made else 'already there'} |" for part in found]
    table = "| Part | ID | This run |\n|---|---|---|\n" + "\n".join(lines)
    in_solution = sorted(f"{row['componenttype']}:{row['objectid']}" for row in members)
    print(table)
    print("Solution components (type:objectid): " + ", ".join(in_solution))
    summary_write("### Setup\n\n" + table + "\n\nSolution components (type:objectid): `" + "`, `".join(in_solution) + "`\n")
    missing = [part for part in wanted if not found[part]]
    if missing:
        raise ProbeError("setup left parts missing: " + ", ".join(missing))


def cmd_teardown():
    """Delete the scratch parts, children first. Each is matched by its unique scratch name."""
    dv = Dataverse()
    found = find_parts(dv)
    done = []
    if found["flow"]:
        dv.call("DELETE", f"/workflows({found['flow']})")
        done.append("flow")
    if found["security role"]:
        dv.call("DELETE", f"/roles({found['security role']})")
        done.append("security role")
    if found["environment variable"]:
        for row in dv.rows("/environmentvariablevalues?$select=environmentvariablevalueid"
                           f"&$filter=_environmentvariabledefinitionid_value eq {found['environment variable']}"):
            dv.call("DELETE", f"/environmentvariablevalues({row['environmentvariablevalueid']})")
        dv.call("DELETE", f"/environmentvariabledefinitions({found['environment variable']})")
        done.append("environment variable")
    if found["connection reference"]:
        dv.call("DELETE", f"/connectionreferences({found['connection reference']})")
        done.append("connection reference")
    if found["table"]:
        dv.call("DELETE", f"/EntityDefinitions(LogicalName='{TABLE}')")
        done.append("table")
    if found["solution"]:
        dv.call("DELETE", f"/solutions({found['solution']})")
        done.append("solution")
    if found["publisher"]:
        dv.call("DELETE", f"/publishers({found['publisher']})")
        done.append("publisher")
    left = [part for part, value in find_parts(dv).items() if value]
    print("Deleted: " + (", ".join(done) or "nothing"))
    print("Left: " + (", ".join(left) or "nothing"))
    summary_write(f"### Teardown\n\nDeleted: {', '.join(done) or 'nothing'}. Left: {', '.join(left) or 'nothing'}.\n")
    if left:
        raise ProbeError("teardown left: " + ", ".join(left))


# ---------- the probe ----------

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
    step = {"name": name, "command": " ".join(argv), "exit": process.returncode, "seconds": seconds,
            "tail": clip(process.stdout[-1500:], 1500)}
    STEPS.append(step)
    if process.returncode != 0 and not allow_fail:
        raise ProbeError(f"{name} failed with exit {process.returncode}")
    return process.returncode == 0


def roots(folder):
    """Every folder under `folder` that is a solution root, with its format."""
    found = []
    if not os.path.isdir(folder):
        return found
    for here, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in ("bin", "obj", ".git")]
        solutions = os.path.join(here, "solutions")
        if os.path.isdir(solutions) and any(
                os.path.isfile(os.path.join(solutions, s, "solution.yml")) for s in os.listdir(solutions)):
            found.append((here, "yaml"))
        if os.path.isfile(os.path.join(here, "Other", "Solution.xml")):
            found.append((here, "xml"))
    return found


def format_of(folder):
    kinds = sorted({kind for _, kind in roots(folder)})
    return "+".join(kinds) if kinds else "none"


def root_of(folder, kind):
    for path, found in roots(folder):
        if found == kind:
            return path
    return None


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
                    samples[name] = [clip(line, 300) for line in lines[2:22]]
                except UnicodeDecodeError:
                    samples[name] = ["(binary file differs)"]
    return {"compared": True, "files": len(set(left) | set(right)), "only_in_first": only_a,
            "only_in_second": only_b, "raw_differ": raw_diff, "canonical_differ": canonical_diff,
            "samples": samples,
            "equal_canonical": not (only_a or only_b or canonical_diff)}


def zip_parts(path):
    """The member names and root components of a solution zip."""
    if not (path and os.path.isfile(path)):
        return None
    with zipfile.ZipFile(path) as archive:
        names = sorted(archive.namelist())
        roots_found = []
        if "solution.xml" in names:
            text = archive.read("solution.xml").decode("utf-8-sig", "replace")
            roots_found = sorted(re.findall(r"<RootComponent\b[^>]*/>", text))
        members = {name: archive.read(name) for name in names}
    return {"names": names, "root_components": roots_found, "members": members}


def compare_zips(a, b):
    first, second = zip_parts(a), zip_parts(b)
    if not (first and second):
        return {"compared": False}
    same_names = first["names"] == second["names"]
    differ = [n for n in first["names"] if n in second["members"] and first["members"][n] != second["members"][n]]
    return {"compared": True, "same_member_names": same_names,
            "only_in_first": sorted(set(first["names"]) - set(second["names"])),
            "only_in_second": sorted(set(second["names"]) - set(first["names"])),
            "same_root_components": first["root_components"] == second["root_components"],
            "root_components_first": first["root_components"],
            "root_components_second": second["root_components"],
            "members_that_differ": differ}


def presence(folder):
    """Which expected parts appear in the tree, and in which files."""
    found = {part: [] for part in EXPECTED}
    if not (folder and os.path.isdir(folder)):
        return found
    for name, path in tree(folder).items():
        try:
            with open(path, "rb") as handle:
                data = handle.read().decode("utf-8-sig", "replace").lower()
        except OSError:
            continue
        for part, marker in EXPECTED.items():
            if marker.lower() in data or marker.lower() in name.lower():
                found[part].append(name)
    return found


def set_envvar_description(dv, text):
    rows = dv.rows(f"/environmentvariabledefinitions?$select=environmentvariabledefinitionid&$filter=schemaname eq '{ENVVAR}'")
    if not rows:
        raise ProbeError("the environment variable is missing: run setup first")
    # Send the default value too: a description-only update clears it (run 37181326).
    dv.call("PATCH", f"/environmentvariabledefinitions({rows[0]['environmentvariabledefinitionid']})",
            {"description": text, "defaultvalue": "spike-default"}, {"If-Match": "*"})


def cmd_envvar_repro():
    """Does a description-only update clear an environment variable's default value? Leaves it restored."""
    dv = Dataverse()
    rows = dv.rows(f"/environmentvariabledefinitions?$select=environmentvariabledefinitionid,defaultvalue,description&$filter=schemaname eq '{ENVVAR}'")
    if not rows:
        raise ProbeError("the environment variable is missing: run setup first")
    row_id = rows[0]["environmentvariabledefinitionid"]
    path = f"/environmentvariabledefinitions({row_id})"
    seen = []

    def read(step):
        row = dv.get(path + "?$select=defaultvalue,description,modifiedon")
        seen.append((step, row.get("defaultvalue"), row.get("description")))

    read("start")
    dv.call("PATCH", path, {"defaultvalue": "spike-default"}, {"If-Match": "*"})
    read("after setting defaultvalue alone")
    dv.call("PATCH", path, {"description": ENVVAR_DESCRIPTION + " Repro."}, {"If-Match": "*"})
    read("after setting description alone")
    dv.call("PATCH", path, {"description": ENVVAR_DESCRIPTION, "defaultvalue": "spike-default"}, {"If-Match": "*"})
    read("after setting both")
    lines = ["| Step | defaultvalue | description |", "|---|---|---|"]
    lines += [f"| {step} | `{default}` | {description} |" for step, default, description in seen]
    print("\n".join(lines))
    summary_write("### Environment variable repro\n\n" + "\n".join(lines) + "\n")
    if seen[-1][1] != "spike-default":
        raise ProbeError("the default value was not restored")


def cmd_probe():
    w = work_dir()
    pac = "pac"
    results = {"pac_version": env("PAC_VERSION"), "run_id": env("GITHUB_RUN_ID"), "steps": STEPS}
    run("pac version", [pac, "help"])

    # Two exports and two clones, the same way each time.
    for n in (1, 2):
        run(f"export {n}", [pac, "solution", "export", "--name", SOLUTION, "--path",
                            os.path.join(w, f"export-{n}.zip"), "--overwrite"])
        run(f"unpack {n}", [pac, "solution", "unpack", "--zipfile", os.path.join(w, f"export-{n}.zip"),
                            "--folder", os.path.join(w, f"unpack-{n}"), "--packagetype", "Unmanaged"])
        run(f"clone {n}", [pac, "solution", "clone", "--name", SOLUTION, "--outputDirectory",
                           os.path.join(w, f"clone-{n}"), "--packagetype", "Unmanaged"])
    formats = {name: format_of(os.path.join(w, name)) for name in ("unpack-1", "unpack-2", "clone-1", "clone-2")}

    # Unpack into a tree that is already YAML: does unpack keep the layout it finds?
    yaml_clone = root_of(os.path.join(w, "clone-1"), "yaml")
    into = os.path.join(w, "unpack-into-yaml")
    if yaml_clone:
        shutil.copytree(yaml_clone, into)
        run("unpack into a YAML tree", [pac, "solution", "unpack", "--zipfile", os.path.join(w, "export-1.zip"),
                                        "--folder", into, "--packagetype", "Unmanaged",
                                        "--allowWrite", "--allowDelete", "--clobber"])
        formats["unpack-into-yaml"] = format_of(into)

    # Sync after a change in the lane, then after the change is undone.
    sync = {"tried": False}
    clone_project = None
    for here, _, files in os.walk(os.path.join(w, "clone-1")):
        if any(f.endswith(".cdsproj") for f in files):
            clone_project = here
            break
    if clone_project:
        sync_copy = os.path.join(w, "clone-sync")
        shutil.copytree(clone_project, sync_copy)
        sync["tried"] = True
        dv = Dataverse()
        try:
            set_envvar_description(dv, f"{ENVVAR_DESCRIPTION} Sync probe, run {env('GITHUB_RUN_ID')}.")
            sync["sync_after_change"] = run("sync after a change", [pac, "solution", "sync", "--solution-folder",
                                                                    sync_copy, "--packagetype", "Unmanaged"])
            sync["format_after_change"] = format_of(sync_copy)
            sync["changed"] = compare(clone_project, sync_copy, "clone-1", "after-sync")
        finally:
            set_envvar_description(dv, ENVVAR_DESCRIPTION)
        sync["sync_after_undo"] = run("sync after the undo", [pac, "solution", "sync", "--solution-folder",
                                                              sync_copy, "--packagetype", "Unmanaged"])
        sync["after_undo"] = compare(clone_project, sync_copy, "clone-1", "after-undo")
    results["sync"] = sync

    # Pick the YAML tree for the pack test: clone first, then unpack, then unpack-into.
    yaml_root, yaml_method = None, None
    for method, folder in (("clone", os.path.join(w, "clone-1")), ("export and unpack", os.path.join(w, "unpack-1")),
                           ("unpack into a YAML tree", into)):
        found = root_of(folder, "yaml")
        if found:
            yaml_root, yaml_method = found, method
            break
    second = {"clone": os.path.join(w, "clone-2"), "export and unpack": os.path.join(w, "unpack-2")}.get(yaml_method)
    results["yaml_method"] = yaml_method
    results["yaml_methods"] = sorted(name for name, kind in formats.items() if "yaml" in kind)
    results["formats"] = formats
    results["stable_unpack"] = compare(root_of(os.path.join(w, "unpack-1"), formats["unpack-1"].split("+")[0]),
                                       root_of(os.path.join(w, "unpack-2"), formats["unpack-2"].split("+")[0]),
                                       "unpack-1", "unpack-2")
    results["stable_clone"] = compare(root_of(os.path.join(w, "clone-1"), "yaml") or root_of(os.path.join(w, "clone-1"), "xml"),
                                      root_of(os.path.join(w, "clone-2"), "yaml") or root_of(os.path.join(w, "clone-2"), "xml"),
                                      "clone-1", "clone-2")
    results["stable_yaml"] = compare(yaml_root, root_of(second, "yaml") if second else None, "first", "second")
    results["presence"] = presence(yaml_root)
    results["yaml_tree"] = sorted(tree(yaml_root)) if yaml_root else []
    results["clone_tree"] = sorted(tree(os.path.join(w, "clone-1")))[:400]
    results["unpack_tree"] = sorted(tree(os.path.join(w, "unpack-1")))[:400]

    # Sign out, then pack. Pack must need no environment and no sign-in.
    run("sign out before pack", [pac, "auth", "clear"])
    run("profiles after sign-out", [pac, "auth", "list"])
    export_zip = os.path.join(w, "export-1.zip")
    xml_root = root_of(os.path.join(w, "unpack-1"), "xml")
    # A sandbox with no network at all, to show pack is offline. Check the sandbox
    # itself works first, so a failed sudo is not read as "no network".
    user = env("USER") or subprocess.run(["id", "-un"], capture_output=True, text=True).stdout.strip()
    keep = [f"{k}={env(k)}" for k in ("PATH", "HOME", "DOTNET_ROOT", "DOTNET_CLI_TELEMETRY_OPTOUT", "DOTNET_NOLOGO") if env(k)]
    sandbox = ["sudo", "-n", "unshare", "--net", "--"]
    sandbox_ok = run("no-network sandbox starts", sandbox + ["true"])
    net_down = sandbox_ok and not run("network is down in the sandbox", sandbox + [
        "curl", "-sS", "--max-time", "5", "-o", "/dev/null", LOGIN_BASE])
    pack = {"no_network_sandbox": net_down}

    def pack_test(kind, root):
        if not root:
            return
        repack = os.path.join(w, f"repack-{kind}.zip")
        pack[f"{kind}_pack"] = run(f"pack the {kind.upper()} tree", [pac, "solution", "pack", "--zipfile", repack,
                                                                      "--folder", root, "--packagetype", "Unmanaged"])
        pack[f"{kind}_vs_export"] = compare_zips(export_zip, repack)
        run(f"unpack the repacked {kind.upper()} zip", [pac, "solution", "unpack", "--zipfile", repack, "--folder",
                                                         os.path.join(w, f"repack-{kind}-unpack"), "--packagetype", "Unmanaged"])
        pack[f"{kind}_round_trip"] = compare(xml_root, root_of(os.path.join(w, f"repack-{kind}-unpack"), "xml"),
                                             "unpack(export)", "unpack(repack)")
        if net_down:
            nonet = os.path.join(w, f"repack-{kind}-nonet.zip")
            pack[f"{kind}_pack_no_network"] = run(f"pack the {kind.upper()} tree with no network", sandbox + [
                "sudo", "-n", "-u", user, "env", *keep,
                pac, "solution", "pack", "--zipfile", nonet, "--folder", root, "--packagetype", "Unmanaged"])
            pack[f"{kind}_nonet_vs_export"] = compare_zips(export_zip, nonet)

    pack_test("yaml", yaml_root)
    pack_test("xml", xml_root)
    results["pack"] = pack

    # The exit test (YAML), and the same checks for the plan's fallback (the XML layout).
    def verdict(root, kind, stable_result):
        present = presence(root)
        all_present = bool(root) and all(present[part] for part in EXPECTED)
        packs = bool(pack.get(f"{kind}_pack")) and pack.get(f"{kind}_vs_export", {}).get("same_root_components", False)
        stable = stable_result.get("equal_canonical", False)
        return {kind: bool(root), "all_five_parts": all_present, "packs_offline": packs,
                "packs_with_no_network": bool(pack.get(f"{kind}_pack_no_network")),
                "round_trip_same": pack.get(f"{kind}_round_trip", {}).get("equal_canonical", False),
                "second_export_same": stable, "pass": bool(root) and all_present and packs and stable}

    results["exit_test"] = verdict(yaml_root, "yaml", results["stable_yaml"])
    results["fallback_xml"] = verdict(xml_root, "xml", results["stable_unpack"])
    results["presence_xml"] = presence(xml_root)
    with open(os.path.join(w, "results.json"), "w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2, default=str)
    print(json.dumps(results["exit_test"], indent=2))


def mark(value):
    return "pass" if value else "FAIL"


def cmd_summary():
    path = os.path.join(work_dir(), "results.json")
    if not os.path.isfile(path):
        summary_write(f"### pac {env('PAC_VERSION')}\n\nNo results.json: the probe did not finish.\n")
        return 1
    with open(path, encoding="utf-8") as handle:
        results = json.load(handle)
    test, xml = results["exit_test"], results["fallback_xml"]
    lines = [f"### pac {results['pac_version']}", "",
             "| Check | YAML (exit test) | XML (fallback) |", "|---|---|---|",
             f"| The tree, headless (YAML method: {results['yaml_method'] or 'none'}) | {mark(test['yaml'])} | {mark(xml['xml'])} |",
             f"| All five parts in it | {mark(test['all_five_parts'])} | {mark(xml['all_five_parts'])} |",
             f"| Packs signed out, same root components | {mark(test['packs_offline'])} | {mark(xml['packs_offline'])} |",
             f"| Packs with no network | {mark(test['packs_with_no_network'])} | {mark(xml['packs_with_no_network'])} |",
             f"| Unpack of the repack equals unpack of the export | {mark(test['round_trip_same'])} | {mark(xml['round_trip_same'])} |",
             f"| A second export gives the same canonical files | {mark(test['second_export_same'])} | {mark(xml['second_export_same'])} |",
             f"| **Result** | **{mark(test['pass'])}** | **{mark(xml['pass'])}** |", "",
             "Formats: " + ", ".join(f"{k} = {v}" for k, v in results["formats"].items()), "",
             "| Step | Exit | Seconds |", "|---|---|---|"]
    lines += [f"| {s['name']} | {s['exit']} | {s['seconds']} |" for s in results["steps"]]
    summary_write("\n".join(lines) + "\n")
    print("\n".join(lines))
    # The job goes red only if neither layout works; the table says which one did.
    return 0 if (test["pass"] or xml["pass"]) else 1


COMMANDS = {"claims": cmd_claims, "setup": cmd_setup, "probe": cmd_probe,
            "envvar-repro": cmd_envvar_repro, "teardown": cmd_teardown, "summary": cmd_summary}


def main(argv):
    if len(argv) != 2 or argv[1] not in COMMANDS:
        print("usage: export_probe.py " + "|".join(COMMANDS), file=sys.stderr)
        return 2
    try:
        return COMMANDS[argv[1]]() or 0
    except ProbeError as error:
        print(f"::error::{error}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
