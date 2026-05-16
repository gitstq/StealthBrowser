# -*- coding: utf-8 -*-
"""WebGL指纹分析模块

WebGL fingerprint analysis module.
分析WebGL渲染器和供应商信息，用于GPU指纹识别。
"""

import hashlib
import random


# 常见GPU渲染器列表 / Common GPU renderer list
COMMON_RENDERERS = {
    "desktop": [
        "ANGLE (Intel, Intel(R) UHD Graphics 630, OpenGL 4.6)",
        "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060, OpenGL 4.6)",
        "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060, OpenGL 4.6)",
        "ANGLE (AMD, AMD Radeon RX 580, OpenGL 4.6)",
        "ANGLE (Intel, Intel(R) Iris(R) Xe Graphics, OpenGL 4.6)",
        "ANGLE (NVIDIA, NVIDIA GeForce GTX 1650, OpenGL 4.5)",
        "ANGLE (AMD, AMD Radeon Pro WX 3200, OpenGL 4.5)",
        "Google SwiftShader",  # 无头模式 / Headless mode
    ],
    "mobile": [
        "Apple GPU",  # iOS设备 / iOS devices
        "Adreno (TM) 640",  # 高通骁龙 / Qualcomm Snapdragon
        "Adreno (TM) 650",
        "Adreno (TM) 730",
        "Mali-G78",  # ARM Mali
        "Mali-G710",
        "PowerVR Rogue GE8320",  # PowerVR
        "Apple M1",
    ],
}

# 常见GPU供应商列表 / Common GPU vendor list
COMMON_VENDORS = {
    "desktop": [
        "Google Inc. (Intel)",
        "Google Inc. (NVIDIA)",
        "Google Inc. (AMD)",
        "Google Inc.",
    ],
    "mobile": [
        "Apple Inc.",
        "Qualcomm",
        "ARM",
        "Imagination Technologies",
    ],
}

# WebGL扩展列表 / WebGL extension list
COMMON_EXTENSIONS = [
    "ANGLE_instanced_arrays",
    "EXT_blend_minmax",
    "EXT_color_buffer_half_float",
    "EXT_float_blend",
    "EXT_frag_depth",
    "EXT_shader_texture_lod",
    "EXT_texture_compression_bzip2",
    "EXT_texture_filter_anisotropic",
    "EXT_sRGB",
    "OES_element_index_uint",
    "OES_fbo_render_mipmap",
    "OES_standard_derivatives",
    "OES_texture_float",
    "OES_texture_float_linear",
    "OES_texture_half_float",
    "OES_texture_half_float_linear",
    "OES_vertex_array_object",
    "WEBGL_color_buffer_float",
    "WEBGL_compressed_texture_s3tc",
    "WEBGL_compressed_texture_s3tc_srgb",
    "WEBGL_debug_renderer_info",
    "WEBGL_debug_shaders",
    "WEBGL_depth_texture",
    "WEBGL_draw_buffers",
    "WEBGL_lose_context",
    "WEBGL_multi_draw",
]


def generate_webgl_fingerprint(device_type="desktop", seed=None):
    """生成模拟WebGL指纹

    Generate simulated WebGL fingerprint.

    Args:
        device_type (str): 设备类型 desktop/mobile / Device type
        seed (int, optional): 随机种子 / Random seed

    Returns:
        dict: WebGL指纹数据 / WebGL fingerprint data
    """
    if seed is not None:
        random.seed(seed)

    renderers = COMMON_RENDERERS.get(device_type, COMMON_RENDERERS["desktop"])
    vendors = COMMON_VENDORS.get(device_type, COMMON_VENDORS["desktop"])

    renderer = random.choice(renderers)
    vendor = random.choice(vendors)

    # 随机选择WebGL扩展子集 / Randomly select WebGL extension subset
    num_extensions = random.randint(15, len(COMMON_EXTENSIONS))
    extensions = sorted(random.sample(COMMON_EXTENSIONS, num_extensions))

    # WebGL参数 / WebGL parameters
    max_texture_size = random.choice([4096, 8192, 16384, 32768])
    max_renderbuffer_size = random.choice([4096, 8192, 16384])
    max_viewport_dims = [max_texture_size, max_texture_size]
    aliased_point_size_range = [1.0, random.choice([64.0, 128.0, 256.0, 512.0])]
    aliased_line_width_range = [1.0, random.choice([1.0, 8.0, 16.0])]

    # 着色精度 / Shader precision
    vertex_shader_high_float = {
        "rangeMin": 127,
        "rangeMax": 127,
        "precision": random.choice([23, 24]),
    }
    fragment_shader_high_float = {
        "rangeMin": 127,
        "rangeMax": 127,
        "precision": random.choice([23, 24]),
    }

    # 生成指纹哈希 / Generate fingerprint hash
    fp_data = f"{renderer}|{vendor}|{','.join(extensions)}|{max_texture_size}"
    webgl_hash = hashlib.sha256(fp_data.encode("utf-8")).hexdigest()[:32]

    # 检测是否为无头模式 / Detect headless mode
    is_headless = "SwiftShader" in renderer

    return {
        "renderer": renderer,
        "vendor": vendor,
        "extensions": extensions,
        "extension_count": len(extensions),
        "max_texture_size": max_texture_size,
        "max_renderbuffer_size": max_renderbuffer_size,
        "max_viewport_dims": max_viewport_dims,
        "aliased_point_size_range": aliased_point_size_range,
        "aliased_line_width_range": aliased_line_width_range,
        "vertex_shader_high_float": vertex_shader_high_float,
        "fragment_shader_high_float": fragment_shader_high_float,
        "hash": webgl_hash,
        "is_headless": is_headless,
        "webgl_version": random.choice(["1.0", "2.0"]),
    }


