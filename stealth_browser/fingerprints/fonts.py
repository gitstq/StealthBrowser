# -*- coding: utf-8 -*-
"""字体检测模块

Font detection module.
通过测量文本渲染宽度来检测系统中已安装的字体。
"""

import random


# 常见系统字体列表 / Common system font list
SYSTEM_FONTS = {
    "windows": [
        "Arial", "Arial Black", "Arial Narrow", "Bahnschrift", "Calibri",
        "Cambria", "Cambria Math", "Candara", "Comic Sans MS", "Consolas",
        "Constantia", "Corbel", "Courier New", "Ebrima", "Franklin Gothic Medium",
        "Gabriola", "Gadugi", "Georgia", "HoloLens MDL2 Assets", "Impact",
        "Ink Free", "Javanese Text", "Leelawadee UI", "Lucida Console",
        "Lucida Sans Unicode", "Malgun Gothic", "Marlett", "Microsoft Himalaya",
        "Microsoft JhengHei", "Microsoft New Tai Lue", "Microsoft PhagsPa",
        "Microsoft Sans Serif", "Microsoft Tai Le", "Microsoft YaHei",
        "Microsoft Yi Baiti", "MingLiU-ExtB", "Mongolian Baiti", "MS Gothic",
        "MS PGothic", "MS UI Gothic", "MV Boli", "Myanmar Text", "Nirmala UI",
        "Palatino Linotype", "PMingLiU-ExtB", "Segoe MDL2 Assets", "Segoe Print",
        "Segoe Script", "Segoe UI", "Segoe UI Historic", "Segoe UI Emoji",
        "Segoe UI Symbol", "SimHei", "SimSun", "Sitka", "Sylfaen",
        "Symbol", "Tahoma", "Times New Roman", "Trebuchet MS", "Verdana",
        "Wingdings", "Wingdings 2", "Wingdings 3", "Yu Gothic",
    ],
    "macos": [
        "American Typewriter", "Andale Mono", "Apple Braille", "Apple Chancery",
        "Apple Color Emoji", "Apple SD Gothic Neo", "Apple Symbols",
        "AppleGothic", "AppleMyungjo", "Arial", "Arial Black", "Arial Hebrew",
        "Arial Narrow", "Arial Rounded MT Bold", "Arial Unicode MS",
        "Avenir", "Avenir Next", "Avenir Next Condensed", "Ayuthaya",
        "Bangla Sangam MN", "Beijing", "BiauKai", "Big Caslon",
        "Brush Script MT", "Chalkboard", "Chalkboard SE", "Chalkduster",
        "Charter", "Cochin", "Copperplate", "Corsiva Hebrew", "Courier",
        "Courier New", "DIN Alternate", "DIN Condensed", "Damascus",
        "DecoType Naskh", "Devanagari MT", "Didot", "Diwan Kufi",
        "Euphemia UCAS", "Futura", "GB18030 Bitmap", "Geeza Pro",
        "Geneva", "Georgia", "Gill Sans", "Gujarati MT", "Gurmukhi MN",
        "Gurmukhi MT Bold", "Heiti SC", "Heiti TC", "Helvetica",
        "Helvetica Neue", "Hiragino Sans", "Hiragino Sans GB",
        "Hoefler Text", "Impact", "Iowan Old Style", "Kailasa",
        "Kannada MN", "Kefa", "Khmer MN", "Kohinoor Bangla",
        "Kohinoor Devanagari", "Kohinoor Telugu", "Korean",
        "Lao MN", "Lucida Grande", "Luminari", "Malayalam MN",
        "Marion", "Marker Felt", "Menlo", "Mishafi", "Mishafi Gold",
        "Monaco", "Mona Lisa", "Mukta Mahee", "Myanmar MN",
        "Nadeem", "New Peninim MT", "Noteworthy", "Noto Sans",
        "Optima", "Oriya MN", "Osaka", "Papyrus", "PCmyungjo",
        "Phosphate", "PingFang HK", "PingFang SC", "PingFang TC",
        "Plantagenet Cherokee", "Raanana", "Rockwell", "STFangsong",
        "STHeiti", "STKaiti", "STSong", "STXihei", "Sana",
        "Sathu", "Savoye LET", "Shree Devanagari 714", "SignPainter",
        "Silom", "Sinhala MN", "Skia", "Snell Roundhand", "Songti SC",
        "Songti TC", "Sukhumvit Set", "Tamil MN", "Telugu MN",
        "Thonburi", "Times New Roman", "Trebuchet MS", "Verdana",
        "Waseem", "Webdings", "Wingdings", "Wingdings 2", "Wingdings 3",
        "Zapf Dingbats", "Zapfino",
    ],
    "linux": [
        "Arial", "Arial Black", "Comic Sans MS", "Courier New", "DejaVu Sans",
        "DejaVu Sans Mono", "DejaVu Serif", "FreeMono", "FreeSans", "FreeSerif",
        "Garuda", "Georgia", "Impact", "Liberation Mono", "Liberation Sans",
        "Liberation Serif", "Lucida Console", "Lucida Sans", "Lucida Sans Typewriter",
        "Microsoft YaHei", "Nimbus Mono L", "Nimbus Roman No9 L", "Nimbus Sans L",
        "Noto Sans", "Noto Sans CJK", "Noto Serif", "Palatino Linotype",
        "Standard Symbols L", "Symbol", "Tahoma", "Times New Roman",
        "Trebuchet MS", "Ubuntu", "Ubuntu Mono", "Utopia", "Verdana",
        "WenQuanYi Micro Hei", "WenQuanYi Zen Hei", "Wingdings",
    ],
    "android": [
        "Roboto", "Roboto Condensed", "Roboto Light", "Roboto Medium",
        "Roboto Mono", "Roboto Slab", "Roboto Thin", "Noto Sans",
        "Noto Sans CJK", "Droid Sans", "Droid Sans Mono", "Droid Serif",
    ],
    "ios": [
        "SF Pro", "SF Pro Display", "SF Pro Rounded", "SF Pro Text",
        "Helvetica", "Helvetica Neue", "Arial", "Arial Rounded MT Bold",
        "Courier", "Courier New", "Georgia", "Menlo", "San Francisco",
        "Thonburi", "Gill Sans", "Marker Felt", "Apple Color Emoji",
        "PingFang HK", "PingFang SC", "PingFang TC", "STHeiti",
    ],
}

