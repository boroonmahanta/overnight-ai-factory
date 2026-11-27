"""Spike 0.11 (plan 11.1, ADO 2447): the Key Vault read and the storage state check.

Probe-only, not a gate script. Prints no secret: never the certificate, the secret's
value, a token or a cookie value.

  vault   As the Test identity (the job's az sign-in), read the secret behind the test
          user's Key Vault certificate, print its metadata only, then try two reads the
          role (Key Vault Secrets User on that one secret) should not allow: listing the
          vault's secrets, and reading the certificate object itself.
  state   Read the storage state file the kit's sign-in wrote and print counts and
          domains only: proof that it exists and holds a session for factory-test.

Run with python3 -I (no user site, no script folder on the path).
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone

API = "7.5"  # Key Vault data plane


def fail(message: str) -> None:
    print(f"::error::{message}")
    sys.exit(1)


def vault_token() -> str:
    """A Key Vault token from the job's az sign-in. Never printed."""
    result = subprocess.run(
        ["az", "account", "get-access-token", "--resource", "https://vault.azure.net",
         "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        # az's error names the AADSTS code (AADSTS700024 if the OIDC assertion ran out).
        lines = [ln for ln in result.stderr.splitlines() if "AADSTS" in ln or "ERROR" in ln]
        fail("no Key Vault token from az: " + (" | ".join(lines)[:600] or f"exit {result.returncode}"))
    return result.stdout.strip()


def get(url: str, token: str) -> tuple[int, dict]:
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, json.loads(response.read() or b"{}")
    except urllib.error.HTTPError as error:
        body = error.read()
        try:
            return error.code, json.loads(body or b"{}")
        except json.JSONDecodeError:
            return error.code, {}


def error_codes(body: dict) -> str:
    err = body.get("error") or {}
    inner = err.get("innererror") or {}
    return f"{err.get('code', '?')}/{inner.get('code', '-')}"


def when(epoch: int | None) -> str:
    if epoch is None:
        return "none"
    return datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def vault() -> None:
    base = f"https://{os.environ['KEYVAULT']}.vault.azure.net"
    name = os.environ["TEST_USER_CERT"]
    token = vault_token()

    # 1. The secret behind the certificate: what playwright-ms-auth reads.
    status, body = get(f"{base}/secrets/{urllib.parse.quote(name)}?api-version={API}", token)
    if status != 200:
        fail(f"read secret {name}: HTTP {status} {error_codes(body)}")
    attrs = body.get("attributes") or {}
    value = body.pop("value", "") or ""
    content_type = body.get("contentType")
    try:
        pfx_bytes = len(base64.b64decode(value, validate=True))
    except (ValueError, TypeError):
        pfx_bytes = -1
    del value
    now = datetime.now(tz=timezone.utc).timestamp()
    print(f"read secret {name}: HTTP 200")
    print(f"  contentType {content_type}; enabled {attrs.get('enabled')}; "
          f"managed by a certificate {body.get('managed', False)}")
    print(f"  not before {when(attrs.get('nbf'))}; expires {when(attrs.get('exp'))}")
    print(f"  value: base64 of {pfx_bytes} bytes (not printed)")
    problems = []
    if content_type != "application/x-pkcs12":
        problems.append("content type is not application/x-pkcs12, so playwright-ms-auth would read it as a password")
    if not attrs.get("enabled"):
        problems.append("secret is disabled")
    if attrs.get("exp") and attrs["exp"] < now:
        problems.append("secret has expired")
    if attrs.get("nbf") and attrs["nbf"] > now:
        problems.append("secret is not valid yet")
    if pfx_bytes <= 0:
        problems.append("value is not base64")
    if problems:
        fail("; ".join(problems))

    # 2. Reads the role should not allow (it is on the one secret, not the vault).
    for label, url in (
        ("list the vault's secrets", f"{base}/secrets?api-version={API}&maxresults=1"),
        (f"read the certificate object {name}", f"{base}/certificates/{urllib.parse.quote(name)}?api-version={API}"),
    ):
        status, body = get(url, token)
        if status == 403:
            print(f"{label}: HTTP 403 {error_codes(body)} (refused, as expected)")
        else:
            print(f"::warning::{label}: HTTP {status}, expected 403; the role is wider than the one secret")
    del token


def state(path: str) -> None:
    if not os.path.isfile(path):
        fail(f"no storage state at {path}")
    size = os.path.getsize(path)
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    cookies = data.get("cookies") or []
    origins = data.get("origins") or []
    host = urllib.parse.urlsplit(os.environ["TEST_URL"]).hostname or ""
    domains = Counter((c.get("domain") or "?").lstrip(".") for c in cookies)
    print(f"storage state written: {size} bytes, {len(cookies)} cookies, {len(origins)} origins with storage")
    for domain, count in sorted(domains.items()):
        print(f"  {count} cookie(s) for {domain}")
    if not any(host == d or host.endswith("." + d) for d in domains):
        fail(f"no cookie for {host}: the state holds no factory-test session")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="mode", required=True)
    sub.add_parser("vault")
    state_parser = sub.add_parser("state")
    state_parser.add_argument("--file", required=True)
    args = parser.parse_args()
    if args.mode == "vault":
        vault()
    else:
        state(args.file)


if __name__ == "__main__":
    main()
