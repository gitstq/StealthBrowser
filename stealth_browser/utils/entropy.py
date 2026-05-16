# -*- coding: utf-8 -*-
"""熵值计算工具模块

Entropy calculation utility module.
提供信息熵、香农熵等计算功能。
"""

import math
from collections import Counter


def shannon_entropy(data):
    """计算香农信息熵

    Calculate Shannon information entropy.

    Args:
        data (list/str): 输入数据序列 / Input data sequence

    Returns:
        float: 信息熵值(比特) / Information entropy in bits
    """
    if not data:
        return 0.0

    # 统计频率 / Count frequencies
    counter = Counter(data)
    total = len(data)

    entropy = 0.0
    for count in counter.values():
        if count > 0:
            probability = count / total
            entropy -= probability * math.log2(probability)

    return entropy


def normalized_entropy(data):
    """计算归一化熵值(0-1范围)

    Calculate normalized entropy (0-1 range).

    Args:
        data (list/str): 输入数据序列 / Input data sequence

    Returns:
        float: 归一化熵值 / Normalized entropy value
    """
    entropy = shannon_entropy(data)
    if not data:
        return 0.0

    # 最大熵 = log2(n) / Maximum entropy = log2(n)
    max_entropy = math.log2(len(set(data))) if len(set(data)) > 1 else 1.0
    if max_entropy == 0:
        return 0.0

    return entropy / max_entropy


def hash_entropy(hash_value):
    """计算哈希值的熵

    Calculate entropy of a hash value.

    Args:
        hash_value (str): 十六进制哈希字符串 / Hexadecimal hash string

    Returns:
        float: 熵值 / Entropy value
    """
    if not hash_value:
        return 0.0

    # 统计每个字符的出现频率 / Count frequency of each character
    counter = Counter(hash_value.lower())
    total = len(hash_value)

    entropy = 0.0
    for count in counter.values():
        probability = count / total
        entropy -= probability * math.log2(probability)

    return entropy


def fingerprint_uniqueness_score(fingerprint_data):
    """计算指纹唯一性评分

    Calculate fingerprint uniqueness score.

    基于指纹各维度的熵值加权计算唯一性。
    Weighted calculation of uniqueness based on entropy of each dimension.

    Args:
        fingerprint_data (dict): 指纹数据字典 / Fingerprint data dictionary

    Returns:
        dict: 包含熵值和唯一性评分的字典 / Dict with entropy and uniqueness scores
    """
    results = {}
    total_weight = 0.0
    weighted_entropy = 0.0

    # 各维度的权重 / Weights for each dimension
    dimension_weights = {
        "canvas": 0.15,
        "webgl": 0.12,
        "audio": 0.08,
        "fonts": 0.10,
        "hardware": 0.08,
        "screen": 0.06,
        "timezone": 0.04,
        "language": 0.04,
        "platform": 0.05,
        "user_agent": 0.08,
        "headers": 0.05,
        "storage": 0.03,
        "webrtc": 0.04,
        "touch": 0.03,
        "media_devices": 0.03,
        "battery": 0.02,
        "connection": 0.02,
        "behavior": 0.02,
    }

    for key, value in fingerprint_data.items():
        if isinstance(value, str):
            ent = hash_entropy(value)
        elif isinstance(value, (list, tuple)):
            ent = shannon_entropy(value) if value else 0.0
        elif isinstance(value, (int, float)):
            # 数值型：用值的范围估算熵 / Numeric: estimate entropy from value range
            ent = min(math.log2(max(abs(value), 1) + 1), 10.0)
        else:
            ent = 0.0

        weight = dimension_weights.get(key, 0.02)
        results[key] = {
            "entropy": round(ent, 4),
            "weight": weight,
            "weighted_entropy": round(ent * weight, 4),
        }
        weighted_entropy += ent * weight
        total_weight += weight

    # 归一化唯一性评分(0-100) / Normalized uniqueness score (0-100)
    if total_weight > 0:
        avg_entropy = weighted_entropy / total_weight
    else:
        avg_entropy = 0.0

    # 将平均熵映射到0-100分 / Map average entropy to 0-100 score
    uniqueness = min(avg_entropy / 4.0 * 100, 100.0)

    results["_summary"] = {
        "total_weighted_entropy": round(weighted_entropy, 4),
        "average_entropy": round(avg_entropy, 4),
        "uniqueness_score": round(uniqueness, 2),
    }

    return results


def calculate_dimension_entropy(value):
    """计算单个维度的熵值

    Calculate entropy for a single dimension.

    Args:
        value: 指纹维度值 / Fingerprint dimension value

    Returns:
        float: 熵值 / Entropy value
    """
    if value is None:
        return 0.0
    if isinstance(value, str):
        return hash_entropy(value)
    elif isinstance(value, (list, tuple)):
        return shannon_entropy(value) if value else 0.0
    elif isinstance(value, (int, float)):
        return min(math.log2(max(abs(value), 1) + 1), 10.0)
    elif isinstance(value, bool):
        return 1.0  # 布尔值的最大熵 / Max entropy for boolean
    elif isinstance(value, dict):
        # 字典取所有值的熵 / Take entropy of all values in dict
        all_values = []
        for v in value.values():
            if isinstance(v, str):
                all_values.extend(list(v))
            elif isinstance(v, (list, tuple)):
                all_values.extend([str(x) for x in v])
            else:
                all_values.append(str(v))
        return shannon_entropy(all_values) if all_values else 0.0
    return 0.0
