#!/usr/bin/env python3
"""Spike 0.19 (plan 11.1): reset fidelity, as the lane identity.

Published as probe/reset_probe.py in GetAI-IP/export-probe (private, scratch),
run by .github/workflows/reset.yml. One subcommand per step:

  baseline  export and unpack the lane's solution, and list what the leftover
            finder sees. Read-only. The reset commit is made from this tree by hand
  plant     leave a night's mess: a flow and a column inside the solution, a flow
            outside it, and a change to the main flow's definition. Then export
            and show the mess against the reset commit
  reset     the probe-only stand-in for reset_environment.py (plan 5.4, steps 2
            to 5): import the reset commit with overwrite and publish, apply the
            lane's environment variable values, remove leftovers, prove the reset.
            It knows nothing of what plant made: it finds leftovers by query
  check     after a reset, look up what plant made, by name
  unplant   delete what plant made, by name. A safety net only; not part of the test
  summary   write the result table; exit 1 if the step failed

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
import xml.etree.ElementTree as ElementTree

LOGIN_BASE = "https://login.microsoftonline.com"
API = "/api/data/v9.2"


class ProbeError(Exception):
    pass


def env(name, default=""):
    return os.environ.get(name, default)


SOLUTION = env("SOLUTION", "FactorySpike")
RESET_COMMIT = env("RESET_COMMIT", "reset-commit/FactorySpike")
LANE_FILE = env("LANE_FILE", "lane/fl1.json")

# Fixed solution component types. Connection reference has an org-specific type
# code, read from its table's ObjectTypeCode.
TYPE_ENTITY, TYPE_ATTRIBUTE, TYPE_ROLE, TYPE_WORKFLOW = 1, 2, 20, 29
TYPE_ENVVAR, TYPE_ENVVALUE = 380, 381

# Brake: a real night leaves a few leftovers. More than this means the finder is
# wrong, so the reset deletes nothing and the lane goes Offline.
MAX_DELETES = 10


def resource():
    return env("ENV_URL").rstrip("/")


def work_dir():
    path = os.path.join(env("RUNNER_TEMP", "/tmp"), "reset-probe", env("MODE", "local"))
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


# ---------- tokens (never printed) ----------

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
        self.writes = []

    def call(self, method, path, body=None, headers=None, ok=(200, 201, 204), timeout=300):
        url = path if path.startswith("http") else self.base + path
        # OData filters hold spaces and quotes; encode what HTTP refuses, keep what OData needs.
        url = urllib.parse.quote(url, safe="/:?&=$(),'@*!-._~%+;")
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
        if method != "GET":
            self.writes.append(f"{method} {path.split('?')[0]} -> {status}")
        if status not in ok:
            raise ProbeError(f"{method} {path.split('?')[0]}: HTTP {status}: {clip(text, 600)}")
        return status, response_headers, (json.loads(text) if text.strip() else {})

    def get(self, path, ok=(200,)):
        return self.call("GET", path, ok=ok)[2]

    def rows(self, path):
        """Every row, following @odata.nextLink."""
        found = []
        status, _, body = self.call("GET", path, headers={"Prefer": "odata.maxpagesize=5000"})
        found += body.get("value", [])
        while body.get("@odata.nextLink"):
            status, _, body = self.call("GET", body["@odata.nextLink"], headers={"Prefer": "odata.maxpagesize=5000"})
            found += body.get("value", [])
        return found

    def meta(self, path):
        """Metadata collections (EntityDefinitions and their parts) do not page."""
        return self.get(path).get("value", [])

    def create(self, entity_set, body, solution=None):
        headers = {"MSCRM.SolutionUniqueName": solution} if solution else {}
        _, response_headers, _ = self.call("POST", "/" + entity_set, body, headers)
        entity_id = response_headers.get("OData-EntityId", "")
        match = re.search(r"\(([0-9a-fA-F-]{36})\)\s*$", entity_id)
        return match.group(1) if match else entity_id


def quote(value):
    return value.replace("'", "''")


# ---------- trees ----------

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


def xml_root(path):
    with open(path, "rb") as handle:
        return ElementTree.fromstring(handle.read().decode("utf-8-sig"))


def read_commit(root):
    """What the reset commit holds, read from the unpacked XML tree itself.

    Other/Solution.xml's RootComponents is not enough: in spike 0.18's export it
    listed the table, the role and the flow, but not the environment variable or
    the connection reference, which live in their own folder and in
    Other/Customizations.xml.
    """
    if not os.path.isfile(os.path.join(root, "Other", "Solution.xml")):
        raise ProbeError(f"{root} is not an unpacked XML solution tree")
    held = {"tables": {}, "workflows": set(), "roles": set(), "envvars": set(), "envvar_values": set(),
            "connrefs": set(), "root_components": []}
    manifest = xml_root(os.path.join(root, "Other", "Solution.xml"))
    held["unique_name"] = manifest.findtext("SolutionManifest/UniqueName")
    for item in manifest.iter("RootComponent"):
        held["root_components"].append(dict(item.attrib))
        if item.get("type") == str(TYPE_WORKFLOW) and item.get("id"):
            held["workflows"].add(bare(item.get("id")))
        if item.get("type") == str(TYPE_ROLE) and item.get("id"):
            held["roles"].add(bare(item.get("id")))
    entities = os.path.join(root, "Entities")
    for folder in sorted(os.listdir(entities)) if os.path.isdir(entities) else []:
        path = os.path.join(entities, folder, "Entity.xml")
        if not os.path.isfile(path):
            continue
        entity = xml_root(path)
        node = entity.find("EntityInfo/entity")
        schema = node.get("Name") if node is not None else folder
        attributes = {(a.findtext("LogicalName") or "").lower() for a in entity.iter("attribute")}
        held["tables"][schema.lower()] = {"schema": schema, "attributes": sorted(a for a in attributes if a)}
    for name in sorted(os.listdir(os.path.join(root, "Workflows"))) if os.path.isdir(os.path.join(root, "Workflows")) else []:
        if name.endswith(".data.xml"):
            workflow = xml_root(os.path.join(root, "Workflows", name))
            held["workflows"].add(bare(workflow.get("WorkflowId")))
    for name in sorted(os.listdir(os.path.join(root, "Roles"))) if os.path.isdir(os.path.join(root, "Roles")) else []:
        if name.endswith(".xml"):
            held["roles"].add(bare(xml_root(os.path.join(root, "Roles", name)).get("id")))
    variables = os.path.join(root, "environmentvariabledefinitions")
    for folder in sorted(os.listdir(variables)) if os.path.isdir(variables) else []:
        path = os.path.join(variables, folder, "environmentvariabledefinition.xml")
        if os.path.isfile(path):
            held["envvars"].add((xml_root(path).get("schemaname") or folder).lower())
            if os.path.isfile(os.path.join(variables, folder, "environmentvariablevalues.json")):
                held["envvar_values"].add(folder.lower())
    customizations = os.path.join(root, "Other", "Customizations.xml")
    if os.path.isfile(customizations):
        for item in xml_root(customizations).iter("connectionreference"):
            held["connrefs"].add((item.get("connectionreferencelogicalname") or "").lower())
    return held


def jsonable(held):
    return {key: (sorted(value) if isinstance(value, set) else value) for key, value in held.items()}


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


def export_unpack(label):
    """Export the lane's solution (unmanaged) and unpack it. Returns the tree's folder."""
    w = work_dir()
    zip_path = os.path.join(w, f"{label}.zip")
    folder = os.path.join(w, label)
    run(f"export ({label})", ["pac", "solution", "export", "--name", SOLUTION, "--path", zip_path, "--overwrite"],
        allow_fail=False)
    run(f"unpack ({label})", ["pac", "solution", "unpack", "--zipfile", zip_path, "--folder", folder,
                              "--packagetype", "Unmanaged"], allow_fail=False)
    return folder


def timed(name, function, *args):
    started = time.time()
    result = function(*args)
    STEPS.append({"name": name, "command": "(Web API)", "exit": 0, "seconds": round(time.time() - started, 1), "tail": ""})
    return result


# ---------- the leftover finder ----------
#
# How to find what the lane identity made outside the solution (run 37428706 and
# reads under Boroon's sign-in, 10 November 2026): the Default Solution's
# solutioncomponent rows are written by SYSTEM, whoever made the component, so
# their createdby cannot say. The maker is on the component's own row instead
# (workflows, roles, connection references and the rest), so the finder asks each
# component table for rows the lane identity created. Tables, columns and other
# metadata keep no maker at all, so for those the finder compares what is in the
# lane with the lane solution and the lane manifest's bootstrap list.

# Classic component types whose rows live in a table that has createdby. The
# newer types, connection references and environment variables among them, are
# read from solutioncomponentdefinitions, which also gives the org-specific codes.
CLASSIC_RECORD_TYPES = {
    20: "role", 26: "savedquery", 29: "workflow", 36: "template", 59: "savedqueryvisualization",
    60: "systemform", 61: "webresource", 62: "sitemap", 63: "connectionrole", 66: "customcontrol",
    70: "fieldsecurityprofile", 80: "appmodule", 90: "plugintype", 91: "pluginassembly",
    92: "sdkmessageprocessingstep", 95: "serviceendpoint", 150: "routingrule", 152: "sla",
    161: "mobileofflineprofile", 300: "canvasapp", 371: "connector",
}

# The types the stand-in reset can delete. Anything else it finds sends the lane Offline.
DELETABLE = {TYPE_WORKFLOW, TYPE_ROLE, TYPE_ENVVAR, TYPE_ENVVALUE}


def solution_ids(dv):
    rows = dv.rows("/solutions?$select=solutionid,uniquename,ismanaged")
    return {row["uniquename"]: row["solutionid"].lower() for row in rows}, \
           {row["solutionid"].lower(): row["uniquename"] for row in rows}


def component_rows(dv, condition):
    return dv.rows("/solutioncomponents?$select=solutioncomponentid,componenttype,objectid,rootsolutioncomponentid,"
                   "rootcomponentbehavior,ismetadata,createdon,_createdby_value,_solutionid_value&$filter=" + condition)


def all_metadata(dv):
    """Every table with its columns: one call, about 7 MB and 6 seconds for 874 tables."""
    return dv.meta("/EntityDefinitions?$select=LogicalName,EntitySetName,PrimaryIdAttribute,IsManaged,IsCustomEntity"
                   "&$expand=Attributes($select=LogicalName,MetadataId,IsCustomAttribute,IsManaged,AttributeOf)")


def table_parts(dv, metadata_id):
    """Every subcomponent of a table that an export with behaviour 0 carries, by ID."""
    entity = dv.get(f"/EntityDefinitions({metadata_id})?$select=LogicalName,SchemaName,IsManaged"
                    "&$expand=Attributes($select=MetadataId),OneToManyRelationships($select=MetadataId),"
                    "ManyToOneRelationships($select=MetadataId),ManyToManyRelationships($select=MetadataId),"
                    "Keys($select=MetadataId)")
    logical = entity["LogicalName"]
    ids = {bare(metadata_id)}
    for key in ("Attributes", "OneToManyRelationships", "ManyToOneRelationships", "ManyToManyRelationships", "Keys"):
        ids |= {bare(item["MetadataId"]) for item in entity.get(key, [])}
    for cast in ("PicklistAttributeMetadata", "StateAttributeMetadata", "StatusAttributeMetadata",
                 "BooleanAttributeMetadata", "MultiSelectPicklistAttributeMetadata"):
        for item in dv.meta(f"/EntityDefinitions({metadata_id})/Attributes/Microsoft.Dynamics.CRM.{cast}"
                            "?$select=MetadataId&$expand=OptionSet($select=MetadataId)"):
            if item.get("OptionSet"):
                ids.add(bare(item["OptionSet"]["MetadataId"]))
    ids |= {bare(r["formid"]) for r in dv.rows(f"/systemforms?$select=formid&$filter=objecttypecode eq '{logical}'")}
    ids |= {bare(r["savedqueryid"]) for r in dv.rows(f"/savedqueries?$select=savedqueryid&$filter=returnedtypecode eq '{logical}'")}
    ids |= {bare(r["savedqueryvisualizationid"]) for r in dv.rows(
        f"/savedqueryvisualizations?$select=savedqueryvisualizationid&$filter=primaryentitytypecode eq '{logical}'")}
    ids |= {bare(r["privilegeid"]) for r in dv.rows(f"/privileges?$select=privilegeid&$filter=endswith(name,'{logical}')")}
    return logical, ids


def made_by_lane(dv, me, entity_sets):
    """Every component row the lane identity created, asked table by table."""
    types = dict(CLASSIC_RECORD_TYPES)
    for row in dv.rows("/solutioncomponentdefinitions?$select=solutioncomponenttype,primaryentityname"):
        types.setdefault(row["solutioncomponenttype"], row["primaryentityname"])
    found, unreadable = {}, []
    for component_type, logical in sorted(types.items()):
        table = entity_sets.get(logical)
        if not (table and table.get("set") and table.get("pk")):
            unreadable.append({"type": component_type, "table": logical, "why": "no entity set"})
            continue
        try:
            rows = dv.rows(f"/{table['set']}?$select={table['pk']}&$filter=_createdby_value eq {me}")
        except ProbeError as error:
            unreadable.append({"type": component_type, "table": logical, "why": clip(error, 160)})
            continue
        for row in rows:
            found[bare(row[table["pk"]])] = {"type": component_type, "table": logical}
    return found, unreadable, len(types)


def describe(dv, component_type, object_id, connref_type):
    """Name a component and say who made it and whether it is managed, for the types the reset handles."""
    oid = bare(object_id)
    try:
        if component_type == TYPE_ENTITY:
            row = dv.get(f"/EntityDefinitions({oid})?$select=LogicalName,IsManaged,IsCustomEntity")
            return {"name": row["LogicalName"], "managed": row["IsManaged"], "custom": row["IsCustomEntity"]}
        if component_type == TYPE_WORKFLOW:
            row = dv.get(f"/workflows({oid})?$select=name,category,statecode,ismanaged,_createdby_value")
            return {"name": row["name"], "managed": row["ismanaged"], "created_by": row["_createdby_value"],
                    "state": row["statecode"], "category": row["category"]}
        if component_type == TYPE_ROLE:
            row = dv.get(f"/roles({oid})?$select=name,ismanaged,_createdby_value")
            return {"name": row["name"], "managed": row["ismanaged"], "created_by": row["_createdby_value"]}
        if component_type == TYPE_ENVVAR:
            row = dv.get(f"/environmentvariabledefinitions({oid})?$select=schemaname,ismanaged,_createdby_value")
            return {"name": row["schemaname"], "managed": row["ismanaged"], "created_by": row["_createdby_value"]}
        if component_type == TYPE_ENVVALUE:
            row = dv.get(f"/environmentvariablevalues({oid})?$select=schemaname,ismanaged,_createdby_value,"
                         "_environmentvariabledefinitionid_value")
            definition = dv.get(f"/environmentvariabledefinitions({row['_environmentvariabledefinitionid_value']})?$select=schemaname")
            return {"name": row["schemaname"], "managed": row["ismanaged"], "created_by": row["_createdby_value"],
                    "definition": definition["schemaname"]}
        if component_type == connref_type:
            row = dv.get(f"/connectionreferences({oid})?$select=connectionreferencelogicalname,ismanaged,_createdby_value")
            return {"name": row["connectionreferencelogicalname"], "managed": row["ismanaged"],
                    "created_by": row["_createdby_value"]}
    except ProbeError as error:
        return {"name": None, "error": clip(error, 300)}
    return {"name": None}


def inventory(dv, held, lane):
    """What the reset must remove, found by query alone.

    In the solution: every root component the reset commit does not hold, and
    every unmanaged custom column of a held table that the commit's Entity.xml
    does not hold. Outside it: every component row the lane identity created that
    the solution does not cover (less the environment variable values the lane
    manifest sets), and every unmanaged custom table or column that neither the
    solution nor the manifest's bootstrap list holds.
    """
    me = dv.get("/WhoAmI")["UserId"].lower()
    connref_type = dv.get("/EntityDefinitions(LogicalName='connectionreference')?$select=ObjectTypeCode")["ObjectTypeCode"]
    by_name, _ = solution_ids(dv)
    lane_id = by_name.get(SOLUTION)
    if not lane_id:
        raise ProbeError(f"solution {SOLUTION} not found")
    tables_meta = all_metadata(dv)
    entity_sets = {t["LogicalName"]: {"set": t.get("EntitySetName"), "pk": t.get("PrimaryIdAttribute")} for t in tables_meta}
    made, unreadable, record_types = made_by_lane(dv, me, entity_sets)

    # What the lane's solution covers: its rows, and every part of a table it holds whole.
    lane_rows = component_rows(dv, f"_solutionid_value eq {lane_id}")
    covered = {bare(r["objectid"]) for r in lane_rows}
    tables = {}
    for row in lane_rows:
        if row["componenttype"] == TYPE_ENTITY and row.get("rootcomponentbehavior") in (0, None):
            logical, ids = table_parts(dv, row["objectid"])
            covered |= ids
            tables[logical] = ids

    root_types = (TYPE_ENTITY, TYPE_ROLE, TYPE_WORKFLOW, TYPE_ENVVAR, TYPE_ENVVALUE, connref_type)
    in_solution, unknown = [], []
    for row in lane_rows:
        component_type, oid = row["componenttype"], bare(row["objectid"])
        if row.get("rootsolutioncomponentid") or (component_type not in root_types
                                                  and any(oid in ids for ids in tables.values())):
            continue  # a part of a held table: judged by the column check below
        info = describe(dv, component_type, oid, connref_type)
        name = (info.get("name") or "").lower()
        if component_type == TYPE_ENTITY:
            is_held = name in held["tables"]
        elif component_type == TYPE_WORKFLOW:
            is_held = oid in held["workflows"]
        elif component_type == TYPE_ROLE:
            is_held = oid in held["roles"]
        elif component_type == TYPE_ENVVAR:
            is_held = name in held["envvars"]
        elif component_type == TYPE_ENVVALUE:
            is_held = (info.get("definition") or "").lower() in held["envvar_values"]
        elif component_type == connref_type:
            is_held = name in held["connrefs"]
        else:
            unknown.append({"where": "in the solution", "type": component_type, "objectid": oid, **info})
            continue
        if not is_held:
            in_solution.append({"type": component_type, "objectid": oid, "made_by_lane": oid in made, **info})

    # Columns on held tables that the commit's Entity.xml does not hold.
    columns = []
    by_table = {t["LogicalName"]: t for t in tables_meta}
    for logical in tables:
        if logical not in held["tables"] or logical not in by_table:
            continue
        want = set(held["tables"][logical]["attributes"])
        for attribute in by_table[logical].get("Attributes", []):
            if attribute.get("AttributeOf") or not attribute.get("IsCustomAttribute"):
                continue
            if attribute["LogicalName"].lower() not in want:
                columns.append({"table": logical, "column": attribute["LogicalName"], "managed": attribute["IsManaged"],
                                "objectid": bare(attribute["MetadataId"])})

    # Outside, rows with a maker: what the lane identity made that the solution does not cover.
    allowed_values = {name.lower() for name in lane.get("environment_variables", {})}
    # Rows that extend a covered table (such as the recycle bin row Dataverse makes with
    # each new table, run 37558056) are parts of that table.
    extension_tables = {t["LogicalName"] for t in tables_meta
                        if any(a["LogicalName"] == "extensionofrecordid" for a in t.get("Attributes", []))}
    strays, allowed = [], []
    for oid, where in sorted(made.items()):
        if oid in covered:
            continue
        if where["table"] in extension_tables:
            row = dv.get(f"/{entity_sets[where['table']]['set']}({oid})?$select=_extensionofrecordid_value")
            if bare(row.get("_extensionofrecordid_value")) in covered:
                continue
        info = describe(dv, where["type"], oid, connref_type)
        item = {"type": where["type"], "table": where["table"], "objectid": oid, **info}
        if where["type"] == TYPE_ENVVALUE and (info.get("definition") or "").lower() in allowed_values:
            allowed.append(item)
        elif (where["type"] in DELETABLE or where["type"] == connref_type) and info.get("name") is not None:
            strays.append(item)
        else:
            unknown.append({"where": "outside the solution, made by the lane identity", **item})

    # Outside, metadata (no maker kept): unmanaged custom tables and columns the solution
    # and the manifest's bootstrap list do not hold.
    allowed_meta = lane.get("outside_allowed", {})
    allowed_tables = {t.lower() for t in allowed_meta.get("tables", [])}
    allowed_columns = {c.lower() for c in allowed_meta.get("columns", [])}
    outside_metadata = []
    for table in tables_meta:
        logical = table["LogicalName"]
        if logical in tables:
            continue  # held whole by the lane's solution: its columns are judged above
        if table.get("IsCustomEntity") and not table.get("IsManaged") and logical not in allowed_tables:
            outside_metadata.append({"table": logical, "why": "unmanaged custom table outside the solution"})
            continue
        for attribute in table.get("Attributes", []):
            name = f"{logical}.{attribute['LogicalName']}".lower()
            if attribute.get("IsCustomAttribute") and not attribute.get("IsManaged") and not attribute.get("AttributeOf") \
                    and name not in allowed_columns:
                outside_metadata.append({"column": name, "why": "unmanaged custom column outside the solution"})

    return {"lane_user": me, "connref_type": connref_type, "lane_solution_rows": len(lane_rows),
            "lane_solution_types": sorted({r["componenttype"] for r in lane_rows}), "covered": len(covered),
            "record_types_asked": record_types, "record_tables_unreadable": unreadable,
            "rows_made_by_lane": len(made), "tables_read": len(tables_meta),
            "in_solution_leftovers": in_solution, "leftover_columns": columns, "outside_leftovers": strays,
            "outside_metadata": outside_metadata, "allowed_outside": allowed, "unknown": unknown,
            "clean": not (in_solution or columns or strays or outside_metadata or unknown)}


def inventory_markdown(title, found):
    lines = [f"### {title}", "",
             f"Lane user `{found['lane_user']}`. Rows in `{SOLUTION}`: {found['lane_solution_rows']} "
             f"(types {found['lane_solution_types']}); IDs it covers: {found['covered']}.", "",
             f"Component types asked for rows the lane identity made: {found['record_types_asked']}, "
             f"of which unreadable: {len(found['record_tables_unreadable'])}. Rows it made: {found['rows_made_by_lane']}. "
             f"Tables read: {found['tables_read']}.", ""]
    for key, label in (("in_solution_leftovers", "In the solution, not in the commit"),
                       ("leftover_columns", "Columns on held tables, not in the commit"),
                       ("outside_leftovers", "Outside the solution, made by the lane identity"),
                       ("outside_metadata", "Outside the solution, custom tables and columns not on the bootstrap list"),
                       ("allowed_outside", "Outside, allowed by the lane manifest"),
                       ("unknown", "Cannot judge (the lane would go Offline)")):
        items = found[key]
        lines.append(f"- {label}: {len(items)}")
        for item in items[:20]:
            lines.append(f"  - `{json.dumps(item, default=str, sort_keys=True)[:300]}`")
    lines.append("")
    lines.append(f"**Clean: {found['clean']}**")
    return "\n".join(lines)


# ---------- the reset (stand-in for reset_environment.py; knows nothing of plant) ----------

def apply_values(dv, lane, lane_solution):
    """Step 3: the lane's environment variable values, kept out of the solution."""
    done = []
    for schema, value in sorted(lane.get("environment_variables", {}).items()):
        definitions = dv.rows(f"/environmentvariabledefinitions?$select=environmentvariabledefinitionid"
                              f"&$filter=schemaname eq '{quote(schema)}'")
        if len(definitions) != 1:
            raise ProbeError(f"environment variable {schema}: {len(definitions)} definitions")
        definition_id = definitions[0]["environmentvariabledefinitionid"]
        values = dv.rows("/environmentvariablevalues?$select=environmentvariablevalueid,value"
                         f"&$filter=_environmentvariabledefinitionid_value eq {definition_id}")
        if len(values) > 1:
            raise ProbeError(f"environment variable {schema}: {len(values)} values")
        if values:
            value_id = values[0]["environmentvariablevalueid"]
            if values[0].get("value") != value:
                dv.call("PATCH", f"/environmentvariablevalues({value_id})", {"value": value}, {"If-Match": "*"})
                action = "updated"
            else:
                action = "already set"
        else:
            value_id = dv.create("environmentvariablevalues", {
                "schemaname": schema, "value": value,
                "EnvironmentVariableDefinitionId@odata.bind": f"/environmentvariabledefinitions({definition_id})"})
            action = "created"
        in_solution = component_rows(dv, f"_solutionid_value eq {lane_solution} and objectid eq {value_id}")
        if in_solution:
            dv.call("POST", "/RemoveSolutionComponent", {
                "SolutionComponent": {"@odata.type": "Microsoft.Dynamics.CRM.solutioncomponent",
                                      "solutioncomponentid": value_id},
                "ComponentType": TYPE_ENVVALUE, "SolutionUniqueName": SOLUTION})
            action += "; it had joined the solution, removed from it"
        done.append({"schema": schema, "value_id": bare(value_id), "action": action})
    return done


