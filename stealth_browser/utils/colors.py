# -*- coding: utf-8 -*-
"""终端颜色工具模块 - ANSI颜色码定义

Terminal color utility module - ANSI color code definitions.
提供跨平台的终端颜色输出支持。
"""

import os
import sys


class Colors:
    """ANSI终端颜色类

    ANSI terminal color class.
    提供常用的终端颜色和样式常量。
    Provides common terminal color and style constants.
    """

    # 重置样式 / Reset style
    RESET = "\033[0m"

    # 前景色 / Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"

    # 亮色前景 / Bright foreground colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # 背景色 / Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    # 样式 / Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    STRIKETHROUGH = "\033[9m"

    # 是否支持颜色 / Whether colors are supported
    _enabled = None

    @classmethod
    def enable(cls):
        """启用颜色输出

        Enable color output.
        """
        cls._enabled = True

    @classmethod
    def disable(cls):
        """禁用颜色输出

        Disable color output.
        """
        cls._enabled = False

    @classmethod
    def is_enabled(cls):
        """检查颜色输出是否启用

        Check if color output is enabled.
        自动检测终端是否支持颜色。
        Automatically detect if terminal supports colors.

        Returns:
            bool: 是否支持颜色输出
        """
        if cls._enabled is not None:
            return cls._enabled
        # 检测是否为支持颜色的终端 / Check if terminal supports colors
        if os.environ.get("NO_COLOR"):
            return False
        if os.environ.get("TERM") == "dumb":
            return False
        if not hasattr(sys.stdout, "isatty"):
            return False
        if not sys.stdout.isatty():
            return False
        # Windows 10+ 支持 ANSI 颜色 / Windows 10+ supports ANSI colors
        if sys.platform == "win32":
            return True
        return True

    @classmethod
    def style(cls, text, *styles):
        """为文本应用颜色样式

        Apply color styles to text.

        Args:
            text (str): 要着色的文本 / Text to colorize
            *styles: 颜色/样式常量 / Color/style constants

        Returns:
            str: 着色后的文本 / Colorized text
        """
        if not cls.is_enabled():
            return text
        return "".join(styles) + text + cls.RESET

    @classmethod
    def red(cls, text):
        """红色文本 / Red text"""
        return cls.style(text, cls.RED)

    @classmethod
    def green(cls, text):
        """绿色文本 / Green text"""
        return cls.style(text, cls.GREEN)

    @classmethod
    def yellow(cls, text):
        """黄色文本 / Yellow text"""
        return cls.style(text, cls.YELLOW)

    @classmethod
    def blue(cls, text):
        """蓝色文本 / Blue text"""
        return cls.style(text, cls.BLUE)

    @classmethod
    def cyan(cls, text):
        """青色文本 / Cyan text"""
        return cls.style(text, cls.CYAN)

    @classmethod
    def magenta(cls, text):
        """品红色文本 / Magenta text"""
        return cls.style(text, cls.MAGENTA)

    @classmethod
    def bold(cls, text):
        """粗体文本 / Bold text"""
        return cls.style(text, cls.BOLD)

    @classmethod
    def dim(cls, text):
        """暗色文本 / Dim text"""
        return cls.style(text, cls.DIM)

    @classmethod
    def success(cls, text):
        """成功标记 / Success marker"""
        return cls.style(text, cls.BRIGHT_GREEN)

    @classmethod
    def warning(cls, text):
        """警告标记 / Warning marker"""
        return cls.style(text, cls.BRIGHT_YELLOW)

    @classmethod
    def error(cls, text):
        """错误标记 / Error marker"""
        return cls.style(text, cls.BRIGHT_RED)

    @classmethod
    def info(cls, text):
        """信息标记 / Info marker"""
        return cls.style(text, cls.BRIGHT_CYAN)


# 状态图标常量 / Status icon constants
ICON_OK = "\u2713"       # ✓
ICON_FAIL = "\u2717"     # ✗
ICON_WARN = "\u26a0"     # ⚠
ICON_INFO = "\u2139"     # ℹ
ICON_ARROW = "\u2192"    # →
ICON_BULLET = "\u2022"   # •
ICON_STAR = "\u2605"     # ★
ICON_BOX = "\u25a0"      # ■
ICON_DIAMOND = "\u25c6"  # ◆
ICON_LINE = "\u2500"     # ─
ICON_CORNER_TL = "\u250c"  # ┌
ICON_CORNER_TR = "\u2510"  # ┐
ICON_CORNER_BL = "\u2514"  # └
ICON_CORNER_BR = "\u2518"  # ┘
ICON_T_DOWN = "\u252c"     # ┬
ICON_T_UP = "\u2534"       # ┴
ICON_T_RIGHT = "\u251c"    # ├
ICON_T_LEFT = "\u2524"     # ┤
ICON_CROSS = "\u253c"      # ┼


