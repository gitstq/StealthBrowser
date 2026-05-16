# -*- coding: utf-8 -*-
"""指纹采集器测试

Fingerprint collector tests.
"""

import sys
import os
import unittest

# 将父目录添加到路径 / Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stealth_browser.engine.collector import FingerprintCollector


class TestFingerprintCollector(unittest.TestCase):
    """指纹采集器测试类

    Fingerprint collector test class.
    """

    def test_init_default(self):
        """测试默认初始化

        Test default initialization.
        """
        collector = FingerprintCollector()
        self.assertEqual(collector.device_type, "desktop")
        self.assertEqual(collector.os_type, "windows")
        self.assertEqual(collector.locale, "zh-CN")
        self.assertIsNone(collector.seed)

    def test_init_custom(self):
        """测试自定义初始化

        Test custom initialization.
        """
        collector = FingerprintCollector(
            device_type="mobile",
            os_type="android",
            locale="en-US",
            seed=42,
        )
        self.assertEqual(collector.device_type, "mobile")
        self.assertEqual(collector.os_type, "android")
        self.assertEqual(collector.locale, "en-US")
        self.assertEqual(collector.seed, 42)

    def test_collect_all_desktop(self):
        """测试桌面端指纹采集

        Test desktop fingerprint collection.
        """
        collector = FingerprintCollector(device_type="desktop", seed=42)
        data = collector.collect_all(verbose=False)

        # 验证所有维度都被采集 / Verify all dimensions are collected
        self.assertIn("canvas", data)
        self.assertIn("webgl", data)
        self.assertIn("audio", data)
        self.assertIn("fonts", data)
        self.assertIn("hardware", data)
        self.assertIn("screen", data)
        self.assertIn("timezone", data)
        self.assertIn("headers", data)
        self.assertIn("storage", data)
        self.assertIn("network", data)
        self.assertIn("behavior", data)

    def test_collect_all_mobile(self):
        """测试移动端指纹采集

        Test mobile fingerprint collection.
        """
        collector = FingerprintCollector(device_type="mobile", seed=42)
        data = collector.collect_all(verbose=False)

        self.assertIn("canvas", data)
        self.assertIn("webgl", data)

    def test_collect_deterministic(self):
        """测试相同种子产生相同结果

        Test same seed produces same results.
        """
        collector_a = FingerprintCollector(seed=12345)
        data_a = collector_a.collect_all(verbose=False)

        collector_b = FingerprintCollector(seed=12345)
        data_b = collector_b.collect_all(verbose=False)

        # Canvas哈希应该相同 / Canvas hash should be the same
        self.assertEqual(data_a["canvas"]["hash"], data_b["canvas"]["hash"])

    def test_dimension_count(self):
        """测试维度数量

        Test dimension count.
        """
        collector = FingerprintCollector(seed=42)
        collector.collect_all(verbose=False)

        self.assertEqual(collector.get_dimension_count(), 11)

    def test_total_data_points(self):
        """测试总数据点数量

        Test total data point count.
        """
        collector = FingerprintCollector(seed=42)
        collector.collect_all(verbose=False)

        total = collector.get_total_data_points()
        self.assertGreater(total, 50)  # 至少50个数据点 / At least 50 data points

    def test_collection_summary(self):
        """测试采集摘要

        Test collection summary.
        """
        collector = FingerprintCollector(seed=42)
        collector.collect_all(verbose=False)

        summary = collector.get_collection_summary()
        self.assertEqual(summary["dimensions_collected"], 11)
        self.assertEqual(summary["total_dimensions"], 11)
        self.assertGreater(summary["total_data_points"], 0)
        self.assertGreater(summary["collection_time"], 0)

    def test_canvas_data_structure(self):
        """测试Canvas数据结构

        Test Canvas data structure.
        """
        collector = FingerprintCollector(seed=42)
        data = collector.collect_all(verbose=False)

        canvas = data["canvas"]
        self.assertIn("hash", canvas)
        self.assertIn("hash_algorithm", canvas)
        self.assertIn("render_text", canvas)
        self.assertIn("font_size", canvas)
        self.assertIn("font_family", canvas)
        self.assertIn("canvas_width", canvas)
        self.assertIn("canvas_height", canvas)
        self.assertEqual(len(canvas["hash"]), 32)  # MD5哈希长度 / MD5 hash length

    def test_webgl_data_structure(self):
        """测试WebGL数据结构

        Test WebGL data structure.
        """
        collector = FingerprintCollector(seed=42)
        data = collector.collect_all(verbose=False)

        webgl = data["webgl"]
        self.assertIn("renderer", webgl)
        self.assertIn("vendor", webgl)
        self.assertIn("extensions", webgl)
        self.assertIn("hash", webgl)
        self.assertIsInstance(webgl["extensions"], list)
        self.assertGreater(len(webgl["extensions"]), 0)

    def test_headers_data_structure(self):
        """测试HTTP头数据结构

        Test HTTP headers data structure.
        """
        collector = FingerprintCollector(seed=42)
        data = collector.collect_all(verbose=False)

        headers = data["headers"]
        self.assertIn("user_agent", headers)
        self.assertIn("headers", headers)
        self.assertIn("tls", headers)
        self.assertIn("ua_info", headers)
        self.assertIsInstance(headers["headers"], dict)
        self.assertIsInstance(headers["tls"], dict)


if __name__ == "__main__":
    unittest.main()
