# -*- coding: utf-8 -*-
"""YAML导出模块

YAML export module.
将指纹数据导出为YAML格式（纯Python实现，无外部依赖）。
"""


def _yaml_value(value, indent=0):
    """将Python值转换为YAML格式字符串

    Convert Python value to YAML format string.

    Args:
        value: Python值 / Python value
        indent (int): 缩进级别 / Indent level

    Returns:
        str: YAML格式字符串 / YAML format string
    """
    prefix = "  " * indent

    if value is None:
        return f"{prefix}null"
    elif isinstance(value, bool):
        return f"{prefix}{'true' if value else 'false'}"
    elif isinstance(value, (int, float)):
        return f"{prefix}{value}"
    elif isinstance(value, str):
        # 检查是否需要引号 / Check if quotes are needed
        if any(c in value for c in [":", "#", "{", "}", "[", "]", ",", "&", "*", "?", "|", "-", "<", ">", "=", "!", "%", "@", "\\"]):
            escaped = value.replace("\\", "\\\\").replace('"', '\\"')
            return f'{prefix}"{escaped}"'
        elif value == "" or value.lower() in ("true", "false", "null", "yes", "no", "on", "off"):
            return f'{prefix}"{value}"'
        else:
            return f"{prefix}{value}"
    elif isinstance(value, dict):
        if not value:
            return f"{{}}"
        lines = []
        for k, v in value.items():
            key_str = str(k)
            if any(c in key_str for c in [":", "#", "{", "}", "[", "]", ",", "&", "*", "?", "|", "-", "<", ">", "=", "!", "%", "@", " ", "\\"]):
                key_str = f'"{key_str}"'
            if isinstance(v, (dict, list)):
                lines.append(f"{prefix}{key_str}:")
                lines.append(_yaml_value(v, indent + 1))
            else:
                lines.append(f"{prefix}{key_str}: {_yaml_value(v, 0).strip()}")
        return "\n".join(lines)
    elif isinstance(value, (list, tuple)):
        if not value:
            return "[]"
        lines = []
        for item in value:
            if isinstance(item, dict):
                lines.append(f"{prefix}-")
                dict_lines = _yaml_value(item, indent + 1).split("\n")
                for i, line in enumerate(dict_lines):
                    if i == 0:
                        lines[-1] += f" {line.strip()}"
                    else:
                        lines.append(f"  {prefix}{line}")
            elif isinstance(item, (list, tuple)):
                lines.append(f"{prefix}-")
                list_lines = _yaml_value(item, indent + 1).split("\n")
                for i, line in enumerate(list_lines):
                    if i == 0:
                        lines[-1] += f" {line.strip()}"
                    else:
                        lines.append(f"  {prefix}{line}")
            else:
                item_str = _yaml_value(item, 0).strip()
                lines.append(f"{prefix}- {item_str}")
        return "\n".join(lines)
    else:
        return f"{prefix}{str(value)}"


def export_yaml(data, filepath=None):
    """导出为YAML格式

    Export as YAML format.

    Args:
        data (dict): 要导出的数据 / Data to export
        filepath (str, optional): 输出文件路径 / Output file path

    Returns:
        str: YAML字符串 / YAML string
    """
    yaml_str = _yaml_value(data)

    if filepath:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(yaml_str)
            f.write("\n")

    return yaml_str


def load_yaml(filepath):
    """从YAML文件加载（简易解析器）

    Load from YAML file (simple parser).

    注意：这是一个简易的YAML解析器，不支持所有YAML特性。
    Note: This is a simple YAML parser, not all YAML features are supported.

    Args:
        filepath (str): YAML文件路径 / YAML file path

    Returns:
        dict: 加载的数据 / Loaded data
    """
    import json

    # 简易YAML转JSON解析 / Simple YAML to JSON conversion
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 使用简易转换 / Use simple conversion
    return _simple_yaml_parse(content)


def _simple_yaml_parse(content):
    """简易YAML解析器

    Simple YAML parser.

    Args:
        content (str): YAML内容 / YAML content

    Returns:
        dict: 解析结果 / Parsed result
    """
    import re

    result = {}
    current_dict = result
    stack = []
    current_key = None

    for line in content.split("\n"):
        stripped = line.strip()

        # 跳过空行和注释 / Skip empty lines and comments
        if not stripped or stripped.startswith("#"):
            continue

        # 计算缩进 / Calculate indentation
        indent = len(line) - len(line.lstrip())

        # 处理列表项 / Handle list items
        if stripped.startswith("- "):
            value = stripped[2:].strip()
            if current_key and current_key in current_dict:
                if not isinstance(current_dict[current_key], list):
                    current_dict[current_key] = []
                current_dict[current_key].append(_parse_yaml_value(value))
            continue

        # 处理键值对 / Handle key-value pairs
        if ":" in stripped:
            colon_idx = stripped.index(":")
            key = stripped[:colon_idx].strip().strip('"').strip("'")
            value = stripped[colon_idx + 1:].strip()

            if value:
                current_dict[key] = _parse_yaml_value(value)
                current_key = key
            else:
                current_dict[key] = {}
                current_key = key

    return result


def _parse_yaml_value(value_str):
    """解析YAML值

    Parse YAML value.

    Args:
        value_str (str): 值字符串 / Value string

    Returns:
        object: 解析后的值 / Parsed value
    """
    # 去除引号 / Remove quotes
    if (value_str.startswith('"') and value_str.endswith('"')) or \
       (value_str.startswith("'") and value_str.endswith("'")):
        return value_str[1:-1]

    # 布尔值 / Boolean values
    if value_str.lower() in ("true", "yes", "on"):
        return True
    if value_str.lower() in ("false", "no", "off"):
        return False

    # 空值 / Null values
    if value_str.lower() in ("null", "~", ""):
        return None

    # 数字 / Numbers
    try:
        if "." in value_str:
            return float(value_str)
        return int(value_str)
    except ValueError:
        pass

    return value_str
