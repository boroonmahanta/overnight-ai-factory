#!/usr/bin/env python3
"""Spike 0.10 (plan 11.1, ADO 2459): Test environment behaviour, by "export both".

Published as probe/import_probe.py in GetAI-IP/import-probe (private, scratch).
Run by .github/workflows/probe.yml, one subcommand per step:

  check          print the OIDC claims (never the token), sign in to the Web API
                 and list every scratch part in that environment. Read-only
  lane           set the scratch solution in factory-lane-1 to STATE (1 to 4), as
                 the lane identity, through the Web API, then publish
  export         with pac signed in to the lane: export unmanaged and managed,
                 twice; unpack each pair with --packagetype Both; compare
  pack           no credentials, no network: the gate's own pack_offline.py on
                 the Both tree, then inspect the zips and unpack them again
  import         with pac signed in to Test: import the gate-packed managed zip
                 with the gate's flags, time it, then read Test's state
  teardown       delete every scratch part from the environment of TARGET (test
                 or lane), then list what is left; fails if anything is

STATE (scratch solution FactoryImportSpike, publisher factoryspike, prefix fspk):
  1  version 1.0.0.1: table fspk_importitem (columns fspk_kept, fspk_dropped),
     table fspk_importextra, global choice fspk_importstage, environment variable
     fspk_ImportSetting, a security role, a cloud flow with no connector (text v1)
  2  version 1.0.0.2: adds column fspk_added; the flow's text becomes v2
  3  version 1.0.0.3: drops column fspk_dropped, table fspk_importextra, the
     environment variable and the flow
  4  version 1.0.0.3 again (the same version): adds column fspk_sameversion
  5  version 1.0.0.3 again: drops column fspk_sameversion

Never prints a token. Standard library only, so it runs under python3 -I.
"""

import base64
import datetime
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
SOLUTION = "FactoryImportSpike"
HOLDING = SOLUTION + "_Upgrade"
TABLE_A_SCHEMA, TABLE_B_SCHEMA = "fspk_ImportItem", "fspk_ImportExtra"
TABLE_A, TABLE_B = TABLE_A_SCHEMA.lower(), TABLE_B_SCHEMA.lower()
SET_A, SET_B = TABLE_A + "s", TABLE_B + "s"
COLUMNS = {  # schema name: (kind, first state, last state)
    "fspk_Kept": ("int", 1, 5),
    "fspk_Dropped": ("text", 1, 2),
    "fspk_Added": ("int", 2, 5),
    "fspk_SameVersion": ("text", 4, 4),  # state 5 drops it, still at 1.0.0.3
}
CHOICE = "fspk_importstage"
ENVVAR = "fspk_ImportSetting"
ROLE = "Factory import spike role"
FLOW = "Factory import spike flow"
FLOW_TEXT = {1: "import spike v1", 2: "import spike v2"}
VERSIONS = {1: "1.0.0.1", 2: "1.0.0.2", 3: "1.0.0.3", 4: "1.0.0.3", 5: "1.0.0.3"}
DESCRIPTION = "Spike 0.10 scratch (ADO 2459). Made by the import probe. Delete after the spike."
TYPE_ENTITY, TYPE_OPTIONSET, TYPE_ROLE, TYPE_WORKFLOW, TYPE_ENVVAR = 1, 9, 20, 29, 380

OIDC_KEYS = ("iss", "aud", "sub", "job_workflow_ref", "workflow_ref", "event_name", "ref",
             "environment", "repository", "repository_id", "repository_owner_id", "runner_environment")


class ProbeError(Exception):
    pass


def env(name, default=""):
    return os.environ.get(name, default)


def root_dir():
    return os.path.join(env("RUNNER_TEMP", "/tmp"), "import-probe")


def work(name):
    path = os.path.join(root_dir(), name)
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


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def save(path, data):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, default=str)


def mark(value):
    return "yes" if value else "NO"


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


def app_token(app_id, resource):
    """Client credentials, with the GitHub OIDC token as the client assertion."""
    form = urllib.parse.urlencode({
        "grant_type": "client_credentials", "client_id": app_id, "scope": resource + "/.default",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": github_oidc_token(),
    }).encode()
    request = urllib.request.Request(f"{LOGIN_BASE}/{env('TENANT_ID')}/oauth2/v2.0/token", data=form,
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
    def __init__(self, url, app_id):
        self.resource = url.rstrip("/")
        self.base = self.resource + API
        self.token = app_token(app_id, self.resource)

    def call(self, method, path, body=None, headers=None, ok=(200, 201, 204), timeout=300):
        url = path if path.startswith("http") else self.base + path
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

    def exists(self, path):
        status, _, _ = self.call("GET", path, ok=(200, 404))
        return status == 200

    def create(self, entity_set, body, in_solution=True):
        headers = {"MSCRM.SolutionUniqueName": SOLUTION} if in_solution else {}
        _, response_headers, _ = self.call("POST", "/" + entity_set, body, headers)
        match = re.search(r"\(([0-9a-fA-F-]{36})\)\s*$", response_headers.get("OData-EntityId", ""))
        return match.group(1) if match else None


def label(text, language):
    return {"@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [{"@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                                 "Label": text, "LanguageCode": language}]}


def quote(value):
    return value.replace("'", "''")


def lane_dv():
    return Dataverse(env("LANE_URL"), env("LANE_APP_ID"))


def test_dv():
    return Dataverse(env("TEST_URL"), env("TEST_APP_ID"))


def flow_clientdata(text):
    """A cloud flow with no connector: a manual trigger and one Compose step. Left off."""
    return json.dumps({"properties": {"connectionReferences": {}, "definition": {
        "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {"$connections": {"defaultValue": {}, "type": "Object"},
                       "$authentication": {"defaultValue": {}, "type": "SecureObject"}},
        "triggers": {"manual": {"metadata": {}, "type": "Request", "kind": "Button",
                                "inputs": {"schema": {"type": "object", "properties": {}, "required": []}}}},
        "actions": {"Compose": {"runAfter": {}, "metadata": {}, "type": "Compose", "inputs": text}}}},
        "schemaVersion": "1.0.0.0"})


