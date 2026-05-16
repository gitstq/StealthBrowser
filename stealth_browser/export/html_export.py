# -*- coding: utf-8 -*-
"""HTML报告导出模块

HTML report export module.
将指纹分析结果导出为可视化的HTML报告。
"""

import json
import time
from datetime import datetime


def export_html(fingerprint_data, analysis_results=None, score_results=None, filepath=None):
    """导出为HTML可视化报告

    Export as HTML visual report.

    Args:
        fingerprint_data (dict): 指纹数据 / Fingerprint data
        analysis_results (dict, optional): 分析结果 / Analysis results
        score_results (dict, optional): 评分结果 / Score results
        filepath (str, optional): 输出文件路径 / Output file path

    Returns:
        str: HTML字符串 / HTML string
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 生成指纹概览 / Generate fingerprint overview
    overview_rows = _generate_overview_rows(fingerprint_data)

    # 生成维度详情 / Generate dimension details
    dimension_sections = _generate_dimension_sections(fingerprint_data)

    # 生成分析结果 / Generate analysis results
    analysis_section = ""
    if analysis_results:
        analysis_section = _generate_analysis_section(analysis_results)

    # 生成评分部分 / Generate score section
    score_section = ""
    if score_results:
        score_section = _generate_score_section(score_results)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>StealthBrowser 指纹分析报告</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
       background: #0d1117; color: #c9d1d9; line-height: 1.6; padding: 20px; }}
.container {{ max-width: 1200px; margin: 0 auto; }}
.header {{ text-align: center; padding: 40px 0; border-bottom: 1px solid #21262d; margin-bottom: 30px; }}
.header h1 {{ font-size: 2em; color: #58a6ff; margin-bottom: 10px; }}
.header .subtitle {{ color: #8b949e; font-size: 1.1em; }}
.header .timestamp {{ color: #484f58; margin-top: 10px; font-size: 0.9em; }}
.section {{ background: #161b22; border: 1px solid #21262d; border-radius: 8px;
            padding: 24px; margin-bottom: 20px; }}
.section h2 {{ color: #58a6ff; font-size: 1.3em; margin-bottom: 16px;
               padding-bottom: 8px; border-bottom: 1px solid #21262d; }}
.overview-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px; }}
.overview-card {{ background: #0d1117; border: 1px solid #21262d; border-radius: 6px;
                  padding: 12px 16px; }}
.overview-card .label {{ color: #8b949e; font-size: 0.85em; margin-bottom: 4px; }}
.overview-card .value {{ color: #f0f6fc; font-weight: 500; word-break: break-all; }}
.dim-section {{ margin-bottom: 16px; }}
.dim-section h3 {{ color: #79c0ff; font-size: 1.1em; margin-bottom: 8px; }}
.data-table {{ width: 100%; border-collapse: collapse; }}
.data-table th {{ text-align: left; color: #8b949e; font-weight: 500;
                 padding: 6px 12px; border-bottom: 1px solid #21262d; font-size: 0.85em; }}
.data-table td {{ padding: 6px 12px; border-bottom: 1px solid #21262d; font-size: 0.9em; }}
.data-table tr:hover {{ background: #1c2128; }}
.score-bar {{ height: 24px; background: #21262d; border-radius: 12px; overflow: hidden; margin: 8px 0; }}
.score-fill {{ height: 100%; border-radius: 12px; transition: width 0.3s; }}
.score-excellent {{ background: linear-gradient(90deg, #238636, #2ea043); }}
.score-good {{ background: linear-gradient(90deg, #9e6a03, #d29922); }}
.score-average {{ background: linear-gradient(90deg, #da3633, #f85149); }}
.score-poor {{ background: linear-gradient(90deg, #8b0000, #da3633); }}
.score-total {{ font-size: 2.5em; font-weight: bold; text-align: center; padding: 20px; }}
.risk-low {{ color: #3fb950; }}
.risk-medium {{ color: #d29922; }}
.risk-high {{ color: #f85149; }}
.risk-critical {{ color: #ff4444; font-weight: bold; }}
.tag {{ display: inline-block; padding: 2px 8px; border-radius: 12px;
        font-size: 0.8em; margin: 2px; }}
.tag-green {{ background: #23863633; color: #3fb950; border: 1px solid #238636; }}
.tag-yellow {{ background: #9e6a0333; color: #d29922; border: 1px solid #9e6a03; }}
.tag-red {{ background: #da363333; color: #f85149; border: 1px solid #da3633; }}
.suggestion {{ background: #1c2128; border-left: 3px solid #d29922;
              padding: 8px 12px; margin: 6px 0; border-radius: 0 4px 4px 0; font-size: 0.9em; }}
.footer {{ text-align: center; padding: 20px; color: #484f58; font-size: 0.85em;
           border-top: 1px solid #21262d; margin-top: 30px; }}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>StealthBrowser 指纹分析报告</h1>
<div class="subtitle">浏览器指纹多维度分析与反检测评估</div>
<div class="timestamp">生成时间: {now}</div>
</div>

<div class="section">
<h2>指纹概览</h2>
<div class="overview-grid">
{overview_rows}
</div>
</div>

{dimension_sections}

{analysis_section}

{score_section}

<div class="footer">
<p>StealthBrowser v1.0.0 | 轻量级反检测浏览器指纹分析工具</p>
<p>本报告由StealthBrowser自动生成，仅供参考</p>
</div>
</div>
</body>
</html>"""

    if filepath:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

    return html


