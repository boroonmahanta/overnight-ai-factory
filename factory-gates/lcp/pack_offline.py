#!/usr/bin/env python3
"""Pack the solution and the Copilot Studio workspaces offline, with clear errors.

Wraps the two pac calls in the gate's `build` job (Appendix A). Both are local
and need no sign-in, so the job keeps no credentials (rule 5). The flags are the
plan's, unchanged.

[untested] pac is not installed here. The fake pac in tests/test_pack_offline.py
stands in for it. Whether these flags are right for pac 2.4.1 and the YAML source
format, and what `pac copilot pack` writes and where, wait for a stage 0 spike.

  pack_offline.py solution --source <src folder> --out <folder>
      Runs, in this order:
        pac solution pack --zipfile <out>/solution_unmanaged.zip --folder <src> --packagetype Unmanaged
        pac solution pack --zipfile <out>/solution_managed.zip --folder <src> --packagetype Managed
      Any old zip is deleted first, so a stale one cannot pass for new. Fails if
      pac exits non-zero, or exits 0 without writing a valid zip. A zero exit is
      not proof every component was packed: pack can drop one silently (plan 5.6),
      which is what the static job's manifest check is for.

  pack_offline.py agents --root <agents folder>
      Runs `pac copilot pack` inside each workspace folder (one per agent), in
      name order. Every workspace is tried; the failures are listed at the end.
      No agents folder, or an empty one, means nothing to pack, which passes.
      Its output is not collected: the plan uploads only the solution zips.

Exit 0 on success, 1 when a pack failed or the input is missing, 2 when pac
cannot be found or for usage errors.
"""
import argparse
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

PAC = "pac"
DEFAULT_TIMEOUT = 900
SHOW_LINES = 40
PACKAGE_TYPES = ("Unmanaged", "Managed")  # unmanaged first, as the plan runs them
INSTALL_HINT = (
    "The build job installs it first: "
    'dotnet tool install --global Microsoft.PowerApps.CLI.Tool --version "$PAC_VERSION"'
)


class PacMissing(Exception):
    pass


def find_pac() -> str:
    found = shutil.which(PAC)
    if not found:
        raise PacMissing(f"pac was not found on PATH. {INSTALL_HINT}")
    return found


def tail(text: str) -> str:
    return "\n".join(f"    {line}" for line in text.rstrip("\n").splitlines()[-SHOW_LINES:])


def run_pac(pac: str, args: list[str], cwd: Path | None, timeout: int, what: str) -> str | None:
    """Run pac once. Return a problem, or None if it exited 0."""
    shown = " ".join([PAC, *args])
    print(f"pack_offline: {shown}" + (f"  (in {cwd})" if cwd else ""), flush=True)
    try:
        done = subprocess.run(
            [pac, *args], cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return f"{what}: `{shown}` ran past the {timeout} second timeout and was stopped"
    output = (done.stdout + done.stderr).decode("utf-8", errors="replace")
    if done.returncode == 0:
        return None
    problem = f"{what}: `{shown}` failed with exit code {done.returncode}"
    return f"{problem}. Last lines of pac's output:\n{tail(output)}" if output.strip() else problem


def pack_solution(source: str, out: str, timeout: int) -> list[str]:
    src = Path(source)
    if not src.is_dir() or not any(src.iterdir()):
        return [f"no solution source to pack: {source} is missing or empty"]
    pac = find_pac()
    Path(out).mkdir(parents=True, exist_ok=True)
    problems = []
    for package_type in PACKAGE_TYPES:
        zip_path = Path(out) / f"solution_{package_type.lower()}.zip"
        zip_path.unlink(missing_ok=True)
        args = ["solution", "pack", "--zipfile", zip_path.as_posix(), "--folder", source,
                "--packagetype", package_type]
        problem = run_pac(pac, args, None, timeout, f"{package_type} solution")
        if problem:
            problems.append(problem)
        elif not zip_path.is_file() or zip_path.stat().st_size == 0:
            problems.append(f"{package_type} solution: pac exited 0 but wrote no zip at {zip_path}")
        elif not zipfile.is_zipfile(zip_path):
            problems.append(f"{package_type} solution: pac exited 0 but {zip_path} is not a zip file")
    return problems


def pack_agents(root: str, timeout: int) -> tuple[list[str], int]:
    """Return the problems and the number of workspaces tried."""
    folder = Path(root)
    workspaces = sorted(
        p for p in folder.iterdir() if p.is_dir() and not p.name.startswith(".")
    ) if folder.is_dir() else []
    if not workspaces:
        return [], 0
    pac = find_pac()
    problems = []
    for ws in workspaces:
        problem = run_pac(pac, ["copilot", "pack"], ws, timeout, f"workspace {ws.as_posix()}")
        if problem:
            problems.append(problem)
    return problems, len(workspaces)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pack the solution and agent workspaces offline.")
    sub = parser.add_subparsers(dest="command", required=True)
    sol = sub.add_parser("solution", help="pac solution pack, unmanaged and managed")
    sol.add_argument("--source", required=True, help="the YAML-format solution folder, src/")
    sol.add_argument("--out", required=True, help="folder for the two zips")
    sol.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="seconds per pac call")
    ag = sub.add_parser("agents", help="pac copilot pack in each workspace")
    ag.add_argument("--root", required=True, help="the folder holding one folder per agent, agents/")
    ag.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="seconds per pac call")
    args = parser.parse_args(argv)

    try:
        if args.command == "solution":
            problems = pack_solution(args.source, args.out, args.timeout)
            done = f"packed {args.source} into {args.out}/solution_unmanaged.zip and solution_managed.zip"
        else:
            problems, count = pack_agents(args.root, args.timeout)
            done = (f"packed {count} workspace(s) under {args.root}" if count
                    else f"no Copilot Studio workspaces under {args.root}; nothing to pack")
    except PacMissing as err:
        print(f"pack_offline: {err}", file=sys.stderr)
        return 2

    if problems:
        for problem in problems:
            print(f"pack_offline: {problem}", file=sys.stderr)
        return 1
    print(f"pack_offline: {done}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