def compose_text(clientdata):
    try:
        return json.loads(clientdata)["properties"]["definition"]["actions"]["Compose"]["inputs"]
    except (ValueError, KeyError, TypeError):
        return None


def expected(state):
    """What the scratch solution holds at each state: part -> present?"""
    parts = {"table " + TABLE_A: True, "table " + TABLE_B: state <= 2, "global choice": True,
             "environment variable": state <= 2, "security role": True, "flow": state <= 2}
    for schema, (_, first, last) in COLUMNS.items():
        parts["column " + schema.lower()] = first <= state <= last
    return parts


def observe(dv):
    """Read the scratch parts in one environment. Read-only."""
    seen = {"at": now_utc()}
    solutions = dv.rows("/solutions?$select=uniquename,version,ismanaged,installedon,modifiedon"
                        f"&$filter=uniquename eq '{SOLUTION}' or uniquename eq '{HOLDING}'")
    seen["solutions"] = {row["uniquename"]: {"version": row.get("version"), "ismanaged": row.get("ismanaged"),
                                             "installedon": row.get("installedon"), "modifiedon": row.get("modifiedon")}
                         for row in solutions}
    present = {}
    present["table " + TABLE_A] = dv.exists(f"/EntityDefinitions(LogicalName='{TABLE_A}')?$select=LogicalName")
    present["table " + TABLE_B] = dv.exists(f"/EntityDefinitions(LogicalName='{TABLE_B}')?$select=LogicalName")
    for schema in COLUMNS:
        present["column " + schema.lower()] = present["table " + TABLE_A] and dv.exists(
            f"/EntityDefinitions(LogicalName='{TABLE_A}')/Attributes(LogicalName='{schema.lower()}')?$select=LogicalName")
    present["global choice"] = dv.exists(f"/GlobalOptionSetDefinitions(Name='{CHOICE}')")
    definitions = dv.rows("/environmentvariabledefinitions?$select=environmentvariabledefinitionid,schemaname,defaultvalue,ismanaged"
                          f"&$filter=schemaname eq '{ENVVAR}'")
    present["environment variable"] = bool(definitions)
    seen["environment variable"] = definitions
    seen["environment variable values"] = dv.rows(
        "/environmentvariablevalues?$select=environmentvariablevalueid,schemaname,value,ismanaged,_environmentvariabledefinitionid_value"
        f"&$filter=schemaname eq '{ENVVAR}'")
    roles = dv.rows(f"/roles?$select=roleid,name,ismanaged&$filter=name eq '{quote(ROLE)}'")
    present["security role"] = bool(roles)
    seen["security roles"] = len(roles)
    flows = dv.rows("/workflows?$select=workflowid,name,statecode,statuscode,ismanaged,clientdata,_ownerid_value"
                    f"&$filter=name eq '{quote(FLOW)}' and category eq 5")
    present["flow"] = bool(flows)
    seen["flows"] = [{"statecode": f.get("statecode"), "statuscode": f.get("statuscode"), "ismanaged": f.get("ismanaged"),
                      "compose": compose_text(f.get("clientdata"))} for f in flows]
    seen["present"] = present
    data = {}
    # Run 41304331: seconds after an upgrade, the Web API refused a new column that its
    # metadata already showed (0x80060888). Wait for it, and record how long that took.
    started, waited, errors = time.time(), None, []
    while True:
        try:
            if present["table " + TABLE_A]:
                cols = ",".join(["fspk_name"] + [s.lower() for s in COLUMNS if present["column " + s.lower()]])
                data[TABLE_A] = dv.rows(f"/{SET_A}?$select={cols}&$top=20")
            if present["table " + TABLE_B]:
                data[TABLE_B] = dv.rows(f"/{SET_B}?$select=fspk_name&$top=20")
            waited = round(time.time() - started, 1)
            break
        except ProbeError as error:
            if "0x80060888" not in str(error) and "0x80040217" not in str(error):
                raise
            errors.append(clip(error, 300))
            if time.time() - started > 600:
                break
            time.sleep(10)
    seen["rows_read_after_seconds"] = waited
    seen["rows_read_errors"] = errors
    for rows in data.values():
        for row in rows:
            for key in [k for k in row if k.startswith("@odata")]:
                del row[key]
    seen["rows"] = data
    return seen


def solution_history(dv, since):
    """The platform's own record of each import, upgrade and uninstall. May be refused."""
    try:
        rows = dv.call("GET", "/msdyn_solutionhistories?$filter=msdyn_name eq '" + SOLUTION + "' or msdyn_name eq '" + HOLDING + "'",
                       headers={"Prefer": 'odata.include-annotations="OData.Community.Display.V1.FormattedValue"'},
                       ok=(200,))[2].get("value", [])
    except ProbeError as error:
        return {"error": clip(error, 400)}
    keep = ("msdyn_name", "msdyn_operation", "msdyn_suboperation", "msdyn_solutionversion", "msdyn_ismanaged",
            "msdyn_starttime", "msdyn_endtime", "msdyn_totaltime", "msdyn_status", "msdyn_result",
            "msdyn_exceptionmessage", "msdyn_activityid", "msdyn_isoverwritecustomizations")
    out = []
    for row in rows:
        if since and (row.get("msdyn_starttime") or "") < since:
            continue
        item = {k: row.get(k) for k in keep if k in row}
        for k in ("msdyn_operation", "msdyn_suboperation", "msdyn_status"):
            name = row.get(k + "@OData.Community.Display.V1.FormattedValue")
            if name:
                item[k + "_name"] = name
        out.append(item)
    return sorted(out, key=lambda r: r.get("msdyn_starttime") or "")


