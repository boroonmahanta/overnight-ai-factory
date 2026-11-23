"""Tests for spec/check_spec.py, the GET AI spec check (DG5, ADO 2544, 23 November 2026).

Each test copies tests/fixtures/specs/project/ into a temporary folder and runs
the script the way the getai-spec-check hook does: `python3 -I`, from the
project root, with `--repo .`. The fixture is a project repo with a good lcp
spec (90101), a good pcp spec (90102), their ticked checklists and stand-in
locked scenario files under tests/.

Each failing case changes the good spec in one place, so it fails on one rule
only, and the test checks that it is that rule. `edit` and `cut` fail the test
if the text they change has gone from the fixture, so a later change to the good
spec cannot quietly turn a case into a pass. The stage 1 exit clause (plan
11.2, "a spec with an open marker or no scenarios cannot become Factory
Eligible") has two whole fixture files in tests/fixtures/specs/exit-clause/.

The last class checks the copies staged beside this folder in the planning repo
(D1): the extension's byte-identical copy of the script and the getai-lcp spec
template. After the move to GHE (DG8) they live in another repo, and the class
skips; the gate's CI job then checks the vendored copy's hash (ADO 2538).
"""
import difflib
import hashlib
import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "spec" / "check_spec.py"
FIXTURES = ROOT / "tests" / "fixtures" / "specs"
PROJECT = FIXTURES / "project"
EXIT_CLAUSE = FIXTURES / "exit-clause"
LCP = "specs/90101-order-follow-up/spec.md"
PCP = "specs/90102-open-orders-export/spec.md"
LCP_CHECKLISTS = "specs/90101-order-follow-up/checklists"

MANIFESTOS = ROOT.parent / "factory-manifestos"
EXTENSION = MANIFESTOS / "spec-kit" / "extensions" / "getai-spec-check"
EXTENSION_COPY = EXTENSION / "scripts" / "check_spec.py"
GETAI_TEMPLATE = MANIFESTOS / "spec-kit" / "presets" / "getai" / "templates" / "spec-template.md"
LCP_TEMPLATE = MANIFESTOS / "spec-kit" / "presets" / "getai-lcp" / "templates" / "spec-template.md"

LINE = re.compile(r"^(FAIL|WARN) \[([\w-]+)\] ", re.MULTILINE)


class Result:
    def __init__(self, proc: subprocess.CompletedProcess) -> None:
        self.code = proc.returncode
        self.out = proc.stdout + proc.stderr
        found = LINE.findall(proc.stdout)
        self.fails = [rule for kind, rule in found if kind == "FAIL"]
        self.warns = [rule for kind, rule in found if kind == "WARN"]


class SpecCheckCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "project"
        shutil.copytree(PROJECT, self.repo)

    def tearDown(self):
        self.tmp.cleanup()

    def read(self, rel):
        return (self.repo / rel).read_text(encoding="utf-8")

    def write(self, rel, text):
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def edit(self, rel, old, new):
        text = self.read(rel)
        self.assertEqual(text.count(old), 1, f"{rel} no longer holds this text exactly once: {old!r}")
        self.write(rel, text.replace(old, new))

    def cut(self, rel, start, end):
        """Remove the text from `start` up to, not including, `end`."""
        text = self.read(rel)
        self.assertEqual(text.count(start), 1, f"{rel} no longer holds {start!r} exactly once")
        a = text.index(start)
        b = text.index(end, a)
        self.write(rel, text[:a] + text[b:])

    def run_check(self, spec=LCP, profile="lcp", repo=True, extra=()):
        args = [sys.executable, "-I", str(SCRIPT), "--spec", spec, "--profile", profile, *extra]
        if repo:
            args += ["--repo", "."]
        return Result(subprocess.run(args, cwd=self.repo, capture_output=True, text=True))

    def assertPasses(self, result, warnings=0):
        self.assertEqual(result.code, 0, result.out)
        self.assertEqual(result.fails, [], result.out)
        self.assertEqual(len(result.warns), warnings, result.out)
        self.assertIn("Result: PASS", result.out)

    def assertFailsOn(self, result, rule, text=None):
        self.assertEqual(result.code, 1, result.out)
        self.assertEqual(set(result.fails), {rule}, result.out)
        self.assertIn("Result: FAIL", result.out)
        if text is not None:
            self.assertIn(text, result.out)


