# -*- coding: utf-8 -*-
"""指纹分析器模块

Fingerprint analyzer module.
分析指纹的唯一性、熵值和异常特征。
"""

from ..utils.entropy import fingerprint_uniqueness_score, calculate_dimension_entropy
from ..utils.colors import Colors, print_table, ICON_OK, ICON_FAIL, ICON_WARN


class FingerprintAnalyzer:
    """指纹分析器

    Fingerprint analyzer.
    分析指纹数据的唯一性、熵值和异常特征。
    Analyzes uniqueness, entropy, and anomalies in fingerprint data.
    """

    def __init__(self, fingerprint_data=None):
        """初始化指纹分析器

        Initialize fingerprint analyzer.

        Args:
            fingerprint_data (dict, optional): 指纹数据 / Fingerprint data
        """
        self.fingerprint_data = fingerprint_data or {}
        self._analysis_results = {}

    def set_fingerprint(self, fingerprint_data):
        """设置指纹数据

        Set fingerprint data.

        Args:
            fingerprint_data (dict): 指纹数据 / Fingerprint data
        """
        self.fingerprint_data = fingerprint_data
        self._analysis_results = {}

    def analyze_all(self, verbose=True):
        """执行全部分析

        Run all analyses.

        Args:
            verbose (bool): 是否显示详细输出 / Whether to show verbose output

        Returns:
            dict: 完整分析结果 / Complete analysis results
        """
        if not self.fingerprint_data:
            return {"error": "未设置指纹数据"}

        if verbose:
            print(f"\n  {Colors.bold(Colors.cyan('正在分析指纹数据...'))}")
            print(f"  {Colors.DIM + '─' * 50 + Colors.RESET}")

        # 计算唯一性评分 / Calculate uniqueness score
        uniqueness = self._analyze_uniqueness(verbose)

        # 计算各维度熵值 / Calculate entropy per dimension
        entropy_analysis = self._analyze_entropy(verbose)

        # 跨浏览器一致性检查 / Cross-browser consistency check
        consistency = self._analyze_consistency(verbose)

        # 异常检测 / Anomaly detection
        anomalies = self._detect_anomalies(verbose)

        self._analysis_results = {
            "uniqueness": uniqueness,
            "entropy": entropy_analysis,
            "consistency": consistency,
            "anomalies": anomalies,
        }

        if verbose:
            print(f"  {Colors.green(ICON_OK)} 分析完成")
            print(f"  {Colors.DIM + '─' * 50 + Colors.RESET}")

        return self._analysis_results

    def _analyze_uniqueness(self, verbose=True):
        """分析指纹唯一性

        Analyze fingerprint uniqueness.

        Returns:
            dict: 唯一性分析结果 / Uniqueness analysis results
        """
        # 提取关键维度用于唯一性计算 / Extract key dimensions for uniqueness
        key_values = {}
        for dim_name, dim_data in self.fingerprint_data.items():
            if isinstance(dim_data, dict):
                # 提取哈希值或关键标识 / Extract hash or key identifier
                if "hash" in dim_data:
                    key_values[dim_name] = dim_data["hash"]
                elif "user_agent" in dim_data:
                    key_values[dim_name] = dim_data["user_agent"]
                elif "renderer" in dim_data:
                    key_values[dim_name] = dim_data["renderer"]
                elif "detected_fonts" in dim_data:
                    key_values[dim_name] = ",".join(dim_data["detected_fonts"][:10])
                elif "timezone" in dim_data:
                    key_values[dim_name] = dim_data["timezone"]
                else:
                    # 取第一个字符串值 / Take first string value
                    for v in dim_data.values():
                        if isinstance(v, str) and len(v) > 5:
                            key_values[dim_name] = v
                            break

        uniqueness = fingerprint_uniqueness_score(key_values)
        score = uniqueness.get("_summary", {}).get("uniqueness_score", 0)

        if verbose:
            print(f"  {Colors.green(ICON_OK)} 唯一性评分: {score:.1f}/100")

        return uniqueness

    def _analyze_entropy(self, verbose=True):
        """分析各维度熵值

        Analyze entropy per dimension.

        Returns:
            dict: 熵值分析结果 / Entropy analysis results
        """
        entropy_results = {}

        for dim_name, dim_data in self.fingerprint_data.items():
            if isinstance(dim_data, dict):
                # 计算整个维度的熵 / Calculate entropy for the whole dimension
                dim_entropy = 0.0
                data_points = 0
                for key, value in dim_data.items():
                    if isinstance(value, (str, list, tuple, int, float)):
                        e = calculate_dimension_entropy(value)
                        dim_entropy += e
                        data_points += 1

                avg_entropy = dim_entropy / data_points if data_points > 0 else 0
                entropy_results[dim_name] = {
                    "total_entropy": round(dim_entropy, 4),
                    "data_points": data_points,
                    "average_entropy": round(avg_entropy, 4),
                    "classification": self._classify_entropy(avg_entropy),
                }

        if verbose:
            rows = []
            for dim, data in entropy_results.items():
                cls = data["classification"]
                icon = ICON_OK if cls == "high" else (ICON_WARN if cls == "medium" else ICON_FAIL)
                rows.append([
                    f"  {icon} {dim}",
                    f"{data['data_points']}",
                    f"{data['average_entropy']:.2f}",
                    cls,
                ])
            print_table(
                ["维度", "数据点", "平均熵", "分类"],
                rows,
                col_widths=[22, 8, 10, 10],
                title="熵值分析",
            )

        return entropy_results

    def _classify_entropy(self, entropy):
        """分类熵值等级

        Classify entropy level.

        Args:
            entropy (float): 熵值 / Entropy value

        Returns:
            str: 等级 high/medium/low / Level
        """
        if entropy >= 3.0:
            return "high"
        elif entropy >= 1.5:
            return "medium"
        return "low"

    def _analyze_consistency(self, verbose=True):
        """分析跨浏览器一致性

        Analyze cross-browser consistency.

        Returns:
            dict: 一致性分析结果 / Consistency analysis results
        """
        inconsistencies = []

        # 检查设备类型一致性 / Check device type consistency
        device_types = set()
        for dim_name, dim_data in self.fingerprint_data.items():
            if isinstance(dim_data, dict) and "device_type" in dim_data:
                device_types.add(dim_data["device_type"])

        if len(device_types) > 1:
            inconsistencies.append({
                "type": "device_type_mismatch",
                "message": f"设备类型不一致: {', '.join(device_types)}",
                "severity": "high",
            })

        # 检查平台一致性 / Check platform consistency
        platforms = set()
        for dim_name, dim_data in self.fingerprint_data.items():
            if isinstance(dim_data, dict) and "platform" in dim_data:
                platforms.add(dim_data["platform"])

        if len(platforms) > 1:
            inconsistencies.append({
                "type": "platform_mismatch",
                "message": f"平台信息不一致: {', '.join(platforms)}",
                "severity": "high",
            })

        # 检查OS一致性 / Check OS consistency
        os_names = set()
        for dim_name, dim_data in self.fingerprint_data.items():
            if isinstance(dim_data, dict) and "os_name" in dim_data:
                os_names.add(dim_data["os_name"])

        if len(os_names) > 1:
            inconsistencies.append({
                "type": "os_mismatch",
                "message": f"操作系统不一致: {', '.join(os_names)}",
                "severity": "high",
            })

        # 检查UA与硬件一致性 / Check UA-hardware consistency
        headers = self.fingerprint_data.get("headers", {})
        hardware = self.fingerprint_data.get("hardware", {})
        ua_info = headers.get("ua_info", {}) if isinstance(headers, dict) else {}

        ua_os = ua_info.get("os", "")
        hw_os = hardware.get("os_name", "") if isinstance(hardware, dict) else ""

        if ua_os and hw_os and ua_os != hw_os:
            inconsistencies.append({
                "type": "ua_hardware_mismatch",
                "message": f"UA声明的OS({ua_os})与硬件检测的OS({hw_os})不一致",
                "severity": "medium",
            })

        # 检查移动/桌面一致性 / Check mobile/desktop consistency
        ua_is_mobile = ua_info.get("is_mobile", False)
        hw_touch = hardware.get("max_touch_points", 0) if isinstance(hardware, dict) else 0

        if ua_is_mobile and hw_touch == 0:
            inconsistencies.append({
                "type": "mobile_touch_mismatch",
                "message": "UA声称移动设备但不支持触摸",
                "severity": "high",
            })
        elif not ua_is_mobile and hw_touch > 1:
            inconsistencies.append({
                "type": "desktop_touch_mismatch",
                "message": "UA声称桌面设备但支持多点触摸",
                "severity": "medium",
            })

        consistency_score = max(0, 100 - len(inconsistencies) * 20)

        if verbose:
            if inconsistencies:
                for inc in inconsistencies:
                    icon = ICON_FAIL if inc["severity"] == "high" else ICON_WARN
                    print(f"  {Colors.red(icon)} 不一致: {inc['message']}")
            else:
                print(f"  {Colors.green(ICON_OK)} 一致性检查通过")
            print(f"  {Colors.DIM}  一致性评分: {consistency_score}/100{Colors.RESET}")

        return {
            "consistency_score": consistency_score,
            "inconsistencies": inconsistencies,
            "is_consistent": len(inconsistencies) == 0,
        }

    def _detect_anomalies(self, verbose=True):
        """检测异常特征

        Detect anomalous features.

        Returns:
            dict: 异常检测结果 / Anomaly detection results
        """
        anomalies = []

        # 检查无头浏览器特征 / Check headless browser indicators
        webgl = self.fingerprint_data.get("webgl", {})
        if isinstance(webgl, dict) and webgl.get("is_headless", False):
            anomalies.append({
                "type": "headless_browser",
                "message": "检测到无头浏览器特征(SwiftShader)",
                "severity": "critical",
                "dimension": "webgl",
            })

        # 检查自动化特征 / Check automation indicators
        headers = self.fingerprint_data.get("headers", {})
        if isinstance(headers, dict):
            ua = headers.get("user_agent", "")
            bot_indicators = ["bot", "spider", "crawl", "python", "curl", "httpclient"]
            for indicator in bot_indicators:
                if indicator in ua.lower():
                    anomalies.append({
                        "type": "automation_detected",
                        "message": f"UA包含自动化标识: {indicator}",
                        "severity": "critical",
                        "dimension": "headers",
                    })
                    break

        # 检查Canvas稳定性 / Check Canvas stability
        canvas = self.fingerprint_data.get("canvas", {})
        if isinstance(canvas, dict) and not canvas.get("is_stable", True):
            anomalies.append({
                "type": "unstable_canvas",
                "message": "Canvas指纹不稳定",
                "severity": "medium",
                "dimension": "canvas",
            })

        # 检查存储异常 / Check storage anomalies
        storage = self.fingerprint_data.get("storage", {})
        if isinstance(storage, dict):
            cookie = storage.get("cookie", {})
            if isinstance(cookie, dict) and not cookie.get("enabled", True):
                anomalies.append({
                    "type": "cookie_disabled",
                    "message": "Cookie被禁用",
                    "severity": "low",
                    "dimension": "storage",
                })

        # 检查字体数量异常 / Check font count anomaly
        fonts = self.fingerprint_data.get("fonts", {})
        if isinstance(fonts, dict):
            font_count = fonts.get("font_count", 0)
            if font_count < 10:
                anomalies.append({
                    "type": "low_font_count",
                    "message": f"字体数量过少: {font_count}",
                    "severity": "medium",
                    "dimension": "fonts",
                })

        if verbose:
            if anomalies:
                for anomaly in anomalies:
                    sev = anomaly["severity"]
                    if sev == "critical":
                        icon = ICON_FAIL
                        color = Colors.red
                    elif sev == "high":
                        icon = ICON_FAIL
                        color = Colors.yellow
                    elif sev == "medium":
                        icon = ICON_WARN
                        color = Colors.yellow
                    else:
                        icon = ICON_WARN
                        color = Colors.dim
                    print(f"  {color(icon)} 异常 [{sev}]: {anomaly['message']}")
            else:
                print(f"  {Colors.green(ICON_OK)} 未检测到异常特征")

        return {
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
            "has_critical": any(a["severity"] == "critical" for a in anomalies),
            "has_anomalies": len(anomalies) > 0,
        }

    def get_results(self):
        """获取分析结果

        Get analysis results.

        Returns:
            dict: 分析结果 / Analysis results
        """
        return self._analysis_results