def listing(dv):
    """Every scratch part in one environment, by its scratch name or prefix. Read-only."""
    found = {}
    found["solutions"] = [r["uniquename"] for r in dv.rows(
        "/solutions?$select=uniquename&$filter=startswith(uniquename,'FactoryImportSpike') or startswith(uniquename,'FactorySpike')")]
    found["publishers"] = [r["uniquename"] for r in dv.rows(
        f"/publishers?$select=uniquename&$filter=uniquename eq '{PUBLISHER}' or customizationprefix eq '{PREFIX}'")]
    found["tables"] = sorted(r["LogicalName"] for r in dv.rows("/EntityDefinitions?$select=LogicalName")
                             if r["LogicalName"].startswith(PREFIX + "_"))
    found["global choices"] = sorted(r["Name"] for r in dv.rows("/GlobalOptionSetDefinitions?$select=Name")
                                     if (r.get("Name") or "").startswith(PREFIX + "_"))
    found["environment variables"] = [r["schemaname"] for r in dv.rows(
        f"/environmentvariabledefinitions?$select=schemaname&$filter=startswith(schemaname,'{PREFIX}_')")]
    found["environment variable values"] = [r["schemaname"] for r in dv.rows(
        f"/environmentvariablevalues?$select=schemaname&$filter=startswith(schemaname,'{PREFIX}_')")]
    found["roles"] = [r["name"] for r in dv.rows("/roles?$select=name&$filter=startswith(name,'Factory import spike') or startswith(name,'Factory spike')")]
    found["workflows"] = [r["name"] for r in dv.rows("/workflows?$select=name&$filter=startswith(name,'Factory import spike') or startswith(name,'Factory spike')")]
    found["connection references"] = [r["connectionreferencelogicalname"] for r in dv.rows(
        f"/connectionreferences?$select=connectionreferencelogicalname&$filter=startswith(connectionreferencelogicalname,'{PREFIX}_')")]
    return found


def listing_table(found):
    lines = ["| Kind | Found |", "|---|---|"]
    lines += [f"| {kind} | {', '.join(f'`{n}`' for n in names) or 'none'} |" for kind, names in found.items()]
    return "\n".join(lines)


# ---------- check ----------

def cmd_check():
    claims = claims_of(github_oidc_token())
    lines = [f"{key}: {claims.get(key)}" for key in OIDC_KEYS]
    print("OIDC claims (not the token):\n  " + "\n  ".join(lines))
    target = env("TARGET")
    dv = test_dv() if target == "test" else lane_dv()
    me = dv.get("/WhoAmI")
    org = dv.rows("/organizations?$select=name,languagecode")[0]
    found = listing(dv)
    print(f"Signed in to {org['name']} as user {me['UserId']}")
    print(json.dumps(found, indent=2))
    summary_write(f"### Check: {target}\n\nOIDC claims (not the token):\n\n```\n" + "\n".join(lines) +
                  f"\n```\n\nSigned in to `{org['name']}` (WhoAmI user `{me['UserId']}`).\n\n" + listing_table(found) + "\n")


# ---------- lane state ----------

def find_lane(dv):
    found = {}
    rows = dv.rows(f"/publishers?$select=publisherid&$filter=uniquename eq '{PUBLISHER}'")
    found["publisher"] = rows[0]["publisherid"] if rows else None
    rows = dv.rows(f"/solutions?$select=solutionid,version&$filter=uniquename eq '{SOLUTION}'")
    found["solution"] = rows[0]["solutionid"] if rows else None
    found["solution version"] = rows[0]["version"] if rows else None
    for table in (TABLE_A, TABLE_B):
        status, _, body = dv.call("GET", f"/EntityDefinitions(LogicalName='{table}')?$select=MetadataId", ok=(200, 404))
        found["table " + table] = body.get("MetadataId") if status == 200 else None
    status, _, body = dv.call("GET", f"/GlobalOptionSetDefinitions(Name='{CHOICE}')", ok=(200, 404))
    found["global choice"] = body.get("MetadataId") if status == 200 else None
    rows = dv.rows(f"/environmentvariabledefinitions?$select=environmentvariabledefinitionid&$filter=schemaname eq '{ENVVAR}'")
    found["environment variable"] = rows[0]["environmentvariabledefinitionid"] if rows else None
    rows = dv.rows(f"/roles?$select=roleid&$filter=name eq '{quote(ROLE)}'")
    found["security role"] = rows[0]["roleid"] if rows else None
    rows = dv.rows(f"/workflows?$select=workflowid,clientdata&$filter=name eq '{quote(FLOW)}' and category eq 5")
    found["flow"] = rows[0]["workflowid"] if rows else None
    found["flow text"] = compose_text(rows[0]["clientdata"]) if rows else None
    return found


def make_table(dv, schema, display, language):
    print(f"Creating table {schema} (can take a minute)")
    dv.call("POST", "/EntityDefinitions", {
        "@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata", "SchemaName": schema,
        "DisplayName": label(display, language), "DisplayCollectionName": label(display + "s", language),
        "Description": label(DESCRIPTION, language), "OwnershipType": "UserOwned",
        "IsActivity": False, "HasActivities": False, "HasNotes": False,
        "Attributes": [{
            "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
            "AttributeType": "String", "AttributeTypeName": {"Value": "StringType"},
            "SchemaName": "fspk_Name", "IsPrimaryName": True, "MaxLength": 100, "FormatName": {"Value": "Text"},
            "RequiredLevel": {"Value": "None", "CanBeChanged": True,
                              "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings"},
            "DisplayName": label("Name", language), "Description": label("Primary name.", language)}],
    }, {"MSCRM.SolutionUniqueName": SOLUTION}, timeout=600)


def make_column(dv, schema, kind, language):
    print(f"Creating column {schema}")
    if kind == "int":
        body = {"@odata.type": "Microsoft.Dynamics.CRM.IntegerAttributeMetadata", "AttributeType": "Integer",
                "AttributeTypeName": {"Value": "IntegerType"}, "MinValue": 0, "MaxValue": 1000000, "Format": "None"}
    else:
        body = {"@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata", "AttributeType": "String",
                "AttributeTypeName": {"Value": "StringType"}, "MaxLength": 100, "FormatName": {"Value": "Text"}}
    body.update({"SchemaName": schema,
                 "RequiredLevel": {"Value": "None", "CanBeChanged": True,
                                   "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings"},
                 "DisplayName": label(schema.split("_", 1)[1], language), "Description": label(DESCRIPTION, language)})
    dv.call("POST", f"/EntityDefinitions(LogicalName='{TABLE_A}')/Attributes", body,
            {"MSCRM.SolutionUniqueName": SOLUTION}, timeout=600)


