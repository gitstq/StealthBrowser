# -*- coding: utf-8 -*-
"""HTTP头/UA/TLS指纹模块

HTTP Headers/User-Agent/TLS fingerprint module.
分析HTTP请求头、User-Agent字符串、TLS特征等。
"""

import hashlib
import random


# 常见User-Agent模板 / Common User-Agent templates
USER_AGENTS = {
    "chrome_desktop": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ],
    "firefox_desktop": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    ],
    "safari_mobile": [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    ],
    "chrome_mobile": [
        "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    ],
    "bot": [
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
        "python-requests/2.31.0",
    ],
}

# 常见HTTP头 / Common HTTP headers
COMMON_HEADERS = {
    "accept": [
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "*/*",
    ],
    "accept_encoding": [
        "gzip, deflate, br",
        "gzip, deflate",
        "gzip, deflate, br, zstd",
    ],
    "accept_language": [
        "zh-CN,zh;q=0.9,en;q=0.8",
        "en-US,en;q=0.9",
        "zh-CN,zh;q=0.9",
        "ja,en-US;q=0.9,en;q=0.8",
    ],
    "sec_ch_ua": [
        '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        '"Not_A Brand";v="8", "Chromium";v="121", "Google Chrome";v="121"',
    ],
    "sec_ch_ua_mobile": ["?0", "?1"],
    "sec_ch_ua_platform": ['"Windows"', '"macOS"', '"Linux"', '"Android"'],
}

# TLS密码套件 / TLS cipher suites
TLS_CIPHER_SUITES = [
    "TLS_AES_128_GCM_SHA256",
    "TLS_AES_256_GCM_SHA384",
    "TLS_CHACHA20_POLY1305_SHA256",
    "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
    "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
    "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
    "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
    "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
    "TLS_RSA_WITH_AES_128_GCM_SHA256",
    "TLS_RSA_WITH_AES_256_GCM_SHA384",
]

# TLS扩展 / TLS extensions
TLS_EXTENSIONS = [
    "server_name", "extended_master_secret", "renegotiation_info",
    "supported_groups", "ec_point_formats", "session_ticket",
    "application_layer_protocol_negotiation", "status_request",
    "signed_certificate_timestamp", "key_share", "psk_key_exchange_modes",
    "supported_versions", "compress_certificate", "application_settings",
]


def generate_headers_fingerprint(browser_type="chrome_desktop", seed=None):
    """生成模拟HTTP头/UA/TLS指纹

    Generate simulated HTTP headers/UA/TLS fingerprint.

    Args:
        browser_type (str): 浏览器类型 / Browser type
        seed (int, optional): 随机种子 / Random seed

    Returns:
        dict: HTTP头/UA/TLS指纹数据 / HTTP headers/UA/TLS fingerprint data
    """
    if seed is not None:
        random.seed(seed)

    # User-Agent / User-Agent
    ua_list = USER_AGENTS.get(browser_type, USER_AGENTS["chrome_desktop"])
    user_agent = random.choice(ua_list)

    # HTTP头 / HTTP headers
    headers = {
        "user-agent": user_agent,
        "accept": random.choice(COMMON_HEADERS["accept"]),
        "accept-encoding": random.choice(COMMON_HEADERS["accept_encoding"]),
        "accept-language": random.choice(COMMON_HEADERS["accept_language"]),
        "connection": random.choice(["keep-alive", "keep-alive"]),
        "upgrade-insecure-requests": "1",
    }

    # 添加Chrome特有的头 / Add Chrome-specific headers
    if "Chrome" in user_agent:
        headers["sec-ch-ua"] = random.choice(COMMON_HEADERS["sec_ch_ua"])
        headers["sec-ch-ua-mobile"] = random.choice(COMMON_HEADERS["sec_ch_ua_mobile"])
        headers["sec-ch-ua-platform"] = random.choice(COMMON_HEADERS["sec_ch_ua_platform"])
        headers["sec-fetch-dest"] = "document"
        headers["sec-fetch-mode"] = "navigate"
        headers["sec-fetch-site"] = "none"
        headers["sec-fetch-user"] = "?1"

    # 添加Firefox特有的头 / Add Firefox-specific headers
    if "Firefox" in user_agent:
        headers["te"] = "trailers"

    # TLS指纹 / TLS fingerprint
    num_ciphers = random.randint(5, len(TLS_CIPHER_SUITES))
    cipher_suites = random.sample(TLS_CIPHER_SUITES, num_ciphers)

    num_extensions = random.randint(8, len(TLS_EXTENSIONS))
    tls_extensions = random.sample(TLS_EXTENSIONS, num_extensions)

    # JA3指纹哈希 / JA3 fingerprint hash
    ja3_data = f"{','.join(cipher_suites)}|{','.join(tls_extensions)}"
    ja3_hash = hashlib.md5(ja3_data.encode("utf-8")).hexdigest()

    # 解析UA信息 / Parse UA info
    ua_info = _parse_user_agent(user_agent)

    return {
        "user_agent": user_agent,
        "headers": headers,
        "header_count": len(headers),
        "tls": {
            "cipher_suites": cipher_suites,
            "extensions": tls_extensions,
            "ja3_hash": ja3_hash,
            "tls_version": random.choice(["TLS 1.2", "TLS 1.3"]),
        },
        "ua_info": ua_info,
        "browser_type": browser_type,
    }


