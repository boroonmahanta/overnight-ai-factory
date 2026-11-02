#!/usr/bin/env python3
"""Hash manifest for the trusted gate scripts (scripts.sha256).

Jobs that hold credentials run only scripts from this repo, after checking them
against the manifest (lcp-gate.yml header rules). Format matches `sha256sum`:
"<hex>  <relative path>". Paths are relative to the gate root, with forward slashes.

  manifest.py make   <root> > scripts.sha256
  manifest.py verify <root> scripts.sha256

verify fails on a changed file, a missing file, or a file under <root>/gate that is
not listed (an unlisted script is an unreviewed script).
"""
import hashlib
import sys
from pathlib import Path

SCAN_DIR = "gate"
SKIP_SUFFIXES = {".pyc"}
SKIP_PARTS = {"__pycache__"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scripts(root: Path) -> list[str]:
    base = root / SCAN_DIR
    found = []
    for path in sorted(base.rglob("*")):
        if not path.is_file() or path.suffix in SKIP_SUFFIXES or SKIP_PARTS & set(path.parts):
            continue
        found.append(path.relative_to(root).as_posix())
    return found


def make(root: Path) -> str:
    return "".join(f"{sha256(root / rel)}  {rel}\n" for rel in scripts(root))


def parse(text: str) -> dict[str, str]:
    entries = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        digest, sep, rel = line.partition("  ")
        if not sep or len(digest) != 64:
            raise ValueError(f"Bad manifest line: {line!r}")
        entries[rel] = digest
    return entries


def verify(root: Path, manifest_text: str) -> list[str]:
    """Return a list of problems. Empty means the scripts match the manifest."""
    listed = parse(manifest_text)
    present = set(scripts(root))
    problems = []
    for rel, digest in sorted(listed.items()):
        path = root / rel
        if not path.is_file():
            problems.append(f"missing: {rel}")
        elif sha256(path) != digest:
            problems.append(f"changed: {rel}")
    for rel in sorted(present - set(listed)):
        problems.append(f"unlisted: {rel}")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) == 3 and argv[1] == "make":
        sys.stdout.write(make(Path(argv[2])))
        return 0
    if len(argv) == 4 and argv[1] == "verify":
        problems = verify(Path(argv[2]), Path(argv[3]).read_text(encoding="utf-8"))
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1 if problems else 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
