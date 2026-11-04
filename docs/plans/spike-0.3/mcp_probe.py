#!/usr/bin/env python3
"""Spike 0.3 (plan 11.1): Dataverse MCP with an app-only token.

Published as probe/mcp_probe.py in GetAI-IP/mcp-probe (private, scratch).
Run by .github/workflows/probe.yml, one subcommand per step:

  claims   print the GitHub OIDC token's claims (never the token)
  local    drive the Dataverse CLI's local MCP proxy (`dataverse mcp <url>`)
           over stdio, as the profile the workflow made
  remote   get an app-only token with the GitHub OIDC token as the client
           assertion, then drive https://<org>/api/mcp over streamable HTTP
  cleanup  delete, through the Web API, the probe rows this app user created
  summary  write the result table; exit 1 if a chosen path failed

Each path does one read (read_query) and, when WRITE is true, one create
(create_record) of a row named "spike-0.3 probe (<path>)", then reads it back.
Never prints a token. Standard library only, so it runs under python3 -I.
"""

import base64
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request

LOGIN_BASE = "https://login.microsoftonline.com"
PROTOCOL = "2025-06-18"
TABLE = "account"
ROW_PREFIX = "spike-0.3 probe"
READS = ("SELECT TOP 1 name FROM organization", "SELECT TOP 1 name FROM account")
GUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")

# Argument names are not documented; they are matched against the tool's own
# inputSchema from tools/list, exact names first, then substrings.
QUERY_ARGS = ("querytext", "query", "sql", "statement")
TABLE_ARGS = ("tablename", "table", "entityname", "entity", "logicalname")
ITEM_ARGS = ("item", "record", "data", "fields", "columns", "attributes", "values", "row")

OIDC_KEYS = ("iss", "aud", "sub", "job_workflow_ref", "job_workflow_sha", "workflow_ref",
             "event_name", "ref", "environment", "repository", "repository_id",
             "repository_owner", "repository_owner_id", "runner_environment", "issuer_scope")
ACCESS_KEYS = ("aud", "appid", "azp", "idtyp", "roles", "scp", "ver")


class ProbeError(Exception):
    pass


def env(name, default=""):
    return os.environ.get(name, default)


def resource():
    return env("ENV_URL").rstrip("/")


def write_on():
    return env("WRITE").lower() == "true"


def chosen_paths():
    paths = env("PATHS", "both")
    return ["local", "remote"] if paths == "both" else [paths]


def results_dir():
    path = os.path.join(env("RUNNER_TEMP", "/tmp"), "mcp-probe")
    os.makedirs(path, exist_ok=True)
    return path


def clip(text, limit=800):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit] + " ...[cut]"


def row_name(label):
    return f"{ROW_PREFIX} ({label})"


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


def print_access_claims(token):
    claims = claims_of(token)
    lines = [f"{key}: {claims.get(key)}" for key in ACCESS_KEYS]
    print("App-only token claims (not the token):\n  " + "\n  ".join(lines))
    summary_write("App-only token claims (not the token):\n\n```\n" + "\n".join(lines) + "\n```\n")


# ---------- HTTP ----------

