#!/usr/bin/env python3
"""Cut the Northwind export (XML layout, unpacked with Both) down to a small test fixture.

Keeps one table (nwind_Shippers, with its forms, their _managed.xml siblings, its
views and ribbon), one global choice (nwind_ordersstatus), one classic workflow
(Sample Data Load Order Option Sets), the model-driven app and its site map (with
their _managed.xml siblings), and the seven relationships that involve
nwind_shippers. Byte-level line and block removal only, so every kept byte is the
export's own. Fails if a removal does not find what it expects.

Usage: cut_fixture.py <src> <dst>
"""
import re
import shutil
import sys
from pathlib import Path

TABLE = "nwind_Shippers"
CHOICE = "nwind_ordersstatus"
WORKFLOW_ID = "6f739d13-1686-448d-9eb5-9c27a247cb52"
APP = "nwind_NorthwindOrdersModeldriven"
KEEP_ROOTS = {("1", TABLE.lower()), ("9", CHOICE), ("29", "{" + WORKFLOW_ID + "}"), ("62", APP), ("80", APP)}


def main(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst)
    for table in (dst / "Entities").iterdir():
        if table.name != TABLE:
            shutil.rmtree(table)
    for choice in (dst / "OptionSets").iterdir():
        if choice.stem != CHOICE:
            choice.unlink()
    for flow in (dst / "Workflows").iterdir():
        if WORKFLOW_ID.upper() not in flow.name.upper():
            flow.unlink()
    assert len(list((dst / "Workflows").iterdir())) == 2

    sol = dst / "Other" / "Solution.xml"
    data = sol.read_bytes()
    kept = 0

    def root(match: re.Match) -> bytes:
        nonlocal kept
        line = match.group(0)
        kind = re.search(rb'type="(\d+)"', line).group(1).decode()
        name = re.search(rb'(?:schemaName|id)="([^"]+)"', line).group(1).decode()
        if (kind, name) in KEEP_ROOTS:
            kept += 1
            return line
        return b""

    data = re.sub(rb'[ \t]*<RootComponent [^>]*/>\r?\n', root, data)
    assert kept == len(KEEP_ROOTS), f"kept {kept} root components"
    sol.write_bytes(data)

    def keep_rel(name: bytes) -> bool:
        return b"nwind_shippers" in name.lower()

    index = dst / "Other" / "Relationships.xml"
    data = re.sub(rb'[ \t]*<EntityRelationship Name="([^"]+)" />\r?\n',
                  lambda m: m.group(0) if keep_rel(m.group(1)) else b"", index.read_bytes())
    assert data.count(b"<EntityRelationship Name=") == 7
    index.write_bytes(data)

    defined = 0
    for path in sorted((dst / "Other" / "Relationships").iterdir()):
        data = re.sub(rb'[ \t]*<EntityRelationship Name="([^"]+)">.*?</EntityRelationship>\r?\n',
                      lambda m: m.group(0) if keep_rel(m.group(1)) else b"", path.read_bytes(), flags=re.S)
        count = data.count(b"<EntityRelationship Name=")
        if count == 0:
            path.unlink()
        else:
            defined += count
            path.write_bytes(data)
    assert defined == 7, f"{defined} relationship definitions kept"
    print(f"cut {src} to {dst}: {sum(1 for p in dst.rglob('*') if p.is_file())} files")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
