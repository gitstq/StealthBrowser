# -*- coding: utf-8 -*-
"""AudioContext指纹分析模块

AudioContext fingerprint analysis module.
分析AudioContext音频处理指纹，用于浏览器唯一性识别。
"""

import hashlib
import random
import struct


def generate_audio_fingerprint(seed=None):
    """生成模拟AudioContext指纹

    Generate simulated AudioContext fingerprint.

    AudioContext指纹通过AudioContext API生成音频信号，
    然后分析输出数据的特征来创建唯一标识。

    Args:
        seed (int, optional): 随机种子 / Random seed

    Returns:
        dict: AudioContext指纹数据 / AudioContext fingerprint data
    """
    if seed is not None:
        random.seed(seed)

    # 模拟音频处理参数 / Simulate audio processing parameters
    sample_rate = random.choice([44100, 48000])
    channel_count = random.choice([1, 2])
    fft_size = random.choice([256, 512, 1024, 2048])

    # 模拟OscillatorNode参数 / Simulate OscillatorNode parameters
    oscillator_type = random.choice(["sine", "square", "sawtooth", "triangle"])
    frequency = random.uniform(10000, 15000)

    # 模拟DynamicsCompressorNode参数 / Simulate DynamicsCompressorNode parameters
    compressor = {
        "threshold": random.uniform(-50, -20),
        "knee": random.uniform(20, 40),
        "ratio": random.uniform(1, 20),
        "attack": random.uniform(0, 0.1),
        "release": random.uniform(0.1, 1.0),
    }

    # 模拟音频输出数据 / Simulate audio output data
    # 生成伪随机浮点数模拟音频样本 / Generate pseudo-random floats simulating audio samples
    num_samples = fft_size
    samples = []
    for i in range(num_samples):
        # 模拟正弦波 + 噪声 / Simulate sine wave + noise
        value = 0.0
        value += 0.5 * (1 if (i % 2 == 0) else -1)  # 方波分量 / Square wave component
        value += random.uniform(-0.01, 0.01)  # 噪声 / Noise
        samples.append(round(value, 6))

    # 计算音频指纹哈希 / Calculate audio fingerprint hash
    sample_bytes = struct.pack(f"{len(samples)}f", *samples)
    audio_hash = hashlib.sha256(sample_bytes).hexdigest()[:32]

    # 计算音频特征 / Calculate audio features
    if samples:
        avg_amplitude = sum(abs(s) for s in samples) / len(samples)
        peak_amplitude = max(abs(s) for s in samples)
        zero_crossings = sum(1 for i in range(1, len(samples)) if samples[i - 1] * samples[i] < 0)
    else:
        avg_amplitude = 0.0
        peak_amplitude = 0.0
        zero_crossings = 0

    return {
        "hash": audio_hash,
        "sample_rate": sample_rate,
        "channel_count": channel_count,
        "fft_size": fft_size,
        "oscillator_type": oscillator_type,
        "frequency": round(frequency, 2),
        "compressor": compressor,
        "sample_count": num_samples,
        "avg_amplitude": round(avg_amplitude, 6),
        "peak_amplitude": round(peak_amplitude, 6),
        "zero_crossings": zero_crossings,
        "is_supported": True,
    }


def analyze_audio_fingerprint(fingerprint):
    """分析AudioContext指纹特征

    Analyze AudioContext fingerprint characteristics.

    Args:
        fingerprint (dict): AudioContext指纹数据 / AudioContext fingerprint data

    Returns:
        dict: 分析结果 / Analysis results
    """
    if not fingerprint or "hash" not in fingerprint:
        return {"error": "无效的AudioContext指纹数据", "risk_level": "unknown"}

    risk_factors = []
    risk_score = 0

    # 检查采样率 / Check sample rate
    sr = fingerprint.get("sample_rate", 0)
    if sr not in (44100, 48000):
        risk_factors.append(f"异常采样率: {sr}")
        risk_score += 15

    # 检查振幅特征 / Check amplitude characteristics
    avg_amp = fingerprint.get("avg_amplitude", 0)
    if avg_amp < 0.01:
        risk_factors.append("平均振幅过低，可能为静音或禁用状态")
        risk_score += 25
    elif avg_amp > 1.0:
        risk_factors.append("平均振幅异常偏高")
        risk_score += 20

    # 检查FFT大小 / Check FFT size
    fft = fingerprint.get("fft_size", 0)
    if fft not in (256, 512, 1024, 2048):
        risk_factors.append(f"异常FFT大小: {fft}")
        risk_score += 10

    # 检查过零率 / Check zero crossing rate
    zcr = fingerprint.get("zero_crossings", 0)
    sample_count = fingerprint.get("sample_count", 1)
    zcr_ratio = zcr / sample_count if sample_count > 0 else 0
    if zcr_ratio > 0.8:
        risk_factors.append("过零率异常偏高，音频信号可能为纯噪声")
        risk_score += 15

    if risk_score >= 50:
        risk_level = "high"
    elif risk_score >= 25:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "hash": fingerprint["hash"],
        "sample_rate": sr,
        "avg_amplitude": avg_amp,
        "zero_crossing_rate": round(zcr_ratio, 4),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
    }