def delete_component(dv, component_type, oid, info, connref_type):
    if component_type == TYPE_WORKFLOW:
        if info.get("state") == 1:
            dv.call("PATCH", f"/workflows({oid})", {"statecode": 0, "statuscode": 1}, {"If-Match": "*"})
        dv.call("DELETE", f"/workflows({oid})")
    elif component_type == TYPE_ENVVAR:
        for row in dv.rows(f"/environmentvariablevalues?$select=environmentvariablevalueid"
                           f"&$filter=_environmentvariabledefinitionid_value eq {oid}"):
            dv.call("DELETE", f"/environmentvariablevalues({row['environmentvariablevalueid']})")
        dv.call("DELETE", f"/environmentvariabledefinitions({oid})")
    elif component_type == TYPE_ENVVALUE:
        dv.call("DELETE", f"/environmentvariablevalues({oid})")
    elif component_type == connref_type:
        dv.call("DELETE", f"/connectionreferences({oid})")
    elif component_type == TYPE_ROLE:
        dv.call("DELETE", f"/roles({oid})")
    elif component_type == TYPE_ENTITY:
        dv.call("DELETE", f"/EntityDefinitions({oid})")
    else:
        raise ProbeError(f"no delete for component type {component_type}")


def remove_leftovers(dv, found):
    """Step 4. Plan first; act only if every item can be judged and the plan is small.

    In the lane's solution the reset commit is the truth: what it does not hold is
    deleted if the lane identity made it (rows with a maker), or if it is an
    unmanaged custom table or column (metadata keeps no maker). Outside the
    solution only rows the lane identity made are deleted. Anything else is
    refused, and one refusal stops every delete: the lane goes Offline and a
    human cleans it.
    """
    me = found["lane_user"]
    plan = []
    for item in found["in_solution_leftovers"]:
        if item.get("managed"):
            plan.append(("refuse", item, "managed"))
        elif item["type"] == TYPE_ENTITY:
            plan.append(("delete", item, "") if item.get("custom")
                        else ("refuse", item, "not a custom table: take it out of the solution by hand"))
        elif item.get("made_by_lane") and bare(item.get("created_by")) == me:
            plan.append(("delete", item, ""))
        else:
            plan.append(("refuse", item, "not made by the lane identity: take it out of the solution by hand"))
    for item in found["leftover_columns"]:
        plan.append(("refuse", item, "managed") if item.get("managed") else ("delete column", item, ""))
    for item in found["outside_leftovers"]:
        plan.append(("refuse", item, "managed") if item.get("managed") else ("delete", item, ""))
    for item in found["outside_metadata"]:
        plan.append(("refuse", item, "metadata keeps no maker: a human decides"))
    refused = [p for p in plan if p[0] == "refuse"]
    if found["unknown"] or refused or len(plan) > MAX_DELETES:
        return {"acted": False, "plan": [(a, i, why) for a, i, why in plan], "unknown": found["unknown"],
                "why": "unknown or refused items, or too many: the lane goes Offline and a human cleans it"}
    done = []
    # Flows first, then columns, then the rest: a flow may use a column or a connection reference.
    order = sorted(plan, key=lambda p: (0 if p[1].get("type") == TYPE_WORKFLOW else 1 if p[0] == "delete column" else 2))
    for action, item, _ in order:
        if action == "delete column":
            dv.call("DELETE", f"/EntityDefinitions(LogicalName='{item['table']}')/Attributes(LogicalName='{item['column'].lower()}')")
        else:
            delete_component(dv, item["type"], item["objectid"], item, found["connref_type"])
        done.append({"action": action, **{k: item.get(k) for k in ("type", "name", "table", "column", "objectid")}})
    if done:
        dv.call("POST", "/PublishAllXml", {})
    return {"acted": True, "done": done}