def _parse_user_agent(ua_string):
    """解析User-Agent字符串

    Parse User-Agent string.

    Args:
        ua_string (str): UA字符串 / UA string

    Returns:
        dict: 解析结果 / Parse result
    """
    info = {
        "browser": "unknown",
        "browser_version": "unknown",
        "os": "unknown",
        "os_version": "unknown",
        "device": "desktop",
        "is_mobile": False,
    }

    ua_lower = ua_string.lower()

    # 浏览器检测 / Browser detection
    if "chrome" in ua_lower and "edg" not in ua_lower:
        info["browser"] = "Chrome"
        # 提取版本 / Extract version
        parts = ua_string.split("Chrome/")
        if len(parts) > 1:
            version = parts[1].split(" ")[0].split(".")[0]
            info["browser_version"] = version
    elif "firefox" in ua_lower:
        info["browser"] = "Firefox"
        parts = ua_string.split("Firefox/")
        if len(parts) > 1:
            version = parts[1].split(" ")[0].split(".")[0]
            info["browser_version"] = version
    elif "safari" in ua_lower and "chrome" not in ua_lower:
        info["browser"] = "Safari"
        parts = ua_string.split("Version/")
        if len(parts) > 1:
            version = parts[1].split(" ")[0].split(".")[0]
            info["browser_version"] = version

    # 操作系统检测 / OS detection
    if "windows" in ua_lower:
        info["os"] = "Windows"
        if "NT 10.0" in ua_string:
            info["os_version"] = "10/11"
    elif "macintosh" in ua_lower or "mac os" in ua_lower:
        info["os"] = "macOS"
    elif "linux" in ua_lower and "android" not in ua_lower:
        info["os"] = "Linux"
    elif "android" in ua_lower:
        info["os"] = "Android"
        info["device"] = "mobile"
        info["is_mobile"] = True
    elif "iphone" in ua_lower or "ipad" in ua_lower:
        info["os"] = "iOS"
        info["device"] = "mobile"
        info["is_mobile"] = True

    # 移动设备检测 / Mobile device detection
    if "mobile" in ua_lower:
        info["device"] = "mobile"
        info["is_mobile"] = True

    return info


def analyze_headers_fingerprint(fingerprint):
    """分析HTTP头/UA/TLS指纹特征

    Analyze HTTP headers/UA/TLS fingerprint characteristics.

    Args:
        fingerprint (dict): HTTP头指纹数据 / HTTP headers fingerprint data

    Returns:
        dict: 分析结果 / Analysis results
    """
    if not fingerprint:
        return {"error": "无效的HTTP头指纹数据", "risk_level": "unknown"}

    risk_factors = []
    risk_score = 0

    # 检查UA / Check User-Agent
    ua = fingerprint.get("user_agent", "")
    ua_info = fingerprint.get("ua_info", {})

    if not ua:
        risk_factors.append("User-Agent为空")
        risk_score += 30
    elif len(ua) < 50:
        risk_factors.append("User-Agent过短，可能为自动化工具")
        risk_score += 25

    # 检查是否为已知bot UA / Check if known bot UA
    bot_indicators = ["bot", "spider", "crawl", "python", "requests", "httpclient", "curl"]
    for indicator in bot_indicators:
        if indicator in ua.lower():
            risk_factors.append(f"User-Agent包含自动化工具标识: {indicator}")
            risk_score += 30
            break

    # 检查HTTP头完整性 / Check HTTP header completeness
    headers = fingerprint.get("headers", {})
    header_count = len(headers)

    if header_count < 5:
        risk_factors.append(f"HTTP头数量过少({header_count}个)")
        risk_score += 15

    # 检查Accept头 / Check Accept header
    accept = headers.get("accept", "")
    if not accept or accept == "*/*":
        risk_factors.append("Accept头异常")
        risk_score += 10

    # 检查Sec-Fetch头 / Check Sec-Fetch headers
    has_sec_fetch = any(k.startswith("sec-fetch") for k in headers)
    browser = ua_info.get("browser", "")
    if browser == "Chrome" and not has_sec_fetch:
        risk_factors.append("Chrome缺少Sec-Fetch头")
        risk_score += 15

    # 检查TLS指纹 / Check TLS fingerprint
    tls = fingerprint.get("tls", {})
    cipher_count = len(tls.get("cipher_suites", []))
    if cipher_count < 5:
        risk_factors.append(f"TLS密码套件过少({cipher_count}个)")
        risk_score += 10

    # 检查JA3指纹 / Check JA3 fingerprint
    ja3 = tls.get("ja3_hash", "")
    if not ja3:
        risk_factors.append("缺少JA3指纹")
        risk_score += 10

    if risk_score >= 50:
        risk_level = "high"
    elif risk_score >= 25:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "user_agent": ua[:80] + "..." if len(ua) > 80 else ua,
        "browser": browser,
        "header_count": header_count,
        "tls_cipher_count": cipher_count,
        "ja3_hash": ja3,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
    }