def http(method, url, token, body=None, headers=None, timeout=120):
    data = None if body is None else json.dumps(body).encode()
    all_headers = {"Authorization": "Bearer " + token}
    if body is not None:
        all_headers["Content-Type"] = "application/json"
    all_headers.update(headers or {})
    request = urllib.request.Request(url, data=data, method=method, headers=all_headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, response.headers, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        return error.code, error.headers, error.read().decode("utf-8", "replace")


def http_problem(status, headers, text):
    parts = [f"HTTP {status}"]
    for name in ("WWW-Authenticate", "x-ms-service-request-id", "REQ_ID", "request-id"):
        if headers.get(name):
            parts.append(f"{name}: {clip(headers.get(name), 400)}")
    if text.strip():
        parts.append("body: " + clip(text, 600))
    return "; ".join(parts)


def parse_body(content_type, text):
    if "text/event-stream" in (content_type or ""):
        found = []
        for line in text.splitlines():
            if line.startswith("data:"):
                try:
                    found.append(json.loads(line[5:].strip()))
                except ValueError:
                    pass
        return found
    if not text.strip():
        return []
    value = json.loads(text)
    return value if isinstance(value, list) else [value]


# ---------- MCP clients ----------

class HttpMcp:
    """Streamable HTTP transport, as a plain client would use /api/mcp."""

    def __init__(self, url, token):
        self.url, self.token = url, token
        self.session, self.proto, self.next_id = None, None, 0

    def _post(self, message):
        headers = {"Accept": "application/json, text/event-stream"}
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        if self.proto:
            headers["MCP-Protocol-Version"] = self.proto
        status, response_headers, text = http("POST", self.url, self.token, message, headers)
        if response_headers.get("Mcp-Session-Id"):
            self.session = response_headers.get("Mcp-Session-Id")
        if status >= 400:
            raise ProbeError(http_problem(status, response_headers, text))
        return response_headers, text

    def notify(self, method):
        self._post({"jsonrpc": "2.0", "method": method})

    def request(self, method, params=None):
        self.next_id += 1
        headers, text = self._post({"jsonrpc": "2.0", "id": self.next_id, "method": method, "params": params or {}})
        for message in parse_body(headers.get("Content-Type"), text):
            if message.get("id") == self.next_id:
                return message
        raise ProbeError(f"no JSON-RPC reply to {method} ({len(text)} bytes back)")

    def close(self):
        pass


class StdioMcp:
    """Newline-delimited JSON-RPC over the proxy's stdin and stdout."""

    def __init__(self, argv, timeout=180):
        print("Starting:", " ".join(argv))
        self.proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     text=True, encoding="utf-8", bufsize=1)
        self.lines, self.timeout, self.next_id, self.proto = queue.Queue(), timeout, 0, None
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        for line in self.proc.stdout:
            self.lines.put(line)
        self.lines.put(None)

    def _send(self, message):
        try:
            self.proc.stdin.write(json.dumps(message) + "\n")
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError):
            raise ProbeError(f"proxy closed its input (exit code {self._exit_code()})") from None

    def _exit_code(self):
        try:
            return self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            return None

    def notify(self, method):
        self._send({"jsonrpc": "2.0", "method": method})

    def request(self, method, params=None):
        self.next_id += 1
        wanted = self.next_id
        self._send({"jsonrpc": "2.0", "id": wanted, "method": method, "params": params or {}})
        deadline = time.monotonic() + self.timeout
        while True:
            left = deadline - time.monotonic()
            if left <= 0:
                raise ProbeError(f"no reply to {method} within {self.timeout} s")
            try:
                line = self.lines.get(timeout=left)
            except queue.Empty:
                continue
            if line is None:
                raise ProbeError(f"proxy exited (code {self._exit_code()}) before replying to {method}")
            line = line.strip()
            if not line:
                continue
            try:
                message = json.loads(line)
            except ValueError:
                print("proxy stdout, not JSON:", clip(line, 300))
                continue
            if message.get("id") == wanted and ("result" in message or "error" in message):
                return message
            if "method" in message:
                print("proxy sent:", message["method"])
                if "id" in message:   # a request from the server; answer so it does not wait
                    if message["method"] == "ping":
                        self._send({"jsonrpc": "2.0", "id": message["id"], "result": {}})
                    else:
                        self._send({"jsonrpc": "2.0", "id": message["id"],
                                    "error": {"code": -32601, "message": "not supported by the probe"}})

    def close(self):
        try:
            self.proc.stdin.close()
        except OSError:
            pass
        try:
            self.proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()


# ---------- the exercise both paths run ----------

def result_of(message, what):
    if "error" in message:
        error = message["error"]
        raise ProbeError(f"{what}: JSON-RPC error {error.get('code')}: {clip(error.get('message'), 600)}"
                         + (f" data: {clip(json.dumps(error.get('data')), 400)}" if error.get("data") else ""))
    return message.get("result") or {}


def pick(schema, wanted):
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