class GoodSpecTests(SpecCheckCase):
    def test_good_lcp_spec_passes(self):
        self.assertPasses(self.run_check(LCP, "lcp"))

    def test_good_pcp_spec_passes(self):
        self.assertPasses(self.run_check(PCP, "pcp"))

    def test_good_specs_pass_without_repo(self):
        self.assertPasses(self.run_check(LCP, "lcp", repo=False))
        self.assertPasses(self.run_check(PCP, "pcp", repo=False))

    def test_html_comments_are_ignored(self):
        # The good lcp spec keeps the template's comments, as specify leaves them,
        # and one holds a placeholder and an unticked box on purpose.
        self.assertIn("comments: [a bracketed placeholder] and - [ ] an unticked box", self.read(LCP))
        self.edit(f"{LCP_CHECKLISTS}/getai.md", "## Notes", "<!--\n- [ ] CHK099 a sample item\n-->\n\n## Notes")
        self.assertPasses(self.run_check())

    def test_finder_files_are_ignored(self):
        (self.repo / LCP_CHECKLISTS / ".DS_Store").write_bytes(b"\x00\x00\x00\x01Bud1\xff\xfe")
        (self.repo / "tests" / ".DS_Store").write_bytes(b"\x00\x00\x00\x01Bud1")
        self.assertPasses(self.run_check())


class ExitClauseTests(SpecCheckCase):
    """Stage 1 exit (plan 11.2): a spec with an open marker or no scenarios cannot become Factory Eligible."""

    def use(self, name):
        shutil.copyfile(EXIT_CLAUSE / name, self.repo / LCP)

    def changed_lines(self, name):
        good = (PROJECT / LCP).read_text(encoding="utf-8").splitlines()
        other = (EXIT_CLAUSE / name).read_text(encoding="utf-8").splitlines()
        added = [line[2:] for line in difflib.ndiff(good, other) if line.startswith("+ ")]
        return [line for line in added if line.strip() and not line.startswith("<!--")]

    def test_open_marker_fails(self):
        self.use("open-marker.md")
        self.assertFailsOn(self.run_check(), "marker", "[NEEDS CLARIFICATION: how many days after the order date?]")

    def test_no_scenarios_fails(self):
        self.use("no-scenarios.md")
        result = self.run_check()
        self.assertFailsOn(result, "criteria")
        for n in (1, 2, 3):
            self.assertIn(f"AC-{n} has no locked scenario ID", result.out)

    def test_each_exit_fixture_is_the_good_spec_with_one_change(self):
        self.assertEqual(len(self.changed_lines("open-marker.md")), 1)
        self.assertEqual(len(self.changed_lines("no-scenarios.md")), 3)
        for line in self.changed_lines("no-scenarios.md"):
            self.assertIn("[to be written by the scenario author]", line)


class MarkerTests(SpecCheckCase):
    def test_marker_inside_a_comment_still_fails(self):
        self.edit(LCP, "### Edge Cases\n", "### Edge Cases\n\n<!-- [NEEDS CLARIFICATION: weekends?] -->\n")
        self.assertFailsOn(self.run_check(), "marker")

    def test_marker_in_lower_case_fails(self):
        self.edit(LCP, "the follow-up date is worked out", "the follow-up date is worked out [needs clarification: holidays?]")
        self.assertFailsOn(self.run_check(), "marker")