def _generate_overview_rows(fingerprint_data):
    """生成概览卡片

    Generate overview cards.

    Args:
        fingerprint_data (dict): 指纹数据 / Fingerprint data

    Returns:
        str: HTML概览卡片 / HTML overview cards
    """
    rows = []

    # Canvas指纹 / Canvas fingerprint
    canvas = fingerprint_data.get("canvas", {})
    if isinstance(canvas, dict) and canvas.get("hash"):
        rows.append(f"""<div class="overview-card">
<div class="label">Canvas 指纹</div>
<div class="value">{canvas['hash'][:24]}...</div>
</div>""")

    # WebGL / WebGL
    webgl = fingerprint_data.get("webgl", {})
    if isinstance(webgl, dict):
        rows.append(f"""<div class="overview-card">
<div class="label">WebGL 渲染器</div>
<div class="value">{webgl.get('renderer', 'N/A')[:40]}</div>
</div>""")

    # User-Agent / User-Agent
    headers = fingerprint_data.get("headers", {})
    if isinstance(headers, dict):
        ua = headers.get("user_agent", "N/A")
        rows.append(f"""<div class="overview-card">
<div class="label">User-Agent</div>
<div class="value">{ua[:60]}...</div>
</div>""")

    # 屏幕 / Screen
    screen = fingerprint_data.get("screen", {})
    if isinstance(screen, dict):
        rows.append(f"""<div class="overview-card">
<div class="label">屏幕分辨率</div>
<div class="value">{screen.get('screen_width', 0)}x{screen.get('screen_height', 0)} @ {screen.get('device_pixel_ratio', 1)}x</div>
</div>""")

    # 硬件 / Hardware
    hardware = fingerprint_data.get("hardware", {})
    if isinstance(hardware, dict):
        rows.append(f"""<div class="overview-card">
<div class="label">CPU核心 / 内存</div>
<div class="value">{hardware.get('hardware_concurrency', 0)} 核心 / {hardware.get('device_memory', 0)} GB</div>
</div>""")

    # 时区 / Timezone
    tz = fingerprint_data.get("timezone", {})
    if isinstance(tz, dict):
        rows.append(f"""<div class="overview-card">
<div class="label">时区 / 语言</div>
<div class="value">{tz.get('timezone', 'N/A')} / {tz.get('primary_language', 'N/A')}</div>
</div>""")

    # 字体数量 / Font count
    fonts = fingerprint_data.get("fonts", {})
    if isinstance(fonts, dict):
        rows.append(f"""<div class="overview-card">
<div class="label">检测到的字体</div>
<div class="value">{fonts.get('font_count', 0)} 个</div>
</div>""")

    # 网络 / Network
    network = fingerprint_data.get("network", {})
    if isinstance(network, dict):
        rows.append(f"""<div class="overview-card">
<div class="label">IP类型</div>
<div class="value">{network.get('ip_type', 'N/A')} ({network.get('ip', 'N/A')})</div>
</div>""")

    return "\n".join(rows)