def cmd_reset():
    """Plan 5.4, steps 2 to 5. Step 1 (transactional test data) is not in this spike."""
    results = {"mode": "reset", "run_id": env("GITHUB_RUN_ID"), "steps": STEPS}
    w = work_dir()
    with open(LANE_FILE, encoding="utf-8") as handle:
        lane = json.load(handle)
    held = read_commit(RESET_COMMIT)
    results["reset_commit"] = {"path": RESET_COMMIT, "sha": env("GITHUB_SHA"), "holds": jsonable(held)}
    if held["unique_name"] != SOLUTION:
        raise ProbeError(f"the reset commit is {held['unique_name']}, not {SOLUTION}")
    try:
        dv = Dataverse()
        by_name, _ = solution_ids(dv)
        results["before"] = timed("inventory before", inventory, dv, held, lane)

        # Step 2: import the solution built from the reset commit, with overwrite and publish.
        zip_path = os.path.join(w, "reset-commit.zip")
        run("pack the reset commit", ["pac", "solution", "pack", "--zipfile", zip_path, "--folder", RESET_COMMIT,
                                      "--packagetype", "Unmanaged"], allow_fail=False)
        run("import with overwrite and publish", ["pac", "solution", "import", "--path", zip_path,
                                                  "--force-overwrite", "--publish-changes"], allow_fail=False)

        # Step 3: the lane's environment variable values.
        results["values"] = timed("apply the lane's values", apply_values, dv, lane, by_name[SOLUTION])

        # Step 4: remove leftovers, found again after the import.
        found = timed("inventory after import", inventory, dv, held, lane)
        results["after_import"] = found
        results["removal"] = timed("remove leftovers", remove_leftovers, dv, found)

        # Step 5: prove it. A fresh export, unpacked, must equal the reset commit exactly.
        proof_tree = export_unpack("proof")
        results["proof_compare"] = compare(RESET_COMMIT, proof_tree, "reset-commit", "proof-export")
        results["after"] = timed("inventory after", inventory, dv, held, lane)
        results["values_after"] = [
            {"schema": schema, "want": value,
             "have": [r.get("value") for r in dv.rows(
                 "/environmentvariablevalues?$select=value&$filter=schemaname eq '" + quote(schema) + "'")]}
            for schema, value in sorted(lane.get("environment_variables", {}).items())]
        results["writes"] = dv.writes
    finally:
        save("results.json", results)
    proof = results["proof_compare"]
    results["pass"] = bool(proof.get("equal_raw") and results["after"]["clean"] and results["removal"].get("acted")
                           and all(v["have"] == [v["want"]] for v in results["values_after"]))
    save("results.json", results)
    summary_write(inventory_markdown("Before the reset", results["before"]))
    summary_write(inventory_markdown("After the import, before removal", results["after_import"]))
    summary_write("### Removal\n\n```\n" + json.dumps(results["removal"], indent=1, default=str)[:4000] + "\n```\n")
    summary_write(inventory_markdown("After the reset", results["after"]))
    print(json.dumps({"pass": results["pass"], "proof": {k: proof.get(k) for k in (
        "equal_raw", "equal_canonical", "only_in_first", "only_in_second", "raw_differ")}}, indent=2))


