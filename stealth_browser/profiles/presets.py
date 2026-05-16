# -*- coding: utf-8 -*-
"""预设指纹配置模块

Preset fingerprint configuration module.
提供多种预设的浏览器指纹配置模板。
"""

from ..fingerprints import (
    generate_canvas_fingerprint,
    generate_webgl_fingerprint,
    generate_audio_fingerprint,
    generate_font_fingerprint,
    generate_hardware_fingerprint,
    generate_network_fingerprint,
    generate_behavior_fingerprint,
    generate_storage_fingerprint,
    generate_screen_fingerprint,
    generate_timezone_fingerprint,
    generate_headers_fingerprint,
)


def _build_preset(
    device_type="desktop",
    os_type="windows",
    locale="zh-CN",
    browser_type="chrome_desktop",
    seed=42,
):
    """构建预设配置的辅助函数

    Helper function to build preset configuration.

    Args:
        device_type (str): 设备类型 / Device type
        os_type (str): 操作系统类型 / OS type
        locale (str): 地区设置 / Locale
        browser_type (str): 浏览器类型 / Browser type
        seed (int): 随机种子 / Random seed

    Returns:
        dict: 预设配置 / Preset configuration
    """
    return {
        "canvas": generate_canvas_fingerprint(seed=seed),
        "webgl": generate_webgl_fingerprint(device_type=device_type, seed=seed + 1),
        "audio": generate_audio_fingerprint(seed=seed + 2),
        "fonts": generate_font_fingerprint(os_type=os_type, seed=seed + 3),
        "hardware": generate_hardware_fingerprint(device_type=device_type, seed=seed + 4),
        "screen": generate_screen_fingerprint(device_type=device_type, seed=seed + 5),
        "timezone": generate_timezone_fingerprint(locale=locale, seed=seed + 6),
        "headers": generate_headers_fingerprint(browser_type=browser_type, seed=seed + 7),
        "storage": generate_storage_fingerprint(seed=seed + 8),
        "network": generate_network_fingerprint(seed=seed + 9),
        "behavior": generate_behavior_fingerprint(device_type=device_type, seed=seed + 10),
    }


# 预设配置字典 / Preset configuration dictionary
PRESETS = {
    "desktop_chrome": {
        "name": "Chrome桌面版",
        "name_en": "Desktop Chrome",
        "description": "模拟Chrome浏览器桌面版指纹，适用于常规桌面浏览场景",
        "device_type": "desktop",
    },
    "desktop_firefox": {
        "name": "Firefox桌面版",
        "name_en": "Desktop Firefox",
        "description": "模拟Firefox浏览器桌面版指纹，适用于需要Firefox兼容性的场景",
        "device_type": "desktop",
    },
    "mobile_safari": {
        "name": "iOS Safari",
        "name_en": "Mobile Safari",
        "description": "模拟iOS Safari浏览器指纹，适用于移动端iOS场景",
        "device_type": "mobile",
    },
    "mobile_chrome": {
        "name": "Android Chrome",
        "name_en": "Mobile Chrome",
        "description": "模拟Android Chrome浏览器指纹，适用于移动端Android场景",
        "device_type": "mobile",
    },
    "bot_friendly": {
        "name": "爬虫友好",
        "name_en": "Bot Friendly",
        "description": "爬虫友好指纹配置，降低被检测概率，适用于自动化采集",
        "device_type": "desktop",
    },
    "stealth_max": {
        "name": "最大隐身",
        "name_en": "Maximum Stealth",
        "description": "最大隐身配置，提供最高级别的反检测能力",
        "device_type": "desktop",
    },
}


def get_preset(preset_name):
    """获取预设指纹配置

    Get preset fingerprint configuration.

    Args:
        preset_name (str): 预设名称 / Preset name

    Returns:
        dict or None: 预设配置 / Preset configuration
    """
    preset_info = PRESETS.get(preset_name)
    if not preset_info:
        return None

    device_type = preset_info["device_type"]

    # 根据预设类型使用不同的参数 / Use different parameters based on preset type
    if preset_name == "desktop_chrome":
        return _build_preset(
            device_type="desktop",
            os_type="windows",
            locale="zh-CN",
            browser_type="chrome_desktop",
            seed=100,
        )
    elif preset_name == "desktop_firefox":
        return _build_preset(
            device_type="desktop",
            os_type="windows",
            locale="zh-CN",
            browser_type="firefox_desktop",
            seed=200,
        )
    elif preset_name == "mobile_safari":
        return _build_preset(
            device_type="mobile",
            os_type="ios",
            locale="zh-CN",
            browser_type="safari_mobile",
            seed=300,
        )
    elif preset_name == "mobile_chrome":
        return _build_preset(
            device_type="mobile",
            os_type="android",
            locale="zh-CN",
            browser_type="chrome_mobile",
            seed=400,
        )
    elif preset_name == "bot_friendly":
        config = _build_preset(
            device_type="desktop",
            os_type="windows",
            locale="zh-CN",
            browser_type="chrome_desktop",
            seed=500,
        )
        # 爬虫友好调整 / Bot-friendly adjustments
        config["behavior"]["bot_probability"] = 0.05  # 低机器人概率
        config["network"]["ip_type"] = "residential"  # 住宅IP
        config["network"]["has_proxy"] = False
        config["storage"]["cookie"]["enabled"] = True
        config["storage"]["localStorage"]["supported"] = True
        return config
    elif preset_name == "stealth_max":
        config = _build_preset(
            device_type="desktop",
            os_type="windows",
            locale="zh-CN",
            browser_type="chrome_desktop",
            seed=600,
        )
        # 最大隐身调整 / Maximum stealth adjustments
        config["behavior"]["bot_probability"] = 0.02  # 极低机器人概率
        config["behavior"]["mouse"]["has_human_pattern"] = True
        config["behavior"]["mouse"]["is_smooth"] = True
        config["behavior"]["keyboard"]["has_typing_pattern"] = True
        config["network"]["ip_type"] = "residential"
        config["network"]["webrtc_support"] = False  # 禁用WebRTC
        config["network"]["has_proxy"] = False
        config["network"]["doh_enabled"] = True
        config["storage"]["dnt"] = None  # 不发送DNT
        config["storage"]["gpc_enabled"] = False  # 不启用GPC
        config["webgl"]["is_headless"] = False
        return config

    return None


def list_presets():
    """列出所有可用预设

    List all available presets.

    Returns:
        list: 预设信息列表 / Preset info list
    """
    result = []
    for name, info in PRESETS.items():
        result.append({
            "name": name,
            "display_name": info["name"],
            "description": info["description"],
            "device_type": info["device_type"],
        })
    return result
