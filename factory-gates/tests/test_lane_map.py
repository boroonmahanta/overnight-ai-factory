import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "gate" / "lcp"))
from lane_map import LaneError, map_branch  # noqa: E402

ALLOWED = "fl1 fl2 fl3"


class LaneMapTests(unittest.TestCase):
    def test_agent_branch_maps_to_lane_and_story(self):
        self.assertEqual(map_branch("agent/fl2/48213-1", ALLOWED), ("fl2", "48213"))

    def test_human_branch_maps_to_none(self):
        self.assertEqual(map_branch("feature/new-form", ALLOWED), ("none", "none"))

    def test_main_and_release_map_to_none(self):
        self.assertEqual(map_branch("main", ALLOWED), ("none", "none"))
        self.assertEqual(map_branch("release", ALLOWED), ("none", "none"))

    def test_unknown_lane_fails(self):
        with self.assertRaises(LaneError):
            map_branch("agent/fl9/48213-1", ALLOWED)

    def test_empty_allowed_list_fails_every_agent_branch(self):
        with self.assertRaises(LaneError):
            map_branch("agent/fl1/1-1", "")

    def test_lane_must_match_whole_word(self):
        # fl1 is allowed; fl10 must not match by prefix.
        with self.assertRaises(LaneError):
            map_branch("agent/fl10/1-1", "fl1")

    def test_malformed_agent_branches_are_not_agent_branches(self):
        for ref in ("agent/fl1/abc-1", "agent/fl1/12", "agent/fl1/12-1/extra", "xagent/fl1/12-1", "agent/fl1/12-1\n"):
            self.assertEqual(map_branch(ref, ALLOWED), ("none", "none"), ref)


if __name__ == "__main__":
    unittest.main()
