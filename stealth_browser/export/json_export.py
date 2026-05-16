# -*- coding: utf-8 -*-
"""JSON导出模块

JSON export module.
将指纹数据导出为JSON格式。
"""

import json


def export_json(data, filepath=None, indent=2):
    """导出为JSON格式

    Export as JSON format.

    Args:
        data (dict): 要导出的数据 / Data to export
        filepath (str, optional): 输出文件路径 / Output file path
        indent (int): 缩进级别 / Indent level

    Returns:
        str: JSON字符串 / JSON string
    """
    json_str = json.dumps(data, indent=indent, ensure_ascii=False, default=str)

    if filepath:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json_str)

    return json_str


def load_json(filepath):
    """从JSON文件加载

    Load from JSON file.

    Args:
        filepath (str): JSON文件路径 / JSON file path

    Returns:
        dict: 加载的数据 / Loaded data
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