def analyze_webgl_fingerprint(fingerprint):
    """分析WebGL指纹特征

    Analyze WebGL fingerprint characteristics.

    Args:
        fingerprint (dict): WebGL指纹数据 / WebGL fingerprint data

    Returns:
        dict: 分析结果 / Analysis results
    """
    if not fingerprint:
        return {"error": "无效的WebGL指纹数据", "risk_level": "unknown"}

    risk_factors = []
    risk_score = 0

    # 检测无头浏览器 / Detect headless browser
    if fingerprint.get("is_headless", False):
        risk_factors.append("检测到SwiftShader渲染器，可能为无头浏览器")
        risk_score += 40

    # 检查扩展数量 / Check extension count
    ext_count = fingerprint.get("extension_count", 0)
    if ext_count < 15:
        risk_factors.append(f"WebGL扩展数量偏少({ext_count}个)，可能为自动化环境")
        risk_score += 20
    elif ext_count > 25:
        risk_factors.append(f"WebGL扩展数量偏多({ext_count}个)，与声称的浏览器不一致")
        risk_score += 10

    # 检查纹理大小 / Check texture size
    max_tex = fingerprint.get("max_texture_size", 0)
    if max_tex < 4096:
        risk_factors.append(f"最大纹理尺寸偏小({max_tex})，可能为低配或虚拟GPU")
        risk_score += 15

    # 检查渲染器与供应商一致性 / Check renderer-vendor consistency
    renderer = fingerprint.get("renderer", "")
    vendor = fingerprint.get("vendor", "")
    if "Intel" in renderer and "Intel" not in vendor:
        risk_factors.append("GPU渲染器与供应商信息不匹配")
        risk_score += 20
    elif "NVIDIA" in renderer and "NVIDIA" not in vendor:
        risk_factors.append("GPU渲染器与供应商信息不匹配")
        risk_score += 20

    if risk_score >= 50:
        risk_level = "high"
    elif risk_score >= 25:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "renderer": renderer,
        "vendor": vendor,
        "is_headless": fingerprint.get("is_headless", False),
        "extension_count": ext_count,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
    }


def compare_webgl_fingerprints(fp_a, fp_b):
    """对比两个WebGL指纹

    Compare two WebGL fingerprints.

    Args:
        fp_a (dict): 指纹A / Fingerprint A
        fp_b (dict): 指纹B / Fingerprint B

    Returns:
        dict: 对比结果 / Comparison results
    """
    if not fp_a or not fp_b:
        return {"error": "无效的指纹数据"}

    renderer_match = fp_a.get("renderer") == fp_b.get("renderer")
    vendor_match = fp_a.get("vendor") == fp_b.get("vendor")

    # 扩展差异 / Extension differences
    ext_a = set(fp_a.get("extensions", []))
    ext_b = set(fp_b.get("extensions", []))
    common_ext = ext_a & ext_b
    only_a = ext_a - ext_b
    only_b = ext_b - ext_a

    if ext_a | ext_b:
        jaccard_similarity = len(common_ext) / len(ext_a | ext_b)
    else:
        jaccard_similarity = 1.0

    return {
        "renderer_match": renderer_match,
        "vendor_match": vendor_match,
        "extension_jaccard": round(jaccard_similarity, 4),
        "common_extensions": len(common_ext),
        "only_in_a": len(only_a),
        "only_in_b": len(only_b),
        "overall_similarity": round(
            (0.4 * int(renderer_match) + 0.3 * int(vendor_match) + 0.3 * jaccard_similarity), 4
        ),
    }
