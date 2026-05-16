# -*- coding: utf-8 -*-
"""Canvas指纹分析模块

Canvas fingerprint analysis module.
分析Canvas 2D渲染指纹，用于浏览器唯一性识别。
"""

import hashlib
import random


# 常见Canvas指纹哈希值(模拟数据集) / Common Canvas fingerprint hashes (simulated dataset)
COMMON_CANVAS_HASHES = [
    "a1b2c3d4e5f6789012345678abcdef01",
    "b2c3d4e5f67890123456789abcdef012",
    "c3d4e5f678901234567890abcdef0123",
    "d4e5f6789012345678901abcdef01234",
    "e5f67890123456789012abcdef012345",
    "1234567890abcdef1234567890abcdef",
    "abcdef1234567890abcdef1234567890",
    "fedcba0987654321fedcba0987654321",
    "cafebabedeadbeefcafebabedeadbeef",
    "0102030405060708090a0b0c0d0e0f10",
]


def generate_canvas_fingerprint(seed=None):
    """生成模拟Canvas指纹

    Generate simulated Canvas fingerprint.

    Canvas指纹通过渲染特定文本和图形到Canvas上，
    然后计算像素数据的哈希值来生成唯一标识。

    Args:
        seed (int, optional): 随机种子 / Random seed

    Returns:
        dict: Canvas指纹数据 / Canvas fingerprint data
    """
    if seed is not None:
        random.seed(seed)

    # 模拟Canvas渲染参数 / Simulate Canvas rendering parameters
    text = "StealthBrowser, Inc. 🌐"
    font_size = random.choice([10, 12, 14, 16, 18, 20, 24, 32])
    font_family = random.choice([
        "Arial", "Helvetica", "Times New Roman", "Courier New",
        "Verdana", "Georgia", "Comic Sans MS", "Impact",
    ])
    fill_style = f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})"
    text_baseline = random.choice(["top", "hanging", "middle", "alphabetic", "ideographic", "bottom"])

    # 模拟渲染结果哈希 / Simulate rendered result hash
    render_data = f"{text}|{font_size}|{font_family}|{fill_style}|{text_baseline}"
    if seed is not None:
        render_data += f"|{seed}"

    canvas_hash = hashlib.md5(render_data.encode("utf-8")).hexdigest()

    # 模拟像素数据摘要 / Simulate pixel data summary
    pixel_count = random.randint(10000, 50000)
    unique_colors = random.randint(50, 500)

    return {
        "hash": canvas_hash,
        "hash_algorithm": "md5",
        "render_text": text,
        "font_size": font_size,
        "font_family": font_family,
        "fill_style": fill_style,
        "text_baseline": text_baseline,
        "canvas_width": 280,
        "canvas_height": 60,
        "pixel_count": pixel_count,
        "unique_colors": unique_colors,
        "is_stable": random.random() > 0.1,  # 90%概率稳定 / 90% chance stable
    }


def analyze_canvas_fingerprint(fingerprint):
    """分析Canvas指纹特征

    Analyze Canvas fingerprint characteristics.

    Args:
        fingerprint (dict): Canvas指纹数据 / Canvas fingerprint data

    Returns:
        dict: 分析结果 / Analysis results
    """
    if not fingerprint or "hash" not in fingerprint:
        return {"error": "无效的Canvas指纹数据", "risk_level": "unknown"}

    canvas_hash = fingerprint["hash"]

    # 检查是否为常见指纹 / Check if it's a common fingerprint
    is_common = canvas_hash in COMMON_CANVAS_HASHES

    # 检查哈希熵 / Check hash entropy
    hash_chars = list(canvas_hash)
    unique_chars = len(set(hash_chars))
    entropy = 0.0
    from collections import Counter
    counter = Counter(hash_chars)
    total = len(hash_chars)
    import math
    for count in counter.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)

    # 风险评估 / Risk assessment
    risk_factors = []
    risk_score = 0

    if is_common:
        risk_factors.append("指纹哈希值在常见数据集中出现")
        risk_score += 30

    if entropy < 3.0:
        risk_factors.append("哈希熵值偏低，可能为伪造指纹")
        risk_score += 20

    if not fingerprint.get("is_stable", True):
        risk_factors.append("指纹不稳定，多次渲染结果不一致")
        risk_score += 25

    if fingerprint.get("unique_colors", 0) < 100:
        risk_factors.append("颜色数量异常偏少")
        risk_score += 15

    if risk_score >= 50:
        risk_level = "high"
    elif risk_score >= 25:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "hash": canvas_hash,
        "is_common": is_common,
        "entropy": round(entropy, 4),
        "unique_chars": unique_chars,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "stability": fingerprint.get("is_stable", True),
    }


def compare_canvas_fingerprints(fp_a, fp_b):
    """对比两个Canvas指纹

    Compare two Canvas fingerprints.

    Args:
        fp_a (dict): 指纹A / Fingerprint A
        fp_b (dict): 指纹B / Fingerprint B

    Returns:
        dict: 对比结果 / Comparison results
    """
    hash_a = fp_a.get("hash", "") if fp_a else ""
    hash_b = fp_b.get("hash", "") if fp_b else ""

    is_same = hash_a == hash_b

    # 计算汉明距离 / Calculate Hamming distance
    hamming_distance = 0
    if hash_a and hash_b and len(hash_a) == len(hash_b):
        for a, b in zip(hash_a, hash_b):
            if a != b:
                hamming_distance += 1

    return {
        "is_identical": is_same,
        "hamming_distance": hamming_distance,
        "similarity": round(1.0 - hamming_distance / max(len(hash_a), 1), 4),
        "hash_a": hash_a[:16] + "...",
        "hash_b": hash_b[:16] + "...",
    }