def _generate_dimension_sections(fingerprint_data):
    """生成各维度详情

    Generate dimension details.

    Args:
        fingerprint_data (dict): 指纹数据 / Fingerprint data

    Returns:
        str: HTML维度详情 / HTML dimension details
    """
    sections = []
    dimension_names = {
        "canvas": "Canvas 指纹",
        "webgl": "WebGL 指纹",
        "audio": "AudioContext 指纹",
        "fonts": "字体检测",
        "hardware": "硬件信息",
        "screen": "屏幕信息",
        "timezone": "时区/语言/地区",
        "headers": "HTTP头/UA/TLS",
        "storage": "存储指纹",
        "network": "网络指纹",
        "behavior": "行为指纹",
    }

    for dim_key, dim_name in dimension_names.items():
        dim_data = fingerprint_data.get(dim_key, {})
        if not dim_data or not isinstance(dim_data, dict):
            continue

        rows = _dict_to_table_rows(dim_data)
        if not rows:
            continue

        sections.append(f"""<div class="section">
<h2>{dim_name}</h2>
<div class="dim-section">
<table class="data-table">
<thead><tr><th>属性</th><th>值</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</div>
</div>""")

    return "\n".join(sections)


def _dict_to_table_rows(data, prefix="", max_depth=3):
    """将字典转换为HTML表格行

    Convert dict to HTML table rows.

    Args:
        data (dict): 数据字典 / Data dict
        prefix (str): 键名前缀 / Key prefix
        max_depth (int): 最大递归深度 / Max recursion depth

    Returns:
        str: HTML表格行 / HTML table rows
    """
    rows = []
    if max_depth <= 0:
        return ""

    for key, value in data.items():
        display_key = f"{prefix}.{key}" if prefix else str(key)

        if isinstance(value, dict):
            rows.append(_dict_to_table_rows(value, display_key, max_depth - 1))
        elif isinstance(value, (list, tuple)):
            if len(value) > 5:
                display_value = f"[{len(value)} 项] " + ", ".join(str(v) for v in value[:3]) + ", ..."
            else:
                display_value = ", ".join(str(v) for v in value)
            rows.append(f"<tr><td>{display_key}</td><td>{display_value}</td></tr>")
        elif isinstance(value, bool):
            display_value = '<span class="tag tag-green">True</span>' if value else '<span class="tag tag-red">False</span>'
            rows.append(f"<tr><td>{display_key}</td><td>{display_value}</td></tr>")
        else:
            display_value = str(value) if value is not None else '<span style="color:#484f58">null</span>'
            rows.append(f"<tr><td>{display_key}</td><td>{display_value}</td></tr>")

    return "\n".join(rows)


