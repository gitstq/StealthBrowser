# -*- coding: utf-8 -*-
"""行为指纹模块

Behavior fingerprint module.
分析鼠标移动、键盘输入、触摸等行为特征。
"""

import math
import random


def generate_behavior_fingerprint(device_type="desktop", seed=None):
    """生成模拟行为指纹

    Generate simulated behavior fingerprint.

    Args:
        device_type (str): 设备类型 / Device type
        seed (int, optional): 随机种子 / Random seed

    Returns:
        dict: 行为指纹数据 / Behavior fingerprint data
    """
    if seed is not None:
        random.seed(seed)

    # 鼠标移动特征 / Mouse movement characteristics
    mouse_data = _generate_mouse_data(seed)

    # 键盘输入特征 / Keyboard input characteristics
    keyboard_data = _generate_keyboard_data(seed)

    # 触摸特征 / Touch characteristics
    touch_data = _generate_touch_data(device_type, seed)

    # 滚动行为 / Scroll behavior
    scroll_data = _generate_scroll_data(seed)

    # 页面交互 / Page interaction
    interaction = {
        "time_on_page": random.uniform(5, 300),  # 页面停留时间(秒)
        "click_count": random.randint(0, 50),
        "scroll_depth": round(random.uniform(0.1, 1.0), 2),  # 滚动深度比例
        "form_interaction": random.choice([True, False]),
        "mouse_movement_distance": round(random.uniform(100, 5000), 2),  # 鼠标移动总距离(像素)
    }

    # 行为评分 / Behavior score
    bot_probability = _calculate_bot_probability(mouse_data, keyboard_data, touch_data)

    return {
        "mouse": mouse_data,
        "keyboard": keyboard_data,
        "touch": touch_data,
        "scroll": scroll_data,
        "interaction": interaction,
        "bot_probability": bot_probability,
        "device_type": device_type,
    }


def _generate_mouse_data(seed=None):
    """生成鼠标移动数据

    Generate mouse movement data.

    Returns:
        dict: 鼠标移动特征 / Mouse movement characteristics
    """
    # 生成模拟鼠标轨迹 / Generate simulated mouse trajectory
    num_points = random.randint(20, 100)
    points = []
    x, y = random.randint(100, 500), random.randint(100, 500)
    for _ in range(num_points):
        dx = random.gauss(0, 15)
        dy = random.gauss(0, 15)
        x = max(0, min(1920, x + dx))
        y = max(0, min(1080, y + dy))
        points.append({"x": round(x, 2), "y": round(y, 2)})

    # 计算鼠标特征 / Calculate mouse characteristics
    distances = []
    speeds = []
    for i in range(1, len(points)):
        dx = points[i]["x"] - points[i - 1]["x"]
        dy = points[i]["y"] - points[i - 1]["y"]
        dist = math.sqrt(dx * dx + dy * dy)
        distances.append(dist)
        speeds.append(dist * random.uniform(30, 120))  # 像素/秒

    avg_speed = sum(speeds) / len(speeds) if speeds else 0
    max_speed = max(speeds) if speeds else 0
    min_speed = min(speeds) if speeds else 0

    # 计算方向变化 / Calculate direction changes
    direction_changes = 0
    for i in range(2, len(points)):
        dx1 = points[i - 1]["x"] - points[i - 2]["x"]
        dy1 = points[i - 1]["y"] - points[i - 2]["y"]
        dx2 = points[i]["x"] - points[i - 1]["x"]
        dy2 = points[i]["y"] - points[i - 1]["y"]
        if dx1 * dx2 + dy1 * dy2 < 0:  # 方向反转 / Direction reversal
            direction_changes += 1

    return {
        "point_count": num_points,
        "avg_speed": round(avg_speed, 2),
        "max_speed": round(max_speed, 2),
        "min_speed": round(min_speed, 2),
        "total_distance": round(sum(distances), 2),
        "direction_changes": direction_changes,
        "is_smooth": random.random() > 0.3,  # 70%概率平滑
        "has_human_pattern": random.random() > 0.2,  # 80%概率有人类模式
    }


def _generate_keyboard_data(seed=None):
    """生成键盘输入数据

    Generate keyboard input data.

    Returns:
        dict: 键盘输入特征 / Keyboard input characteristics
    """
    # 模拟按键间隔 / Simulate key press intervals
    num_keys = random.randint(10, 100)
    key_intervals = [random.lognormvariate(math.log(100), 0.8) for _ in range(num_keys)]

    avg_interval = sum(key_intervals) / len(key_intervals) if key_intervals else 0
    std_interval = (sum((x - avg_interval) ** 2 for x in key_intervals) / len(key_intervals)) ** 0.5 if key_intervals else 0

    # 模拟按键持续时间 / Simulate key press duration
    key_durations = [random.gauss(80, 25) for _ in range(num_keys)]
    avg_duration = sum(key_durations) / len(key_durations) if key_durations else 0

    return {
        "key_count": num_keys,
        "avg_interval_ms": round(avg_interval, 2),
        "std_interval_ms": round(std_interval, 2),
        "avg_key_duration_ms": round(avg_duration, 2),
        "has_typing_pattern": random.random() > 0.3,
        "error_rate": round(random.uniform(0, 0.05), 4),  # 打字错误率
    }


