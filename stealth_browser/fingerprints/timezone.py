# -*- coding: utf-8 -*-
"""时区/语言/地区指纹模块

Timezone/Language/Locale fingerprint module.
分析时区偏移、语言列表、地区设置等。
"""

import random


# 常见时区数据 / Common timezone data
COMMON_TIMEZONES = {
    "Asia/Shanghai": {"offset": -480, "name": "中国标准时间"},
    "Asia/Tokyo": {"offset": -540, "name": "日本标准时间"},
    "Asia/Kolkata": {"offset": -330, "name": "印度标准时间"},
    "Asia/Seoul": {"offset": -540, "name": "韩国标准时间"},
    "Asia/Singapore": {"offset": -480, "name": "新加坡标准时间"},
    "America/New_York": {"offset": 300, "name": "美国东部时间"},
    "America/Chicago": {"offset": 360, "name": "美国中部时间"},
    "America/Denver": {"offset": 420, "name": "美国山地时间"},
    "America/Los_Angeles": {"offset": 480, "name": "美国太平洋时间"},
    "Europe/London": {"offset": 0, "name": "格林尼治标准时间"},
    "Europe/Paris": {"offset": -60, "name": "中欧标准时间"},
    "Europe/Berlin": {"offset": -60, "name": "中欧标准时间"},
    "Europe/Moscow": {"offset": -180, "name": "莫斯科标准时间"},
    "Australia/Sydney": {"offset": -660, "name": "澳大利亚东部时间"},
    "Pacific/Auckland": {"offset": -720, "name": "新西兰标准时间"},
}

# 常见语言配置 / Common language configurations
COMMON_LANGUAGES = {
    "zh-CN": ["zh-CN", "zh", "en-US", "en"],
    "zh-TW": ["zh-TW", "zh", "en-US", "en"],
    "en-US": ["en-US", "en"],
    "en-GB": ["en-GB", "en"],
    "ja-JP": ["ja-JP", "ja", "en-US", "en"],
    "ko-KR": ["ko-KR", "ko", "en-US", "en"],
    "de-DE": ["de-DE", "de", "en-US", "en"],
    "fr-FR": ["fr-FR", "fr", "en-US", "en"],
    "es-ES": ["es-ES", "es", "en-US", "en"],
    "pt-BR": ["pt-BR", "pt", "en-US", "en"],
}


def generate_timezone_fingerprint(locale="zh-CN", seed=None):
    """生成模拟时区/语言/地区指纹

    Generate simulated timezone/language/locale fingerprint.

    Args:
        locale (str): 地区设置 / Locale setting
        seed (int, optional): 随机种子 / Random seed

    Returns:
        dict: 时区/语言/地区指纹数据 / Timezone/language/locale fingerprint data
    """
    if seed is not None:
        random.seed(seed)

    # 选择时区 / Select timezone
    tz_name = random.choice(list(COMMON_TIMEZONES.keys()))
    tz_info = COMMON_TIMEZONES[tz_name]

    # 语言列表 / Language list
    languages = COMMON_LANGUAGES.get(locale, COMMON_LANGUAGES["en-US"])
    # 随机调整语言顺序和数量 / Randomly adjust language order and count
    num_langs = random.randint(1, len(languages))
    languages = sorted(random.sample(languages, num_langs), key=lambda x: random.random())

    # 时区偏移 / Timezone offset
    timezone_offset = tz_info["offset"]

    # 日期格式 / Date format
    date_format = random.choice([
        "YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY",
        "DD.MM.YYYY", "YYYY/MM/DD",
    ])

    # 数字格式 / Number format
    number_format = {
        "decimal_separator": random.choice([".", ","]),
        "thousands_separator": random.choice([",", ".", " ", ""]),
        "currency_symbol": random.choice(["$", "€", "£", "¥", "₹", "₩", "₽"]),
    }

    # 日历 / Calendar
    calendar = random.choice(["gregory", "gregorian", "japanese", "buddhist", "islamic"])

    # 是否使用夏令时 / Daylight saving time
    has_dst = random.choice([True, False])

    # 时区偏移历史 / Timezone offset history
    if has_dst:
        dst_offset = timezone_offset - 60  # 夏令时偏移
    else:
        dst_offset = timezone_offset

    return {
        "timezone": tz_name,
        "timezone_offset": timezone_offset,
        "timezone_name": tz_info["name"],
        "has_dst": has_dst,
        "dst_offset": dst_offset,
        "languages": languages,
        "primary_language": languages[0] if languages else "en-US",
        "locale": locale,
        "date_format": date_format,
        "number_format": number_format,
        "calendar": calendar,
        "charset": random.choice(["UTF-8", "UTF-8"]),  # 现代浏览器几乎都是UTF-8
    }


def analyze_timezone_fingerprint(fingerprint):
    """分析时区/语言/地区指纹特征

    Analyze timezone/language/locale fingerprint characteristics.

    Args:
        fingerprint (dict): 时区/语言/地区指纹数据 / Fingerprint data

    Returns:
        dict: 分析结果 / Analysis results
    """
    if not fingerprint:
        return {"error": "无效的时区指纹数据", "risk_level": "unknown"}

    risk_factors = []
    risk_score = 0

    # 检查时区与语言一致性 / Check timezone-language consistency
    tz = fingerprint.get("timezone", "")
    primary_lang = fingerprint.get("primary_language", "")

    # 时区与语言不匹配检测 / Timezone-language mismatch detection
    mismatch_rules = {
        "Asia/Shanghai": ["zh-CN", "zh-TW"],
        "Asia/Tokyo": ["ja-JP"],
        "Asia/Seoul": ["ko-KR"],
        "America/New_York": ["en-US"],
        "Europe/London": ["en-GB", "en-US"],
        "Europe/Paris": ["fr-FR"],
        "Europe/Berlin": ["de-DE"],
    }

    expected_langs = mismatch_rules.get(tz, [])
    if expected_langs and primary_lang not in expected_langs:
        risk_factors.append(f"时区({tz})与语言({primary_lang})不匹配")
        risk_score += 20

    # 检查语言列表 / Check language list
    languages = fingerprint.get("languages", [])
    if not languages:
        risk_factors.append("语言列表为空")
        risk_score += 15
    elif len(languages) > 10:
        risk_factors.append(f"语言列表过长({len(languages)}个)")
        risk_score += 10

    # 检查时区偏移 / Check timezone offset
    offset = fingerprint.get("timezone_offset", 0)
    tz_info = COMMON_TIMEZONES.get(tz, {})
    expected_offset = tz_info.get("offset")
    if expected_offset is not None and offset != expected_offset:
        risk_factors.append(f"时区偏移({offset})与声称的时区({tz})不匹配")
        risk_score += 25

    # 检查夏令时 / Check DST
    has_dst = fingerprint.get("has_dst", False)
    dst_offset = fingerprint.get("dst_offset", 0)
    if has_dst and dst_offset == offset:
        risk_factors.append("声称支持夏令时但偏移量未变化")
        risk_score += 15

    if risk_score >= 50:
        risk_level = "high"
    elif risk_score >= 25:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "timezone": tz,
        "primary_language": primary_lang,
        "timezone_language_match": not (expected_langs and primary_lang not in expected_langs),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
    }
