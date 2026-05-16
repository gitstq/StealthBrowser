# -*- coding: utf-8 -*-
"""指纹配置生成器测试

Fingerprint configuration generator tests.
"""

import sys
import os
import json
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stealth_browser.engine.generator import FingerprintGenerator
from stealth_browser.profiles.presets import PRESETS, get_preset, list_presets


class TestFingerprintGenerator(unittest.TestCase):
    """指纹配置生成器测试类

    Fingerprint generator test class.
    """

    def setUp(self):
        """测试前置设置

        Test setup.
        """
        self.generator = FingerprintGenerator()

    def test_from_preset_desktop_chrome(self):
        """测试Chrome桌面版预设

        Test desktop Chrome preset.
        """
        config = self.generator.from_preset("desktop_chrome")

        self.assertIsInstance(config, dict)
        self.assertIn("canvas", config)
        self.assertIn("webgl", config)
        self.assertIn("headers", config)

    def test_from_preset_mobile_safari(self):
        """测试iOS Safari预设

        Test mobile Safari preset.
        """
        config = self.generator.from_preset("mobile_safari")

        self.assertIsInstance(config, dict)
        self.assertIn("canvas", config)

    def test_from_preset_invalid(self):
        """测试无效预设

        Test invalid preset.
        """
        with self.assertRaises(ValueError):
            self.generator.from_preset("nonexistent_preset")

    def test_from_preset_randomize(self):
        """测试预设随机化

        Test preset randomization.
        """
        config_a = self.generator.from_preset("desktop_chrome", randomize=False, seed=42)
        config_b = self.generator.from_preset("desktop_chrome", randomize=False, seed=42)

        # 相同种子不随机化应该相同 / Same seed without randomization should be same
        self.assertEqual(config_a["canvas"]["hash"], config_b["canvas"]["hash"])

        config_c = self.generator.from_preset("desktop_chrome", randomize=True, seed=99)
        # 不同种子随机化应该不同 / Different seed with randomization should differ
        # 注意：不保证一定不同，但概率极低 / Note: not guaranteed, but extremely unlikely
        self.assertIsInstance(config_c, dict)

    def test_random_desktop(self):
        """测试随机生成桌面配置

        Test random desktop configuration generation.
        """
        config = self.generator.random(device_type="desktop", seed=42)

        self.assertIsInstance(config, dict)
        self.assertIn("canvas", config)
        self.assertIn("webgl", config)
        self.assertIn("audio", config)
        self.assertIn("fonts", config)
        self.assertIn("hardware", config)
        self.assertIn("screen", config)
        self.assertIn("timezone", config)
        self.assertIn("headers", config)
        self.assertIn("storage", config)
        self.assertIn("network", config)
        self.assertIn("behavior", config)

    def test_random_mobile(self):
        """测试随机生成移动配置

        Test random mobile configuration generation.
        """
        config = self.generator.random(device_type="mobile", seed=42)

        self.assertIsInstance(config, dict)
        self.assertIn("canvas", config)

    def test_custom_with_overrides(self):
        """测试自定义配置覆盖

        Test custom configuration with overrides.
        """
        config = self.generator.custom(
            base_preset="desktop_chrome",
            overrides={
                "canvas": {"hash": "custom_hash_value_12345678"},
            },
        )

        self.assertEqual(config["canvas"]["hash"], "custom_hash_value_12345678")

    def test_custom_without_base(self):
        """测试无基础预设的自定义配置

        Test custom configuration without base preset.
        """
        config = self.generator.custom(overrides={"test_key": "test_value"})

        self.assertIsInstance(config, dict)
        self.assertEqual(config.get("test_key"), "test_value")

    def test_get_config(self):
        """测试获取配置

        Test getting configuration.
        """
        self.generator.from_preset("desktop_chrome")
        config = self.generator.get_config()

        self.assertIsInstance(config, dict)
        self.assertIn("canvas", config)

    def test_to_dict(self):
        """测试导出为字典

        Test export to dictionary.
        """
        self.generator.from_preset("desktop_chrome")
        config_dict = self.generator.to_dict()

        self.assertIsInstance(config_dict, dict)
        # 确保是深拷贝 / Ensure it's a deep copy
        config_dict["canvas"]["hash"] = "modified"
        self.assertNotEqual(
            self.generator.get_config()["canvas"]["hash"],
            "modified",
        )

    def test_to_json(self):
        """测试导出为JSON

        Test export to JSON.
        """
        self.generator.from_preset("desktop_chrome")
        json_str = self.generator.to_json()

        self.assertIsInstance(json_str, str)
        # 验证是有效JSON / Verify it's valid JSON
        parsed = json.loads(json_str)
        self.assertIn("canvas", parsed)

    def test_compare_configs(self):
        """测试配置对比

        Test configuration comparison.
        """
        config_a = self.generator.from_preset("desktop_chrome", seed=42)
        config_b = self.generator.from_preset("desktop_firefox", seed=42)

        results = self.generator.compare_configs(config_a, config_b)

        self.assertIsInstance(results, dict)
        # 至少应该有canvas维度的对比 / Should have at least canvas comparison
        self.assertIn("canvas", results)

    def test_compare_same_config(self):
        """测试相同配置对比

        Test comparing same configuration.
        """
        config = self.generator.from_preset("desktop_chrome", seed=42)

        results = self.generator.compare_configs(config, config)

        self.assertIn("canvas", results)
        canvas_result = results["canvas"]
        self.assertTrue(canvas_result.get("hash_match", False))

    def test_list_presets(self):
        """测试列出预设

        Test listing presets.
        """
        presets = self.generator.list_presets()

        self.assertIsInstance(presets, list)
        self.assertIn("desktop_chrome", presets)
        self.assertIn("desktop_firefox", presets)
        self.assertIn("mobile_safari", presets)
        self.assertIn("mobile_chrome", presets)
        self.assertIn("bot_friendly", presets)
        self.assertIn("stealth_max", presets)

    def test_compare_empty_configs(self):
        """测试空配置对比

        Test comparing empty configurations.
        """
        results = self.generator.compare_configs({}, {"canvas": {"hash": "test"}})

        # 空配置A应该导致某些维度缺失 / Empty config A should cause missing dimensions
        self.assertIsInstance(results, dict)

    def test_compare_none_configs(self):
        """测试None配置对比

        Test comparing None configurations.
        """
        results = self.generator.compare_configs(None, None)

        self.assertIn("error", results)


