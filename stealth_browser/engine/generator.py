# -*- coding: utf-8 -*-
"""指纹配置生成器模块

Fingerprint configuration generator module.
生成、随机化和自定义指纹配置。
"""

import copy
import json
import random

from ..profiles.presets import PRESETS, get_preset
from ..fingerprints import (
    generate_canvas_fingerprint,
    generate_webgl_fingerprint,
    generate_audio_fingerprint,
    generate_font_fingerprint,
    generate_hardware_fingerprint,
    generate_network_fingerprint,
    generate_behavior_fingerprint,
    generate_storage_fingerprint,
    generate_screen_fingerprint,
    generate_timezone_fingerprint,
    generate_headers_fingerprint,
)
from ..utils.colors import Colors, ICON_OK, ICON_WARN


class FingerprintGenerator:
    """指纹配置生成器

    Fingerprint configuration generator.
    支持从预设模板生成、随机化生成和自定义参数生成。
    Supports generation from presets, randomization, and custom parameters.
    """

    def __init__(self):
        """初始化生成器

        Initialize generator.
        """
        self._config = {}

    def from_preset(self, preset_name, randomize=False, seed=None):
        """从预设模板生成指纹配置

        Generate fingerprint configuration from preset template.

        Args:
            preset_name (str): 预设名称 / Preset name
            randomize (bool): 是否随机化 / Whether to randomize
            seed (int, optional): 随机种子 / Random seed

        Returns:
            dict: 指纹配置 / Fingerprint configuration
        """
        preset = get_preset(preset_name)
        if not preset:
            raise ValueError(f"未知预设: {preset_name}。可用预设: {', '.join(PRESETS.keys())}")

        self._config = copy.deepcopy(preset)

        if randomize:
            self._config = self._randomize_config(self._config, seed)

        return self._config

    def random(self, device_type="desktop", seed=None):
        """随机生成指纹配置

        Randomly generate fingerprint configuration.

        Args:
            device_type (str): 设备类型 / Device type
            seed (int, optional): 随机种子 / Random seed

        Returns:
            dict: 指纹配置 / Fingerprint configuration
        """
        if seed is not None:
            random.seed(seed)

        self._config = {
            "canvas": generate_canvas_fingerprint(seed=seed),
            "webgl": generate_webgl_fingerprint(device_type=device_type, seed=seed),
            "audio": generate_audio_fingerprint(seed=seed),
            "fonts": generate_font_fingerprint(
                os_type=self._get_os_type(device_type), seed=seed
            ),
            "hardware": generate_hardware_fingerprint(device_type=device_type, seed=seed),
            "screen": generate_screen_fingerprint(device_type=device_type, seed=seed),
            "timezone": generate_timezone_fingerprint(seed=seed),
            "headers": generate_headers_fingerprint(
                browser_type=self._get_browser_type(device_type), seed=seed
            ),
            "storage": generate_storage_fingerprint(seed=seed),
            "network": generate_network_fingerprint(seed=seed),
            "behavior": generate_behavior_fingerprint(device_type=device_type, seed=seed),
        }

        return self._config

    def custom(self, base_preset=None, overrides=None):
        """自定义生成指纹配置

        Custom generate fingerprint configuration.

        Args:
            base_preset (str, optional): 基础预设名称 / Base preset name
            overrides (dict, optional): 覆盖参数 / Override parameters

        Returns:
            dict: 指纹配置 / Fingerprint configuration
        """
        if base_preset:
            self._config = copy.deepcopy(get_preset(base_preset) or {})
        else:
            self._config = {}

        if overrides:
            self._apply_overrides(self._config, overrides)

        return self._config

    def _apply_overrides(self, config, overrides):
        """递归应用覆盖参数

        Recursively apply override parameters.

        Args:
            config (dict): 配置字典 / Configuration dict
            overrides (dict): 覆盖参数 / Override parameters
        """
        for key, value in overrides.items():
            if isinstance(value, dict) and key in config and isinstance(config[key], dict):
                self._apply_overrides(config[key], value)
            else:
                config[key] = value

    def _randomize_config(self, config, seed=None):
        """随机化配置

        Randomize configuration.

        Args:
            config (dict): 原始配置 / Original configuration
            seed (int, optional): 随机种子 / Random seed

        Returns:
            dict: 随机化后的配置 / Randomized configuration
        """
        if seed is not None:
            random.seed(seed)

        # 随机化Canvas指纹 / Randomize Canvas fingerprint
        if "canvas" in config:
            config["canvas"] = generate_canvas_fingerprint(seed=seed)

        # 随机化WebGL指纹 / Randomize WebGL fingerprint
        if "webgl" in config:
            device_type = config.get("webgl", {}).get("device_type", "desktop")
            config["webgl"] = generate_webgl_fingerprint(device_type=device_type, seed=seed)

        # 随机化Audio指纹 / Randomize Audio fingerprint
        if "audio" in config:
            config["audio"] = generate_audio_fingerprint(seed=seed)

        # 随机化字体 / Randomize fonts
        if "fonts" in config:
            os_type = config.get("fonts", {}).get("os_type", "windows")
            config["fonts"] = generate_font_fingerprint(os_type=os_type, seed=seed)

        # 随机化硬件 / Randomize hardware
        if "hardware" in config:
            device_type = config.get("hardware", {}).get("device_type", "desktop")
            config["hardware"] = generate_hardware_fingerprint(device_type=device_type, seed=seed)

        # 随机化屏幕 / Randomize screen
        if "screen" in config:
            device_type = config.get("screen", {}).get("device_type", "desktop")
            config["screen"] = generate_screen_fingerprint(device_type=device_type, seed=seed)

        # 随机化时区 / Randomize timezone
        if "timezone" in config:
            config["timezone"] = generate_timezone_fingerprint(seed=seed)

        # 随机化HTTP头 / Randomize headers
        if "headers" in config:
            browser_type = config.get("headers", {}).get("browser_type", "chrome_desktop")
            config["headers"] = generate_headers_fingerprint(browser_type=browser_type, seed=seed)

        # 随机化存储 / Randomize storage
        if "storage" in config:
            config["storage"] = generate_storage_fingerprint(seed=seed)

        # 随机化网络 / Randomize network
        if "network" in config:
            config["network"] = generate_network_fingerprint(seed=seed)

        # 随机化行为 / Randomize behavior
        if "behavior" in config:
            device_type = config.get("behavior", {}).get("device_type", "desktop")
            config["behavior"] = generate_behavior_fingerprint(device_type=device_type, seed=seed)

        return config

    def _get_os_type(self, device_type):
        """根据设备类型获取OS类型

        Get OS type based on device type.

        Args:
            device_type (str): 设备类型 / Device type

        Returns:
            str: OS类型 / OS type
        """
        if device_type == "mobile":
            return random.choice(["android", "ios"])
        return random.choice(["windows", "macos", "linux"])

    def _get_browser_type(self, device_type):
        """根据设备类型获取浏览器类型

        Get browser type based on device type.

        Args:
            device_type (str): 设备类型 / Device type

        Returns:
            str: 浏览器类型 / Browser type
        """
        if device_type == "mobile":
            return random.choice(["chrome_mobile", "safari_mobile"])
        return random.choice(["chrome_desktop", "firefox_desktop"])

    def get_config(self):
        """获取当前配置

        Get current configuration.

        Returns:
            dict: 指纹配置 / Fingerprint configuration
        """
        return self._config

    def to_dict(self):
        """导出为字典

        Export as dictionary.

        Returns:
            dict: 指纹配置字典 / Fingerprint configuration dict
        """
        return copy.deepcopy(self._config)

    def to_json(self, indent=2):
        """导出为JSON字符串

        Export as JSON string.

        Args:
            indent (int): 缩进级别 / Indent level

        Returns:
            str: JSON字符串 / JSON string
        """
        return json.dumps(self._config, indent=indent, ensure_ascii=False, default=str)

    def list_presets(self):
        """列出所有可用预设

        List all available presets.

        Returns:
            list: 预设名称列表 / Preset name list
        """
        return list(PRESETS.keys())

    def compare_configs(self, config_a, config_b):
        """对比两个指纹配置

        Compare two fingerprint configurations.

        Args:
            config_a (dict): 配置A / Configuration A
            config_b (dict): 配置B / Configuration B

        Returns:
            dict: 对比结果 / Comparison results
        """
        if not config_a or not config_b:
            return {"error": "无效的配置数据"}

        results = {}
        all_dimensions = set(list(config_a.keys()) + list(config_b.keys()))

        for dim in all_dimensions:
            data_a = config_a.get(dim, {})
            data_b = config_b.get(dim, {})

            if isinstance(data_a, dict) and isinstance(data_b, dict):
                # 对比哈希值 / Compare hash values
                hash_a = data_a.get("hash", "")
                hash_b = data_b.get("hash", "")
                if hash_a and hash_b:
                    results[dim] = {
                        "hash_match": hash_a == hash_b,
                        "hash_a": hash_a[:16] + "...",
                        "hash_b": hash_b[:16] + "...",
                    }
                else:
                    # 对比关键字段 / Compare key fields
                    common_keys = set(data_a.keys()) & set(data_b.keys())
                    matches = sum(1 for k in common_keys if data_a[k] == data_b[k])
                    total = len(common_keys)
                    similarity = matches / total if total > 0 else 0
                    results[dim] = {
                        "field_matches": matches,
                        "total_fields": total,
                        "similarity": round(similarity, 4),
                    }

        return results