# ---------- the probe's own modes (these know what plant made) ----------

PLANT_FLOW_IN = "Factory spike leftover flow"
PLANT_FLOW_OUT = "Factory spike stray flow"
PLANT_COLUMN = "fspk_Leftover"
MAIN_FLOW = "Factory spike flow"
TABLE = "fspk_spikeitem"
PLANT_NOTE = "Spike 0.19 scratch: a planted leftover. The reset should remove it."


def flow_clientdata(top, with_connref=True):
    connector = "/providers/Microsoft.PowerApps/apis/shared_commondataserviceforapps"
    if with_connref:
        references = {"shared_commondataserviceforapps": {
            "runtimeSource": "embedded", "connection": {"connectionReferenceLogicalName": "fspk_spikedataverse"},
            "api": {"name": "shared_commondataserviceforapps"}}}
        actions = {"List_rows": {"runAfter": {}, "metadata": {}, "type": "OpenApiConnection", "inputs": {
            "host": {"apiId": connector, "connectionName": "shared_commondataserviceforapps", "operationId": "ListRecords"},
            "parameters": {"entityName": "fspk_spikeitems", "$top": top},
            "authentication": "@parameters('$authentication')"}}}
    else:
        references = {}
        actions = {"Compose": {"runAfter": {}, "metadata": {}, "type": "Compose", "inputs": "stray"}}
    return json.dumps({"properties": {"connectionReferences": references, "definition": {
        "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {"$connections": {"defaultValue": {}, "type": "Object"},
                       "$authentication": {"defaultValue": {}, "type": "SecureObject"}},
        "triggers": {"manual": {"metadata": {}, "type": "Request", "kind": "Button",
                                "inputs": {"schema": {"type": "object", "properties": {}, "required": []}}}},
        "actions": actions}}, "schemaVersion": "1.0.0.0"})


