# -*- coding: utf-8 -*-
"""网络指纹模块

Network fingerprint module.
分析IP、WebRTC、DNS等网络相关指纹。
"""

import hashlib
import random


def generate_network_fingerprint(seed=None):
    """生成模拟网络指纹

    Generate simulated network fingerprint.

    Args:
        seed (int, optional): 随机种子 / Random seed

    Returns:
        dict: 网络指纹数据 / Network fingerprint data
    """
    if seed is not None:
        random.seed(seed)

    # 模拟IP地址 / Simulate IP address
    ip = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

    # 检测是否为VPN/代理IP特征 / Detect VPN/proxy IP characteristics
    is_datacenter = random.random() < 0.1  # 10%概率为数据中心IP
    is_vpn = random.random() < 0.05  # 5%概率为VPN
    is_tor = random.random() < 0.02  # 2%概率为Tor

    # IP类型 / IP type
    if is_tor:
        ip_type = "tor"
    elif is_vpn:
        ip_type = "vpn"
    elif is_datacenter:
        ip_type = "datacenter"
    else:
        ip_type = "residential"

    # WebRTC / WebRTC
    webrtc_support = random.choice([True, True, True, False])  # 75%支持
    webrtc_local_ip = None
    webrtc_public_ip = None
    if webrtc_support:
        webrtc_local_ip = f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"
        webrtc_public_ip = ip  # WebRTC泄露公网IP

    # DNS / DNS
    dns_servers = random.choice([
        ["8.8.8.8", "8.8.4.4"],  # Google DNS
        ["1.1.1.1", "1.0.0.1"],  # Cloudflare DNS
        ["208.67.222.222", "208.67.220.220"],  # OpenDNS
        ["114.114.114.114", "114.114.115.115"],  # 114 DNS
    ])

    # 连接信息 / Connection info
    connection_type = random.choice(["wifi", "4g", "ethernet", "cellular"])
    isp = random.choice([
        "China Telecom", "China Unicom", "China Mobile",
        "AT&T", "Verizon", "Comcast", "Spectrum",
    ])

    # HTTP代理检测 / HTTP proxy detection
    has_proxy = random.random() < 0.08  # 8%概率使用代理
    proxy_type = None
    if has_proxy:
        proxy_type = random.choice(["http", "https", "socks5", "socks4"])

    # DoH (DNS over HTTPS) / DoH
    doh_enabled = random.choice([True, False])

    # 网络延迟模拟 / Network latency simulation
    latency = {
        "dns_lookup": random.randint(5, 100),
        "tcp_connect": random.randint(10, 200),
        "tls_handshake": random.randint(20, 300),
        "total": 0,
    }
    latency["total"] = latency["dns_lookup"] + latency["tcp_connect"] + latency["tls_handshake"]

    return {
        "ip": ip,
        "ip_type": ip_type,
        "is_datacenter": is_datacenter,
        "is_vpn": is_vpn,
        "is_tor": is_tor,
        "webrtc_support": webrtc_support,
        "webrtc_local_ip": webrtc_local_ip,
        "webrtc_public_ip": webrtc_public_ip,
        "dns_servers": dns_servers,
        "connection_type": connection_type,
        "isp": isp,
        "has_proxy": has_proxy,
        "proxy_type": proxy_type,
        "doh_enabled": doh_enabled,
        "latency": latency,
    }


def analyze_network_fingerprint(fingerprint):
    """分析网络指纹特征

    Analyze network fingerprint characteristics.

    Args:
        fingerprint (dict): 网络指纹数据 / Network fingerprint data

    Returns:
        dict: 分析结果 / Analysis results
    """
    if not fingerprint:
        return {"error": "无效的网络指纹数据", "risk_level": "unknown"}

    risk_factors = []
    risk_score = 0

    # 检查IP类型 / Check IP type
    ip_type = fingerprint.get("ip_type", "")
    if ip_type == "tor":
        risk_factors.append("检测到Tor出口节点")
        risk_score += 35
    elif ip_type == "vpn":
        risk_factors.append("检测到VPN连接")
        risk_score += 20
    elif ip_type == "datacenter":
        risk_factors.append("IP属于数据中心，非住宅IP")
        risk_score += 30

    # 检查WebRTC泄露 / Check WebRTC leak
    if fingerprint.get("webrtc_support", False):
        local_ip = fingerprint.get("webrtc_local_ip")
        public_ip = fingerprint.get("webrtc_public_ip")
        if local_ip and public_ip:
            risk_factors.append("WebRTC可能泄露本地IP地址")
            risk_score += 15

    # 检查代理 / Check proxy
    if fingerprint.get("has_proxy", False):
        proxy_type = fingerprint.get("proxy_type", "unknown")
        risk_factors.append(f"检测到{proxy_type}代理")
        risk_score += 15

    # 检查DNS一致性 / Check DNS consistency
    dns_servers = fingerprint.get("dns_servers", [])
    public_dns = {"8.8.8.8", "1.1.1.1", "208.67.222.222", "114.114.114.114"}
    has_public_dns = any(d in public_dns for d in dns_servers)
    if has_public_dns:
        risk_factors.append("使用公共DNS服务器，可能影响DNS指纹一致性")
        risk_score += 5

    if risk_score >= 50:
        risk_level = "high"
    elif risk_score >= 25:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "ip": fingerprint.get("ip", ""),
        "ip_type": ip_type,
        "webrtc_leak": fingerprint.get("webrtc_support", False) and fingerprint.get("webrtc_local_ip"),
        "has_proxy": fingerprint.get("has_proxy", False),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "anonymity_score": max(0, 100 - risk_score),
    }