def _generate_analysis_section(analysis_results):
    """生成分析结果部分

    Generate analysis results section.

    Args:
        analysis_results (dict): 分析结果 / Analysis results

    Returns:
        str: HTML分析部分 / HTML analysis section
    """
    sections = []

    # 唯一性评分 / Uniqueness score
    uniqueness = analysis_results.get("uniqueness", {})
    summary = uniqueness.get("_summary", {})
    uniq_score = summary.get("uniqueness_score", 0)

    if uniq_score >= 70:
        uniq_class = "risk-high"
        uniq_label = "高唯一性"
    elif uniq_score >= 40:
        uniq_class = "risk-medium"
        uniq_label = "中等唯一性"
    else:
        uniq_class = "risk-low"
        uniq_label = "低唯一性"

    sections.append(f"""<div class="section">
<h2>唯一性分析</h2>
<div class="score-total {uniq_class}">{uniq_score:.1f}/100</div>
<p style="text-align:center;color:#8b949e;">{uniq_label} - 指纹可被用于追踪的概率</p>
</div>""")

    # 异常检测 / Anomaly detection
    anomalies = analysis_results.get("anomalies", {})
    anomaly_list = anomalies.get("anomalies", [])

    if anomaly_list:
        anomaly_rows = ""
        for anomaly in anomaly_list:
            severity = anomaly.get("severity", "medium")
            if severity == "critical":
                tag_class = "tag-red"
            elif severity == "high":
                tag_class = "tag-yellow"
            else:
                tag_class = "tag-yellow"
            anomaly_rows += f"""<tr>
<td>{anomaly.get('dimension', 'N/A')}</td>
<td>{anomaly.get('message', 'N/A')}</td>
<td><span class="tag {tag_class}">{severity}</span></td>
</tr>"""

        sections.append(f"""<div class="section">
<h2>异常检测</h2>
<table class="data-table">
<thead><tr><th>维度</th><th>描述</th><th>严重程度</th></tr></thead>
<tbody>{anomaly_rows}</tbody>
</table>
</div>""")

    return "\n".join(sections)


def _generate_score_section(score_results):
    """生成评分部分

    Generate score section.

    Args:
        score_results (dict): 评分结果 / Score results

    Returns:
        str: HTML评分部分 / HTML score section
    """
    total = score_results.get("total_score", 0)
    grade = score_results.get("grade", "unknown")

    if total >= 80:
        score_class = "score-excellent"
        grade_text = "优秀"
    elif total >= 60:
        score_class = "score-good"
        grade_text = "良好"
    elif total >= 40:
        score_class = "score-average"
        grade_text = "一般"
    else:
        score_class = "score-poor"
        grade_text = "较差"

    # 各维度评分 / Dimension scores
    dim_scores = score_results.get("dimensions", {})
    dim_rows = ""
    dim_names = {
        "randomization": "指纹随机化程度",
        "consistency": "浏览器一致性",
        "behavior": "行为模拟真实性",
        "network": "网络匿名性",
    }
    for dim_key, dim_name in dim_names.items():
        dim_data = dim_scores.get(dim_key, {})
        score = dim_data.get("score", 0)
        max_score = dim_data.get("max_score", 25)
        percent = score / max_score * 100 if max_score > 0 else 0

        if percent >= 80:
            bar_class = "score-excellent"
        elif percent >= 50:
            bar_class = "score-good"
        elif percent >= 30:
            bar_class = "score-average"
        else:
            bar_class = "score-poor"

        dim_rows += f"""<tr>
<td>{dim_name}</td>
<td>
<div class="score-bar">
<div class="score-fill {bar_class}" style="width:{percent}%"></div>
</div>
</td>
<td>{score}/{max_score}</td>
</tr>"""

    # 改进建议 / Suggestions
    suggestions = score_results.get("suggestions", [])
    suggestion_html = ""
    for s in suggestions:
        suggestion_html += f'<div class="suggestion">{s}</div>'

    return f"""<div class="section">
<h2>反检测评分</h2>
<div class="score-total {score_class}">{total}/100</div>
<p style="text-align:center;color:#8b949e;">等级: {grade_text}</p>
<table class="data-table" style="margin-top:20px;">
<thead><tr><th>评分维度</th><th>得分</th><th>分数</th></tr></thead>
<tbody>{dim_rows}</tbody>
</table>
{suggestion_html}
</div>"""