class ChecklistTests(SpecCheckCase):
    def test_unticked_getai_item_fails(self):
        self.edit(f"{LCP_CHECKLISTS}/getai.md", "- [x] CHK004", "- [ ] CHK004")
        self.assertFailsOn(self.run_check(), "checklist", "1 item not ticked: CHK004")

    def test_unticked_spec_kit_item_fails(self):
        self.edit(f"{LCP_CHECKLISTS}/requirements.md", "- [x] Edge cases are identified", "- [ ] Edge cases are identified")
        self.assertFailsOn(self.run_check(), "checklist", "requirements.md")

    def test_unticked_item_in_a_new_checklist_fails(self):
        self.write(f"{LCP_CHECKLISTS}/ux.md", "# UX Checklist\n\n- [x] CHK001 Labels\n- [ ] CHK002 Focus order\n")
        self.assertFailsOn(self.run_check(), "checklist", "CHK002")

    def test_missing_lcp_checklist_fails(self):
        (self.repo / LCP_CHECKLISTS / "lcp.md").unlink()
        self.assertFailsOn(self.run_check(), "checklist", "lcp.md: missing")

    def test_missing_checklists_folder_fails(self):
        shutil.rmtree(self.repo / LCP_CHECKLISTS)
        self.assertFailsOn(self.run_check(), "checklist", "getai.md: missing")

    def test_getai_checklist_with_no_items_fails(self):
        self.write(f"{LCP_CHECKLISTS}/getai.md", "# GET AI Checklist: Order follow-up date\n\nAll reviewed.\n")
        self.assertFailsOn(self.run_check(), "checklist", "holds no checklist items")

    def test_pcp_needs_no_lcp_checklist(self):
        self.assertFalse((self.repo / "specs/90102-open-orders-export/checklists/lcp.md").exists())
        self.assertPasses(self.run_check(PCP, "pcp"))


class NfrTests(SpecCheckCase):
    def test_missing_section_fails(self):
        self.cut(LCP, "## Non-Functional Requirements", "## Constraints")
        self.assertFailsOn(self.run_check(), "nfr", "no Non-Functional Requirements section")

    def test_empty_section_fails(self):
        self.cut(LCP, "- **NFR-001 Performance**", "## Constraints")
        self.assertFailsOn(self.run_check(), "nfr", "is empty")

    def test_placeholder_line_fails(self):
        self.edit(LCP, "The follow-up date is set within one minute of saving the order.", "[target, or n/a: reason]")
        self.assertFailsOn(self.run_check(), "nfr", "NFR-001 Performance is still the template placeholder")

    def test_na_without_reason_fails(self):
        self.edit(LCP, "n/a: the platform's own run history shows each failed run, and nothing more is needed.", "n/a")
        self.assertFailsOn(self.run_check(), "nfr", "NFR-005 Observability says n/a with no reason")

    def test_line_with_no_target_fails(self):
        self.edit(LCP, "The follow-up date is set within one minute of saving the order.", "")
        self.assertFailsOn(self.run_check(), "nfr", "NFR-001 Performance has no target")


class AssumptionTests(SpecCheckCase):
    def test_not_yet_approved_fails(self):
        self.edit(LCP, "every order they work on (approved: Spec Owner, 2026-11-24)", "every order they work on (not yet approved)")
        self.assertFailsOn(self.run_check(), "assumption", "is not approved")

    def test_approval_on_a_wrapped_line_counts(self):
        # The second assumption in the good spec wraps onto a second line, which holds its approval.
        self.assertIn("count as days\n  when the follow-up date is worked out (approved:", self.read(LCP))
        self.assertPasses(self.run_check())

    def test_impossible_date_fails(self):
        self.edit(LCP, "every order they work on (approved: Spec Owner, 2026-11-24)", "every order they work on (approved: Spec Owner, 2026-13-40)")
        self.assertFailsOn(self.run_check(), "assumption", "not a real date")

    def test_missing_approver_fails(self):
        self.edit(LCP, "every order they work on (approved: Spec Owner, 2026-11-24)", "every order they work on (approved: <who>, 2026-11-24)")
        self.assertFailsOn(self.run_check(), "assumption", "does not say who approved it")

    def test_template_placeholder_fails(self):
        self.edit(LCP, "- Salespeople can already read every order they work on (approved: Spec Owner, 2026-11-24)",
                  "- [Assumption about target users, e.g., \"Users have stable internet connectivity\"]")
        self.assertFailsOn(self.run_check(), "assumption")

    def test_none_needs_no_approval(self):
        self.assertIn("## Assumptions\n\n- None.\n", self.read(PCP))
        self.assertPasses(self.run_check(PCP, "pcp"))


