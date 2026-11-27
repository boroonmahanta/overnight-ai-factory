"""Make the "Northwind Orders User" role in the NorthwindTraders solution, in the lane.

Session 61, 27 November 2026, at Boroon's word ("Role in the solution", then "Yes,
make it"). Day work in factory-lane-1, as Boroon (his az sign-in), by the Web API with
the solution header: live build, plan 5.6. The driver's export of the solution is then
the pull request's source in AI-Business-Solutions/ai-factory-nwt. Finding 19 in this
folder's README says why the role is needed.

  make   create the role in the root business unit, inside NorthwindTraders; add its
         privileges; share the Northwind Orders app with it; publish the app
  show   read the role back: its solution, its privileges by table, the app's roles

The role: on nwind_orders, Create, Write, Delete and Append at user level, Read and
Append To at organisation level; on the other 11 Northwind tables, Read and Append To at
organisation level; no Assign or Share anywhere. Prints no token.

  python3 -I northwind_role.py make --env https://factory-lane-1.crm6.dynamics.com
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request

SOLUTION = "NorthwindTraders"
ROLE = "Northwind Orders User"
DESCRIPTION = ("Users of the Northwind Orders app: read every Northwind table, and create, "
               "edit and delete their own orders.")
APP = "nwind_NorthwindOrdersModeldriven"
ORDERS = "nwind_orders"
TABLES = [
    "nwind_categories", "nwind_customers", "nwind_employees", "nwind_inventorytransactions",
    "nwind_invoices", "nwind_orderdetails", "nwind_orders", "nwind_products",
    "nwind_purchaseorderdetails", "nwind_purchaseorders", "nwind_shippers", "nwind_suppliers",
]
# privilege -> depth, per table
ORDER_RIGHTS = {"Create": "Basic", "Read": "Global", "Write": "Basic", "Delete": "Basic",
                "Append": "Basic", "AppendTo": "Global"}
OTHER_RIGHTS = {"Read": "Global", "AppendTo": "Global"}
# Dataverse gives every new role these, at organisation level, before any are added
# (seen 27 November 2026: the role held them right after the create). Kept, not removed.
PLATFORM_DEFAULTS = {
    "prvreadsdkmessage", "prvreadsdkmessageprocessingstep", "prvreadsdkmessageprocessingstepimage",
    "prvreadplugintype", "prvreadpluginassembly", "prvreadsharepointdocument",
    "prvreadsharepointdata", "prvwritesharepointdata", "prvcreatesharepointdata",
}


class Api:
    def __init__(self, env: str):
        self.env = env.rstrip("/")
        out = subprocess.run(["az", "account", "get-access-token", "--resource", self.env,
                              "--query", "accessToken", "-o", "tsv"],
                             capture_output=True, text=True, check=True)
        self.token = out.stdout.strip()

    def call(self, method: str, path: str, body=None, headers=None):
        url = f"{self.env}/api/data/v9.2/{path}".replace(" ", "%20").replace("'", "%27")
        h = {"Authorization": f"Bearer {self.token}", "Accept": "application/json",
             "OData-MaxVersion": "4.0", "OData-Version": "4.0"}
        data = None
        if body is not None:
            h["Content-Type"] = "application/json"
            data = json.dumps(body).encode()
        h.update(headers or {})
        req = urllib.request.Request(url, data=data, headers=h, method=method)
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                raw = r.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            sys.exit(f"{method} {path.split('?')[0]}: HTTP {e.code} {e.read()[:500]!r}")

    def get(self, path: str):
        return self.call("GET", path)


def root_bu(api: Api) -> str:
    bus = [b for b in api.get("businessunits?$select=businessunitid,name,_parentbusinessunitid_value")["value"]
           if not b.get("_parentbusinessunitid_value")]
    if len(bus) != 1:
        sys.exit(f"expected one root business unit, found {len(bus)}")
    return bus[0]["businessunitid"]


def find_role(api: Api, bu: str):
    roles = api.get(f"roles?$select=roleid,name&$filter=name eq '{ROLE}' and _businessunitid_value eq {bu}")["value"]
    return roles[0]["roleid"] if roles else None


def app_id(api: Api) -> str:
    apps = api.get(f"appmodules?$select=appmoduleid,uniquename&$filter=uniquename eq '{APP}'")["value"]
    if len(apps) != 1:
        sys.exit(f"expected the app {APP}, found {len(apps)}")
    return apps[0]["appmoduleid"]


def wanted() -> dict[str, str]:
    want = {}
    for table in TABLES:
        for right, depth in (ORDER_RIGHTS if table == ORDERS else OTHER_RIGHTS).items():
            want[f"prv{right}{table}"] = depth
    return want


def make(api: Api) -> None:
    bu = root_bu(api)
    if find_role(api, bu):
        sys.exit(f"the role {ROLE!r} already exists in the root business unit: run show")
    want = wanted()
    privs = {p["name"].lower(): p for p in api.get("privileges?$select=name,privilegeid&$filter=contains(name,'nwind_')")["value"]}
    missing = [n for n in want if n.lower() not in privs]
    if missing:
        sys.exit(f"privileges not found: {missing}")

    role = api.call("POST", "roles?$select=roleid,name",
                    {"name": ROLE, "description": DESCRIPTION, "businessunitid@odata.bind": f"/businessunits({bu})"},
                    {"MSCRM.SolutionUniqueName": SOLUTION, "Prefer": "return=representation"})
    rid = role["roleid"]
    print(f"made the role {ROLE!r} in {SOLUTION}")

    api.call("POST", f"roles({rid})/Microsoft.Dynamics.CRM.AddPrivilegesRole", {"Privileges": [
        {"PrivilegeId": privs[n.lower()]["privilegeid"], "PrivilegeName": privs[n.lower()]["name"],
         "Depth": depth, "BusinessUnitId": bu}
        for n, depth in want.items()]})
    print(f"added {len(want)} privileges")

    aid = app_id(api)
    api.call("POST", f"appmodules({aid})/appmoduleroles_association/$ref",
             {"@odata.id": f"{api.env}/api/data/v9.2/roles({rid})"})
    print(f"shared the app {APP} with the role")

    api.call("POST", "PublishXml",
             {"ParameterXml": f"<importexportxml><appmodules><appmodule>{aid}</appmodule></appmodules></importexportxml>"})
    print("published the app")


DEPTH_NAMES = {"Basic": "user", "Local": "business unit", "Deep": "parent: child business units", "Global": "organisation"}


def show(api: Api) -> int:
    bu = root_bu(api)
    rid = find_role(api, bu)
    if not rid:
        print(f"no role {ROLE!r} in the root business unit")
        return 1
    sol = api.get(f"solutions?$select=solutionid&$filter=uniquename eq '{SOLUTION}'")["value"][0]["solutionid"]
    in_sol = api.get(f"solutioncomponents?$select=componenttype&$filter=_solutionid_value eq {sol} and objectid eq {rid}")["value"]
    print(f"role {ROLE!r}: in {SOLUTION}: {bool(in_sol)} (component type {[c['componenttype'] for c in in_sol]})")

    held = api.get(f"RetrieveRolePrivilegesRole(RoleId={rid})")["RolePrivileges"]
    names = {p["privilegeid"]: p["name"] for p in api.get("privileges?$select=name,privilegeid&$filter=contains(name,'nwind_')")["value"]}
    got = {}
    others = set()
    for p in held:
        name = names.get(p["PrivilegeId"])
        if name is None:
            others.add(api.get(f"privileges({p['PrivilegeId']})?$select=name")["name"].lower())
            continue
        got[name.lower()] = p["Depth"]
    want = {k.lower(): v for k, v in wanted().items()}
    for table in TABLES:
        rights = sorted((n[3:-len(table)], d) for n, d in got.items() if n.endswith(table))
        print(f"  {table}: " + ", ".join(f"{r} {DEPTH_NAMES.get(d, d)}" for r, d in rights))
    print(f"  {len(got)} Northwind privileges; {len(others)} others, "
          f"{'all' if others <= PLATFORM_DEFAULTS else 'NOT all'} the platform's defaults for a new role")
    ok = got == want and others <= PLATFORM_DEFAULTS
    if not ok:
        print(f"  DIFFERS from the design: missing {sorted(set(want) - set(got))}, extra {sorted(set(got) - set(want))}, "
              f"depths {[(n, got[n], want[n]) for n in want if n in got and got[n] != want[n]]}")

    roles = [r["name"] for r in api.get(f"appmodules({app_id(api)})/appmoduleroles_association?$select=name")["value"]]
    print(f"app {APP} shared with: {roles}")
    ok = ok and ROLE in roles and bool(in_sol)
    print("matches the design" if ok else "does NOT match the design")
    return 0 if ok else 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("mode", choices=["make", "show"])
    parser.add_argument("--env", required=True, help="the lane's URL, https://factory-lane-1.crm6.dynamics.com")
    args = parser.parse_args()
    if "factory-lane-1." not in args.env:
        sys.exit("this script changes factory-lane-1 only")
    api = Api(args.env)
    if args.mode == "make":
        make(api)
        sys.exit(show(api))
    sys.exit(show(api))


if __name__ == "__main__":
    main()