def call_tool(rpc, name, arguments):
    print(f"tools/call {name} {clip(json.dumps(arguments), 300)}")
    result = result_of(rpc.request("tools/call", {"name": name, "arguments": arguments}), name)
    text = " ".join(part.get("text", "") for part in result.get("content") or [] if isinstance(part, dict))
    if result.get("structuredContent") is not None:
        text += " " + json.dumps(result["structuredContent"])
    if result.get("isError"):
        raise ProbeError(f"{name} returned isError: {clip(text, 800)}")
    print("  reply:", clip(text, 800))
    return text


def show_schema(tool):
    print(f"  {tool['name']} inputSchema: {clip(json.dumps(tool.get('inputSchema')), 900)}")


def exercise(rpc, label, result):
    init = result_of(rpc.request("initialize", {
        "protocolVersion": PROTOCOL, "capabilities": {},
        "clientInfo": {"name": "spike-0.3-probe", "version": "1"}}), "initialize")
    rpc.proto = init.get("protocolVersion")
    print(f"initialize: server {init.get('serverInfo')}, protocol {init.get('protocolVersion')}, "
          f"capabilities {sorted((init.get('capabilities') or {}).keys())}")
    rpc.notify("notifications/initialized")
    result["initialize"] = True

    tools = result_of(rpc.request("tools/list"), "tools/list").get("tools") or []
    by_name = {tool.get("name"): tool for tool in tools}
    print("tools:", ", ".join(sorted(name for name in by_name if name)))
    result["tools"] = len(by_name)

    reader = by_name.get("read_query")
    if not reader:
        raise ProbeError("tools/list has no read_query")
    show_schema(reader)
    query_arg, _ = pick(reader.get("inputSchema"), QUERY_ARGS)
    if not query_arg:
        raise ProbeError("cannot tell read_query's argument name; see its inputSchema above")
    last = None
    for sql in READS:
        try:
            call_tool(rpc, "read_query", {query_arg: sql})
            result["read"] = True
            break
        except ProbeError as error:
            last = error
            print("  read failed:", error)
    if not result["read"]:
        raise last

    if not write_on():
        print("WRITE is false: no create.")
        return
    creator = by_name.get("create_record")
    if not creator:
        raise ProbeError("tools/list has no create_record")
    show_schema(creator)
    table_arg, _ = pick(creator.get("inputSchema"), TABLE_ARGS)
    item_arg, item_schema = pick(creator.get("inputSchema"), ITEM_ARGS)
    if not table_arg or not item_arg:
        raise ProbeError("cannot tell create_record's argument names; see its inputSchema above")
    item = {"name": row_name(label)}
    value = json.dumps(item) if (item_schema or {}).get("type") == "string" else item
    result["create"] = False
    reply = call_tool(rpc, "create_record", {table_arg: TABLE, item_arg: value})
    found = GUID.search(reply)
    if not found:
        raise ProbeError("create_record replied without a GUID")
    result["create"], result["record_id"] = True, found.group(0)
    result["readback"] = False
    back = call_tool(rpc, "read_query", {query_arg: f"SELECT accountid, name FROM {TABLE} WHERE name = '{row_name(label)}'"})
    result["readback"] = row_name(label) in back


def run_path(label, make_client):
    result = {"path": label, "initialize": False, "read": False, "create": None,
              "readback": None, "record_id": None, "tools": None, "error": None}
    rpc = None
    try:
        rpc = make_client()
        exercise(rpc, label, result)
    except ProbeError as error:
        result["error"] = str(error)
        print(f"::error::{label} path: {clip(error, 900)}")
    except Exception as error:   # keep going to the summary; show the trace for the record
        traceback.print_exc()
        result["error"] = f"{type(error).__name__}: {error}"
        print(f"::error::{label} path: {clip(result['error'], 900)}")
    finally:
        if rpc:
            rpc.close()
    with open(os.path.join(results_dir(), label + ".json"), "w", encoding="utf-8") as handle:
        json.dump(result, handle)
    print(json.dumps(result, indent=1))
    return 0 if result_ok(result) else 1


def result_ok(result):
    return bool(result.get("read")) and (not write_on() or bool(result.get("create")))


# ---------- subcommands ----------

def cmd_claims():
    claims = claims_of(github_oidc_token())
    lines = [f"{key}: {claims.get(key)}" for key in OIDC_KEYS]
    print("\n".join(lines))
    summary_write("### OIDC claims (not the token)\n\n```\n" + "\n".join(lines) + "\n```\n")
    return 0


