#!/usr/bin/env python3
"""Remove token-shaped strings from every file under a folder, before upload.

GitHub tokens (ghp_, gho_, ghs_, ghu_, ghr_, github_pat_) and JWTs (eyJ...).
Prints how many it removed per file, never the values. Exit 0 always: the
upload must still happen so the run can be read; the count is in the summary.

  python3 -I probe/scrub.py out
"""
import re
import sys
from pathlib import Path

PATTERNS = [
    re.compile(rb"\b(?:gh[opsur]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    re.compile(rb"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}"),
]


def main():
    root = Path(sys.argv[1])
    total = 0
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.is_symlink():
            continue
        data = p.read_bytes()
        n = 0
        for pat in PATTERNS:
            data, k = pat.subn(b"[removed]", data)
            n += k
        if n:
            p.write_bytes(data)
            print(f"removed {n} from {p.relative_to(root)}")
            total += n
    print(f"token-shaped strings removed: {total}")


if __name__ == "__main__":
    main()
