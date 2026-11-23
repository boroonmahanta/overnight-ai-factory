#!/usr/bin/env python3
"""GET AI spec check: is a Spec Kit spec ready to be Factory Eligible?

Plan 6.1, 6.3, 6.4 and 6.6; DG5 (ADO 2544) in the planning repo's
`docs/plans/stage-1-day-gate-plan.md`.

One script, two copies (D3, Boroon, 7 November 2026). The source is
`spec/check_spec.py` in `GetAI-IP/factory-gates`. The `getai-spec-check` Spec
Kit extension ships a byte-identical copy, which its mandatory
`before_implement` hook runs. The gate's CI job runs its own trusted copy on
every spec pull request and checks the vendored copy's hash (ADO 2538), so a
hook that was skipped or edited is caught there.

It reads the spec format of the `getai` and `getai-lcp` presets (DG4). It fails
on, by rule name:

  spec        the spec file is missing or not UTF-8 text
  header      no YAML header; a header line that is not `key: "value"`; a key
              given twice; a missing or invalid lane (A, B), profile (lcp, pcp,
              and the same as --profile), ambition (low, high) or work_size
              (XS, S, M, L, XL); profile lcp on a lane other than B (plan 6.3)
  ado-id      an ado_id that is missing or not digits, or a spec folder not
              named `<ado_id>-<short-name>`
  design      design_document, design_version or prototype neither filled nor
              `n/a: <reason>`; a design version that says "latest"; a design
              document with no exact version; a Teams link as the document
  marker      an open `[NEEDS CLARIFICATION` marker, anywhere in the spec
  checklist   an unticked item in any file under the spec's `checklists/`; a
              missing or empty `getai.md` (and `lcp.md` for profile lcp)
  nfr         a missing or empty Non-Functional Requirements section; an NFR
              line still a bracketed placeholder, or `n/a` with no reason
  assumption  an Assumptions line not ending `(approved: <who>, <YYYY-MM-DD>)`
  criteria    no `AC-<n>` IDs; an acceptance scenario without one; an ID given
              twice; no Acceptance Scenario Map; an `AC-<n>` with no scenario ID
              in the map (the placeholder "[to be written by the scenario
              author]" counts as none); a map row for an ID the spec does not
              define; fewer than 20 criteria on lane A (plan 6.6)
  lcp-field   for profile lcp: no Low-Code Fields section, or a field in it
              that is missing, empty, a bracketed placeholder, or "Not
              applicable" without a reason
  scenario    with --repo: a scenario ID in the map that resolves to no file
              under tests/. An ID resolves to a file whose name is the ID plus
              its extensions (`tests/scenarios/<id>.yaml`,
              `tests/acceptance/ui/<id>.spec.ts`), or, if it holds a slash, to
              that path under tests/. DG7 (2546) sets the scenario conventions
              and may change this.

It warns, without failing (design-leak, plan 6.6), when a line names a library,
schema or file layout, or holds a code block, outside Constraints. The Low-Code
Fields and the Acceptance Scenario Map are exempt too: plan 6.3 asks for names
there. Text inside HTML comments is ignored, except for markers.

Usage:
  python3 -I check_spec.py --spec specs/<ado-id>-<name>/spec.md --profile lcp [--repo .]

Exit 0 when nothing fails (warnings allowed), 1 otherwise, usage errors
included. Standard library only. Python 3.10 or later, as the gate; it also runs
on 3.9, the `python3` many Macs ship with.
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

PROFILES = ("lcp", "pcp")
LANES = ("A", "B")
AMBITIONS = ("low", "high")
WORK_SIZES = ("XS", "S", "M", "L", "XL")
DESIGN_FIELDS = ("design_document", "design_version", "prototype")
LANE_A_FLOOR = 20
REQUIRED_CHECKLISTS = {"lcp": ("getai.md", "lcp.md"), "pcp": ("getai.md",)}
CHECKLIST_TEMPLATES = {"getai.md": "getai-checklist", "lcp.md": "getai-lcp-checklist"}

# The fields under "## Low-Code Fields" in the getai-lcp spec template, in its
# order. While both are staged in one repo, a test checks this list against the
# template's `###` headings.
LCP_FIELDS = (
    "Solution boundaries",
    "Data model intent",
    "Connection references",
    "Environment variables and values per environment",
    "Names",
    "Reference components",
    "Inventory check",
    "Open questions",
    "Security roles",
    "Design-first mock or prototype",
    "Testability contract",
    "Verify profile change",
    "Glossary terms",
    "Copilot Studio agent",
    "Residency tier",
    "Licence impact",
    "Kind of change to a model-driven app",
)

LCP_SECTION = "low-code fields"
NFR_SECTION = "non-functional requirements"
MAP_SECTION = "acceptance scenario map"
ASSUMPTIONS_SECTION = "assumptions"
LEAK_EXEMPT = ("constraints", LCP_SECTION, MAP_SECTION)
NOT_A_SCENARIO = {"none", "tbd", "todo", "n/a"}

HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
ITEM = re.compile(r"^ ?(?:[-*+]|\d+[.)])\s+(.*)$")
CHECKBOX = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\[(.)\]\s*(.*)$")
MARKER = re.compile(r"\[\s*NEEDS CLARIFICATION[^\]]*\]?", re.IGNORECASE)
PLACEHOLDER = re.compile(r"\[[^\[\]]*\]")
PLACEHOLDER_AT_END = re.compile(r"(?:^|:\s*)(\[[^\[\]]*\])\.?$")
BOLD_LABEL = re.compile(r"^\*\*([^*]+)\*\*\s*:?\s*")
NOT_APPLICABLE = re.compile(r"(?:n/a|not applicable)\b", re.IGNORECASE)
NOT_APPLICABLE_REASON = re.compile(r"(?:n/a|not applicable)\s*:\s*(.*)", re.IGNORECASE | re.DOTALL)
KEY_VALUE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*")
ADO_ID = re.compile(r"[1-9][0-9]*")
AC_DEFINED = re.compile(r"^(?:\*\*)?AC-([0-9]+)\b")
AC_CELL = re.compile(r"AC-([0-9]+)")
GIVEN = re.compile(r"^(?:\*\*)?Given\b")
SCENARIO_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]*")
APPROVED = re.compile(r"\(approved:\s*([^,()]*?)\s*,\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\s*\)\s*\.?\s*$")
TABLE_SEPARATOR = re.compile(r":?-{3,}:?")
URL = re.compile(r"https?://\S+|\]\([^)]*\)")

# Design leak (plan 6.6): first match wins, one warning per line.
LEAKS = (
    ("a schema", re.compile(
        r"(?i)\b(?:create|alter|drop)\s+table\b|\bprimary\s+key\b|\bforeign\s+key\b"
        r"|\bn?varchar\b|\buniqueidentifier\b|\"\$schema\"")),
    ("a schema name", re.compile(r"(?<![\w.-])[a-z][a-z0-9]{1,7}_[a-z][a-z0-9_]{2,}\b")),
    ("a library", re.compile(
        r"\b(?:npm|pnpm|yarn)\s+(?:i|install|add)\b|\bpip3?\s+install\b|\bdotnet\s+add\s+package\b"
        r"|\bInstall-Module\b|\bfrom\s+[\w.]+\s+import\b|\bimport\s+[\w.{}*, ]+\s+from\s+['\"]"
        r"|\brequire\(\s*['\"]|(?<![\w.@])@?[a-z][\w-]*(?:/[\w.-]+)?@[0-9]+(?:\.[0-9]+)+")),
    ("a library", re.compile(
        r"\b(?:React|Angular|Vue\.js|Svelte|Next\.js|Node\.js|Django|Flask|FastAPI|Spring Boot"
        r"|Entity Framework|jQuery|Tailwind|Lodash|Axios|pandas|NumPy|Newtonsoft|Prisma|Sequelize"
        r"|TypeORM|Moment\.js)\b")),
    ("a file layout", re.compile(r"(?<![\w/.-])(?:[\w.-]+/)+[\w.-]+\.[A-Za-z][A-Za-z0-9]{0,4}\b")),
    ("a file layout", re.compile(
        r"(?<![\w/.-])(?:src|lib|tests?|scripts|plugins|apps|agents|builders|workflows|deploy"
        r"|config|bin|docs|handoff|specs)/")),
    ("a file layout", re.compile(
        r"(?<![\w/.-])[\w-]+\.(?:py|ts|tsx|js|mjs|cjs|jsx|json|ya?ml|xml|cs|csproj|sln|sql|ps1"
        r"|psm1|sh|java|kt|go|rs|rb|php|css|scss|html?|toml|ini|cfg|dll|msapp)\b")),
)


class Report:
    def __init__(self) -> None:
        self.failures: list[tuple[str, str, str]] = []
        self.warnings: list[tuple[str, str, str]] = []

    def fail(self, rule: str, where: str, message: str) -> None:
        self.failures.append((rule, where, message))

    def warn(self, rule: str, where: str, message: str) -> None:
        self.warnings.append((rule, where, message))

    def render(self, spec: str, profile: str) -> str:
        lines = [f"GET AI spec check: {spec} (profile {profile})"]
        lines += [f"FAIL [{rule}] {where}: {message}" for rule, where, message in self.failures]
        lines += [f"WARN [{rule}] {where}: {message}" for rule, where, message in self.warnings]
        counts = f"{plural(len(self.failures), 'failure')} and {plural(len(self.warnings), 'warning')}"
        if self.failures:
            lines.append(f"Result: FAIL, {counts}. The spec is not ready for implement or Factory Eligible.")
        else:
            lines.append(f"Result: PASS, {counts}.")
        return "\n".join(lines)


def plural(n: int, word: str) -> str:
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def quote(text: str, limit: int = 70) -> str:
    text = " ".join(text.split())
    return f'"{text}"' if len(text) <= limit else f'"{text[:limit - 3]}..."'


def strip_comments(text: str) -> str:
    """Blank out HTML comments, keeping their line breaks so line numbers hold."""
    return re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.DOTALL)


def norm_title(title: str) -> str:
    title = re.sub(r"\*?\([^)]*\)\*?", "", title)
    title = re.sub(r"[*_`]", "", title)
    return " ".join(title.lower().split())


def is_placeholder(text: str) -> bool:
    return PLACEHOLDER.fullmatch(text.strip().rstrip(".").strip()) is not None


def not_applicable_reason(text: str) -> str | None:
    """None if the text is not "n/a" or "Not applicable"; "" if it has no reason."""
    text = text.strip()
    if not NOT_APPLICABLE.match(text):
        return None
    m = NOT_APPLICABLE_REASON.fullmatch(text)
    if not m:
        return ""
    reason = m.group(1).strip()
    return "" if not reason or is_placeholder(reason) else reason


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    return all(TABLE_SEPARATOR.fullmatch(cell.replace(" ", "")) for cell in cells if cell) and any(cells)


def strip_item_marker(line: str) -> str:
    m = ITEM.match(line)
    return m.group(1).strip() if m else line.strip()


class Spec:
    def __init__(self, path: Path, text: str) -> None:
        self.path = path
        text = text.lstrip("﻿")
        self.raw = text.splitlines()
        self.lines = strip_comments(text).splitlines()
        self.lines += [""] * (len(self.raw) - len(self.lines))
        self.in_fence: list[bool] = []
        self.fence_starts: set[int] = set()
        fence = None
        for i, line in enumerate(self.lines):
            stripped = line.lstrip()
            if fence is None and stripped.startswith(("```", "~~~")):
                fence = stripped[:3]
                self.fence_starts.add(i)
                self.in_fence.append(True)
            elif fence is not None:
                self.in_fence.append(True)
                if stripped.startswith(fence):
                    fence = None
            else:
                self.in_fence.append(False)
        self.header: dict[str, tuple[str, int]] = {}
        self.has_header = False
        self.body_start = 0
        self.headings: list[tuple[int, int, str]] = []

    def where(self, index: int) -> str:
        return f"{self.path}:{index + 1}"

    def index_headings(self) -> None:
        for i in range(self.body_start, len(self.lines)):
            if self.in_fence[i]:
                continue
            m = HEADING.match(self.lines[i])
            if m:
                self.headings.append((i, len(m.group(1)), norm_title(m.group(2))))

    def section(self, title: str, level: int | None = None) -> tuple[int, int, int] | None:
        """(heading index, first body index, end index) of the first matching section."""
        for k, (i, lvl, norm) in enumerate(self.headings):
            if norm == title and (level is None or lvl == level):
                end = len(self.lines)
                for j, lvl2, _ in self.headings[k + 1:]:
                    if lvl2 <= lvl:
                        end = j
                        break
                return i, i + 1, end
        return None

    def subsections(self, start: int, end: int, level: int) -> list[tuple[int, str, int, int]]:
        found = [(i, norm) for i, lvl, norm in self.headings if start <= i < end and lvl == level]
        result = []
        for k, (i, norm) in enumerate(found):
            stop = end
            for j, lvl, _ in self.headings:
                if i < j < end and lvl <= level:
                    stop = j
                    break
            result.append((i, norm, i + 1, stop))
        return result

    def items(self, start: int, end: int) -> list[tuple[int, str]]:
        """Top-level list items, each joined with its continuation lines."""
        items: list[list] = []
        current = None
        for i in range(start, end):
            if self.in_fence[i]:
                current = None
                continue
            line = self.lines[i]
            if not line.strip():
                current = None
                continue
            m = ITEM.match(line)
            if m:
                current = [i, m.group(1).strip()]
                items.append(current)
            elif HEADING.match(line) or line.lstrip().startswith("|"):
                current = None
            elif current is not None:
                current[1] += " " + line.strip()
        return [(i, text) for i, text in items]

    def table_rows(self, start: int, end: int) -> list[tuple[int, list[str]]]:
        """Data rows of the tables in a range: header and separator rows dropped."""
        rows: list[tuple[int, list[str]]] = []
        previous = None
        for i in range(start, end):
            line = self.lines[i].strip()
            if self.in_fence[i] or not line.startswith("|"):
                previous = None
                continue
            cells = table_cells(line)
            if is_separator(cells):
                if rows and previous is not None and rows[-1][0] == previous:
                    rows.pop()
                previous = None
                continue
            rows.append((i, cells))
            previous = i
        return rows


def parse_header(spec: Spec, report: Report) -> None:
    if not spec.raw or spec.raw[0].strip() != "---":
        report.fail("header", spec.where(0), "no YAML header: the spec must start with the getai preset's `---` header")
        return
    end = None
    for i in range(1, len(spec.raw)):
        if spec.raw[i].strip() == "---":
            end = i
            break
        if HEADING.match(spec.raw[i]):
            # The spec's title comes before any `---`: the header was never closed.
            break
    if end is None:
        report.fail("header", spec.where(0), "the YAML header has no closing `---` line before the spec's title")
        return
    spec.has_header = True
    spec.body_start = end + 1
    for i in range(1, end):
        line = spec.raw[i]
        if not line.strip():
            continue
        m = KEY_VALUE.fullmatch(line)
        if not m:
            report.fail("header", spec.where(i), f'header line {quote(line)} is not `key: "value"`')
            continue
        key, value = m.groups()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
            if m.group(2)[0] == '"':
                value = value.replace('\\"', '"').replace("\\\\", "\\")
        else:
            value = re.sub(r"\s+#.*$", "", value)
        if key in spec.header:
            report.fail("header", spec.where(i), f"`{key}` is given twice in the header")
            continue
        spec.header[key] = (value.strip(), i)


def check_choice(spec: Spec, report: Report, key: str, choices: tuple[str, ...]) -> str | None:
    allowed = ", ".join(choices)
    if key not in spec.header:
        report.fail("header", spec.where(0), f"`{key}` is missing from the header; use one of {allowed}")
        return None
    value, i = spec.header[key]
    if value not in choices:
        what = "the template placeholder" if is_placeholder(value) else quote(value)
        report.fail("header", spec.where(i), f"`{key}` is {what}; use one of {allowed}")
        return None
    return value


def check_header(spec: Spec, report: Report, profile: str) -> str | None:
    """Check the story fields; return the lane if it is valid."""
    if not spec.has_header:
        return None
    lane = check_choice(spec, report, "lane", LANES)
    header_profile = check_choice(spec, report, "profile", PROFILES)
    if header_profile and header_profile != profile:
        report.fail("header", spec.where(spec.header["profile"][1]),
                    f"`profile` is {header_profile}, but the check ran with --profile {profile}")
    if profile == "lcp" and lane and lane != "B":
        report.fail("header", spec.where(spec.header["lane"][1]),
                    f"profile lcp runs on lane B (plan 6.3); `lane` is {lane}")
    check_choice(spec, report, "ambition", AMBITIONS)
    check_choice(spec, report, "work_size", WORK_SIZES)

    if "ado_id" not in spec.header:
        report.fail("ado-id", spec.where(0), "`ado_id` is missing from the header; every spec carries its ADO work item ID")
    else:
        ado_id, i = spec.header["ado_id"]
        if not ADO_ID.fullmatch(ado_id):
            what = "the template placeholder" if is_placeholder(ado_id) else quote(ado_id)
            report.fail("ado-id", spec.where(i), f"`ado_id` is {what}; it must be the ADO work item ID, digits only")
        else:
            folder = spec.path.parent.name
            if not (folder.startswith(f"{ado_id}-") and len(folder) > len(ado_id) + 1):
                report.fail("ado-id", spec.where(i),
                            f"the spec's folder is {quote(folder)}; name it `{ado_id}-<short-name>`, "
                            "never with Spec Kit's own numbering")

    filled = {}
    for key in DESIGN_FIELDS:
        if key not in spec.header:
            report.fail("design", spec.where(0), f"`{key}` is missing from the header; fill it, or write `n/a: <reason>`")
            continue
        value, i = spec.header[key]
        reason = not_applicable_reason(value)
        if not value or is_placeholder(value):
            what = "empty" if not value else "the template placeholder"
            report.fail("design", spec.where(i), f"`{key}` is {what}; fill it, or write `n/a: <reason>`")
        elif reason == "":
            report.fail("design", spec.where(i), f"`{key}` says n/a with no reason; write `n/a: <reason>`")
        else:
            filled[key] = (value, i, reason is None)
    document = filled.get("design_document")
    version = filled.get("design_version")
    if version and version[2] and re.search(r"\blatest\b", version[0], re.IGNORECASE):
        report.fail("design", spec.where(version[1]),
                    "`design_version` says latest; give the exact approved version identifier")
    if document and document[2] and version and not version[2]:
        report.fail("design", spec.where(version[1]),
                    "`design_document` names a document but `design_version` is n/a; give its exact approved version")
    if document and document[2] and "teams.microsoft.com" in document[0].lower():
        report.fail("design", spec.where(document[1]),
                    "`design_document` is a Teams link; give the SharePoint document identity (plan 6.4)")
    return lane


def check_markers(spec: Spec, report: Report) -> None:
    for i, line in enumerate(spec.raw):
        for m in MARKER.finditer(line):
            report.fail("marker", spec.where(i),
                        f"open marker {quote(m.group(0))}; answer it in clarify and replace the marker with the answer")


def check_checklists(spec: Spec, report: Report, profile: str) -> None:
    folder = spec.path.parent / "checklists"
    required = REQUIRED_CHECKLISTS[profile]
    for name in required:
        if not (folder / name).is_file():
            report.fail("checklist", str(folder / name),
                        f"missing; specify writes it from the `{CHECKLIST_TEMPLATES[name]}` template, "
                        "and a reviewer ticks it")
    if not folder.is_dir():
        return
    for path in sorted(p for p in folder.rglob("*") if p.is_file()):
        if any(part.startswith(".") for part in path.relative_to(folder).parts):
            continue
        try:
            text = strip_comments(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError) as exc:
            report.fail("checklist", str(path), f"cannot be read as UTF-8 text ({exc.__class__.__name__})")
            continue
        items, open_items, fence = 0, [], False
        for n, line in enumerate(text.splitlines(), start=1):
            if line.lstrip().startswith(("```", "~~~")):
                fence = not fence
                continue
            m = None if fence else CHECKBOX.match(line)
            if not m:
                continue
            items += 1
            if m.group(1) not in "xX":
                chk = re.search(r"\bCHK[0-9]+\b", m.group(2))
                open_items.append((n, chk.group(0) if chk else f"line {n}"))
        if path.name in required and path.parent == folder and items == 0:
            report.fail("checklist", str(path), "holds no checklist items")
        if open_items:
            names = [name for _, name in open_items]
            shown = ", ".join(names[:10]) + (f" and {len(names) - 10} more" if len(names) > 10 else "")
            report.fail("checklist", f"{path}:{open_items[0][0]}",
                        f"{plural(len(names), 'item')} not ticked: {shown}. A reviewer ticks them, never the agent")


def check_nfr(spec: Spec, report: Report) -> None:
    found = spec.section(NFR_SECTION)
    if found is None:
        report.fail("nfr", spec.where(spec.body_start), "no Non-Functional Requirements section")
        return
    heading, start, end = found
    items = spec.items(start, end)
    if not items:
        report.fail("nfr", spec.where(heading),
                    "the Non-Functional Requirements section is empty; give each NFR line a testable target, "
                    "or `n/a: <reason>`")
        return
    for i, text in items:
        label = BOLD_LABEL.match(text)
        name = label.group(1).strip() if label else quote(text, 40)
        value = text[label.end():].strip() if label else text
        reason = not_applicable_reason(value)
        if not value:
            report.fail("nfr", spec.where(i), f"{name} has no target")
        elif is_placeholder(value):
            report.fail("nfr", spec.where(i), f"{name} is still the template placeholder; give a testable target, or `n/a: <reason>`")
        elif reason == "":
            report.fail("nfr", spec.where(i), f"{name} says n/a with no reason; write `n/a: <reason>`")


def check_assumptions(spec: Spec, report: Report) -> None:
    found = spec.section(ASSUMPTIONS_SECTION)
    if found is None:
        return
    _, start, end = found
    for i, text in spec.items(start, end):
        if re.fullmatch(r"(?i)none\.?", text):
            continue
        m = APPROVED.search(text)
        if not m:
            report.fail("assumption", spec.where(i),
                        f"{quote(text, 50)} is not approved; end it with `(approved: <who>, <YYYY-MM-DD>)` once the owner approves it")
            continue
        who, date = m.groups()
        if not who or is_placeholder(who) or who.startswith("<"):
            report.fail("assumption", spec.where(i), f"{quote(text, 50)} does not say who approved it")
        try:
            datetime.date.fromisoformat(date)
        except ValueError:
            report.fail("assumption", spec.where(i), f"{quote(text, 50)} has approval date {date}, which is not a real date")


def scenario_ids(cell: str) -> tuple[list[str], list[str]]:
    """(valid IDs, invalid tokens) in a map cell. Placeholders and "none" count as no ID."""
    cell = PLACEHOLDER.sub(" ", cell)
    tokens = [t.strip("`*") for t in re.split(r"[,;\s]+", cell)]
    tokens = [t for t in tokens if t and t.lower() not in NOT_A_SCENARIO]
    good = [t for t in tokens if SCENARIO_ID.fullmatch(t)]
    bad = [t for t in tokens if not SCENARIO_ID.fullmatch(t)]
    return good, bad


def check_criteria(spec: Spec, report: Report, lane: str | None, profile: str) -> dict[str, list[str]]:
    """Check the AC IDs and the map; return each scenario ID with the criteria that use it."""
    found_map = spec.section(MAP_SECTION)
    defined: dict[int, int] = {}
    for i, text in spec.items(spec.body_start, len(spec.lines)):
        if found_map and found_map[1] <= i < found_map[2]:
            continue
        m = AC_DEFINED.match(text)
        if m:
            n = int(m.group(1))
            if n in defined:
                report.fail("criteria", spec.where(i), f"AC-{n} is defined twice (also line {defined[n] + 1})")
            else:
                defined[n] = i
        elif GIVEN.match(text):
            report.fail("criteria", spec.where(i),
                        "an acceptance scenario has no ID; start it with `**AC-<n>**:` so locked scenarios can point at it")
    if not defined:
        report.fail("criteria", spec.where(spec.body_start),
                    "no acceptance criterion IDs; start every acceptance scenario with `**AC-<n>**:`")
    if lane == "A" and profile != "lcp" and len(defined) < LANE_A_FLOOR:
        report.fail("criteria", spec.where(spec.body_start),
                    f"lane A needs at least {LANE_A_FLOOR} testable criteria (plan 6.6); this spec has {len(defined)}")
    if found_map is None:
        report.fail("criteria", spec.where(spec.body_start), "no Acceptance Scenario Map section")
        return {}

    heading, start, end = found_map
    mapped: dict[int, list[str]] = {}
    rows: dict[int, int] = {}
    used: dict[str, list[str]] = {}
    for i, cells in spec.table_rows(start, end):
        key = cells[0].strip("`* ")
        m = AC_CELL.fullmatch(key)
        if not m:
            report.fail("criteria", spec.where(i), f"a map row names {quote(key, 30)}, not an AC-<n> ID")
            continue
        n = int(m.group(1))
        rows.setdefault(n, i)
        good, bad = scenario_ids(cells[1] if len(cells) > 1 else "")
        for token in bad:
            report.fail("criteria", spec.where(i), f"{quote(token, 30)} in the map row for AC-{n} is not a scenario ID")
        mapped.setdefault(n, []).extend(good)
        for sid in good:
            used.setdefault(sid, [])
            if f"AC-{n}" not in used[sid]:
                used[sid].append(f"AC-{n}")
        if defined and n not in defined:
            report.fail("criteria", spec.where(i), f"the map names AC-{n}, but no acceptance scenario has that ID")
    for n in sorted(defined):
        if not mapped.get(n):
            where = spec.where(rows.get(n, heading))
            report.fail("criteria", where,
                        f"AC-{n} has no locked scenario ID in the Acceptance Scenario Map "
                        "(the placeholder counts as none)")
    return used


def check_scenario_files(spec: Spec, report: Report, repo: Path, used: dict[str, list[str]]) -> None:
    tests = repo / "tests"
    if not used:
        return
    if not tests.is_dir():
        report.fail("scenario", str(tests), "no tests/ folder in --repo, so no scenario ID resolves")
        return
    root = tests.resolve()
    names = set()
    for path in tests.rglob("*"):
        if path.is_file() and not any(part.startswith(".") for part in path.relative_to(tests).parts):
            names.add(path.name)
    found_map = spec.section(MAP_SECTION)
    where = spec.where(found_map[0]) if found_map else str(spec.path)
    for sid, criteria in used.items():
        if "/" in sid:
            relative = sid[len("tests/"):] if sid.startswith("tests/") else sid
            target = (tests / relative).resolve()
            resolved = target.is_file() and target.is_relative_to(root)
        else:
            resolved = any(name == sid or name.startswith(sid + ".") for name in names)
        if not resolved:
            report.fail("scenario", where,
                        f"scenario ID {sid} ({', '.join(criteria)}) resolves to no file under tests/; "
                        f"name the file after the ID, for example tests/scenarios/{sid.rsplit('/', 1)[-1]}.yaml")


def check_lcp_fields(spec: Spec, report: Report) -> None:
    found = spec.section(LCP_SECTION, level=2)
    if found is None:
        report.fail("lcp-field", spec.where(spec.body_start), "no `## Low-Code Fields` section (profile lcp, plan 6.3)")
        return
    heading, start, end = found
    fields = spec.subsections(start, end, 3)
    present = {norm for _, norm, _, _ in fields}
    for title in LCP_FIELDS:
        if norm_title(title) not in present:
            report.fail("lcp-field", spec.where(heading),
                        f"the field \"{title}\" is missing; fill it, or write `Not applicable: <reason>`")
    for i, norm, body_start, body_end in fields:
        title = spec.lines[i].lstrip("#").strip()
        title = re.sub(r"\s*\*?\([^)]*\)\*?\s*$", "", title)
        body = [(j, spec.lines[j].strip()) for j in range(body_start, body_end) if spec.lines[j].strip()]
        if not body:
            report.fail("lcp-field", spec.where(i), f"\"{title}\" is empty; fill it, or write `Not applicable: <reason>`")
            continue
        reason = not_applicable_reason(strip_item_marker(body[0][1]))
        if reason == "":
            report.fail("lcp-field", spec.where(body[0][0]),
                        f"\"{title}\" says Not applicable with no reason; write `Not applicable: <reason>`")
            continue
        for j, line in body:
            leftover = None
            if line.startswith("|"):
                cells = table_cells(line)
                if not is_separator(cells):
                    leftover = next((c for c in cells if c and is_placeholder(c)), None)
            else:
                m = PLACEHOLDER_AT_END.search(strip_item_marker(line))
                leftover = m.group(1) if m else None
            if leftover:
                report.fail("lcp-field", spec.where(j),
                            f"\"{title}\" still holds the placeholder {quote(leftover, 50)}; fill it, "
                            "or write `Not applicable: <reason>`")
                break


def check_design_leak(spec: Spec, report: Report) -> None:
    owner = ""
    levels = {i: lvl for i, lvl, _ in spec.headings}
    norms = {i: norm for i, _, norm in spec.headings}
    for i in range(spec.body_start, len(spec.lines)):
        if levels.get(i, 9) <= 2:
            owner = norms[i]
        if owner in LEAK_EXEMPT:
            continue
        if spec.in_fence[i]:
            if i in spec.fence_starts:
                report.warn("design-leak", spec.where(i),
                            "a code block outside Constraints; move technical design to Constraints (plan 6.6)")
            continue
        line = URL.sub(" ", spec.lines[i])
        for what, pattern in LEAKS:
            m = pattern.search(line)
            if m:
                report.warn("design-leak", spec.where(i),
                            f"names {what} ({quote(m.group(0), 40)}) outside Constraints; say what users need, "
                            "or move it to Constraints (plan 6.6)")
                break


def check(spec_path: Path, profile: str, repo: Path | None, report: Report) -> None:
    if not spec_path.is_file():
        report.fail("spec", str(spec_path), "no such spec file")
        return
    try:
        text = spec_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        report.fail("spec", str(spec_path), f"cannot be read as UTF-8 text ({exc.__class__.__name__})")
        return
    spec = Spec(spec_path, text)
    parse_header(spec, report)
    spec.index_headings()
    lane = check_header(spec, report, profile)
    check_markers(spec, report)
    check_checklists(spec, report, profile)
    check_nfr(spec, report)
    check_assumptions(spec, report)
    used = check_criteria(spec, report, lane, profile)
    if repo is not None:
        if repo.is_dir():
            check_scenario_files(spec, report, repo, used)
        else:
            report.fail("scenario", str(repo), "--repo is not a folder")
    if profile == "lcp":
        check_lcp_fields(spec, report)
    check_design_leak(spec, report)


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        print(f"check_spec.py: {message}", file=sys.stderr)
        sys.exit(1)


def main(argv: list[str] | None = None) -> int:
    parser = Parser(description="GET AI spec check (plan 6.1). Exit 0 when nothing fails, 1 otherwise.")
    parser.add_argument("--spec", required=True, type=Path, help="the spec.md to check")
    parser.add_argument("--profile", required=True, choices=PROFILES, help="the story's profile")
    parser.add_argument("--repo", type=Path, help="the project repo root; scenario IDs must resolve under its tests/")
    args = parser.parse_args(argv)
    report = Report()
    check(args.spec, args.profile, args.repo, report)
    print(report.render(str(args.spec), args.profile))
    return 1 if report.failures else 0


if __name__ == "__main__":
    sys.exit(main())
