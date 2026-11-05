"""Tests for tool-fallback-cascade."""
import unittest
from tool_fallback_cascade.cascade import FallbackCascade


class TestFallbackCascade(unittest.TestCase):
    def setUp(self):
        self.cascade = FallbackCascade("test")

    def test_fallback_progression(self):
        self.cascade.add_handler("h1", lambda: 1 / 0)
        self.cascade.add_handler("h2", lambda: "recovered")
        res = self.cascade.execute()
        self.assertTrue(res["success"])
        self.assertEqual(res["handler_used"], "h2")
        self.assertTrue(res["degraded"])
        self.assertEqual(len(res["prior_errors"]), 1)


if __name__ == "__main__":
    unittest.main()