def find_flow(dv, name):
    rows = dv.rows(f"/workflows?$select=workflowid,clientdata&$filter=name eq '{quote(name)}' and category eq 5")
    return rows[0] if rows else None


def find_column(dv):
    status, _, body = dv.call("GET", f"/EntityDefinitions(LogicalName='{TABLE}')/Attributes(LogicalName='{PLANT_COLUMN.lower()}')"
                                     "?$select=MetadataId", ok=(200, 404))
    return body.get("MetadataId") if status == 200 else None


def main_flow_top(dv):
    flow = find_flow(dv, MAIN_FLOW)
    if not flow:
        raise ProbeError("the main flow is missing")
    data = json.loads(flow["clientdata"])
    return flow, data, data["properties"]["definition"]["actions"]["List_rows"]["inputs"]["parameters"]["$top"]


def cmd_plant():
    results = {"mode": "plant", "run_id": env("GITHUB_RUN_ID"), "steps": STEPS}
    held = read_commit(RESET_COMMIT)
    with open(LANE_FILE, encoding="utf-8") as handle:
        lane = json.load(handle)
    dv = Dataverse()
    language = dv.rows("/organizations?$select=languagecode")[0]["languagecode"]
    made = []
    if not find_flow(dv, PLANT_FLOW_IN):
        dv.create("workflows", {"category": 5, "type": 1, "primaryentity": "none", "name": PLANT_FLOW_IN,
                                "description": PLANT_NOTE, "clientdata": flow_clientdata(1)}, solution=SOLUTION)
        made.append("leftover flow, in the solution")
    if not find_column(dv):
        label = lambda text: {"@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [
            {"@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": text, "LanguageCode": language}]}
        dv.call("POST", f"/EntityDefinitions(LogicalName='{TABLE}')/Attributes", {
            "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
            "AttributeType": "String", "AttributeTypeName": {"Value": "StringType"},
            "SchemaName": PLANT_COLUMN, "MaxLength": 100, "FormatName": {"Value": "Text"},
            "RequiredLevel": {"Value": "None", "CanBeChanged": True,
                              "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings"},
            "DisplayName": label("Leftover"), "Description": label(PLANT_NOTE)}, {"MSCRM.SolutionUniqueName": SOLUTION})
        made.append("leftover column, in the solution")
    if not find_flow(dv, PLANT_FLOW_OUT):
        dv.create("workflows", {"category": 5, "type": 1, "primaryentity": "none", "name": PLANT_FLOW_OUT,
                                "description": PLANT_NOTE, "clientdata": flow_clientdata(1, with_connref=False)})
        made.append("stray flow, outside the solution")
    flow, data, top = main_flow_top(dv)
    if top != 7:
        data["properties"]["definition"]["actions"]["List_rows"]["inputs"]["parameters"]["$top"] = 7
        dv.call("PATCH", f"/workflows({flow['workflowid']})", {"clientdata": json.dumps(data)}, {"If-Match": "*"})
        made.append("main flow changed: $top 1 to 7")
    dv.call("POST", "/PublishAllXml", {})
    results["made"] = made
    # Where each planted part landed.
    by_name, by_id = solution_ids(dv)
    where = {}
    for label_text, oid in (("leftover flow", (find_flow(dv, PLANT_FLOW_IN) or {}).get("workflowid")),
                            ("stray flow", (find_flow(dv, PLANT_FLOW_OUT) or {}).get("workflowid")),
                            ("leftover column", find_column(dv))):
        rows = component_rows(dv, f"objectid eq {oid}") if oid else []
        where[label_text] = sorted(f"{by_id.get(r['_solutionid_value'].lower(), r['_solutionid_value'])}"
                                   f" (type {r['componenttype']}, root {r['rootsolutioncomponentid'] or '-'})" for r in rows)
    results["planted_in"] = where
    tree_after = export_unpack("dirty")
    results["dirty_compare"] = compare(RESET_COMMIT, tree_after, "reset-commit", "dirty-export")
    results["inventory"] = inventory(dv, held, lane)
    results["writes"] = dv.writes
    save("results.json", results)
    summary_write("### Planted\n\n" + "\n".join(f"- {m}" for m in made) + "\n\nWhere they landed:\n\n" +
                  "\n".join(f"- {k}: {', '.join(v) or 'nowhere'}" for k, v in where.items()) + "\n")
    summary_write(inventory_markdown("What the finder sees after planting", results["inventory"]))


