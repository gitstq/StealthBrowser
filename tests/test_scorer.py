# -*- coding: utf-8 -*-
"""反检测评分引擎测试

Anti-detection scoring engine tests.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stealth_browser.engine.collector import FingerprintCollector
from stealth_browser.engine.analyzer import FingerprintAnalyzer
from stealth_browser.engine.scorer import AntiDetectScorer


class TestAntiDetectScorer(unittest.TestCase):
    """反检测评分引擎测试类

    Anti-detection scoring engine test class.
    """

    def setUp(self):
        """测试前置设置

        Test setup.
        """
        collector = FingerprintCollector(seed=42)
        self.fingerprint_data = collector.collect_all(verbose=False)

        analyzer = FingerprintAnalyzer(self.fingerprint_data)
        self.analysis_results = analyzer.analyze_all(verbose=False)

        self.scorer = AntiDetectScorer(self.fingerprint_data, self.analysis_results)

    def test_score(self):
        """测试评分功能

        Test scoring.
        """
        results = self.scorer.score(verbose=False)

        self.assertIn("total_score", results)
        self.assertIn("max_score", results)
        self.assertIn("dimensions", results)
        self.assertIn("grade", results)

    def test_total_score_range(self):
        """测试总分范围

        Test total score range.
        """
        results = self.scorer.score(verbose=False)

        self.assertGreaterEqual(results["total_score"], 0)
        self.assertLessEqual(results["total_score"], 100)
        self.assertEqual(results["max_score"], 100)

    def test_dimension_scores(self):
        """测试各维度评分

        Test dimension scores.
        """
        results = self.scorer.score(verbose=False)
        dimensions = results["dimensions"]

        self.assertIn("randomization", dimensions)
        self.assertIn("consistency", dimensions)
        self.assertIn("behavior", dimensions)
        self.assertIn("network", dimensions)

        for dim_name, dim_data in dimensions.items():
            self.assertIn("score", dim_data)
            self.assertIn("max_score", dim_data)
            self.assertGreaterEqual(dim_data["score"], 0)
            self.assertLessEqual(dim_data["score"], dim_data["max_score"])

    def test_grade(self):
        """测试评分等级

        Test score grade.
        """
        results = self.scorer.score(verbose=False)
        grade = results["grade"]

        self.assertIn(grade, ["excellent", "good", "average", "poor", "critical"])

    def test_empty_data(self):
        """测试空数据评分

        Test scoring with empty data.
        """
        scorer = AntiDetectScorer()
        results = scorer.score(verbose=False)

        self.assertIn("error", results)

    def test_set_data(self):
        """测试设置数据

        Test setting data.
        """
        scorer = AntiDetectScorer()
        scorer.set_data(self.fingerprint_data, self.analysis_results)
        results = scorer.score(verbose=False)

        self.assertNotIn("error", results)

    def test_suggestions(self):
        """测试改进建议

        Test improvement suggestions.
        """
        results = self.scorer.score(verbose=False)

        self.assertIn("suggestions", results)
        self.assertIsInstance(results["suggestions"], list)

    def test_dimension_details(self):
        """测试维度详情

        Test dimension details.
        """
        results = self.scorer.score(verbose=False)
        dimensions = results["dimensions"]

        for dim_name, dim_data in dimensions.items():
            self.assertIn("details", dim_data)
            self.assertIsInstance(dim_data["details"], list)


if __name__ == "__main__":
    unittest.main()