def progress_bar(current, total, width=40, prefix="", suffix=""):
    """生成进度条字符串

    Generate progress bar string.

    Args:
        current (int): 当前进度 / Current progress
        total (int): 总数 / Total count
        width (int): 进度条宽度 / Progress bar width
        prefix (str): 前缀文本 / Prefix text
        suffix (str): 后缀文本 / Suffix text

    Returns:
        str: 进度条字符串 / Progress bar string
    """
    if total == 0:
        percent = 100.0
    else:
        percent = current / total * 100
    filled = int(width * current / total) if total > 0 else width
    empty = width - filled

    if Colors.is_enabled():
        bar = Colors.GREEN + "█" * filled + Colors.RESET
        bar += Colors.DIM + "░" * empty + Colors.RESET
    else:
        bar = "#" * filled + "-" * empty

    return f"\r{prefix}[{bar}] {percent:5.1f}% {suffix}"


def print_table(headers, rows, col_widths=None, title=None):
    """打印彩色表格

    Print a colored table.

    Args:
        headers (list): 表头列表 / Header list
        rows (list): 行数据列表 / Row data list
        col_widths (list): 列宽列表 / Column width list
        title (str): 表格标题 / Table title
    """
    if not rows and not headers:
        return

    # 计算列宽 / Calculate column widths
    if col_widths is None:
        col_widths = []
        for i, header in enumerate(headers):
            max_w = len(str(header))
            for row in rows:
                if i < len(row):
                    max_w = max(max_w, len(str(row[i])))
            col_widths.append(max_w + 2)

    # 打印标题 / Print title
    if title:
        print(f"\n  {Colors.bold(Colors.cyan(title))}")
        print(f"  {Colors.DIM + ICON_LINE * (sum(col_widths) + len(col_widths) + 1) + Colors.RESET}")

    # 打印表头 / Print header
    header_line = "│"
    for i, header in enumerate(headers):
        w = col_widths[i] if i < len(col_widths) else len(str(header)) + 2
        header_line += f" {Colors.BOLD}{str(header):<{w-2}}{Colors.RESET} │"
    print(f"  {header_line}")

    # 打印分隔线 / Print separator
    sep_line = "├"
    for i, w in enumerate(col_widths):
        sep_line += ICON_LINE * (w + 1) + "┤"
    print(f"  {sep_line}")

    # 打印数据行 / Print data rows
    for row in rows:
        row_line = "│"
        for i, cell in enumerate(row):
            w = col_widths[i] if i < len(col_widths) else len(str(cell)) + 2
            row_line += f" {str(cell):<{w-2}} │"
        print(f"  {row_line}")


def print_score_gauge(score, max_score=100, label="反检测评分"):
    """打印ASCII评分仪表盘

    Print ASCII score gauge.

    Args:
        score (int/float): 分数 / Score
        max_score (int): 满分 / Max score
        label (str): 标签 / Label
    """
    percent = score / max_score * 100

    # 确定颜色和等级 / Determine color and grade
    if percent >= 80:
        color = Colors.BRIGHT_GREEN
        grade = "优秀"
        grade_icon = ICON_OK
    elif percent >= 60:
        color = Colors.BRIGHT_YELLOW
        grade = "良好"
        grade_icon = ICON_WARN
    elif percent >= 40:
        color = Colors.YELLOW
        grade = "一般"
        grade_icon = ICON_WARN
    else:
        color = Colors.BRIGHT_RED
        grade = "较差"
        grade_icon = ICON_FAIL

    # 生成仪表盘 / Generate gauge
    gauge_width = 30
    filled = int(gauge_width * percent / 100)

    if Colors.is_enabled():
        gauge = color + "█" * filled + Colors.DIM + "░" * (gauge_width - filled) + Colors.RESET
    else:
        gauge = "#" * filled + "-" * (gauge_width - filled)

    print()
    print(f"  {Colors.BOLD}╔{'═' * 42}╗{Colors.RESET}")
    print(f"  {Colors.BOLD}║{Colors.RESET}  {label:^36s}  {Colors.BOLD}║{Colors.RESET}")
    print(f"  {Colors.BOLD}╠{'═' * 42}╣{Colors.RESET}")
    print(f"  {Colors.BOLD}║{Colors.RESET}  [{gauge}]  {Colors.BOLD}║{Colors.RESET}")
    print(f"  {Colors.BOLD}║{Colors.RESET}  {color}{Colors.BOLD}{score:>5.1f}{Colors.RESET}/{max_score}  "
          f"  等级: {color}{grade_icon} {grade}{Colors.RESET}  {Colors.BOLD}║{Colors.RESET}")
    print(f"  {Colors.BOLD}╚{'═' * 42}╝{Colors.RESET}")
    print()