def cmd_baseline():
    results = {"mode": "baseline", "run_id": env("GITHUB_RUN_ID"), "steps": STEPS}
    with open(LANE_FILE, encoding="utf-8") as handle:
        lane = json.load(handle)
    folder = export_unpack("baseline")
    commit = RESET_COMMIT if os.path.isdir(RESET_COMMIT) else folder
    results["commit_used"] = commit
    held = read_commit(commit)
    results["holds"] = jsonable(held)
    if commit != folder:
        results["baseline_vs_commit"] = compare(commit, folder, "reset-commit", "baseline-export")
    dv = Dataverse()
    results["inventory"] = inventory(dv, held, lane)
    save("results.json", results)
    summary_write(inventory_markdown("What the finder sees now", results["inventory"]))


def cmd_check():
    dv = Dataverse()
    _, _, top = main_flow_top(dv)
    found = {"leftover flow present": bool(find_flow(dv, PLANT_FLOW_IN)),
             "stray flow present": bool(find_flow(dv, PLANT_FLOW_OUT)),
             "leftover column present": bool(find_column(dv)),
             "main flow $top": top}
    found["all undone"] = not (found["leftover flow present"] or found["stray flow present"]
                               or found["leftover column present"]) and top == 1
    print(json.dumps(found, indent=2))
    summary_write("### Planted parts after the reset (looked up by name)\n\n```\n" + json.dumps(found, indent=2) + "\n```\n")
    return 0 if found["all undone"] else 1