class HeaderTests(SpecCheckCase):
    def test_no_header_fails(self):
        text = self.read(LCP)
        self.write(LCP, text[text.index("# Feature Specification"):])
        self.assertFailsOn(self.run_check(), "header", "no YAML header")

    def test_unclosed_header_fails(self):
        self.edit(LCP, 'prototype: "n/a: one new column on an existing form and view, with no new screen"\n---\n',
                  'prototype: "n/a: one new column on an existing form and view, with no new screen"\n')
        self.assertFailsOn(self.run_check(), "header", "no closing")

    def test_lane_not_a_or_b_fails(self):
        self.edit(LCP, 'lane: "B"', 'lane: "C"')
        self.assertFailsOn(self.run_check(), "header", '`lane` is "C"; use one of A, B')

    def test_lane_placeholder_fails(self):
        self.edit(LCP, 'lane: "B"', 'lane: "[A | B]"')
        self.assertFailsOn(self.run_check(), "header", "`lane` is the template placeholder")

    def test_profile_differs_from_flag_fails(self):
        self.edit(PCP, 'profile: "pcp"', 'profile: "lcp"')
        self.assertFailsOn(self.run_check(PCP, "pcp"), "header", "`profile` is lcp, but the check ran with --profile pcp")

    def test_lcp_on_lane_a_fails(self):
        self.edit(LCP, 'lane: "B"', 'lane: "A"')
        self.assertFailsOn(self.run_check(), "header", "profile lcp runs on lane B")

    def test_ambition_missing_fails(self):
        self.edit(LCP, 'ambition: "low"\n', "")
        self.assertFailsOn(self.run_check(), "header", "`ambition` is missing")

    def test_ambition_invalid_fails(self):
        self.edit(LCP, 'ambition: "low"', 'ambition: "medium"')
        self.assertFailsOn(self.run_check(), "header", "use one of low, high")

    def test_work_size_invalid_fails(self):
        self.edit(LCP, 'work_size: "S"', 'work_size: "XXL"')
        self.assertFailsOn(self.run_check(), "header", "use one of XS, S, M, L, XL")

    def test_key_given_twice_fails(self):
        self.edit(LCP, 'lane: "B"\n', 'lane: "B"\nlane: "A"\n')
        self.assertFailsOn(self.run_check(), "header", "`lane` is given twice")

    def test_line_that_is_not_key_value_fails(self):
        self.edit(LCP, 'work_size: "S"', 'work_size "S"')
        self.assertFailsOn(self.run_check(), "header", 'is not `key: "value"`')

    def test_unquoted_values_are_read(self):
        self.edit(LCP, 'lane: "B"', "lane: B")
        self.edit(LCP, 'work_size: "S"', "work_size: 'S'")
        self.assertPasses(self.run_check())


class AdoIdTests(SpecCheckCase):
    def test_missing_fails(self):
        self.edit(LCP, 'ado_id: "90101"\n', "")
        self.assertFailsOn(self.run_check(), "ado-id", "`ado_id` is missing")

    def test_not_digits_fails(self):
        self.edit(LCP, 'ado_id: "90101"', 'ado_id: "AB-90101"')
        self.assertFailsOn(self.run_check(), "ado-id", "digits only")

    def test_placeholder_fails(self):
        self.edit(LCP, 'ado_id: "90101"', 'ado_id: "[ADO work item ID, digits only]"')
        self.assertFailsOn(self.run_check(), "ado-id", "the template placeholder")

    def test_folder_for_another_id_fails(self):
        self.edit(LCP, 'ado_id: "90101"', 'ado_id: "90199"')
        self.assertFailsOn(self.run_check(), "ado-id", "name it `90199-<short-name>`")

    def test_spec_kit_numbered_folder_fails(self):
        shutil.move(self.repo / "specs/90101-order-follow-up", self.repo / "specs/001-order-follow-up")
        self.assertFailsOn(self.run_check("specs/001-order-follow-up/spec.md"), "ado-id", '"001-order-follow-up"')

    def test_folder_with_id_and_no_name_fails(self):
        shutil.move(self.repo / "specs/90101-order-follow-up", self.repo / "specs/90101-")
        self.assertFailsOn(self.run_check("specs/90101-/spec.md"), "ado-id")


