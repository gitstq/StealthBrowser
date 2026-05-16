# -*- coding: utf-8 -*-
"""存储指纹模块

Storage fingerprint module.
分析Cookie、LocalStorage、IndexedDB等存储特征。
"""

import random


def generate_storage_fingerprint(seed=None):
    """生成模拟存储指纹

    Generate simulated storage fingerprint.

    Args:
        seed (int, optional): 随机种子 / Random seed

    Returns:
        dict: 存储指纹数据 / Storage fingerprint data
    """
    if seed is not None:
        random.seed(seed)

    # Cookie支持 / Cookie support
    cookie_enabled = random.choice([True, True, True, False])  # 75%启用
    cookie_count = random.randint(0, 50) if cookie_enabled else 0
    third_party_cookie = random.choice([True, True, False]) if cookie_enabled else False

    # LocalStorage / LocalStorage
    localStorage_supported = random.choice([True, True, True, False])
    localStorage_size = random.randint(0, 5000000) if localStorage_supported else 0  # 最大5MB
    localStorage_keys = random.randint(0, 100) if localStorage_supported else 0

    # SessionStorage / SessionStorage
    sessionStorage_supported = localStorage_supported
    sessionStorage_size = random.randint(0, 5000000) if sessionStorage_supported else 0

    # IndexedDB / IndexedDB
    indexeddb_supported = random.choice([True, True, True, False])
    indexeddb_databases = random.randint(0, 10) if indexeddb_supported else 0

    # WebSQL (已废弃但部分浏览器仍支持) / WebSQL (deprecated but some browsers still support)
    websql_supported = random.choice([True, False, False])

    # Cache API / Cache API
    cache_api_supported = random.choice([True, True, True, False])
    cache_storage_count = random.randint(0, 5) if cache_api_supported else 0

    # Service Worker / Service Worker
    service_worker_supported = random.choice([True, True, True, False])

    # 存储配额 / Storage quota
    storage_quota = random.choice([
        1073741824,   # 1GB
        2147483648,   # 2GB
        5368709120,   # 5GB
        10737418240,  # 10GB
        None,         # 未知
    ])
    storage_used = random.randint(0, 100000000) if storage_quota else 0  # 最大100MB已用

    # Do Not Track / Do Not Track
    dnt = random.choice(["1", "0", None])

    # Global Privacy Control / GPC
    gpc_enabled = random.choice([True, False, False])

    return {
        "cookie": {
            "enabled": cookie_enabled,
            "count": cookie_count,
            "third_party_allowed": third_party_cookie,
            "max_per_domain": 50,
        },
        "localStorage": {
            "supported": localStorage_supported,
            "estimated_size": localStorage_size,
            "key_count": localStorage_keys,
        },
        "sessionStorage": {
            "supported": sessionStorage_supported,
            "estimated_size": sessionStorage_size,
        },
        "indexedDB": {
            "supported": indexeddb_supported,
            "database_count": indexeddb_databases,
        },
        "webSQL": {
            "supported": websql_supported,
        },
        "cacheAPI": {
            "supported": cache_api_supported,
            "cache_count": cache_storage_count,
        },
        "serviceWorker": {
            "supported": service_worker_supported,
        },
        "storage_quota": {
            "quota": storage_quota,
            "used": storage_used,
            "usage_ratio": round(storage_used / storage_quota, 4) if storage_quota else None,
        },
        "dnt": dnt,
        "gpc_enabled": gpc_enabled,
    }


def analyze_storage_fingerprint(fingerprint):
    """分析存储指纹特征

    Analyze storage fingerprint characteristics.

    Args:
        fingerprint (dict): 存储指纹数据 / Storage fingerprint data

    Returns:
        dict: 分析结果 / Analysis results
    """
    if not fingerprint:
        return {"error": "无效的存储指纹数据", "risk_level": "unknown"}

    risk_factors = []
    risk_score = 0

    # 检查Cookie / Check Cookie
    cookie = fingerprint.get("cookie", {})
    if not cookie.get("enabled", True):
        risk_factors.append("Cookie被禁用，可能导致网站功能异常")
        risk_score += 15

    # 检查LocalStorage / Check LocalStorage
    ls = fingerprint.get("localStorage", {})
    if not ls.get("supported", True):
        risk_factors.append("LocalStorage不可用，可能为隐私模式")
        risk_score += 20

    # 检查IndexedDB / Check IndexedDB
    idb = fingerprint.get("indexedDB", {})
    if not idb.get("supported", True):
        risk_factors.append("IndexedDB不可用")
        risk_score += 10

    # 检查Service Worker / Check Service Worker
    sw = fingerprint.get("serviceWorker", {})
    if not sw.get("supported", True):
        risk_factors.append("Service Worker不可用，可能为旧版浏览器")
        risk_score += 5

    # 检查DNT/GPC / Check DNT/GPC
    dnt = fingerprint.get("dnt")
    gpc = fingerprint.get("gpc_enabled", False)
    if dnt == "1" and gpc:
        risk_factors.append("同时启用DNT和GPC，隐私特征明显")
        risk_score += 10

    # 检查存储使用率 / Check storage usage
    quota = fingerprint.get("storage_quota", {})
    usage_ratio = quota.get("usage_ratio")
    if usage_ratio is not None and usage_ratio > 0.9:
        risk_factors.append("存储空间使用率过高")
        risk_score += 5

    if risk_score >= 50:
        risk_level = "high"
    elif risk_score >= 25:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "cookie_enabled": cookie.get("enabled", True),
        "localStorage_supported": ls.get("supported", True),
        "indexeddb_supported": idb.get("supported", True),
        "service_worker_supported": sw.get("supported", True),
        "dnt": dnt,
        "gpc_enabled": gpc,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
    }