def cmd_lane():
    state = int(env("STATE"))
    if state not in VERSIONS:
        raise ProbeError("STATE must be 1 to 5")
    dv = lane_dv()
    me = dv.get("/WhoAmI")
    language = dv.rows("/organizations?$select=languagecode")[0]["languagecode"]
    found = find_lane(dv)
    actions = []

    if not found["publisher"]:
        found["publisher"] = dv.create("publishers", {
            "uniquename": PUBLISHER, "friendlyname": "Factory spike", "description": DESCRIPTION,
            "customizationprefix": PREFIX, "customizationoptionvalueprefix": OPTION_PREFIX}, in_solution=False)
        actions.append("made the publisher")
    if not found["solution"]:
        found["solution"] = dv.create("solutions", {
            "uniquename": SOLUTION, "friendlyname": "Factory import spike", "version": VERSIONS[state],
            "description": DESCRIPTION, "publisherid@odata.bind": f"/publishers({found['publisher']})"}, in_solution=False)
        actions.append("made the solution")
    if not found["global choice"]:
        dv.call("POST", "/GlobalOptionSetDefinitions", {
            "@odata.type": "Microsoft.Dynamics.CRM.OptionSetMetadata", "Name": CHOICE, "IsGlobal": True,
            "OptionSetType": "Picklist", "DisplayName": label("Import stage", language),
            "Description": label(DESCRIPTION, language),
            "Options": [{"Value": OPTION_PREFIX * 10000 + n, "Label": label(text, language)}
                        for n, text in enumerate(("One", "Two"))]}, {"MSCRM.SolutionUniqueName": SOLUTION})
        actions.append("made the global choice")
    if not found["table " + TABLE_A]:
        make_table(dv, TABLE_A_SCHEMA, "Import item", language)
        actions.append("made table " + TABLE_A)
    for schema, (kind, first, last) in COLUMNS.items():
        path = f"/EntityDefinitions(LogicalName='{TABLE_A}')/Attributes(LogicalName='{schema.lower()}')"
        there = dv.exists(path + "?$select=LogicalName")
        if first <= state <= last and not there:
            make_column(dv, schema, kind, language)
            actions.append("made column " + schema.lower())
        elif not (first <= state <= last) and there:
            dv.call("DELETE", path, timeout=600)
            actions.append("deleted column " + schema.lower())
    if state <= 2 and not found["table " + TABLE_B]:
        make_table(dv, TABLE_B_SCHEMA, "Import extra", language)
        actions.append("made table " + TABLE_B)
    elif state > 2 and found["table " + TABLE_B]:
        dv.call("DELETE", f"/EntityDefinitions(LogicalName='{TABLE_B}')", timeout=600)
        actions.append("deleted table " + TABLE_B)
    if state <= 2 and not found["environment variable"]:
        dv.create("environmentvariabledefinitions", {
            "schemaname": ENVVAR, "displayname": "Import setting", "description": DESCRIPTION,
            "type": 100000000, "defaultvalue": "lane-default"})
        actions.append("made the environment variable")
    elif state > 2 and found["environment variable"]:
        for row in dv.rows("/environmentvariablevalues?$select=environmentvariablevalueid"
                           f"&$filter=_environmentvariabledefinitionid_value eq {found['environment variable']}"):
            dv.call("DELETE", f"/environmentvariablevalues({row['environmentvariablevalueid']})")
        dv.call("DELETE", f"/environmentvariabledefinitions({found['environment variable']})")
        actions.append("deleted the environment variable")
    if not found["security role"]:
        found["security role"] = dv.create("roles", {
            "name": ROLE, "description": DESCRIPTION, "businessunitid@odata.bind": f"/businessunits({me['BusinessUnitId']})"})
        privileges = dv.rows("/privileges?$select=privilegeid,name&$filter=" + urllib.parse.quote(
            f"name eq 'prvRead{TABLE_A}' or name eq 'prvWrite{TABLE_A}' or name eq 'prvCreate{TABLE_A}'"))
        if privileges:
            dv.call("POST", f"/roles({found['security role']})/Microsoft.Dynamics.CRM.AddPrivilegesRole", {
                "Privileges": [{"PrivilegeId": p["privilegeid"], "BusinessUnitId": me["BusinessUnitId"], "Depth": "Basic"}
                               for p in privileges]})
        actions.append(f"made the security role ({len(privileges)} privileges)")
    if state <= 2:
        text = FLOW_TEXT[state]
        if not found["flow"]:
            dv.create("workflows", {"category": 5, "type": 1, "primaryentity": "none", "name": FLOW,
                                    "description": DESCRIPTION, "clientdata": flow_clientdata(text)})
            actions.append(f"made the flow ({text})")
        elif found["flow text"] != text:
            dv.call("PATCH", f"/workflows({found['flow']})", {"clientdata": flow_clientdata(text)}, {"If-Match": "*"})
            actions.append(f"changed the flow's text to {text}")
    elif found["flow"]:
        dv.call("DELETE", f"/workflows({found['flow']})")
        actions.append("deleted the flow")
    if found["solution version"] != VERSIONS[state]:
        dv.call("PATCH", f"/solutions({found['solution']})", {"version": VERSIONS[state]}, {"If-Match": "*"})
        actions.append(f"set the version to {VERSIONS[state]}")

    # Every kept part must be a solution component. Add any that the create header missed.
    found = find_lane(dv)
    members = {row["objectid"].lower() for row in dv.rows(
        f"/solutioncomponents?$select=objectid,componenttype&$filter=_solutionid_value eq {found['solution']}")}
    wanted = {"table " + TABLE_A: TYPE_ENTITY, "table " + TABLE_B: TYPE_ENTITY, "global choice": TYPE_OPTIONSET,
              "security role": TYPE_ROLE, "flow": TYPE_WORKFLOW, "environment variable": TYPE_ENVVAR}
    for part, component_type in wanted.items():
        object_id = found.get(part)
        if object_id and object_id.lower() not in members:
            dv.call("POST", "/AddSolutionComponent", {
                "ComponentId": object_id, "ComponentType": component_type, "SolutionUniqueName": SOLUTION,
                "AddRequiredComponents": False, "DoNotIncludeSubcomponents": False})
            actions.append(f"added the {part} to the solution (the header missed it)")
    started = time.time()
    dv.call("POST", "/PublishAllXml", {}, timeout=900)
    actions.append(f"published all ({round(time.time() - started, 1)} s)")
    components = sorted(f"{r['componenttype']}:{r['objectid']}" for r in dv.rows(
        f"/solutioncomponents?$select=objectid,componenttype&$filter=_solutionid_value eq {found['solution']}"))

    seen = observe(dv)
    want = expected(state)
    wrong = [part for part, value in want.items() if seen["present"].get(part) != value]
    version = seen["solutions"].get(SOLUTION, {}).get("version")
    out = {"state": state, "actions": actions, "components": components, "seen": seen, "wrong": wrong, "version": version}
    save(os.path.join(work("lane"), "lane.json"), out)
    lines = [f"### Lane state {state} (version {version})", "", "Actions: " + "; ".join(actions or ["none needed"]), "",
             "| Part | Wanted | In the lane |", "|---|---|---|"]
    lines += [f"| {part} | {mark(value)} | {mark(seen['present'].get(part))} |" for part, value in want.items()]
    lines += ["", "Solution components (type:objectid): " + ", ".join(f"`{c}`" for c in components)]
    summary_write("\n".join(lines) + "\n")
    print("\n".join(lines))
    if wrong or version != VERSIONS[state]:
        raise ProbeError(f"the lane is not at state {state}: wrong {wrong}, version {version}")


