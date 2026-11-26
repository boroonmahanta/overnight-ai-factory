#!/usr/bin/env python3
"""Copy an unmanaged solution zip without its canvas apps (ADO 3059, Session 48).

Byte-level edits only, so every other byte of every other member stays as
Microsoft shipped it:
- drop every member under CanvasApps/;
- solution.xml: drop each <RootComponent type="300" .../> line;
- customizations.xml: drop the whole <CanvasApps>...</CanvasApps> block;
- [Content_Types].xml: drop each <Override PartName="/CanvasApps/..." /> entry.
Fails if any edit finds nothing to change, or if "CanvasApp" is left anywhere.

Usage: strip_canvas.py <in.zip> <out.zip>
"""
import re
import sys
import zipfile

ROOT_300 = re.compile(rb'[ \t]*<RootComponent type="300"[^>]*/>\r?\n')
BLOCK = re.compile(rb'[ \t]*<CanvasApps>.*?</CanvasApps>\r?\n', re.S)
OVERRIDE = re.compile(rb'<Override PartName="/CanvasApps/[^"]*" ContentType="[^"]*" />')


def edit(name: str, data: bytes) -> bytes:
    if name == "solution.xml":
        new, n = ROOT_300.subn(b"", data)
        assert n == 5, f"solution.xml: {n} canvas root components, expected 5"
    elif name == "customizations.xml":
        new, n = BLOCK.subn(b"", data)
        assert n == 1, f"customizations.xml: {n} CanvasApps blocks, expected 1"
    elif name == "[Content_Types].xml":
        new, n = OVERRIDE.subn(b"", data)
        assert n == 5, f"[Content_Types].xml: {n} canvas overrides, expected 5"
    else:
        return data
    assert b"CanvasApp" not in new, f"{name}: CanvasApp still present"
    return new


def main(src: str, dst: str) -> None:
    dropped = 0
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            if info.filename.startswith("CanvasApps/"):
                dropped += 1
                continue
            data = edit(info.filename, zin.read(info))
            out = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            out.compress_type = zipfile.ZIP_DEFLATED
            out.external_attr = info.external_attr
            zout.writestr(out, data)
    assert dropped == 10, f"dropped {dropped} CanvasApps members, expected 10"
    print(f"wrote {dst}: dropped {dropped} CanvasApps members, edited 3 XML files")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
