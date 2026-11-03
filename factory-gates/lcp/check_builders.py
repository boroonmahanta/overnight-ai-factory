#!/usr/bin/env python3
"""Run every builder in a project repo, then fail if the tree no longer matches its commit.

Agents edit builder inputs and per-component builders, never generated output
(plan section 5.6). This check proves the committed output is what the
committed builders make. It is the first step of the gate's `build` job
(Appendix A), before `pac solution pack`.

It runs PR code, so the job it runs in holds no credentials (rule 5). It is a
gate-repo script so its logic is tested here, but it is only as trusted as that
job: a hostile builder can defeat it. It exists to catch honest drift, such as a
hand edit to generated output or an output file left out of the commit.

What it does, from the project root:
  1. Runs each workflows/build/*.py in name order, as `python -B <builder>`, with
     the project root as the working directory. Every builder runs, even after one
     fails, so one run reports every problem.
  2. Fails if any builder exits non-zero or runs past the timeout.
  3. Fails if any tracked file differs from the starting commit (`git diff`,
     staged or not), or if a builder wrote a file git does not know and does not
     ignore. The plan's inline step used `git diff --exit-code` only, which misses
     a new output file that was never committed; pack would still ship it.

Helper modules belong in builders/lib/ (protected) or a subfolder, not beside the
builders: every *.py directly in workflows/build/ is run.

Usage:
  check_builders.py --root <project repo> [--timeout <seconds per builder>]

Exit 0 when clean, 1 when a builder failed or the tree drifted, 2 for usage
errors (root missing, not the top of a git work tree).
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

BUILDER_GLOB = "workflows/build/*.py"
DEFAULT_TIMEOUT = 600
SHOW_LINES = 40  # lines of builder output or diff to show on failure


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True
    ).stdout.decode("utf-8", errors="surrogateescape")


def indent(lines: list[str]) -> str:
    return "\n".join(f"    {line}" for line in lines)


def tail(text: str) -> str:
    return indent(text.rstrip("\n").splitlines()[-SHOW_LINES:])


def head(text: str) -> str:
    return indent(text.splitlines()[:SHOW_LINES])


def find_builders(root: Path) -> list[Path]:
    return sorted(p for p in root.glob(BUILDER_GLOB) if p.is_file())


def run_builder(root: Path, builder: Path, timeout: int) -> str | None:
    """Run one builder. Return a problem, or None if it exited 0."""
    rel = builder.relative_to(root).as_posix()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")  # no __pycache__ in the tree
    try:
        done = subprocess.run(
            [sys.executable, "-B", rel],
            cwd=root,
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return f"builder {rel} ran past the {timeout} second timeout and was stopped"
    if done.returncode == 0:
        return None
    output = (done.stdout + done.stderr).decode("utf-8", errors="replace")
    problem = f"builder {rel} failed with exit code {done.returncode}"
    return f"{problem}. Last lines of its output:\n{tail(output)}" if output.strip() else problem


def drift(root: Path, start: str) -> list[str]:
    """Tracked files that differ from the start commit, then unknown new files."""
    problems = []
    changed = git(root, "diff", "--name-status", "--no-renames", "-z", start, "--")
    fields = [f for f in changed.split("\0") if f]
    for status, path in zip(fields[0::2], fields[1::2]):
        word = {"M": "changed", "D": "deleted", "A": "added", "T": "type changed"}.get(status, status)
        problems.append(f"{word}: {path}")
    untracked = git(root, "ls-files", "--others", "--exclude-standard", "-z")
    problems += [f"not in the commit: {path}" for path in untracked.split("\0") if path]
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run every builder, then fail on any drift.")
    parser.add_argument("--root", required=True, help="the project repo, checked out")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="seconds per builder")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"check_builders: {args.root} is not a folder", file=sys.stderr)
        return 2
    try:
        top = Path(git(root, "rev-parse", "--show-toplevel").strip()).resolve()
        start = git(root, "rev-parse", "HEAD").strip()
    except subprocess.CalledProcessError:
        print(f"check_builders: {args.root} is not a git work tree with a commit", file=sys.stderr)
        return 2
    if top != root:
        print(f"check_builders: --root must be the top of the work tree ({top})", file=sys.stderr)
        return 2

    builders = find_builders(root)
    problems = []
    for builder in builders:
        print(f"check_builders: running {builder.relative_to(root).as_posix()}", flush=True)
        problem = run_builder(root, builder, args.timeout)
        if problem:
            problems.append(problem)

    drifted = drift(root, start)
    if drifted:
        problems.append(
            "Generated files do not match builders. Re-run the builders and commit the result; "
            "never edit generated output by hand:\n" + indent(drifted)
        )
        diff = git(root, "--no-pager", "diff", "--no-ext-diff", "--no-textconv", start, "--")
        if diff.strip():
            problems.append("First lines of the diff (- committed, + what the builders make):\n" + head(diff))

    if problems:
        for problem in problems:
            print(f"check_builders: {problem}", file=sys.stderr)
        return 1
    if not builders:
        print(f"check_builders: no builders match {BUILDER_GLOB}; nothing to run, tree is clean")
    else:
        print(f"check_builders: {len(builders)} builder(s) ran, generated files match the commit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