def cmd_local():
    return run_path("local", lambda: StdioMcp([env("DATAVERSE_BIN", "dataverse"), "mcp", resource()]))


def cmd_remote():
    def client():
        token = app_token()
        print_access_claims(token)
        return HttpMcp(resource() + "/api/mcp", token)
    return run_path("remote", client)


def cmd_cleanup():
    """Delete probe rows this app user created. Nothing else."""
    token = app_token()
    api = resource() + "/api/data/v9.2"
    odata = {"Accept": "application/json", "OData-MaxVersion": "4.0", "OData-Version": "4.0"}
    status, headers, text = http("GET", api + "/WhoAmI", token, headers=odata)
    if status != 200:
        raise ProbeError("WhoAmI: " + http_problem(status, headers, text))
    me = json.loads(text)["UserId"]
    query = urllib.parse.urlencode({
        "$select": "accountid,name,createdon",
        "$filter": f"startswith(name,'{ROW_PREFIX}') and _createdby_value eq {me}",
    }, quote_via=urllib.parse.quote)

    def probe_rows():
        status, headers, text = http("GET", f"{api}/accounts?{query}", token, headers=odata)
        if status != 200:
            raise ProbeError("query probe rows: " + http_problem(status, headers, text))
        return json.loads(text).get("value", [])

    rows = probe_rows()
    print(f"Probe rows created by this app user: {len(rows)}")
    for row in rows:
        status, headers, text = http("DELETE", f"{api}/accounts({row['accountid']})", token, headers=odata)
        print(f"  delete '{row['name']}' {row['accountid']} (created {row.get('createdon')}): HTTP {status}")
        if status != 204:
            print("  " + http_problem(status, headers, text))
    left = probe_rows()
    print(f"Probe rows left: {len(left)}")
    outcome = {"found": len(rows), "left": len(left)}
    with open(os.path.join(results_dir(), "cleanup.json"), "w", encoding="utf-8") as handle:
        json.dump(outcome, handle)
    return 0 if not left else 1


def mark(value):
    return {True: "pass", False: "FAIL", None: "-"}.get(value, str(value))


def cmd_summary():
    lines = ["### Spike 0.3 result", "",
             f"WRITE: {write_on()}", "",
             "| Path | initialize | tools | read | create | read back | error |",
             "|---|---|---|---|---|---|---|"]
    failed = False
    for label in chosen_paths():
        path = os.path.join(results_dir(), label + ".json")
        if not os.path.exists(path):
            lines.append(f"| {label} | - | - | - | - | - | did not run |")
            failed = True
            continue
        with open(path, encoding="utf-8") as handle:
            result = json.load(handle)
        failed |= not result_ok(result)
        error = clip(result.get("error") or "", 300).replace("|", "/")
        lines.append(f"| {label} | {mark(result.get('initialize'))} | {result.get('tools') or '-'} | "
                     f"{mark(result.get('read'))} | {mark(result.get('create'))} | "
                     f"{mark(result.get('readback'))} | {error} |")
    cleanup = os.path.join(results_dir(), "cleanup.json")
    if os.path.exists(cleanup):
        with open(cleanup, encoding="utf-8") as handle:
            outcome = json.load(handle)
        lines += ["", f"Clean-up: {outcome['found']} probe row(s) found, {outcome['left']} left."]
        failed |= outcome["left"] != 0
    elif write_on():
        lines += ["", "Clean-up: did not report. Check for rows named 'spike-0.3 probe'."]
        failed = True
    text = "\n".join(lines)
    print(text)
    summary_write(text)
    return 1 if failed else 0


COMMANDS = {"claims": cmd_claims, "local": cmd_local, "remote": cmd_remote,
            "cleanup": cmd_cleanup, "summary": cmd_summary}


def main(argv):
    if len(argv) != 1 or argv[0] not in COMMANDS:
        print("usage: mcp_probe.py " + "|".join(COMMANDS), file=sys.stderr)
        return 2
    try:
        return COMMANDS[argv[0]]()
    except ProbeError as error:
        print(f"::error::{argv[0]}: {clip(error, 900)}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
