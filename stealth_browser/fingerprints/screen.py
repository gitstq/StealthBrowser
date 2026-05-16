# -*- coding: utf-8 -*-
"""屏幕指纹模块

Screen fingerprint module.
分析屏幕分辨率、色深、像素比等屏幕特征。
"""

import random


# 常见屏幕分辨率 / Common screen resolutions
COMMON_RESOLUTIONS = {
    "desktop": [
        (1920, 1080),  # Full HD
        (2560, 1440),  # QHD
        (3840, 2160),  # 4K UHD
        (1366, 768),   # HD
        (1536, 864),   # HD+
        (1440, 900),   # WXGA+
        (1680, 1050),  # WSXGA+
        (2560, 1080),  # UW-FHD
        (3440, 1440),  # UW-QHD
        (1280, 720),   # HD 720p
    ],
    "mobile": [
        (390, 844),    # iPhone 14
        (414, 896),    # iPhone 11 Pro Max
        (375, 667),    # iPhone SE
        (393, 873),    # Pixel 7
        (412, 915),    # Samsung Galaxy S23
        (360, 780),    # Common Android
        (384, 854),    # Common Android
        (414, 896),    # iPhone XR
        (320, 568),    # iPhone SE 1st gen
        (430, 932),    # iPhone 14 Pro Max
    ],
}


def generate_screen_fingerprint(device_type="desktop", seed=None):
    """生成模拟屏幕指纹

    Generate simulated screen fingerprint.

    Args:
        device_type (str): 设备类型 / Device type
        seed (int, optional): 随机种子 / Random seed

    Returns:
        dict: 屏幕指纹数据 / Screen fingerprint data
    """
    if seed is not None:
        random.seed(seed)

    resolutions = COMMON_RESOLUTIONS.get(device_type, COMMON_RESOLUTIONS["desktop"])
    screen_w, screen_h = random.choice(resolutions)

    # 可用屏幕区域(减去任务栏等) / Available screen area (minus taskbar etc.)
    if device_type == "desktop":
        avail_w = screen_w
        avail_h = screen_h - random.choice([40, 48, 56])  # 任务栏高度
    else:
        avail_w = screen_w
        avail_h = screen_h

    # 设备像素比 / Device pixel ratio
    if device_type == "mobile":
        dpr = random.choice([2.0, 2.625, 3.0, 3.5])
    else:
        dpr = random.choice([1.0, 1.25, 1.5, 1.75, 2.0])

    # 颜色深度 / Color depth
    color_depth = random.choice([24, 30, 32])

    # 像素深度 / Pixel depth
    pixel_depth = color_depth

    # 视口大小 / Viewport size
    viewport_w = avail_w
    viewport_h = avail_h

    # 物理像素 / Physical pixels
    physical_w = int(screen_w * dpr)
    physical_h = int(screen_h * dpr)

    # 屏幕方向 / Screen orientation
    if device_type == "mobile":
        orientation = random.choice(["portrait-primary", "landscape-primary"])
    else:
        orientation = "landscape-primary"

    # HDR支持 / HDR support
    hdr_support = random.choice([True, False, False])

    # 色域 / Color gamut
    color_gamut = random.choice(["srgb", "p3", "rec2020"])

    # 对比度偏好 / Contrast preference
    contrast_preference = random.choice(["no-preference", "more", "less", "custom"])

    # 减少动画偏好 / Reduced motion preference
    prefers_reduced_motion = random.choice([True, False, False])

    # 暗色模式偏好 / Dark mode preference
    prefers_color_scheme = random.choice(["light", "dark", "no-preference"])

    return {
        "screen_width": screen_w,
        "screen_height": screen_h,
        "available_width": avail_w,
        "available_height": avail_h,
        "viewport_width": viewport_w,
        "viewport_height": viewport_h,
        "device_pixel_ratio": dpr,
        "color_depth": color_depth,
        "pixel_depth": pixel_depth,
        "physical_width": physical_w,
        "physical_height": physical_h,
        "orientation": orientation,
        "hdr_support": hdr_support,
        "color_gamut": color_gamut,
        "contrast_preference": contrast_preference,
        "prefers_reduced_motion": prefers_reduced_motion,
        "prefers_color_scheme": prefers_color_scheme,
        "device_type": device_type,
    }


def analyze_screen_fingerprint(fingerprint):
    """分析屏幕指纹特征

    Analyze screen fingerprint characteristics.

    Args:
        fingerprint (dict): 屏幕指纹数据 / Screen fingerprint data

    Returns:
        dict: 分析结果 / Analysis results
    """
    if not fingerprint:
        return {"error": "无效的屏幕指纹数据", "risk_level": "unknown"}

    risk_factors = []
    risk_score = 0

    device_type = fingerprint.get("device_type", "desktop")

    # 检查分辨率 / Check resolution
    w = fingerprint.get("screen_width", 0)
    h = fingerprint.get("screen_height", 0)
    resolution = (w, h)

    common = COMMON_RESOLUTIONS.get(device_type, [])
    if resolution not in common:
        risk_factors.append(f"非常见分辨率: {w}x{h}")
        risk_score += 10

    # 检查像素比 / Check device pixel ratio
    dpr = fingerprint.get("device_pixel_ratio", 1.0)
    if device_type == "mobile" and dpr < 1.5:
        risk_factors.append(f"移动设备像素比偏低: {dpr}")
        risk_score += 15
    elif device_type == "desktop" and dpr > 2.0:
        risk_factors.append(f"桌面设备像素比偏高: {dpr}")
        risk_score += 10

    # 检查色深 / Check color depth
    cd = fingerprint.get("color_depth", 0)
    if cd not in (24, 30, 32):
        risk_factors.append(f"异常色深: {cd}")
        risk_score += 15

    # 检查可用区域 / Check available area
    avail_h = fingerprint.get("available_height", 0)
    screen_h = fingerprint.get("screen_height", 0)
    if device_type == "desktop" and avail_h == screen_h:
        risk_factors.append("可用高度等于屏幕高度，未检测到任务栏")
        risk_score += 10

    # 检查视口与屏幕关系 / Check viewport-screen relationship
    vp_w = fingerprint.get("viewport_width", 0)
    vp_h = fingerprint.get("viewport_height", 0)
    if vp_w > w or vp_h > h:
        risk_factors.append("视口尺寸大于屏幕尺寸")
        risk_score += 20

    if risk_score >= 50:
        risk_level = "high"
    elif risk_score >= 25:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "resolution": f"{w}x{h}",
        "device_pixel_ratio": dpr,
        "color_depth": cd,
        "is_common_resolution": resolution in common,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
    }
