#!/usr/bin/env python3
"""Hash manifest for the trusted files in the gate repo (scripts.sha256).

Jobs that hold credentials run only scripts from this repo, after checking them
against the manifest (lcp-gate.yml header rules). Format matches `sha256sum`:
"<hex>  <relative path>". Paths are relative to the gate repo root, with forward
slashes. The workflow checks the gate repo out at `gate/` and runs
`sha256sum --check --strict scripts.sha256` there, so a script listed as
`lcp/x.py` is called as `gate/lcp/x.py`.

What is hashed (decided by Boroon, 3 November 2026): every file in the repo that
a gate job reads, not only scripts. That covers prompts, rubrics, agent
definitions under .github/agents/, danger-rules.yml, trust.yml and project
settings, because rule 17 puts them next to gate scripts and they shape the
verdict and the Merge Danger floor as much as code does. Nothing added later has
to be remembered: a new folder is hashed unless it is listed below as not hashed.

Not hashed, because no gate job reads them: tests/, README.md, the test-only
files, this manifest itself, and .github/ apart from .github/agents/ (the
workflow is the root of trust, pinned by the required-workflow ruleset, and
Dependabot edits its pins by PR).

  manifest.py make   <root> > scripts.sha256
  manifest.py verify <root> scripts.sha256

verify fails on a changed file, a missing file, or a trusted file that is not
listed (an unlisted file is an unreviewed file). sha256sum does not catch an
unlisted file, so the committed-manifest test is what catches it before release.
"""
import hashlib
import sys
from pathlib import Path

MANIFEST = "scripts.sha256"
# ".git" is a file, not a folder, in a git worktree or submodule.
NOT_HASHED_FILES = {MANIFEST, "README.md", "pending-scripts.txt", "requirements-test.txt", ".gitignore", ".git"}
NOT_HASHED_DIRS = ("tests/", ".git/")
GITHUB_DIR = ".github/"
GITHUB_HASHED = ".github/agents/"
SKIP_SUFFIXES = {".pyc"}
SKIP_PARTS = {"__pycache__"}


def is_hashed(rel: str) -> bool:
    """rel is a forward-slash path relative to the gate repo root."""
    if rel.startswith(GITHUB_DIR):
        return rel.startswith(GITHUB_HASHED)
    if rel.startswith(NOT_HASHED_DIRS) or rel in NOT_HASHED_FILES:
        return False
    if SKIP_PARTS & set(rel.split("/")) or Path(rel).suffix in SKIP_SUFFIXES:
        return False
    return True


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def trusted_files(root: Path) -> list[str]:
    found = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if is_hashed(rel):
            found.append(rel)
    return found


def make(root: Path) -> str:
    return "".join(f"{sha256(root / rel)}  {rel}\n" for rel in trusted_files(root))


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
    """Return a list of problems. Empty means the trusted files match the manifest."""
    listed = parse(manifest_text)
    present = set(trusted_files(root))
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
