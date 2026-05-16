# -*- coding: utf-8 -*-
"""指纹分析器测试

Fingerprint analyzer tests.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stealth_browser.engine.collector import FingerprintCollector
from stealth_browser.engine.analyzer import FingerprintAnalyzer
from stealth_browser.utils.entropy import shannon_entropy, normalized_entropy, hash_entropy


class TestFingerprintAnalyzer(unittest.TestCase):
    """指纹分析器测试类

    Fingerprint analyzer test class.
    """

    def setUp(self):
        """测试前置设置

        Test setup.
        """
        collector = FingerprintCollector(seed=42)
        self.fingerprint_data = collector.collect_all(verbose=False)
        self.analyzer = FingerprintAnalyzer(self.fingerprint_data)

    def test_analyze_all(self):
        """测试全部分析

        Test full analysis.
        """
        results = self.analyzer.analyze_all(verbose=False)

        self.assertIn("uniqueness", results)
        self.assertIn("entropy", results)
        self.assertIn("consistency", results)
        self.assertIn("anomalies", results)

    def test_uniqueness_analysis(self):
        """测试唯一性分析

        Test uniqueness analysis.
        """
        results = self.analyzer.analyze_all(verbose=False)
        uniqueness = results["uniqueness"]

        self.assertIn("_summary", uniqueness)
        summary = uniqueness["_summary"]
        self.assertIn("uniqueness_score", summary)
        self.assertGreaterEqual(summary["uniqueness_score"], 0)
        self.assertLessEqual(summary["uniqueness_score"], 100)

    def test_entropy_analysis(self):
        """测试熵值分析

        Test entropy analysis.
        """
        results = self.analyzer.analyze_all(verbose=False)
        entropy = results["entropy"]

        # 至少应该有canvas维度的熵值 / Should have at least canvas dimension entropy
        self.assertIn("canvas", entropy)
        canvas_entropy = entropy["canvas"]
        self.assertIn("total_entropy", canvas_entropy)
        self.assertIn("data_points", canvas_entropy)
        self.assertIn("average_entropy", canvas_entropy)
        self.assertIn("classification", canvas_entropy)
        self.assertIn(canvas_entropy["classification"], ["high", "medium", "low"])

    def test_consistency_analysis(self):
        """测试一致性分析

        Test consistency analysis.
        """
        results = self.analyzer.analyze_all(verbose=False)
        consistency = results["consistency"]

        self.assertIn("consistency_score", consistency)
        self.assertIn("inconsistencies", consistency)
        self.assertIn("is_consistent", consistency)
        self.assertGreaterEqual(consistency["consistency_score"], 0)
        self.assertLessEqual(consistency["consistency_score"], 100)

    def test_anomaly_detection(self):
        """测试异常检测

        Test anomaly detection.
        """
        results = self.analyzer.analyze_all(verbose=False)
        anomalies = results["anomalies"]

        self.assertIn("anomaly_count", anomalies)
        self.assertIn("anomalies", anomalies)
        self.assertIn("has_critical", anomalies)
        self.assertIn("has_anomalies", anomalies)
        self.assertGreaterEqual(anomalies["anomaly_count"], 0)

    def test_empty_data(self):
        """测试空数据处理

        Test empty data handling.
        """
        analyzer = FingerprintAnalyzer()
        results = analyzer.analyze_all(verbose=False)

        self.assertIn("error", results)

    def test_set_fingerprint(self):
        """测试设置指纹数据

        Test setting fingerprint data.
        """
        analyzer = FingerprintAnalyzer()
        analyzer.set_fingerprint(self.fingerprint_data)
        results = analyzer.analyze_all(verbose=False)

        self.assertNotIn("error", results)

    def test_get_results(self):
        """测试获取结果

        Test getting results.
        """
        self.analyzer.analyze_all(verbose=False)
        results = self.analyzer.get_results()

        self.assertIsInstance(results, dict)
        self.assertIn("uniqueness", results)


class TestEntropyFunctions(unittest.TestCase):
    """熵值计算函数测试类

    Entropy calculation function test class.
    """

    def test_shannon_entropy_empty(self):
        """测试空数据熵值

        Test empty data entropy.
        """
        self.assertEqual(shannon_entropy([]), 0.0)
        self.assertEqual(shannon_entropy(""), 0.0)

    def test_shannon_entropy_uniform(self):
        """测试均匀分布熵值

        Test uniform distribution entropy.
        """
        # 完全均匀分布的熵 = log2(n) / Entropy of uniform distribution = log2(n)
        import math
        data = list("abcd")
        expected = math.log2(4)  # 2.0
        result = shannon_entropy(data)
        self.assertAlmostEqual(result, expected, places=4)

    def test_shannon_entropy_single(self):
        """测试单一值熵值

        Test single value entropy.
        """
        self.assertEqual(shannon_entropy("aaaa"), 0.0)
        self.assertEqual(shannon_entropy([1, 1, 1]), 0.0)

    def test_normalized_entropy(self):
        """测试归一化熵值

        Test normalized entropy.
        """
        data = list("abcd")
        result = normalized_entropy(data)
        self.assertAlmostEqual(result, 1.0, places=4)

    def test_hash_entropy(self):
        """测试哈希熵值

        Test hash entropy.
        """
        hash_val = "a1b2c3d4e5f6789012345678abcdef0"
        result = hash_entropy(hash_val)
        self.assertGreater(result, 0.0)

    def test_hash_entropy_empty(self):
        """测试空哈希熵值

        Test empty hash entropy.
        """
        self.assertEqual(hash_entropy(""), 0.0)


if __name__ == "__main__":
    unittest.main()