def _generate_touch_data(device_type="desktop", seed=None):
    """生成触摸数据

    Generate touch data.

    Args:
        device_type (str): 设备类型 / Device type

    Returns:
        dict: 触摸特征 / Touch characteristics
    """
    if device_type != "mobile":
        return {
            "touch_supported": False,
            "touch_points": 0,
            "avg_pressure": 0,
            "avg_radius_x": 0,
            "avg_radius_y": 0,
        }

    num_touches = random.randint(5, 30)
    pressures = [random.uniform(0.1, 1.0) for _ in range(num_touches)]
    radius_x = [random.uniform(5, 30) for _ in range(num_touches)]
    radius_y = [random.uniform(5, 30) for _ in range(num_touches)]

    return {
        "touch_supported": True,
        "touch_points": num_touches,
        "avg_pressure": round(sum(pressures) / len(pressures), 4),
        "avg_radius_x": round(sum(radius_x) / len(radius_x), 2),
        "avg_radius_y": round(sum(radius_y) / len(radius_y), 2),
        "multi_touch": random.choice([True, False]),
    }


def _generate_scroll_data(seed=None):
    """生成滚动数据

    Generate scroll data.

    Returns:
        dict: 滚动特征 / Scroll characteristics
    """
    num_scroll_events = random.randint(5, 50)
    scroll_deltas = [random.gauss(0, 50) for _ in range(num_scroll_events)]
    scroll_speeds = [abs(d) * random.uniform(1, 5) for d in scroll_deltas]

    return {
        "scroll_events": num_scroll_events,
        "avg_delta": round(sum(scroll_deltas) / len(scroll_deltas), 2),
        "avg_speed": round(sum(scroll_speeds) / len(scroll_speeds), 2),
        "max_speed": round(max(scroll_speeds), 2) if scroll_speeds else 0,
        "has_smooth_scroll": random.random() > 0.4,
        "scroll_pattern": random.choice(["linear", "accelerating", "decelerating", "variable"]),
    }


def _calculate_bot_probability(mouse_data, keyboard_data, touch_data):
    """计算机器人概率

    Calculate bot probability.

    Args:
        mouse_data (dict): 鼠标数据 / Mouse data
        keyboard_data (dict): 键盘数据 / Keyboard data
        touch_data (dict): 触摸数据 / Touch data

    Returns:
        float: 机器人概率(0-1) / Bot probability (0-1)
    """
    bot_score = 0.0

    # 鼠标特征评估 / Mouse feature assessment
    if not mouse_data.get("has_human_pattern", True):
        bot_score += 0.25
    if not mouse_data.get("is_smooth", True):
        bot_score += 0.15
    if mouse_data.get("direction_changes", 0) < 2:
        bot_score += 0.1

    # 键盘特征评估 / Keyboard feature assessment
    if not keyboard_data.get("has_typing_pattern", True):
        bot_score += 0.2
    if keyboard_data.get("std_interval_ms", 0) < 10:
        bot_score += 0.15  # 间隔过于均匀，像机器人

    # 触摸特征评估 / Touch feature assessment
    if touch_data.get("touch_supported", False):
        if touch_data.get("avg_pressure", 0) < 0.2:
            bot_score += 0.1

    return round(min(bot_score, 1.0), 4)


def analyze_behavior_fingerprint(fingerprint):
    """分析行为指纹特征

    Analyze behavior fingerprint characteristics.

    Args:
        fingerprint (dict): 行为指纹数据 / Behavior fingerprint data

    Returns:
        dict: 分析结果 / Analysis results
    """
    if not fingerprint:
        return {"error": "无效的行为指纹数据", "risk_level": "unknown"}

    risk_factors = []
    risk_score = 0

    bot_prob = fingerprint.get("bot_probability", 0)

    if bot_prob > 0.6:
        risk_factors.append(f"机器人概率较高: {bot_prob:.1%}")
        risk_score += 40
    elif bot_prob > 0.3:
        risk_factors.append(f"机器人概率中等: {bot_prob:.1%}")
        risk_score += 20

    # 检查鼠标特征 / Check mouse features
    mouse = fingerprint.get("mouse", {})
    if not mouse.get("has_human_pattern", True):
        risk_factors.append("鼠标移动模式不符合人类行为特征")
        risk_score += 15

    if mouse.get("avg_speed", 0) > 2000:
        risk_factors.append("鼠标移动速度异常快")
        risk_score += 10

    # 检查键盘特征 / Check keyboard features
    keyboard = fingerprint.get("keyboard", {})
    if keyboard.get("std_interval_ms", 0) < 10:
        risk_factors.append("按键间隔过于均匀，疑似自动化输入")
        risk_score += 15

    # 检查页面交互 / Check page interaction
    interaction = fingerprint.get("interaction", {})
    if interaction.get("time_on_page", 0) < 2:
        risk_factors.append("页面停留时间过短")
        risk_score += 10

    if risk_score >= 50:
        risk_level = "high"
    elif risk_score >= 25:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "bot_probability": bot_prob,
        "human_probability": round(1.0 - bot_prob, 4),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
    }