class TestPresets(unittest.TestCase):
    """预设配置测试类

    Preset configuration test class.
    """

    def test_all_presets_valid(self):
        """测试所有预设都有效

        Test all presets are valid.
        """
        for name in PRESETS:
            config = get_preset(name)
            self.assertIsNotNone(config, f"预设 {name} 返回None")
            self.assertIsInstance(config, dict, f"预设 {name} 不是字典")

    def test_list_presets_info(self):
        """测试预设列表信息

        Test preset list info.
        """
        presets = list_presets()

        self.assertEqual(len(presets), len(PRESETS))
        for preset in presets:
            self.assertIn("name", preset)
            self.assertIn("display_name", preset)
            self.assertIn("description", preset)
            self.assertIn("device_type", preset)

    def test_stealth_max_config(self):
        """测试最大隐身配置

        Test maximum stealth configuration.
        """
        config = get_preset("stealth_max")

        self.assertIsNotNone(config)
        # 验证隐身特征 / Verify stealth features
        self.assertFalse(config["network"].get("webrtc_support", True))
        self.assertTrue(config["network"].get("doh_enabled", False))

    def test_bot_friendly_config(self):
        """测试爬虫友好配置

        Test bot-friendly configuration.
        """
        config = get_preset("bot_friendly")

        self.assertIsNotNone(config)
        self.assertEqual(config["network"].get("ip_type"), "residential")


if __name__ == "__main__":
    unittest.main()