# ---------- commands, trees and zips ----------

STEPS = []
LOGS = []  # a command may set its own log folder


def run(name, argv, cwd=None, logs=None):
    """Run a command, keep its output in a log file, record the step."""
    logs = logs or (LOGS[0] if LOGS else os.path.join(root_dir(), "logs"))
    os.makedirs(logs, exist_ok=True)
    log_path = os.path.join(logs, re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") + ".log")
    started = time.time()
    print(f"\n::group::{name}: {' '.join(argv)}", flush=True)
    process = subprocess.run(argv, cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, text=True)
    seconds = round(time.time() - started, 1)
    with open(log_path, "w", encoding="utf-8") as handle:
        handle.write(process.stdout)
    print(process.stdout[-8000:])
    print(f"::endgroup::\n{name}: exit {process.returncode} in {seconds} s", flush=True)
    STEPS.append({"name": name, "command": " ".join(argv), "exit": process.returncode, "seconds": seconds,
                  "tail": clip(process.stdout[-2000:], 2000)})
    return process.returncode == 0


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
    only_a, only_b = sorted(set(left) - set(right)), sorted(set(right) - set(left))
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
    return {"compared": True, "files": len(set(left) | set(right)), "only_in_first": only_a, "only_in_second": only_b,
            "raw_differ": raw_diff, "canonical_differ": canonical_diff, "samples": samples,
            "byte_identical": not (only_a or only_b or raw_diff),
            "equal_canonical": not (only_a or only_b or canonical_diff)}


def zip_facts(path):
    if not (path and os.path.isfile(path)):
        return None
    with zipfile.ZipFile(path) as archive:
        names = sorted(archive.namelist())
        text = archive.read("solution.xml").decode("utf-8-sig", "replace") if "solution.xml" in names else ""
        members = {name: archive.read(name) for name in names}
    managed = re.search(r"<Managed>(\d)</Managed>", text)
    version = re.search(r"<Version>([^<]+)</Version>", text)
    return {"bytes": os.path.getsize(path), "names": names, "managed": managed.group(1) if managed else None,
            "version": version.group(1) if version else None,
            "root_components": sorted(re.findall(r"<RootComponent\b[^>]*/>", text)), "members": members}


def compare_zips(a, b):
    first, second = zip_facts(a), zip_facts(b)
    if not (first and second):
        return {"compared": False}
    return {"compared": True, "same_member_names": first["names"] == second["names"],
            "only_in_first": sorted(set(first["names"]) - set(second["names"])),
            "only_in_second": sorted(set(second["names"]) - set(first["names"])),
            "same_root_components": first["root_components"] == second["root_components"],
            "members_that_differ": [n for n in first["names"] if n in second["members"]
                                    and first["members"][n] != second["members"][n]],
            "managed": [first["managed"], second["managed"]], "version": [first["version"], second["version"]]}


def public(facts):
    return {k: v for k, v in (facts or {}).items() if k != "members"} if facts else None


# ---------- export ----------

def cmd_export():
    w = work("export")
    results = {"state": env("STATE"), "pac_version": env("PAC_VERSION"), "run_id": env("GITHUB_RUN_ID"), "steps": STEPS}
    try:
        for n in (1, 2):
            d = os.path.join(w, f"round-{n}")
            os.makedirs(d, exist_ok=True)
            unmanaged, managed = os.path.join(d, SOLUTION + ".zip"), os.path.join(d, SOLUTION + "_managed.zip")
            run(f"export unmanaged {n}", ["pac", "solution", "export", "--name", SOLUTION, "--path", unmanaged, "--overwrite"])
            run(f"export managed {n}", ["pac", "solution", "export", "--name", SOLUTION, "--path", managed,
                                        "--managed", "--overwrite"])
            run(f"unpack Both {n}", ["pac", "solution", "unpack", "--zipfile", unmanaged, "--folder",
                                     os.path.join(d, "src"), "--packagetype", "Both"])
        r1 = os.path.join(w, "round-1")
        run("unpack Unmanaged only 1", ["pac", "solution", "unpack", "--zipfile", os.path.join(r1, SOLUTION + ".zip"),
                                        "--folder", os.path.join(r1, "unmanaged-only"), "--packagetype", "Unmanaged"])
        run("unpack Managed only 1", ["pac", "solution", "unpack", "--zipfile", os.path.join(r1, SOLUTION + "_managed.zip"),
                                      "--folder", os.path.join(r1, "managed-only"), "--packagetype", "Managed"])
        src, unmanaged_only = os.path.join(r1, "src"), os.path.join(r1, "unmanaged-only")
        both, plain = tree(src), tree(unmanaged_only)
        same_name_differ = []
        for name in sorted(set(both) & set(plain)):
            with open(both[name], "rb") as h1, open(plain[name], "rb") as h2:
                if h1.read() != h2.read():
                    same_name_differ.append(name)
        results["both_tree"] = sorted(both)
        results["both_extra_files"] = sorted(set(both) - set(plain))
        results["both_missing_files"] = sorted(set(plain) - set(both))
        results["both_same_name_but_differ"] = same_name_differ
        results["both_vs_unmanaged_samples"] = compare(unmanaged_only, src, "unmanaged-only", "both")["samples"]
        results["second_export_both_tree"] = compare(src, os.path.join(w, "round-2", "src"), "round-1", "round-2")
        results["second_export_unmanaged_zip"] = compare_zips(os.path.join(r1, SOLUTION + ".zip"),
                                                              os.path.join(w, "round-2", SOLUTION + ".zip"))
        results["second_export_managed_zip"] = compare_zips(os.path.join(r1, SOLUTION + "_managed.zip"),
                                                            os.path.join(w, "round-2", SOLUTION + "_managed.zip"))
        results["zips"] = {name: public(zip_facts(os.path.join(r1, name))) for name in (SOLUTION + ".zip", SOLUTION + "_managed.zip")}
    finally:
        save(os.path.join(w, "export.json"), results)
    times = {s["name"]: s["seconds"] for s in STEPS}
    unmanaged_s = [times.get(f"export unmanaged {n}") for n in (1, 2)]
    managed_s = [times.get(f"export managed {n}") for n in (1, 2)]
    stable = results["second_export_both_tree"]
    lines = [f"### Export, state {env('STATE')} (pac {env('PAC_VERSION')})", "",
             "| Step | Exit | Seconds |", "|---|---|---|"]
    lines += [f"| {s['name']} | {s['exit']} | {s['seconds']} |" for s in STEPS]
    lines += ["", f"Export seconds, unmanaged: {unmanaged_s}; managed: {managed_s}.",
              f"Second export, Both tree byte-identical: **{mark(stable.get('byte_identical'))}** "
              f"(canonical: {mark(stable.get('equal_canonical'))}; {stable.get('files')} files; "
              f"differ: {stable.get('raw_differ')}; only in one: {stable.get('only_in_first')} {stable.get('only_in_second')}).",
              f"Files Both writes beyond an Unmanaged unpack: {results['both_extra_files']}.",
              f"Same name, different bytes: {results['both_same_name_but_differ']}. Missing from Both: {results['both_missing_files']}."]
    summary_write("\n".join(lines) + "\n")
    print("\n".join(lines))
    if any(s["exit"] != 0 for s in STEPS):
        raise ProbeError("an export or unpack step failed")


# ---------- pack (no credentials) ----------

def cmd_pack():
    version = env("PAC_VERSION")
    w = work(f"pack-{version}")
    LOGS.append(os.path.join(w, "logs"))
    export_dir = os.path.join(root_dir(), "export", "round-1")
    src = os.path.join(export_dir, "src")
    gate_pack = os.path.join(env("GITHUB_WORKSPACE"), "probe", "pack_offline.py")
    out = os.path.join(w, "out")
    results = {"state": env("STATE"), "pac_version": version, "run_id": env("GITHUB_RUN_ID"), "steps": STEPS}
    try:
        user = env("USER") or subprocess.run(["id", "-un"], capture_output=True, text=True).stdout.strip()
        keep = [f"{k}={env(k)}" for k in ("PATH", "HOME", "DOTNET_ROOT", "DOTNET_CLI_TELEMETRY_OPTOUT", "DOTNET_NOLOGO") if env(k)]
        sandbox = ["sudo", "-n", "unshare", "--net", "--"]
        as_user = sandbox + ["sudo", "-n", "-u", user, "env", *keep]
        sandbox_ok = run("no-network sandbox starts", sandbox + ["true"])
        net_down = sandbox_ok and not run("network is down in the sandbox", sandbox + [
            "curl", "-sS", "--max-time", "5", "-o", "/dev/null", LOGIN_BASE])
        results["no_network"] = net_down
        prefix = as_user if net_down else []
        results["pack_ok"] = run("gate pack_offline.py solution (Unmanaged, then Managed)",
                                 prefix + [sys.executable, "-I", gate_pack, "solution", "--source", src, "--out", out])
        packed_u, packed_m = os.path.join(out, "solution_unmanaged.zip"), os.path.join(out, "solution_managed.zip")
        results["packed"] = {"unmanaged": public(zip_facts(packed_u)), "managed": public(zip_facts(packed_m))}
        results["vs_export_unmanaged"] = compare_zips(os.path.join(export_dir, SOLUTION + ".zip"), packed_u)
        results["vs_export_managed"] = compare_zips(os.path.join(export_dir, SOLUTION + "_managed.zip"), packed_m)
        run("unpack the packed unmanaged zip", prefix + ["pac", "solution", "unpack", "--zipfile", packed_u, "--folder",
                                                         os.path.join(w, "rt-unmanaged"), "--packagetype", "Unmanaged"])
        run("unpack the packed managed zip", prefix + ["pac", "solution", "unpack", "--zipfile", packed_m, "--folder",
                                                       os.path.join(w, "rt-managed"), "--packagetype", "Managed"])
        results["round_trip_unmanaged"] = compare(os.path.join(export_dir, "unmanaged-only"), os.path.join(w, "rt-unmanaged"),
                                                  "unpack(export)", "unpack(pack)")
        results["round_trip_managed"] = compare(os.path.join(export_dir, "managed-only"), os.path.join(w, "rt-managed"),
                                                "unpack(export managed)", "unpack(pack managed)")
    finally:
        save(os.path.join(w, "pack.json"), results)
    p = results.get("packed", {})
    lines = [f"### Pack offline, state {env('STATE')} (pac {version})", "",
             f"No network in the sandbox: **{mark(results.get('no_network'))}**. The gate's `pack_offline.py`: **{mark(results.get('pack_ok'))}**.", "",
             "| Zip | Managed flag | Version | Same members as the export | Same root components | Unpack equals the export's (canonical) |",
             "|---|---|---|---|---|---|"]
    for kind in ("unmanaged", "managed"):
        facts, versus = p.get(kind) or {}, results.get(f"vs_export_{kind}", {})
        trip = results.get(f"round_trip_{kind}", {})
        lines.append(f"| {kind} | {facts.get('managed')} | {facts.get('version')} | {mark(versus.get('same_member_names'))} | "
                     f"{mark(versus.get('same_root_components'))} | {mark(trip.get('equal_canonical'))} |")
    lines += ["", "| Step | Exit | Seconds |", "|---|---|---|"] + [f"| {s['name']} | {s['exit']} | {s['seconds']} |" for s in STEPS]
    summary_write("\n".join(lines) + "\n")
    print("\n".join(lines))
    if not results.get("pack_ok"):
        raise ProbeError("the gate's pack failed")


# ---------- import into Test ----------

def settings_file(w, zip_path, state, mode):
    path = os.path.join(w, "settings.json")
    if mode == "none":
        return None, None
    if mode == "stale":
        data = {"EnvironmentVariables": [{"SchemaName": ENVVAR, "Value": "test-value-stale"}], "ConnectionReferences": []}
    else:
        run("create settings from the zip", ["pac", "solution", "create-settings", "--solution-zip", zip_path,
                                              "--settings-file", path])
        with open(path, encoding="utf-8-sig") as handle:
            data = json.load(handle)
        for item in data.get("EnvironmentVariables", []):
            item["Value"] = f"test-value-s{state}"
    save(path, data)
    return path, data


def cmd_import():
    state = int(env("STATE"))
    w = work("import")
    zip_path = os.path.join(root_dir(), "pack-" + env("PAC_VERSION"), "out", "solution_managed.zip")
    results = {"state": state, "pac_version": env("PAC_VERSION"), "run_id": env("GITHUB_RUN_ID"),
               "zip": public(zip_facts(zip_path)), "steps": STEPS}
    try:
        dv = test_dv()
        results["before"] = observe(dv)
        if env("CHECKER") == "true":
            # The gate's checker_gate.py needs the report zip in --outputDirectory. Run 41298256
            # (pac 2.4.1) said it downloaded one file but the folder was empty, so try both
            # versions and look for the report anywhere it might have gone.
            results["checker"] = {}
            for version, binary in (("2.4.1", "pac"), ("2.15.1", env("PAC_ALT"))):
                if not binary:
                    continue
                out_dir = os.path.join(w, f"checker-{version}")
                started_at = time.time()
                ok = run(f"solution checker as the Test identity (pac {version})", [
                    binary, "solution", "check", "--path", zip_path, "--geo", "Australia", "--outputDirectory", out_dir],
                    cwd=w)
                found = []
                for base in (root_dir(), env("GITHUB_WORKSPACE"), env("HOME")):
                    for here, dirs, names in os.walk(base or "/nonexistent"):
                        dirs[:] = [d for d in dirs if d not in (".git", ".nuget", ".dotnet", "node_modules")]
                        for name in names:
                            path = os.path.join(here, name)
                            if (name.lower().endswith((".sarif", ".zip")) and "FactoryImportSpike" in name
                                    and os.path.getmtime(path) >= started_at - 1):
                                found.append(path)
                results["checker"][version] = {"exit_ok": ok, "out_dir_exists": os.path.isdir(out_dir),
                                               "out_dir_files": sorted(tree(out_dir)) if os.path.isdir(out_dir) else [],
                                               "report_files_anywhere": sorted(found)}
        path, data = settings_file(w, zip_path, state, env("SETTINGS", "fresh"))
        results["settings"] = data
        argv = ["pac", "solution", "import", "--path", zip_path]
        if path:
            argv += ["--settings-file", path]
        if env("IMPORT_MODE", "gate") == "gate":
            argv += ["--stage-and-upgrade"]
        argv += ["--async", "--max-async-wait-time", "30"]
        started = now_utc()
        results["import_started"] = started
        results["import_mode"] = env("IMPORT_MODE", "gate")
        results["import_ok"] = run("import managed (" + ("the gate's flags, --stage-and-upgrade" if results["import_mode"] == "gate"
                                                          else "plain, no --stage-and-upgrade") + ")", argv)
        dv = test_dv()  # a fresh token: the import can outlast nothing, but be safe
        results["after"] = observe(dv)
        results["history"] = solution_history(dv, started[:16])
        want = expected(state)
        results["expected"] = want
        results["wrong"] = [p for p, v in want.items() if results["after"]["present"].get(p) != v]
        if env("SEED") == "true" and results["import_ok"]:
            body = {"fspk_name": f"seed-{env('GITHUB_RUN_ID')}"}
            if results["after"]["present"].get("column fspk_dropped"):
                body["fspk_dropped"] = "seeded before the drop"
            if results["after"]["present"].get("column fspk_kept"):
                body["fspk_kept"] = 7
            dv.call("POST", "/" + SET_A, body)
            if results["after"]["present"].get("table " + TABLE_B):
                dv.call("POST", "/" + SET_B, {"fspk_name": f"seed-extra-{env('GITHUB_RUN_ID')}"})
            results["seeded"] = observe(dv)["rows"]
    finally:
        save(os.path.join(w, "import.json"), results)
    after, before = results.get("after", {}), results.get("before", {})
    step = next((s for s in STEPS if s["name"].startswith("import managed")), {})
    lines = [f"### Import into Test, state {state} (pac {env('PAC_VERSION')}, import {env('IMPORT_MODE', 'gate')}, settings {env('SETTINGS', 'fresh')})", "",
             f"Checker: {json.dumps(results.get('checker'))}.",
             f"Before: {json.dumps(before.get('solutions'))}. After: {json.dumps(after.get('solutions'))}.",
             f"Import exit {step.get('exit')} in **{step.get('seconds')} s**.", "",
             "| Part | Expected | Before | After |", "|---|---|---|---|"]
    for part, value in results.get("expected", {}).items():
        lines.append(f"| {part} | {mark(value)} | {mark(before.get('present', {}).get(part))} | {mark(after.get('present', {}).get(part))} |")
    lines += ["", f"Flows after: {json.dumps(after.get('flows'))}.",
              f"Environment variable values after: {json.dumps(after.get('environment variable values'))}.",
              f"Rows after: {json.dumps(after.get('rows'))}.",
              f"Not as expected: {results.get('wrong')}.", "",
              "Solution history since the import started:", "", "```", json.dumps(results.get("history"), indent=1)[:6000], "```", "",
              "| Step | Exit | Seconds |", "|---|---|---|"] + [f"| {s['name']} | {s['exit']} | {s['seconds']} |" for s in STEPS]
    summary_write("\n".join(lines) + "\n")
    print("\n".join(lines))
    if not results.get("import_ok"):
        raise ProbeError("the import failed")


# ---------- teardown ----------

def cmd_teardown():
    target = env("TARGET")
    dv = test_dv() if target == "test" else lane_dv()
    before = listing(dv)
    done = []
    if target == "test":
        for name in (HOLDING, SOLUTION):
            for row in dv.rows(f"/solutions?$select=solutionid&$filter=uniquename eq '{name}'"):
                started = time.time()
                dv.call("DELETE", f"/solutions({row['solutionid']})", timeout=1800)
                done.append(f"uninstalled {name} ({round(time.time() - started, 1)} s)")
    else:
        found = find_lane(dv)
        if found["flow"]:
            dv.call("DELETE", f"/workflows({found['flow']})")
            done.append("flow")
        if found["security role"]:
            dv.call("DELETE", f"/roles({found['security role']})")
            done.append("security role")
        if found["environment variable"]:
            dv.call("DELETE", f"/environmentvariabledefinitions({found['environment variable']})")
            done.append("environment variable")
        for table in (TABLE_B, TABLE_A):
            if found["table " + table]:
                dv.call("DELETE", f"/EntityDefinitions(LogicalName='{table}')", timeout=900)
                done.append("table " + table)
        if found["global choice"]:
            dv.call("DELETE", f"/GlobalOptionSetDefinitions(Name='{CHOICE}')", timeout=600)
            done.append("global choice")
        if found["solution"]:
            dv.call("DELETE", f"/solutions({found['solution']})")
            done.append("solution")
    # Values left behind (a settings file can make one in Test), then the publisher.
    for row in dv.rows(f"/environmentvariablevalues?$select=environmentvariablevalueid,schemaname&$filter=startswith(schemaname,'{PREFIX}_')"):
        dv.call("DELETE", f"/environmentvariablevalues({row['environmentvariablevalueid']})")
        done.append("environment variable value " + row["schemaname"])
    for row in dv.rows(f"/publishers?$select=publisherid&$filter=uniquename eq '{PUBLISHER}'"):
        dv.call("DELETE", f"/publishers({row['publisherid']})")
        done.append("publisher")
    after = listing(dv)
    left = {kind: names for kind, names in after.items() if names}
    save(os.path.join(work("teardown"), f"teardown-{target}.json"), {"before": before, "done": done, "after": after})
    summary_write(f"### Teardown: {target}\n\nDeleted: {', '.join(done) or 'nothing'}.\n\nBefore:\n\n" + listing_table(before) +
                  "\n\nAfter:\n\n" + listing_table(after) + "\n")
    print("Deleted: " + (", ".join(done) or "nothing"))
    print("After: " + json.dumps(after))
    if left:
        raise ProbeError("teardown left: " + json.dumps(left))


def cmd_observe():
    """Read the scratch solution's state in Test, with its whole solution history. Read-only."""
    dv = test_dv()
    seen = observe(dv)
    history = solution_history(dv, None)
    want = expected(int(env("STATE")))
    wrong = [p for p, v in want.items() if seen["present"].get(p) != v]
    save(os.path.join(work("observe"), "observe.json"), {"seen": seen, "history": history, "expected": want, "wrong": wrong})
    lines = [f"### Test as it stands (compared with state {env('STATE')})", "", f"Solutions: {json.dumps(seen['solutions'])}.",
             f"Rows read after {seen.get('rows_read_after_seconds')} s; errors first: {seen.get('rows_read_errors')}.", "",
             "| Part | Expected | In Test |", "|---|---|---|"]
    lines += [f"| {p} | {mark(v)} | {mark(seen['present'].get(p))} |" for p, v in want.items()]
    lines += ["", f"Flows: {json.dumps(seen.get('flows'))}.", f"Values: {json.dumps(seen.get('environment variable values'))}.",
              f"Rows: {json.dumps(seen.get('rows'))}.", f"Not as expected: {wrong}.", "", "Solution history:", "", "```",
              json.dumps(history, indent=1)[:8000], "```"]
    summary_write("\n".join(lines) + "\n")
    print("\n".join(lines))


COMMANDS = {"check": cmd_check, "observe": cmd_observe, "lane": cmd_lane, "export": cmd_export, "pack": cmd_pack,
            "import": cmd_import, "teardown": cmd_teardown}


def main(argv):
    if len(argv) != 2 or argv[1] not in COMMANDS:
        print("usage: import_probe.py " + "|".join(COMMANDS), file=sys.stderr)
        return 2
    try:
        return COMMANDS[argv[1]]() or 0
    except ProbeError as error:
        print(f"::error::{error}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