class DesignFieldTests(SpecCheckCase):
    def test_version_latest_fails(self):
        self.edit(LCP, 'design_version: "3.0"', 'design_version: "Latest"')
        self.assertFailsOn(self.run_check(), "design", "says latest")

    def test_version_missing_fails(self):
        self.edit(LCP, 'design_version: "3.0"\n', "")
        self.assertFailsOn(self.run_check(), "design", "`design_version` is missing")

    def test_document_without_version_fails(self):
        self.edit(LCP, 'design_version: "3.0"', 'design_version: "n/a: not versioned"')
        self.assertFailsOn(self.run_check(), "design", "give its exact approved version")

    def test_teams_link_fails(self):
        self.edit(LCP, 'design_document: "SharePoint site factory-samples, library Designs, item ID 1042"',
                  'design_document: "https://teams.microsoft.com/l/channel/19%3aabc/Designs"')
        self.assertFailsOn(self.run_check(), "design", "is a Teams link")

    def test_prototype_placeholder_fails(self):
        self.edit(LCP, 'prototype: "n/a: one new column on an existing form and view, with no new screen"',
                  'prototype: "[link to the approved mock or prototype on the ADO item; or n/a: reason]"')
        self.assertFailsOn(self.run_check(), "design", "`prototype` is the template placeholder")

    def test_prototype_na_without_reason_fails(self):
        self.edit(LCP, 'prototype: "n/a: one new column on an existing form and view, with no new screen"', 'prototype: "n/a"')
        self.assertFailsOn(self.run_check(), "design", "`prototype` says n/a with no reason")

    def test_empty_field_fails(self):
        self.edit(LCP, 'prototype: "n/a: one new column on an existing form and view, with no new screen"', 'prototype: ""')
        self.assertFailsOn(self.run_check(), "design", "`prototype` is empty")

    def test_all_three_na_with_reasons_pass(self):
        self.assertIn('design_document: "n/a: no user interface', self.read(PCP))
        self.assertPasses(self.run_check(PCP, "pcp"))


class LowCodeFieldTests(SpecCheckCase):
    def test_empty_field_fails(self):
        self.edit(LCP, "### Security roles\n\nNone change.\n", "### Security roles\n\n")
        self.assertFailsOn(self.run_check(), "lcp-field", '"Security roles" is empty')

    def test_placeholder_field_fails(self):
        self.edit(LCP, "### Residency tier\n\nT2.\n", "### Residency tier\n\n[T1 to T4 (plan 9.4). It decides the engine and whether the factory may run this story at all]\n")
        self.assertFailsOn(self.run_check(), "lcp-field", '"Residency tier" still holds the placeholder')

    def test_not_applicable_without_reason_fails(self):
        self.edit(LCP, "Not applicable: no agent changes.", "Not applicable")
        self.assertFailsOn(self.run_check(), "lcp-field", '"Copilot Studio agent" says Not applicable with no reason')

    def test_missing_field_fails(self):
        self.cut(LCP, "### Licence impact", "### Kind of change")
        self.assertFailsOn(self.run_check(), "lcp-field", 'the field "Licence impact" is missing')

    def test_placeholder_table_cell_fails(self):
        self.edit(LCP, "| smpl_FollowUpDays | Number |", "| [schema name] | Number |")
        self.assertFailsOn(self.run_check(), "lcp-field", '"[schema name]"')

    def test_placeholder_after_a_label_fails(self):
        self.edit(LCP, "(facts the team looks up): none", "(facts the team looks up): [question, or none]")
        self.assertFailsOn(self.run_check(), "lcp-field", '"Open questions" still holds the placeholder')

    def test_template_guidance_line_left_in_fails(self):
        self.edit(LCP, "The number of days is the same everywhere, so its default value is 7.",
                  "[Connection references' connections go in this table too. No default value for a value that differs between environments]")
        self.assertFailsOn(self.run_check(), "lcp-field")

    def test_missing_section_fails(self):
        text = self.read(LCP)
        self.write(LCP, text[:text.index("## Low-Code Fields")])
        self.assertFailsOn(self.run_check(), "lcp-field", "no `## Low-Code Fields` section")

    def test_pcp_has_no_low_code_fields(self):
        self.assertNotIn("Low-Code Fields", self.read(PCP))
        self.assertPasses(self.run_check(PCP, "pcp"))


