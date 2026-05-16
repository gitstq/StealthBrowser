# -*- coding: utf-8 -*-
"""硬件指纹模块

Hardware fingerprint module.
分析CPU核心数、设备内存、GPU等硬件信息。
"""

import random


# 常见硬件配置 / Common hardware configurations
HARDWARE_PROFILES = {
    "desktop": {
        "cpu_cores": [2, 4, 6, 8, 12, 16],
        "device_memory": [2, 4, 8, 16, 32],
        "gpu_types": [
            {"vendor": "Intel", "model": "UHD Graphics 630"},
            {"vendor": "NVIDIA", "model": "GeForce GTX 1060"},
            {"vendor": "NVIDIA", "model": "GeForce GTX 1650"},
            {"vendor": "NVIDIA", "model": "GeForce RTX 3060"},
            {"vendor": "NVIDIA", "model": "GeForce RTX 4070"},
            {"vendor": "AMD", "model": "Radeon RX 580"},
            {"vendor": "AMD", "model": "Radeon RX 6700 XT"},
            {"vendor": "Intel", "model": "Iris Xe Graphics"},
        ],
    },
    "mobile": {
        "cpu_cores": [2, 4, 6, 8],
        "device_memory": [2, 3, 4, 6, 8],
        "gpu_types": [
            {"vendor": "Apple", "model": "A14 GPU"},
            {"vendor": "Apple", "model": "A15 GPU"},
            {"vendor": "Apple", "model": "A16 GPU"},
            {"vendor": "Qualcomm", "model": "Adreno 640"},
            {"vendor": "Qualcomm", "model": "Adreno 650"},
            {"vendor": "Qualcomm", "model": "Adreno 730"},
            {"vendor": "ARM", "model": "Mali-G78"},
            {"vendor": "ARM", "model": "Mali-G710"},
        ],
    },
}


def generate_hardware_fingerprint(device_type="desktop", seed=None):
    """生成模拟硬件指纹

    Generate simulated hardware fingerprint.

    Args:
        device_type (str): 设备类型 / Device type
        seed (int, optional): 随机种子 / Random seed

    Returns:
        dict: 硬件指纹数据 / Hardware fingerprint data
    """
    if seed is not None:
        random.seed(seed)

    profiles = HARDWARE_PROFILES.get(device_type, HARDWARE_PROFILES["desktop"])

    # CPU核心数 / CPU core count
    cpu_cores = random.choice(profiles["cpu_cores"])
    # hardwareConcurrency API返回值
    hardware_concurrency = cpu_cores

    # 设备内存 / Device memory
    device_memory = random.choice(profiles["device_memory"])

    # GPU信息 / GPU info
    gpu = random.choice(profiles["gpu_types"])

    # 最大触摸点数 / Max touch points
    if device_type == "mobile":
        max_touch_points = random.choice([1, 5, 10])
    else:
        max_touch_points = random.choice([0, 1, 5])

    # 平台信息 / Platform info
    if device_type == "desktop":
        platform = random.choice(["Win32", "MacIntel", "Linux x86_64"])
    else:
        platform = random.choice(["Linux armv8l", "MacIntel", "Win32"])

    # 处理器信息 / Processor info
    if platform == "Win32":
        platform_arch = "x86"
        os_name = "Windows"
    elif platform == "MacIntel":
        platform_arch = "x86_64"
        os_name = "macOS"
    else:
        platform_arch = "x86_64"
        os_name = "Linux"

    # 电池状态 / Battery status
    battery = {
        "charging": random.choice([True, False]),
        "charging_time": random.choice([0, 3600, 7200]) if not random.random() > 0.5 else 0,
        "discharging_time": random.choice([3600, 7200, 14400, 28800]),
        "level": round(random.uniform(0.1, 1.0), 2),
    }

    # 媒体设备 / Media devices
    media_devices = {
        "audioinput": random.randint(0, 3),
        "audiooutput": random.randint(1, 4),
        "videoinput": random.randint(0, 2),
    }

    # 连接类型 / Connection type
    connection = {
        "effective_type": random.choice(["4g", "3g", "wifi"]),
        "rtt": random.randint(0, 300),
        "downlink": round(random.uniform(1.5, 100), 2),
        "save_data": random.choice([True, False]),
    }

    return {
        "hardware_concurrency": hardware_concurrency,
        "device_memory": device_memory,
        "gpu_vendor": gpu["vendor"],
        "gpu_model": gpu["model"],
        "max_touch_points": max_touch_points,
        "platform": platform,
        "platform_arch": platform_arch,
        "os_name": os_name,
        "battery": battery,
        "media_devices": media_devices,
        "connection": connection,
        "device_type": device_type,
    }


def analyze_hardware_fingerprint(fingerprint):
    """分析硬件指纹特征

    Analyze hardware fingerprint characteristics.

    Args:
        fingerprint (dict): 硬件指纹数据 / Hardware fingerprint data

    Returns:
        dict: 分析结果 / Analysis results
    """
    if not fingerprint:
        return {"error": "无效的硬件指纹数据", "risk_level": "unknown"}

    risk_factors = []
    risk_score = 0

    # 检查CPU核心数 / Check CPU core count
    cores = fingerprint.get("hardware_concurrency", 0)
    if cores <= 1:
        risk_factors.append(f"CPU核心数异常({cores})，可能为虚拟机")
        risk_score += 25
    elif cores > 32:
        risk_factors.append(f"CPU核心数异常偏高({cores})，可能为服务器")
        risk_score += 15

    # 检查设备内存 / Check device memory
    mem = fingerprint.get("device_memory", 0)
    if mem < 2:
        risk_factors.append(f"设备内存过少({mem}GB)")
        risk_score += 20
    elif mem > 32:
        risk_factors.append(f"设备内存异常偏高({mem}GB)")
        risk_score += 10

    # 检查CPU与内存匹配度 / Check CPU-memory match
    if cores <= 2 and mem >= 16:
        risk_factors.append("CPU核心数与内存不匹配")
        risk_score += 15

    # 检查触摸点数 / Check touch points
    touch = fingerprint.get("max_touch_points", 0)
    device_type = fingerprint.get("device_type", "desktop")
    if device_type == "mobile" and touch == 0:
        risk_factors.append("移动设备不支持触摸")
        risk_score += 20

    # 检查平台一致性 / Check platform consistency
    platform = fingerprint.get("platform", "")
    os_name = fingerprint.get("os_name", "")
    if platform == "Win32" and os_name != "Windows":
        risk_factors.append("平台信息与OS不匹配")
        risk_score += 20
    elif platform == "MacIntel" and os_name != "macOS":
        risk_factors.append("平台信息与OS不匹配")
        risk_score += 20

    if risk_score >= 50:
        risk_level = "high"
    elif risk_score >= 25:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "cpu_cores": cores,
        "device_memory": mem,
        "platform": platform,
        "device_type": device_type,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
    }
