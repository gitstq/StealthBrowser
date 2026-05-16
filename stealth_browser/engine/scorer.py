# -*- coding: utf-8 -*-
"""反检测评分引擎模块

Anti-detection scoring engine module.
评估浏览器指纹的反检测能力，给出0-100的综合评分。
"""

from ..utils.colors import Colors, print_score_gauge, print_table, ICON_OK, ICON_FAIL, ICON_WARN


class AntiDetectScorer:
    """反检测评分引擎

    Anti-detection scoring engine.
    评估指纹配置的反检测能力，从四个维度打分。
    Evaluates anti-detection capability from four dimensions.
    """

    # 评分维度及权重 / Scoring dimensions and weights
    DIMENSIONS = {
        "randomization": {
            "name": "指纹随机化程度",
            "name_en": "Fingerprint Randomization",
            "max_score": 25,
            "description": "评估指纹数据的随机化和多样性",
        },
        "consistency": {
            "name": "浏览器一致性",
            "name_en": "Browser Consistency",
            "max_score": 25,
            "description": "评估各维度数据之间的逻辑一致性",
        },
        "behavior": {
            "name": "行为模拟真实性",
            "name_en": "Behavior Authenticity",
            "max_score": 25,
            "description": "评估行为特征是否模拟真实用户",
        },
        "network": {
            "name": "网络匿名性",
            "name_en": "Network Anonymity",
            "max_score": 25,
            "description": "评估网络层面的匿名保护程度",
        },
    }

    def __init__(self, fingerprint_data=None, analysis_results=None):
        """初始化评分引擎

        Initialize scoring engine.

        Args:
            fingerprint_data (dict, optional): 指纹数据 / Fingerprint data
            analysis_results (dict, optional): 分析结果 / Analysis results
        """
        self.fingerprint_data = fingerprint_data or {}
        self.analysis_results = analysis_results or {}
        self._scores = {}
        self._total_score = 0
        self._suggestions = []

    def set_data(self, fingerprint_data, analysis_results=None):
        """设置数据

        Set data.

        Args:
            fingerprint_data (dict): 指纹数据 / Fingerprint data
            analysis_results (dict, optional): 分析结果 / Analysis results
        """
        self.fingerprint_data = fingerprint_data
        if analysis_results:
            self.analysis_results = analysis_results

    def score(self, verbose=True):
        """执行评分

        Execute scoring.

        Args:
            verbose (bool): 是否显示详细输出 / Whether to show verbose output

        Returns:
            dict: 评分结果 / Scoring results
        """
        if not self.fingerprint_data:
            return {"error": "未设置指纹数据"}

        if verbose:
            print(f"\n  {Colors.bold(Colors.cyan('正在进行反检测评分...'))}")
            print(f"  {Colors.DIM + '─' * 50 + Colors.RESET}")

        # 各维度评分 / Score each dimension
        randomization_score = self._score_randomization()
        consistency_score = self._score_consistency()
        behavior_score = self._score_behavior()
        network_score = self._score_network()

        self._scores = {
            "randomization": randomization_score,
            "consistency": consistency_score,
            "behavior": behavior_score,
            "network": network_score,
        }

        # 计算总分 / Calculate total score
        self._total_score = (
            randomization_score["score"]
            + consistency_score["score"]
            + behavior_score["score"]
            + network_score["score"]
        )

        if verbose:
            self._print_score_report()

        return self.get_results()

    def _score_randomization(self):
        """评分：指纹随机化程度(0-25)

        Score: Fingerprint randomization (0-25).

        Returns:
            dict: 评分详情 / Score details
        """
        score = 0
        details = []

        # Canvas指纹熵值 / Canvas fingerprint entropy
        canvas = self.fingerprint_data.get("canvas", {})
        if isinstance(canvas, dict) and canvas.get("hash"):
            details.append(f"Canvas指纹: {canvas['hash'][:16]}...")
            score += 5

        # WebGL指纹 / WebGL fingerprint
        webgl = self.fingerprint_data.get("webgl", {})
        if isinstance(webgl, dict) and webgl.get("hash"):
            details.append(f"WebGL指纹: {webgl['hash'][:16]}...")
            if not webgl.get("is_headless", False):
                score += 5
            else:
                details.append("  ⚠ 使用SwiftShader(无头模式)")
                score += 2

        # Audio指纹 / Audio fingerprint
        audio = self.fingerprint_data.get("audio", {})
        if isinstance(audio, dict) and audio.get("hash"):
            details.append(f"Audio指纹: {audio['hash'][:16]}...")
            score += 4

        # 字体多样性 / Font diversity
        fonts = self.fingerprint_data.get("fonts", {})
        if isinstance(fonts, dict):
            font_count = fonts.get("font_count", 0)
            if font_count >= 30:
                score += 4
                details.append(f"字体数量: {font_count}(良好)")
            elif font_count >= 15:
                score += 2
                details.append(f"字体数量: {font_count}(一般)")
            else:
                details.append(f"字体数量: {font_count}(偏少)")

        # 屏幕分辨率 / Screen resolution
        screen = self.fingerprint_data.get("screen", {})
        if isinstance(screen, dict):
            w = screen.get("screen_width", 0)
            h = screen.get("screen_height", 0)
            if w > 0 and h > 0:
                score += 3
                details.append(f"屏幕分辨率: {w}x{h}")

        # 时区/语言 / Timezone/Language
        tz = self.fingerprint_data.get("timezone", {})
        if isinstance(tz, dict) and tz.get("timezone"):
            score += 2
            details.append(f"时区: {tz['timezone']}")

        # 唯一性评分参考 / Uniqueness score reference
        uniqueness = self.analysis_results.get("uniqueness", {})
        summary = uniqueness.get("_summary", {})
        uniq_score = summary.get("uniqueness_score", 0)
        if uniq_score > 60:
            score += 2
            details.append(f"唯一性评分: {uniq_score:.1f}(高)")

        score = min(score, 25)

        return {
            "score": score,
            "max_score": 25,
            "details": details,
        }

    def _score_consistency(self):
        """评分：浏览器一致性(0-25)

        Score: Browser consistency (0-25).

        Returns:
            dict: 评分详情 / Score details
        """
        score = 25  # 满分开始，发现不一致则扣分 / Start at full, deduct for inconsistencies
        details = []

        # 使用分析结果中的一致性检查 / Use consistency check from analysis results
        consistency = self.analysis_results.get("consistency", {})
        inconsistencies = consistency.get("inconsistencies", [])

        for inc in inconsistencies:
            severity = inc.get("severity", "medium")
            if severity == "high":
                score -= 8
            elif severity == "medium":
                score -= 4
            else:
                score -= 2
            details.append(f"- {inc['message']}")

        if not inconsistencies:
            details.append("所有维度数据一致")

        # 异常检测扣分 / Anomaly detection deductions
        anomalies = self.analysis_results.get("anomalies", {})
        anomaly_list = anomalies.get("anomalies", [])
        for anomaly in anomaly_list:
            severity = anomaly.get("severity", "medium")
            if severity == "critical":
                score -= 5
                details.append(f"- 严重异常: {anomaly['message']}")
            elif severity == "high":
                score -= 3
            elif severity == "medium":
                score -= 1

        score = max(0, min(score, 25))

        return {
            "score": score,
            "max_score": 25,
            "details": details,
        }

    def _score_behavior(self):
        """评分：行为模拟真实性(0-25)

        Score: Behavior authenticity (0-25).

        Returns:
            dict: 评分详情 / Score details
        """
        score = 0
        details = []

        behavior = self.fingerprint_data.get("behavior", {})
        if not isinstance(behavior, dict):
            return {"score": 0, "max_score": 25, "details": ["无行为数据"]}

        # 机器人概率评估 / Bot probability assessment
        bot_prob = behavior.get("bot_probability", 0.5)
        human_prob = 1.0 - bot_prob

        if human_prob > 0.8:
            score += 10
            details.append(f"人类行为概率: {human_prob:.1%}(优秀)")
        elif human_prob > 0.6:
            score += 7
            details.append(f"人类行为概率: {human_prob:.1%}(良好)")
        elif human_prob > 0.4:
            score += 4
            details.append(f"人类行为概率: {human_prob:.1%}(一般)")
        else:
            score += 1
            details.append(f"人类行为概率: {human_prob:.1%}(较差)")

        # 鼠标行为 / Mouse behavior
        mouse = behavior.get("mouse", {})
        if isinstance(mouse, dict):
            if mouse.get("has_human_pattern", False):
                score += 5
                details.append("鼠标移动模式: 自然")
            else:
                score += 1
                details.append("鼠标移动模式: 异常")

            if mouse.get("is_smooth", False):
                score += 3
                details.append("鼠标轨迹: 平滑")
            else:
                score += 1
                details.append("鼠标轨迹: 不规则")

        # 键盘行为 / Keyboard behavior
        keyboard = behavior.get("keyboard", {})
        if isinstance(keyboard, dict):
            if keyboard.get("has_typing_pattern", False):
                score += 4
                details.append("键盘输入模式: 自然")
            else:
                score += 1
                details.append("键盘输入模式: 异常")

            std_interval = keyboard.get("std_interval_ms", 0)
            if std_interval > 20:
                score += 3
                details.append(f"按键间隔标准差: {std_interval:.1f}ms(自然)")
            else:
                details.append(f"按键间隔标准差: {std_interval:.1f}ms(过于均匀)")

        score = min(score, 25)

        return {
            "score": score,
            "max_score": 25,
            "details": details,
        }

    def _score_network(self):
        """评分：网络匿名性(0-25)

        Score: Network anonymity (0-25).

        Returns:
            dict: 评分详情 / Score details
        """
        score = 0
        details = []

        network = self.fingerprint_data.get("network", {})
        if not isinstance(network, dict):
            return {"score": 0, "max_score": 25, "details": ["无网络数据"]}

        # IP类型评分 / IP type scoring
        ip_type = network.get("ip_type", "")
        if ip_type == "residential":
            score += 8
            details.append(f"IP类型: 住宅IP(最佳)")
        elif ip_type == "vpn":
            score += 5
            details.append(f"IP类型: VPN(中等)")
        elif ip_type == "datacenter":
            score += 2
            details.append(f"IP类型: 数据中心(较差)")
        elif ip_type == "tor":
            score += 3
            details.append(f"IP类型: Tor(匿名但易识别)")

        # WebRTC泄露 / WebRTC leak
        if not network.get("webrtc_support", False):
            score += 5
            details.append("WebRTC: 已禁用(安全)")
        elif not network.get("webrtc_local_ip"):
            score += 4
            details.append("WebRTC: 无本地IP泄露")
        else:
            details.append(f"WebRTC: 可能泄露本地IP")
            score += 1

        # 代理检测 / Proxy detection
        if not network.get("has_proxy", False):
            score += 5
            details.append("代理: 未检测到代理")
        else:
            proxy_type = network.get("proxy_type", "unknown")
            details.append(f"代理: 检测到{proxy_type}代理")
            score += 2

        # DNS / DNS
        dns_servers = network.get("dns_servers", [])
        if dns_servers:
            score += 4
            details.append(f"DNS: {', '.join(dns_servers[:2])}")

        # DoH / DoH
        if network.get("doh_enabled", False):
            score += 3
            details.append("DNS over HTTPS: 已启用")

        score = min(score, 25)

        return {
            "score": score,
            "max_score": 25,
            "details": details,
        }

    def _print_score_report(self):
        """打印评分报告

        Print score report.
        """
        # 打印各维度评分 / Print dimension scores
        rows = []
        for dim_key, dim_info in self.DIMENSIONS.items():
            dim_score = self._scores.get(dim_key, {})
            s = dim_score.get("score", 0)
            mx = dim_info["max_score"]

            if s >= mx * 0.8:
                icon = ICON_OK
                color = Colors.green(f"{s}/{mx}")
            elif s >= mx * 0.5:
                icon = ICON_WARN
                color = Colors.yellow(f"{s}/{mx}")
            else:
                icon = ICON_FAIL
                color = Colors.red(f"{s}/{mx}")

            rows.append([
                f"  {icon} {dim_info['name']}",
                color,
            ])

        print_table(
            ["评分维度", "得分"],
            rows,
            col_widths=[30, 12],
            title="反检测评分详情",
        )

        # 打印各维度详细说明 / Print dimension details
        for dim_key, dim_info in self.DIMENSIONS.items():
            dim_score = self._scores.get(dim_key, {})
            details = dim_score.get("details", [])
            if details:
                print(f"\n  {Colors.DIM}{dim_info['name']}:{Colors.RESET}")
                for detail in details:
                    print(f"    {Colors.DIM}• {detail}{Colors.RESET}")

        # 打印总分仪表盘 / Print total score gauge
        print_score_gauge(self._total_score, 100, "反检测综合评分")

        # 生成改进建议 / Generate improvement suggestions
        self._generate_suggestions()

        if self._suggestions:
            print(f"  {Colors.bold(Colors.yellow('改进建议:'))}")
            for i, suggestion in enumerate(self._suggestions, 1):
                print(f"    {Colors.DIM}{i}. {suggestion}{Colors.RESET}")

    def _generate_suggestions(self):
        """生成改进建议

        Generate improvement suggestions.
        """
        self._suggestions = []

        # 随机化建议 / Randomization suggestions
        rand_score = self._scores.get("randomization", {}).get("score", 0)
        if rand_score < 15:
            self._suggestions.append("增加Canvas和WebGL指纹的随机化程度")
        if rand_score < 20:
            self._suggestions.append("增加字体列表的多样性")

        # 一致性建议 / Consistency suggestions
        cons_score = self._scores.get("consistency", {}).get("score", 0)
        if cons_score < 20:
            self._suggestions.append("确保User-Agent与硬件/平台信息一致")
        if cons_score < 15:
            self._suggestions.append("修复检测到的不一致项")

        # 行为建议 / Behavior suggestions
        beh_score = self._scores.get("behavior", {}).get("score", 0)
        if beh_score < 15:
            self._suggestions.append("优化鼠标移动轨迹，增加自然随机性")
        if beh_score < 20:
            self._suggestions.append("增加按键间隔的随机性")

        # 网络建议 / Network suggestions
        net_score = self._scores.get("network", {}).get("score", 0)
        if net_score < 15:
            self._suggestions.append("使用住宅IP代替数据中心IP")
        if net_score < 20:
            self._suggestions.append("禁用WebRTC以防止IP泄露")

    def get_results(self):
        """获取评分结果

        Get scoring results.

        Returns:
            dict: 评分结果 / Scoring results
        """
        return {
            "total_score": self._total_score,
            "max_score": 100,
            "dimensions": self._scores,
            "suggestions": self._suggestions,
            "grade": self._get_grade(),
        }

    def _get_grade(self):
        """获取评分等级

        Get score grade.

        Returns:
            str: 等级 / Grade
        """
        if self._total_score >= 80:
            return "excellent"
        elif self._total_score >= 60:
            return "good"
        elif self._total_score >= 40:
            return "average"
        elif self._total_score >= 20:
            return "poor"
        return "critical"