# 用于检测的测试字符串 / Test strings for detection
FONT_TEST_STRING = "mmmmmmmmmmlli"
FONT_TEST_SIZE = "72px"


def generate_font_fingerprint(os_type="windows", seed=None):
    """生成模拟字体指纹

    Generate simulated font fingerprint.

    Args:
        os_type (str): 操作系统类型 / OS type
        seed (int, optional): 随机种子 / Random seed

    Returns:
        dict: 字体指纹数据 / Font fingerprint data
    """
    if seed is not None:
        random.seed(seed)

    # 获取对应OS的字体列表 / Get font list for corresponding OS
    available_fonts = SYSTEM_FONTS.get(os_type, SYSTEM_FONTS["windows"])

    # 随机移除一些字体，模拟不同安装情况 / Randomly remove some fonts
    num_fonts = random.randint(int(len(available_fonts) * 0.6), len(available_fonts))
    detected_fonts = sorted(random.sample(available_fonts, num_fonts))

    # 添加一些Google Fonts / Add some Google Fonts
    google_fonts = [
        "Open Sans", "Roboto", "Lato", "Montserrat", "Oswald",
        "Raleway", "Poppins", "Merriweather", "Ubuntu", "Noto Sans",
        "Source Sans Pro", "Nunito", "Playfair Display", "PT Sans",
    ]
    num_google = random.randint(0, min(8, len(google_fonts)))
    detected_fonts.extend(sorted(random.sample(google_fonts, num_google)))
    detected_fonts = sorted(set(detected_fonts))

    # 模拟字体度量 / Simulate font metrics
    font_metrics = {}
    for font in detected_fonts[:20]:  # 只为前20个字体生成度量
        font_metrics[font] = {
            "width": random.randint(100, 400),
            "height": random.randint(60, 100),
            "ascent": random.randint(40, 80),
            "descent": random.randint(10, 30),
        }

    return {
        "detected_fonts": detected_fonts,
        "font_count": len(detected_fonts),
        "os_type": os_type,
        "test_string": FONT_TEST_STRING,
        "test_size": FONT_TEST_SIZE,
        "font_metrics": font_metrics,
        "has_google_fonts": num_google > 0,
        "google_font_count": num_google,
    }


def analyze_font_fingerprint(fingerprint):
    """分析字体指纹特征

    Analyze font fingerprint characteristics.

    Args:
        fingerprint (dict): 字体指纹数据 / Font fingerprint data

    Returns:
        dict: 分析结果 / Analysis results
    """
    if not fingerprint or "detected_fonts" not in fingerprint:
        return {"error": "无效的字体指纹数据", "risk_level": "unknown"}

    detected = fingerprint.get("detected_fonts", [])
    os_type = fingerprint.get("os_type", "unknown")

    risk_factors = []
    risk_score = 0

    # 检查字体数量 / Check font count
    font_count = len(detected)
    if font_count < 20:
        risk_factors.append(f"检测到的字体数量过少({font_count}个)，可能为无头浏览器")
        risk_score += 30
    elif font_count > 200:
        risk_factors.append(f"检测到的字体数量异常多({font_count}个)")
        risk_score += 15

    # 检查OS与字体一致性 / Check OS-font consistency
    expected_fonts = set(SYSTEM_FONTS.get(os_type, []))
    detected_set = set(detected)
    os_fonts_found = detected_set & expected_fonts

    if len(os_fonts_found) < 5:
        risk_factors.append(f"与声称的OS({os_type})匹配的字体过少")
        risk_score += 25

    # 检查Google Fonts / Check Google Fonts
    google_count = fingerprint.get("google_font_count", 0)
    if google_count > 10:
        risk_factors.append(f"Google Fonts数量偏多({google_count}个)")
        risk_score += 10

    # 检查关键字体 / Check critical fonts
    critical_fonts = {
        "windows": ["Arial", "Times New Roman", "Courier New", "Verdana"],
        "macos": ["Helvetica", "Helvetica Neue", "Arial", "Georgia"],
        "linux": ["DejaVu Sans", "Liberation Sans", "FreeSans"],
        "android": ["Roboto", "Droid Sans"],
        "ios": ["Helvetica", "Helvetica Neue", "SF Pro"],
    }
    critical = critical_fonts.get(os_type, [])
    missing_critical = [f for f in critical if f not in detected_set]
    if missing_critical:
        risk_factors.append(f"缺少关键系统字体: {', '.join(missing_critical)}")
        risk_score += 20

    if risk_score >= 50:
        risk_level = "high"
    elif risk_score >= 25:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "font_count": font_count,
        "os_type": os_type,
        "os_font_match": len(os_fonts_found),
        "missing_critical_fonts": missing_critical,
        "google_font_count": google_count,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
    }