class CriteriaTests(SpecCheckCase):
    def test_no_criterion_ids_fails(self):
        for prefix in ("1. **AC-1**: **Given** a new", "2. **AC-2**: **Given** an open", "1. **AC-3**: **Given** three"):
            self.edit(LCP, prefix, prefix.replace(prefix[3:prefix.index("**Given**")], ""))
        self.assertFailsOn(self.run_check(), "criteria", "no acceptance criterion IDs")

    def test_scenario_without_id_fails(self):
        self.edit(LCP, "2. **AC-2**: **Given** an open order", "2. **Given** an open order")
        self.assertFailsOn(self.run_check(), "criteria", "an acceptance scenario has no ID")

    def test_criterion_with_placeholder_only_fails(self):
        self.edit(LCP, "| AC-2 | wf-follow-up-clear-01 |", "| AC-2 | [to be written by the scenario author] |")
        result = self.run_check()
        self.assertFailsOn(result, "criteria", "AC-2 has no locked scenario ID")
        self.assertEqual(len(result.fails), 1, result.out)

    def test_criterion_with_none_fails(self):
        self.edit(LCP, "| AC-2 | wf-follow-up-clear-01 |", "| AC-2 | none |")
        self.assertFailsOn(self.run_check(), "criteria", "AC-2 has no locked scenario ID")

    def test_criterion_missing_from_map_fails(self):
        self.edit(LCP, "| AC-3 | ui-follow-up-view-01 |\n", "")
        self.assertFailsOn(self.run_check(), "criteria", "AC-3 has no locked scenario ID")

    def test_map_missing_fails(self):
        self.cut(LCP, "## Acceptance Scenario Map", "## Non-Functional Requirements")
        self.assertFailsOn(self.run_check(), "criteria", "no Acceptance Scenario Map section")

    def test_criterion_defined_twice_fails(self):
        self.edit(LCP, "1. **AC-3**: **Given** three", "1. **AC-2**: **Given** three")
        self.assertFailsOn(self.run_check(), "criteria", "AC-2 is defined twice")

    def test_map_row_for_unknown_criterion_fails(self):
        self.edit(LCP, "| AC-3 | ui-follow-up-view-01 |\n", "| AC-3 | ui-follow-up-view-01 |\n| AC-9 | wf-follow-up-set-01 |\n")
        self.assertFailsOn(self.run_check(), "criteria", "the map names AC-9")

    def test_map_row_that_is_not_a_criterion_fails(self):
        self.edit(LCP, "| AC-3 | ui-follow-up-view-01 |\n", "| AC-3 | ui-follow-up-view-01 |\n| FR-001 | wf-follow-up-set-01 |\n")
        self.assertFailsOn(self.run_check(), "criteria", 'names "FR-001", not an AC-<n> ID')

    def add_criteria(self, last):
        scenarios = "".join(
            f"{n}. **AC-{n}**: **Given** order set {n}, **When** the export runs, **Then** the list matches set {n}.\n"
            for n in range(3, last + 1))
        self.edit(PCP, "**Then** the list holds only its column headings.\n",
                  "**Then** the list holds only its column headings.\n" + scenarios)
        rows = "".join(f"| AC-{n} | orders-export-{n:02d} |\n" for n in range(3, last + 1))
        self.edit(PCP, "| AC-2 | `orders-export-02` |\n", "| AC-2 | `orders-export-02` |\n" + rows)
        self.edit(PCP, 'lane: "B"', 'lane: "A"')

    def test_lane_a_with_19_criteria_fails(self):
        self.add_criteria(19)
        self.assertFailsOn(self.run_check(PCP, "pcp", repo=False), "criteria", "lane A needs at least 20 testable criteria (plan 6.6); this spec has 19")

    def test_lane_a_with_20_criteria_passes(self):
        self.add_criteria(20)
        self.assertPasses(self.run_check(PCP, "pcp", repo=False))

    def test_lane_b_has_no_floor(self):
        self.assertIn("**AC-2**", self.read(PCP))
        self.assertNotIn("**AC-3**", self.read(PCP))
        self.assertPasses(self.run_check(PCP, "pcp"))