def cmd_unplant():
    dv = Dataverse()
    done = []
    for name in (PLANT_FLOW_IN, PLANT_FLOW_OUT):
        flow = find_flow(dv, name)
        if flow:
            dv.call("DELETE", f"/workflows({flow['workflowid']})")
            done.append(name)
    if find_column(dv):
        dv.call("DELETE", f"/EntityDefinitions(LogicalName='{TABLE}')/Attributes(LogicalName='{PLANT_COLUMN.lower()}')")
        done.append(PLANT_COLUMN)
    flow, data, top = main_flow_top(dv)
    if top != 1:
        data["properties"]["definition"]["actions"]["List_rows"]["inputs"]["parameters"]["$top"] = 1
        dv.call("PATCH", f"/workflows({flow['workflowid']})", {"clientdata": json.dumps(data)}, {"If-Match": "*"})
        done.append("main flow $top back to 1")
    dv.call("POST", "/PublishAllXml", {})
    print("Undone: " + (", ".join(done) or "nothing"))
    summary_write("### Unplant\n\nUndone: " + (", ".join(done) or "nothing") + "\n")


def cmd_summary():
    path = os.path.join(work_dir(), "results.json")
    if not os.path.isfile(path):
        summary_write(f"### {env('MODE')}\n\nNo results.json: the step did not finish.\n")
        return 1
    with open(path, encoding="utf-8") as handle:
        results = json.load(handle)
    lines = [f"### {results['mode']}: steps", "", "| Step | Exit | Seconds |", "|---|---|---|"]
    lines += [f"| {s['name']} | {s['exit']} | {s['seconds']} |" for s in results["steps"]]
    for key in ("baseline_vs_commit", "dirty_compare", "proof_compare"):
        if key in results:
            c = results[key]
            lines += ["", f"**{key}**: equal raw {c.get('equal_raw')}, equal canonical {c.get('equal_canonical')}; "
                      f"only in the commit {c.get('only_in_first')}; only in the export {c.get('only_in_second')}; "
                      f"files that differ {c.get('raw_differ')}", ""]
            for name, sample in list(c.get("samples", {}).items())[:6]:
                lines += [f"`{name}`:", "```diff", *sample, "```"]
    if results["mode"] == "reset":
        lines += ["", f"Values after: `{results.get('values_after')}`", "", f"## Reset result: **{'pass' if results.get('pass') else 'FAIL'}**"]
    summary_write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if results["mode"] != "reset" or results.get("pass") else 1


COMMANDS = {"baseline": cmd_baseline, "plant": cmd_plant, "reset": cmd_reset, "check": cmd_check,
            "unplant": cmd_unplant, "summary": cmd_summary}


def main(argv):
    if len(argv) != 2 or argv[1] not in COMMANDS:
        print("usage: reset_probe.py " + "|".join(COMMANDS), file=sys.stderr)
        return 2
    try:
        return COMMANDS[argv[1]]() or 0
    except ProbeError as error:
        print(f"::error::{error}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
