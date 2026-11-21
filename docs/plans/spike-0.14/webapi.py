#!/usr/bin/env python3
"""A trusted helper for the Dataverse Web API, for the agent in spike 0.14 part 4b (option (b)).

Published as probe/webapi.py in GetAI-IP/export-probe (private, scratch). A stand-in for plan 5.6's
"trusted helper scripts for the Web API": it sits in the driver's folder, not the agent's, and the
agent runs it as a command. It

  - signs every call as the lane identity, with a token it gets from the Azure CLI's cache
    (`az account get-access-token`); the token is never printed, logged or handed back;
  - sends every write with the header MSCRM.SolutionUniqueName set to the lane's solution
    ($SOLUTION), which the agent cannot change;
  - takes GET, POST and PATCH only. DELETE and PUT are refused: an additive story deletes nothing,
    and a metadata update by PUT replaces a whole definition. So are $batch, and the solution
    actions that are the driver's job or remove things (import, export, remove a component, delete);
  - sends PATCH with If-Match: *, so a PATCH to a row that does not exist fails rather than makes one;
  - logs each call (method, path, status, seconds, error text) to $WEBAPI_LOG for the driver.

usage: webapi.py METHOD PATH [--body JSON | --body @FILE] [--out FILE]

  PATH is relative to /api/data/v9.2. Write it WITHOUT a leading slash: Copilot CLI reads an argument
  that starts with / as a file path outside the session's folders, and a night run denies it
  (run 40126131). For example
    "systemforms?$select=formid,name,formxml&$filter=objecttypecode eq 'account' and type eq 2"
    "systemforms(<formid>)"      with PATCH and a body of the columns to change, e.g. {"formxml": "..."}
    "savedqueries(<id>)"         with PATCH and {"layoutxml": "...", "fetchxml": "..."}
    "PublishXml"                 with POST and {"ParameterXml": "<importexportxml>...</importexportxml>"}
  --out FILE writes the response body to FILE instead of printing it.

Exit 0 on HTTP 2xx, 1 on any other status, 2 on a refused or malformed request.
Not a gate script. Standard library only (python3 -I).
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "/api/data/v9.2"
JWT = re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]*")
METHODS = ("GET", "POST", "PATCH")
# The first path segment of a POST that this helper never sends: the driver's jobs, and anything that removes.
REFUSED_ACTIONS = re.compile(r"^/(\$batch|ImportSolution\w*|ExportSolution\w*|StageSolution|StageAndUpgrade\w*|"
                             r"DeleteAndPromote\w*|UninstallSolution\w*|RemoveSolutionComponent|CloneAs\w*|"
                             r"Delete\w*)(\b|$)", re.I)


def redact(text):
    return JWT.sub("[token removed]", text or "")


def log(entry):
    path = os.environ.get("WEBAPI_LOG")
    if not path:
        return
    entry["at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def refuse(method, path, why):
    log({"method": method, "path": path[:300], "refused": why})
    print(f"refused: {why}", file=sys.stderr)
    return 2


def token(resource):
    """A Dataverse token from the Azure CLI's cache. Never shown."""
    process = subprocess.run(["az", "account", "get-access-token", "--resource", resource, "--query", "accessToken",
                              "--output", "tsv"], stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=120)
    if process.returncode != 0 or not process.stdout.strip():
        raise RuntimeError("the Azure CLI gave no token: " + redact(process.stderr)[-300:])
    return process.stdout.strip()


def parse(argv):
    if len(argv) < 2 or argv[0] in ("-h", "--help"):
        return None
    method, path, body, out = argv[0].upper(), argv[1], None, None
    rest = argv[2:]
    while rest:
        flag = rest.pop(0)
        if flag == "--body" and rest:
            body = rest.pop(0)
        elif flag == "--out" and rest:
            out = rest.pop(0)
        else:
            raise ValueError(f"unknown or incomplete option: {flag}")
    return method, path, body, out


def main(argv):
    try:
        parsed = parse(argv)
    except ValueError as error:
        print(f"{error}\n{__doc__.split('usage:', 1)[1].split('Not a gate', 1)[0]}", file=sys.stderr)
        return 2
    if parsed is None:
        print(__doc__)
        return 0
    method, path, body, out = parsed
    if path and not path.startswith("/") and "://" not in path:
        path = "/" + path   # the documented form has no leading slash (see usage)
    if method not in METHODS:
        return refuse(method, path, f"{method} is not allowed: this route makes additive changes only "
                                    "(GET, POST, PATCH). A change that needs a delete or a PUT stops for a person.")
    if not path.startswith("/") or "://" in path or "\n" in path or ".." in path:
        return refuse(method, path, "PATH must be relative to /api/data/v9.2, e.g. systemforms(<id>)")
    if method != "GET" and REFUSED_ACTIONS.search(path):
        return refuse(method, path, "this action is not allowed here: exports, imports and removals are not the "
                                    "agent's job")
    data = None
    if body is not None:
        try:
            if body.startswith("@"):
                with open(body[1:], encoding="utf-8") as handle:
                    body = handle.read()
            data = json.dumps(json.loads(body)).encode()
        except (OSError, ValueError) as error:
            print(f"the body is not readable JSON: {error}", file=sys.stderr)
            return 2
    resource = os.environ.get("ENV_URL", "").rstrip("/")
    solution = os.environ.get("SOLUTION", "")
    if not resource or not solution:
        print("ENV_URL and SOLUTION must be set (the driver sets them)", file=sys.stderr)
        return 2
    headers = {"Accept": "application/json", "OData-MaxVersion": "4.0", "OData-Version": "4.0",
               "Prefer": 'odata.include-annotations="*"'}
    if data is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
    if method != "GET":
        headers["MSCRM.SolutionUniqueName"] = solution
    if method == "PATCH":
        headers["If-Match"] = "*"
    started = time.time()
    try:
        headers["Authorization"] = "Bearer " + token(resource)
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as error:
        log({"method": method, "path": path[:300], "status": None, "error": str(error)[:300]})
        print(error, file=sys.stderr)
        return 1
    url = resource + API + urllib.parse.quote(path, safe="/:?&=$(),'@*!-._~%+;")
    request = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            status, response_headers, text = response.status, response.headers, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        status, response_headers, text = error.code, error.headers, error.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError) as error:
        log({"method": method, "path": path[:300], "status": None, "error": str(error)[:300]})
        print(f"no answer: {error}", file=sys.stderr)
        return 1
    seconds = round(time.time() - started, 1)
    text = redact(text)
    entry = {"method": method, "path": path[:300], "status": status, "seconds": seconds,
             "body_bytes": len(data or b""), "solution_header": method != "GET"}
    if status >= 400:
        try:
            entry["error"] = (json.loads(text).get("error") or {}).get("message", "")[:500]
        except ValueError:
            entry["error"] = text[:500]
    entity_id = response_headers.get("OData-EntityId") if response_headers else None
    if entity_id:
        entry["entity_id"] = entity_id.rsplit("/", 1)[-1][:200]
    log(entry)
    print(f"HTTP {status}" + (f"  OData-EntityId: {entity_id}" if entity_id else ""), file=sys.stderr)
    if out:
        with open(out, "w", encoding="utf-8") as handle:
            handle.write(text)
        print(f"body written to {out} ({len(text)} characters)", file=sys.stderr)
    elif text.strip():
        try:
            print(json.dumps(json.loads(text), indent=2))
        except ValueError:
            print(text)
    return 0 if 200 <= status < 300 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