class ScenarioFileTests(SpecCheckCase):
    def test_unresolved_id_fails_with_repo(self):
        self.edit(LCP, "| AC-3 | ui-follow-up-view-01 |", "| AC-3 | ui-follow-up-view-02 |")
        self.assertFailsOn(self.run_check(), "scenario", "scenario ID ui-follow-up-view-02 (AC-3) resolves to no file under tests/")

    def test_unresolved_id_is_not_checked_without_repo(self):
        self.edit(LCP, "| AC-3 | ui-follow-up-view-01 |", "| AC-3 | ui-follow-up-view-02 |")
        self.assertPasses(self.run_check(repo=False))

    def test_id_with_extensions_resolves(self):
        # ui-follow-up-view-01 resolves to tests/acceptance/ui/ui-follow-up-view-01.spec.ts.
        self.assertTrue((self.repo / "tests/acceptance/ui/ui-follow-up-view-01.spec.ts").is_file())
        self.assertPasses(self.run_check())

    def test_id_that_only_starts_the_same_does_not_resolve(self):
        self.edit(LCP, "| AC-3 | ui-follow-up-view-01 |", "| AC-3 | ui-follow-up-view |")
        self.assertFailsOn(self.run_check(), "scenario")

    def test_path_id_resolves(self):
        self.edit(LCP, "| AC-3 | ui-follow-up-view-01 |", "| AC-3 | tests/acceptance/ui/ui-follow-up-view-01.spec.ts |")
        self.assertPasses(self.run_check())

    def test_path_outside_tests_fails(self):
        self.edit(LCP, "| AC-3 | ui-follow-up-view-01 |", "| AC-3 | tests/../specs/90101-order-follow-up/spec.md |")
        self.assertFailsOn(self.run_check(), "scenario")

    def test_no_tests_folder_fails(self):
        shutil.rmtree(self.repo / "tests")
        self.assertFailsOn(self.run_check(), "scenario", "no tests/ folder")

    def test_repo_that_is_not_a_folder_fails(self):
        self.assertFailsOn(self.run_check(repo=False, extra=("--repo", "nowhere")), "scenario", "--repo is not a folder")


