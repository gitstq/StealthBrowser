# -*- coding: utf-8 -*-
"""指纹采集器模块

Fingerprint collector module.
采集50+维度的浏览器指纹数据。
"""

import random
import time

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
from ..utils.colors import Colors, progress_bar, ICON_OK


class FingerprintCollector:
    """指纹采集器

    Fingerprint collector.
    负责采集所有维度的浏览器指纹数据。
    Collects browser fingerprint data across all dimensions.
    """

    # 所有可采集的维度 / All collectable dimensions
    DIMENSIONS = [
        "canvas", "webgl", "audio", "fonts", "hardware",
        "screen", "timezone", "headers", "storage",
        "network", "behavior",
    ]

    def __init__(self, device_type="desktop", os_type="windows", locale="zh-CN", seed=None):
        """初始化指纹采集器

        Initialize fingerprint collector.

        Args:
            device_type (str): 设备类型 desktop/mobile / Device type
            os_type (str): 操作系统类型 / OS type
            locale (str): 地区设置 / Locale setting
            seed (int, optional): 随机种子 / Random seed
        """
        self.device_type = device_type
        self.os_type = os_type
        self.locale = locale
        self.seed = seed
        self._collected_data = {}
        self._collection_time = 0

    def collect_all(self, verbose=True):
        """采集所有维度指纹

        Collect all dimension fingerprints.

        Args:
            verbose (bool): 是否显示进度 / Whether to show progress

        Returns:
            dict: 完整指纹数据 / Complete fingerprint data
        """
        start_time = time.time()

        if verbose:
            print(f"\n  {Colors.bold(Colors.cyan('正在采集浏览器指纹...'))}")
            print(f"  {Colors.DIM + '─' * 50 + Colors.RESET}")

        total = len(self.DIMENSIONS)
        for i, dimension in enumerate(self.DIMENSIONS):
            if verbose:
                bar = progress_bar(i, total, width=30, prefix="  ", suffix=f" {dimension}")
                print(bar, end="", flush=True)

            self._collected_data[dimension] = self._collect_dimension(dimension)

            if verbose:
                print(f"\r  {Colors.green(ICON_OK)} 采集完成: {dimension:<20s} "
                      f"({len(str(self._collected_data[dimension])):>6} bytes)")

        self._collection_time = round(time.time() - start_time, 3)

        if verbose:
            print(f"\r  {Colors.green(ICON_OK)} 采集完成: 全部维度{' ' * 14} "
                  f"({self._collection_time:.3f}s)")
            print(f"  {Colors.DIM + '─' * 50 + Colors.RESET}")

        return self._collected_data

    def _collect_dimension(self, dimension):
        """采集单个维度

        Collect a single dimension.

        Args:
            dimension (str): 维度名称 / Dimension name

        Returns:
            dict: 维度指纹数据 / Dimension fingerprint data
        """
        seed = self.seed
        if seed is not None:
            # 每个维度使用不同的种子偏移 / Use different seed offset per dimension
            dim_seed = seed + hash(dimension) % 100000
        else:
            dim_seed = None

        collectors = {
            "canvas": lambda: generate_canvas_fingerprint(seed=dim_seed),
            "webgl": lambda: generate_webgl_fingerprint(
                device_type=self.device_type, seed=dim_seed
            ),
            "audio": lambda: generate_audio_fingerprint(seed=dim_seed),
            "fonts": lambda: generate_font_fingerprint(
                os_type=self.os_type, seed=dim_seed
            ),
            "hardware": lambda: generate_hardware_fingerprint(
                device_type=self.device_type, seed=dim_seed
            ),
            "screen": lambda: generate_screen_fingerprint(
                device_type=self.device_type, seed=dim_seed
            ),
            "timezone": lambda: generate_timezone_fingerprint(
                locale=self.locale, seed=dim_seed
            ),
            "headers": lambda: generate_headers_fingerprint(
                browser_type=self._get_browser_type(), seed=dim_seed
            ),
            "storage": lambda: generate_storage_fingerprint(seed=dim_seed),
            "network": lambda: generate_network_fingerprint(seed=dim_seed),
            "behavior": lambda: generate_behavior_fingerprint(
                device_type=self.device_type, seed=dim_seed
            ),
        }

        collector = collectors.get(dimension)
        if collector:
            return collector()
        return {}

    def _get_browser_type(self):
        """根据设备类型获取浏览器类型

        Get browser type based on device type.

        Returns:
            str: 浏览器类型 / Browser type
        """
        if self.device_type == "mobile":
            return random.choice(["chrome_mobile", "safari_mobile"])
        return random.choice(["chrome_desktop", "firefox_desktop"])

    def get_collected_data(self):
        """获取已采集的数据

        Get collected data.

        Returns:
            dict: 已采集的指纹数据 / Collected fingerprint data
        """
        return self._collected_data

    def get_dimension_count(self):
        """获取已采集的维度数量

        Get number of collected dimensions.

        Returns:
            int: 维度数量 / Dimension count
        """
        return len(self._collected_data)

    def get_total_data_points(self):
        """获取总数据点数量

        Get total data point count.

        Returns:
            int: 总数据点数 / Total data point count
        """
        count = 0
        for dim_data in self._collected_data.values():
            count += self._count_data_points(dim_data)
        return count

    @staticmethod
    def _count_data_points(data, depth=0):
        """递归统计数据点

        Recursively count data points.

        Args:
            data: 数据 / Data
            depth (int): 递归深度 / Recursion depth

        Returns:
            int: 数据点数量 / Data point count
        """
        if depth > 10:
            return 1
        if isinstance(data, dict):
            return sum(FingerprintCollector._count_data_points(v, depth + 1) for v in data.values())
        elif isinstance(data, (list, tuple)):
            return sum(FingerprintCollector._count_data_points(item, depth + 1) for item in data)
        return 1

    def get_collection_summary(self):
        """获取采集摘要

        Get collection summary.

        Returns:
            dict: 采集摘要信息 / Collection summary
        """
        return {
            "dimensions_collected": len(self._collected_data),
            "total_dimensions": len(self.DIMENSIONS),
            "total_data_points": self.get_total_data_points(),
            "collection_time": self._collection_time,
            "device_type": self.device_type,
            "os_type": self.os_type,
            "locale": self.locale,
        }