class DesignLeakTests(SpecCheckCase):
    def assertWarnsOnly(self, result, text):
        self.assertPasses(result, warnings=1)
        self.assertEqual(result.warns, ["design-leak"], result.out)
        self.assertIn(text, result.out)

    def test_file_layout_warns_only(self):
        self.edit(LCP, "should contact the customer.\n", "should contact the customer. The flow is saved in src/Workflows/SetFollowUp.json.\n")
        self.assertWarnsOnly(self.run_check(), "names a file layout")

    def test_schema_name_warns_only(self):
        self.edit(LCP, "MUST set an open order's follow-up date", "MUST set `smpl_followupdate`")
        self.assertWarnsOnly(self.run_check(), "names a schema name")

    def test_schema_warns_only(self):
        self.edit(LCP, "- **Order**: a customer's order", "- **Order**: a table with a PRIMARY KEY on order number, a customer's order")
        self.assertWarnsOnly(self.run_check(), "names a schema")

    def test_library_warns_only(self):
        self.edit(PCP, "oldest first.\n\n**Why", "oldest first, on a page built in React.\n\n**Why")
        self.assertWarnsOnly(self.run_check(PCP, "pcp"), "names a library")

    def test_installed_package_warns_only(self):
        self.edit(PCP, "- **FR-002**:", "- **FR-002**: Run `npm install csv-writer@1.6.0` first.\n- **FR-003**:")
        self.assertWarnsOnly(self.run_check(PCP, "pcp"), "names a library")

    def test_code_block_warns_only(self):
        self.edit(PCP, "## Success Criteria", "```sql\nSELECT number FROM orders WHERE shipped IS NULL\n```\n\n## Success Criteria")
        self.assertWarnsOnly(self.run_check(PCP, "pcp"), "a code block outside Constraints")

    def test_design_in_constraints_and_low_code_fields_does_not_warn(self):
        lcp = self.read(LCP)
        self.assertIn("in `src/Entities/smpl_order/`", lcp[lcp.index("## Constraints"):lcp.index("## Low-Code Fields")])
        self.assertIn("Column `smpl_followupdate`", lcp[lcp.index("## Low-Code Fields"):])
        self.assertIn("writes `exports/open-orders.csv`", self.read(PCP))
        self.assertPasses(self.run_check())
        self.assertPasses(self.run_check(PCP, "pcp"))

    def test_links_do_not_warn(self):
        self.edit(LCP, "**Why this priority**: Orders go quiet",
                  "**Why this priority**: See [the sales notes](https://example.com/sales/notes/follow-up.html). Orders go quiet")
        self.assertPasses(self.run_check())


class CommandLineTests(SpecCheckCase):
    def test_missing_spec_file_fails(self):
        self.assertFailsOn(self.run_check("specs/90101-order-follow-up/nope.md"), "spec", "no such spec file")

    def test_invalid_profile_exits_1(self):
        result = self.run_check(profile="code")
        self.assertEqual(result.code, 1, result.out)
        self.assertIn("invalid choice", result.out)

    def test_missing_argument_exits_1(self):
        proc = subprocess.run([sys.executable, "-I", str(SCRIPT), "--profile", "lcp"], cwd=self.repo, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("--spec", proc.stderr)


@unittest.skipUnless(MANIFESTOS.is_dir(), "factory-manifestos is not staged beside this folder (after DG8 the gate's CI job checks the vendored copy, ADO 2538)")
class StagedCopyTests(SpecCheckCase):
    """While both are staged in the planning repo (D1), the two copies cannot drift."""

    def test_extension_copy_is_byte_identical(self):
        self.assertTrue(EXTENSION_COPY.is_file(), f"missing: {EXTENSION_COPY}")
        gate = hashlib.sha256(SCRIPT.read_bytes()).hexdigest()
        extension = hashlib.sha256(EXTENSION_COPY.read_bytes()).hexdigest()
        self.assertEqual(gate, extension, "the extension's check_spec.py differs from spec/check_spec.py; copy it again")

    def test_hook_command_runs_the_extension_copy(self):
        command = (EXTENSION / "commands" / "run.md").read_text(encoding="utf-8")
        self.assertIn("python3 -I .specify/extensions/getai-spec-check/scripts/check_spec.py", command)

    def test_low_code_fields_match_the_template(self):
        module_spec = importlib.util.spec_from_file_location("check_spec_module", SCRIPT)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        template = LCP_TEMPLATE.read_text(encoding="utf-8")
        headings = re.findall(r"^### (.+?)\s*$", template, re.MULTILINE)
        self.assertEqual(list(module.LCP_FIELDS), headings)

    def test_unfilled_template_fails(self):
        getai = GETAI_TEMPLATE.read_text(encoding="utf-8")
        lcp = LCP_TEMPLATE.read_text(encoding="utf-8")
        core = "# Feature Specification: [FEATURE NAME]\n"
        self.write("specs/90103-template/spec.md", getai.replace("{CORE_TEMPLATE}", core) + "\n" + lcp)
        result = self.run_check("specs/90103-template/spec.md")
        self.assertEqual(result.code, 1, result.out)
        self.assertLessEqual({"header", "ado-id", "design", "checklist", "nfr", "criteria", "lcp-field"}, set(result.fails), result.out)


if __name__ == "__main__":
    unittest.main()
