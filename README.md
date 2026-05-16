<div align="center">

```
 ██████╗ ███████╗████████╗██████╗  ██████╗     ██████╗  ██████╗ ███╗   ██╗ ██████╗
██╔════╝ ██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗    ██╔══██╗██╔═══██╗████╗  ██║██╔════╝
██║  ███╗█████╗     ██║   ██████╔╝██║   ██║    ██████╔╝██║   ██║██╔██╗ ██║██║  ███╗
██║   ██║██╔══╝     ██║   ██╔══██╗██║   ██║    ██╔══██╗██║   ██║██║╚██╗██║██║   ██║
╚██████╔╝███████╗   ██║   ██║  ██║╚██████╔╝    ██████╔╝╚██████╔╝██║ ╚████║╚██████╔╝
 ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝     ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝
```

**轻量级反检测浏览器指纹分析 CLI 引擎**
**Lightweight Anti-Detection Browser Fingerprint Analysis CLI Engine**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-success.svg)]()
[![Tests: 53](https://img.shields.io/badge/Tests-53%20passed-brightgreen.svg)]()
[![Fingerprint Dimensions: 50+](https://img.shields.io/badge/Fingerprint_Dimensions-50%2B-orange.svg)]()

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

<a id="简体中文"></a>

# 🎉 项目介绍

**StealthBrowser** 是一款专为安全研究人员、爬虫工程师和隐私爱好者打造的**轻量级反检测浏览器指纹分析 CLI 引擎**。

## 解决的痛点

在日常的 Web 自动化、数据采集和隐私保护场景中，浏览器指纹识别技术被广泛用于检测和拦截自动化工具。传统的指纹检测方案往往存在以下问题：

| 痛点 | 说明 |
|------|------|
| **依赖臃肿** | 现有工具多依赖 Selenium、Playwright 等重型框架，部署成本高 |
| **维度不足** | 仅覆盖 Canvas/WebGL 等少数维度，容易被绕过 |
| **缺乏评分** | 无法量化评估反检测效果，难以针对性优化 |
| **配置僵化** | 缺少预设配置，每次都需要手动调参 |

## 核心价值

- **零外部依赖** — 纯 Python 标准库实现，`pip install` 即用，无需安装浏览器驱动
- **50+ 维度指纹采集** — 全面覆盖 Canvas、WebGL、Audio、字体、硬件、网络、行为、存储、屏幕、时区、HTTP 头等维度
- **反检测评分系统** — 0-100 分量化评分，从一致性、唯一性、熵值、稳定性四个维度综合评估
- **6 种预设指纹配置** — Chrome / Firefox / Safari / 移动端 / 爬虫 / 最大隐身，一键切换
- **多格式导出** — 支持 JSON、YAML、HTML 三种格式输出
- **TUI 终端仪表盘** — 在终端中直接可视化查看分析结果

## 差异化亮点

StealthBrowser 与同类工具的核心区别在于：**它不是一个浏览器自动化工具，而是一个指纹分析引擎**。它专注于指纹的采集、评分和配置生成，可以与任何浏览器自动化框架配合使用，也可以独立运行进行环境检测。

---

# ✨ 核心特性

- **🔍 50+ 维度指纹采集** — 深度覆盖 Canvas、WebGL（渲染器/供应商/扩展）、AudioContext、字体枚举、硬件并发数/内存/显卡、网络信息/连接类型、行为特征（鼠标/键盘/触控）、存储检测（Cookie/LocalStorage/IndexedDB）、屏幕分辨率/色深/像素比、时区/语言/地区、HTTP 请求头分析等

- **📊 四维度反检测评分** — 从**一致性**（各维度间是否矛盾）、**唯一性**（指纹在群体中的稀有度）、**熵值**（信息的随机性程度）、**稳定性**（多次采集的波动情况）四个维度进行 0-100 分量化评估

- **🎭 6 种预设指纹配置** — 内置 Chrome、Firefox、Safari、移动端（iOS/Android）、爬虫（低资源消耗）、最大隐身（最高匿名性）六套预设方案，支持自定义扩展

- **📋 多格式导出** — JSON（结构化数据）、YAML（可读配置）、HTML（可视化报告）三种输出格式，满足不同使用场景

- **🖥️ TUI 终端可视化仪表盘** — 基于 `curses` 的终端 UI，实时展示指纹分析结果，支持键盘交互浏览各维度详情

- **🧪 53 个单元测试** — 完善的测试覆盖，确保采集逻辑和评分算法的准确性

- **📦 零外部依赖** — 全部基于 Python 标准库（`json`、`yaml`、`urllib`、`curses`、`hashlib`、`subprocess` 等），无第三方包依赖

- **⚡ 高性能采集** — 并行化指纹采集流程，单次全量扫描耗时 < 3 秒

---

# 🚀 快速开始

## 环境要求

| 项目 | 要求 |
|------|------|
| **Python** | 3.8 及以上版本 |
| **操作系统** | Windows / macOS / Linux |
| **终端** | 支持 ANSI 转义序列或 `curses` 的终端（TUI 功能需要） |

## 安装

```bash
# 从 PyPI 安装（推荐）
pip install stealth-browser

# 或从源码安装
git clone https://github.com/your-username/stealth-browser.git
cd stealth-browser
pip install .
```

## 启动

```bash
# 查看帮助信息
stealth-browser --help

# 快速扫描当前浏览器环境指纹
stealth-browser scan

# 运行反检测评分
stealth-browser score

# 启动 TUI 可视化仪表盘
stealth-browser report --tui
```

---

# 📖 详细使用指南

## 1. `scan` — 指纹扫描

采集当前环境的完整浏览器指纹数据。

```bash
# 全量扫描所有维度
stealth-browser scan

# 指定输出格式
stealth-browser scan --format json     # JSON 格式
stealth-browser scan --format yaml     # YAML 格式
stealth-browser scan --format html     # HTML 格式

# 指定输出文件
stealth-browser scan --output result.json

# 仅扫描特定维度
stealth-browser scan --dimensions canvas,webgl,audio,fonts

# 静默模式（仅输出数据，无进度信息）
stealth-browser scan --quiet
```

**输出示例（JSON）：**

```json
{
  "canvas": {
    "hash": "a1b2c3d4e5f6...",
    "text_metrics": true,
    "image_data": true
  },
  "webgl": {
    "renderer": "ANGLE (Intel, Mesa Intel(R) UHD Graphics...)",
    "vendor": "Google Inc. (Intel)",
    "extensions": ["ANGLE_instanced_arrays", "OES_texture_float", "..."],
    "parameters": {
      "MAX_TEXTURE_SIZE": 16384,
      "MAX_RENDERBUFFER_SIZE": 16384
    }
  },
  "audio": {
    "sample_rate": 44100,
    "channel_count": 2,
    "hash": "f6e5d4c3b2a1..."
  }
}
```

## 2. `score` — 反检测评分

对当前环境进行反检测能力评分。

```bash
# 运行完整评分
stealth-browser score

# 查看各维度详细评分
stealth-browser score --verbose

# 仅查看总分
stealth-browser score --summary
```

**评分维度说明：**

| 维度 | 满分 | 说明 |
|------|------|------|
| **一致性 (Consistency)** | 25 | 各指纹维度之间是否存在矛盾（如声称是 macOS 却使用 Windows 字体） |
| **唯一性 (Uniqueness)** | 25 | 指纹在全局指纹库中的稀有程度，越普通越不易被追踪 |
| **熵值 (Entropy)** | 25 | 指纹数据的随机性，人工伪造的指纹往往熵值异常 |
| **稳定性 (Stability)** | 25 | 多次采集结果的波动程度，真实浏览器指纹应高度稳定 |

**输出示例：**

```
╔══════════════════════════════════════════════╗
║        StealthBrowser 反检测评分报告          ║
╠══════════════════════════════════════════════╣
║                                              ║
║  一致性 (Consistency)  ████████████░░░░  82  ║
║  唯一性 (Uniqueness)   ██████████████░░  88  ║
║  熵值 (Entropy)        ████████████████  95  ║
║  稳定性 (Stability)    █████████████░░░  79  ║
║                                              ║
║  ═════════════════════════════════════════    ║
║  综合评分: 86 / 100  [优秀]                  ║
║                                              ║
╚══════════════════════════════════════════════╝
```

## 3. `generate` — 指纹配置生成

根据预设或自定义参数生成指纹配置文件。

```bash
# 使用预设配置生成
stealth-browser generate --preset chrome
stealth-browser generate --preset firefox
stealth-browser generate --preset safari
stealth-browser generate --preset mobile
stealth-browser generate --preset crawler
stealth-browser generate --preset max-stealth

# 自定义生成
stealth-browser generate --custom --os windows --browser chrome --screen 1920x1080

# 导出为指定格式
stealth-browser generate --preset chrome --format yaml --output chrome-profile.yaml
```

**可用预设一览：**

| 预设名称 | 说明 | 适用场景 |
|----------|------|----------|
| `chrome` | 模拟 Chrome 浏览器指纹 | 通用场景，兼容性最佳 |
| `firefox` | 模拟 Firefox 浏览器指纹 | 通用场景，隐私性较好 |
| `safari` | 模拟 Safari 浏览器指纹 | macOS 专用场景 |
| `mobile` | 模拟移动端浏览器指纹 | 移动端模拟、App 内嵌 WebView |
| `crawler` | 爬虫专用低资源指纹 | 大规模数据采集，降低被检测概率 |
| `max-stealth` | 最大隐身配置 | 高匿名需求场景，牺牲部分兼容性 |

## 4. `report` — 可视化报告

生成并展示指纹分析报告。

```bash
# 生成 HTML 报告
stealth-browser report --format html --output report.html

# 启动 TUI 终端仪表盘
stealth-browser report --tui

# 生成 Markdown 格式报告
stealth-browser report --format markdown --output report.md
```

## 5. `compare` — 指纹对比

对比两组指纹配置或两次扫描结果的差异。

```bash
# 对比两个指纹文件
stealth-browser compare profile-a.json profile-b.json

# 对比当前环境与预设配置
stealth-browser compare --preset chrome

# 仅对比特定维度
stealth-browser compare profile-a.json profile-b.json --dimensions canvas,webgl
```

**输出示例：**

```
指纹对比报告
═══════════════════════════════════════════════════

维度          │ Profile A          │ Profile B          │ 差异
──────────────┼────────────────────┼────────────────────┼──────
Canvas Hash   │ a1b2c3d4...        │ e5f6a7b8...        │ ⚠ 不同
WebGL 渲染器   │ NVIDIA GeForce...  │ AMD Radeon...      │ ⚠ 不同
音频采样率     │ 44100              │ 44100              │ ✅ 一致
屏幕分辨率     │ 1920x1080          │ 1920x1080          │ ✅ 一致
时区           │ Asia/Shanghai      │ America/New_York   │ ⚠ 不同

差异率: 40% (2/5 维度完全一致)
```

## 6. `presets` — 预设管理

管理内置和自定义的指纹预设配置。

```bash
# 列出所有可用预设
stealth-browser presets list

# 查看预设详情
stealth-browser presets show chrome

# 导入自定义预设
stealth-browser presets import my-preset.yaml

# 导出预设
stealth-browser presets export chrome --output chrome-export.yaml
```

---

# 💡 设计思路与迭代规划

## 技术选型原因

| 决策 | 选择 | 原因 |
|------|------|------|
| **语言** | Python | 安全研究领域生态最丰富，脚本化能力强 |
| **依赖策略** | 零外部依赖 | 降低部署门槛，避免依赖冲突，适合 CI/CD 和容器化场景 |
| **输出格式** | JSON/YAML/HTML | JSON 适合程序处理，YAML 适合人工阅读，HTML 适合分享展示 |
| **终端 UI** | `curses` | Python 标准库原生支持，跨平台兼容 |
| **评分算法** | 加权多维评分 | 简单直观，便于理解和扩展 |

## 后续迭代规划

- [ ] **v0.2** — 增加浏览器自动化集成模块（Selenium/Playwright 适配层）
- [ ] **v0.3** — 支持指纹历史趋势追踪和基线对比
- [ ] **v0.4** — 增加代理指纹检测（VPN/代理/Tor 出口节点识别）
- [ ] **v0.5** — 提供 Web API 服务模式，支持远程调用
- [ ] **v1.0** — 正式稳定版发布，完善文档和插件系统

---

# 📦 打包与部署指南

## 从 PyPI 安装

```bash
pip install stealth-browser
```

## 从源码安装

```bash
git clone https://github.com/your-username/stealth-browser.git
cd stealth-browser
pip install -e .    # 开发模式安装
# 或
pip install .       # 正式安装
```

## 构建发布包

```bash
# 安装构建工具
pip install build

# 构建 sdist 和 wheel
python -m build

# 发布到 PyPI
python -m twine upload dist/*
```

## Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .

ENTRYPOINT ["stealth-browser"]
CMD ["--help"]
```

```bash
# 构建镜像
docker build -t stealth-browser .

# 运行扫描
docker run --rm stealth-browser scan --format json
```

## 在 CI/CD 中使用

```yaml
# GitHub Actions 示例
- name: Install StealthBrowser
  run: pip install stealth-browser

- name: Run Fingerprint Scan
  run: stealth-browser scan --format json --output fingerprint.json

- name: Run Anti-Detection Score
  run: stealth-browser score --summary
```

---

# 🤝 贡献指南

我们欢迎并感谢所有形式的贡献！无论是提交 Bug 报告、改进文档，还是提交代码 PR。

## 提交 Issue

1. 在提交 Issue 前，请先搜索已有 Issue 列表，确认问题未被提出
2. 使用清晰的标题描述问题
3. 附上完整的复现步骤、环境信息和错误日志
4. 如有可能，附上最小化的复现代码

## 提交 Pull Request

1. **Fork** 本仓库并创建你的特性分支：`git checkout -b feature/your-feature-name`
2. 确保所有**现有测试通过**：`python -m pytest tests/`
3. 为新功能**编写测试用例**，保持测试覆盖率
4. 确保代码通过 **lint 检查**：`python -m flake8 src/`
5. **提交** 并编写清晰的 Commit Message（遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范）
6. **推送** 到你的 Fork 并创建 Pull Request

## 代码规范

- 遵循 PEP 8 编码规范
- 函数和类需包含完整的 docstring
- 类型注解覆盖所有公共 API
- 单个函数不超过 50 行

---

# 📄 开源协议

本项目基于 [MIT License](https://opensource.org/licenses/MIT) 开源。

```
MIT License

Copyright (c) 2024 StealthBrowser Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**[回到顶部 ⬆](#stealthbrowser)**

</div>

---
---

<a id="繁體中文"></a>

# 🎉 專案介紹

**StealthBrowser** 是一款專為安全研究人員、爬蟲工程師和隱私愛好者打造的**輕量級反偵測瀏覽器指紋分析 CLI 引擎**。

## 解決的痛點

在日常的 Web 自動化、資料採集和隱私保護場景中，瀏覽器指紋辨識技術被廣泛用於偵測和攔截自動化工具。傳統的指紋偵測方案往往存在以下問題：

| 痛點 | 說明 |
|------|------|
| **依賴臃腫** | 現有工具多依賴 Selenium、Playwright 等重型框架，部署成本高 |
| **維度不足** | 僅涵蓋 Canvas/WebGL 等少數維度，容易被繞過 |
| **缺乏評分** | 無法量化評估反偵測效果，難以針對性最佳化 |
| **配置僵化** | 缺少預設配置，每次都需要手動調參 |

## 核心價值

- **零外部依賴** — 純 Python 標準函式庫實作，`pip install` 即用，無需安裝瀏覽器驅動
- **50+ 維度指紋採集** — 全面涵蓋 Canvas、WebGL、Audio、字型、硬體、網路、行為、儲存、螢幕、時區、HTTP 請求頭等維度
- **反偵測評分系統** — 0-100 分量化評分，從一致性、唯一性、熵值、穩定性四個維度綜合評估
- **6 種預設指紋配置** — Chrome / Firefox / Safari / 行動端 / 爬蟲 / 最大隱身，一鍵切換
- **多格式匯出** — 支援 JSON、YAML、HTML 三種格式輸出
- **TUI 終端儀表板** — 在終端中直接視覺化查看分析結果

## 差異化亮點

StealthBrowser 與同類工具的核心區別在於：**它不是一個瀏覽器自動化工具，而是一個指紋分析引擎**。它專注於指紋的採集、評分和配置生成，可以與任何瀏覽器自動化框架搭配使用，也可以獨立運行進行環境偵測。

---

# ✨ 核心特性

- **🔍 50+ 維度指紋採集** — 深度涵蓋 Canvas、WebGL（渲染器/供應商/擴充功能）、AudioContext、字型列舉、硬體並行數/記憶體/顯示卡、網路資訊/連線類型、行為特徵（滑鼠/鍵盤/觸控）、儲存偵測（Cookie/LocalStorage/IndexedDB）、螢幕解析度/色深/像素比、時區/語言/地區、HTTP 請求頭分析等

- **📊 四維度反偵測評分** — 從**一致性**（各維度間是否矛盾）、**唯一性**（指紋在群體中的稀有度）、**熵值**（資訊的隨機性程度）、**穩定性**（多次採集的波動情況）四個維度進行 0-100 分量化評估

- **🎭 6 種預設指紋配置** — 內建 Chrome、Firefox、Safari、行動端（iOS/Android）、爬蟲（低資源消耗）、最大隱身（最高匿名性）六套預設方案，支援自訂擴充

- **📋 多格式匯出** — JSON（結構化資料）、YAML（可讀配置）、HTML（視覺化報告）三種輸出格式，滿足不同使用場景

- **🖥️ TUI 終端視覺化儀表板** — 基於 `curses` 的終端 UI，即時展示指紋分析結果，支援鍵盤互動瀏覽各維度詳情

- **🧪 53 個單元測試** — 完善的測試覆蓋，確保採集邏輯和評分演算法的準確性

- **📦 零外部依賴** — 全部基於 Python 標準函式庫（`json`、`yaml`、`urllib`、`curses`、`hashlib`、`subprocess` 等），無第三方套件依賴

- **⚡ 高效能採集** — 平行化指紋採集流程，單次全量掃描耗時 < 3 秒

---

# 🚀 快速開始

## 環境要求

| 項目 | 要求 |
|------|------|
| **Python** | 3.8 及以上版本 |
| **作業系統** | Windows / macOS / Linux |
| **終端** | 支援 ANSI 跳脫序列或 `curses` 的終端（TUI 功能需要） |

## 安裝

```bash
# 從 PyPI 安裝（推薦）
pip install stealth-browser

# 或從原始碼安裝
git clone https://github.com/your-username/stealth-browser.git
cd stealth-browser
pip install .
```

## 啟動

```bash
# 查看說明資訊
stealth-browser --help

# 快速掃描目前瀏覽器環境指紋
stealth-browser scan

# 執行反偵測評分
stealth-browser score

# 啟動 TUI 視覺化儀表板
stealth-browser report --tui
```

---

# 📖 詳細使用指南

## 1. `scan` — 指紋掃描

採集目前環境的完整瀏覽器指紋資料。

```bash
# 全量掃描所有維度
stealth-browser scan

# 指定輸出格式
stealth-browser scan --format json     # JSON 格式
stealth-browser scan --format yaml     # YAML 格式
stealth-browser scan --format html     # HTML 格式

# 指定輸出檔案
stealth-browser scan --output result.json

# 僅掃描特定維度
stealth-browser scan --dimensions canvas,webgl,audio,fonts

# 靜默模式（僅輸出資料，無進度資訊）
stealth-browser scan --quiet
```

**輸出範例（JSON）：**

```json
{
  "canvas": {
    "hash": "a1b2c3d4e5f6...",
    "text_metrics": true,
    "image_data": true
  },
  "webgl": {
    "renderer": "ANGLE (Intel, Mesa Intel(R) UHD Graphics...)",
    "vendor": "Google Inc. (Intel)",
    "extensions": ["ANGLE_instanced_arrays", "OES_texture_float", "..."],
    "parameters": {
      "MAX_TEXTURE_SIZE": 16384,
      "MAX_RENDERBUFFER_SIZE": 16384
    }
  },
  "audio": {
    "sample_rate": 44100,
    "channel_count": 2,
    "hash": "f6e5d4c3b2a1..."
  }
}
```

## 2. `score` — 反偵測評分

對目前環境進行反偵測能力評分。

```bash
# 執行完整評分
stealth-browser score

# 查看各維度詳細評分
stealth-browser score --verbose

# 僅查看總分
stealth-browser score --summary
```

**評分維度說明：**

| 維度 | 滿分 | 說明 |
|------|------|------|
| **一致性 (Consistency)** | 25 | 各指紋維度之間是否存在矛盾（如聲稱是 macOS 卻使用 Windows 字型） |
| **唯一性 (Uniqueness)** | 25 | 指紋在全域指紋庫中的稀有程度，越普通越不易被追蹤 |
| **熵值 (Entropy)** | 25 | 指紋資料的隨機性，人工偽造的指紋往往熵值異常 |
| **穩定性 (Stability)** | 25 | 多次採集結果的波動程度，真實瀏覽器指紋應高度穩定 |

**輸出範例：**

```
╔══════════════════════════════════════════════╗
║       StealthBrowser 反偵測評分報告           ║
╠══════════════════════════════════════════════╣
║                                              ║
║  一致性 (Consistency)  ████████████░░░░  82  ║
║  唯一性 (Uniqueness)   ██████████████░░  88  ║
║  熵值 (Entropy)        ████████████████  95  ║
║  穩定性 (Stability)    █████████████░░░  79  ║
║                                              ║
║  ═════════════════════════════════════════    ║
║  綜合評分: 86 / 100  [優秀]                  ║
║                                              ║
╚══════════════════════════════════════════════╝
```

## 3. `generate` — 指紋配置生成

根據預設或自訂參數生成指紋配置檔案。

```bash
# 使用預設配置生成
stealth-browser generate --preset chrome
stealth-browser generate --preset firefox
stealth-browser generate --preset safari
stealth-browser generate --preset mobile
stealth-browser generate --preset crawler
stealth-browser generate --preset max-stealth

# 自訂生成
stealth-browser generate --custom --os windows --browser chrome --screen 1920x1080

# 匯出為指定格式
stealth-browser generate --preset chrome --format yaml --output chrome-profile.yaml
```

**可用預設一覽：**

| 預設名稱 | 說明 | 適用場景 |
|----------|------|----------|
| `chrome` | 模擬 Chrome 瀏覽器指紋 | 通用場景，相容性最佳 |
| `firefox` | 模擬 Firefox 瀏覽器指紋 | 通用場景，隱私性較好 |
| `safari` | 模擬 Safari 瀏覽器指紋 | macOS 專用場景 |
| `mobile` | 模擬行動端瀏覽器指紋 | 行動端模擬、App 內嵌 WebView |
| `crawler` | 爬蟲專用低資源指紋 | 大規模資料採集，降低被偵測機率 |
| `max-stealth` | 最大隱身配置 | 高匿名需求場景，犧牲部分相容性 |

## 4. `report` — 視覺化報告

生成並展示指紋分析報告。

```bash
# 生成 HTML 報告
stealth-browser report --format html --output report.html

# 啟動 TUI 終端儀表板
stealth-browser report --tui

# 生成 Markdown 格式報告
stealth-browser report --format markdown --output report.md
```

## 5. `compare` — 指紋對比

對比兩組指紋配置或兩次掃描結果的差異。

```bash
# 對比兩個指紋檔案
stealth-browser compare profile-a.json profile-b.json

# 對比目前環境與預設配置
stealth-browser compare --preset chrome

# 僅對比特定維度
stealth-browser compare profile-a.json profile-b.json --dimensions canvas,webgl
```

**輸出範例：**

```
指紋對比報告
═══════════════════════════════════════════════════

維度          │ Profile A          │ Profile B          │ 差異
──────────────┼────────────────────┼────────────────────┼──────
Canvas Hash   │ a1b2c3d4...        │ e5f6a7b8...        │ ⚠ 不同
WebGL 渲染器   │ NVIDIA GeForce...  │ AMD Radeon...      │ ⚠ 不同
音訊取樣率     │ 44100              │ 44100              │ ✅ 一致
螢幕解析度     │ 1920x1080          │ 1920x1080          │ ✅ 一致
時區           │ Asia/Shanghai      │ America/New_York   │ ⚠ 不同

差異率: 40% (2/5 維度完全一致)
```

## 6. `presets` — 預設管理

管理內建和自訂的指紋預設配置。

```bash
# 列出所有可用預設
stealth-browser presets list

# 查看預設詳情
stealth-browser presets show chrome

# 匯入自訂預設
stealth-browser presets import my-preset.yaml

# 匯出預設
stealth-browser presets export chrome --output chrome-export.yaml
```

---

# 💡 設計思路與迭代規劃

## 技術選型原因

| 決策 | 選擇 | 原因 |
|------|------|------|
| **語言** | Python | 安全研究領域生態最豐富，腳本化能力強 |
| **依賴策略** | 零外部依賴 | 降低部署門檻，避免依賴衝突，適合 CI/CD 和容器化場景 |
| **輸出格式** | JSON/YAML/HTML | JSON 適合程式處理，YAML 適合人工閱讀，HTML 適合分享展示 |
| **終端 UI** | `curses` | Python 標準函式庫原生支援，跨平台相容 |
| **評分演算法** | 加權多維評分 | 簡單直觀，便於理解和擴充 |

## 後續迭代規劃

- [ ] **v0.2** — 增加瀏覽器自動化整合模組（Selenium/Playwright 介面卡層）
- [ ] **v0.3** — 支援指紋歷史趨勢追蹤和基線對比
- [ ] **v0.4** — 增加代理指紋偵測（VPN/代理/Tor 出口節點辨識）
- [ ] **v0.5** — 提供 Web API 服務模式，支援遠端呼叫
- [ ] **v1.0** — 正式穩定版發布，完善文件和外掛系統

---

# 📦 打包與部署指南

## 從 PyPI 安裝

```bash
pip install stealth-browser
```

## 從原始碼安裝

```bash
git clone https://github.com/your-username/stealth-browser.git
cd stealth-browser
pip install -e .    # 開發模式安裝
# 或
pip install .       # 正式安裝
```

## 建構發布包

```bash
# 安裝建構工具
pip install build

# 建構 sdist 和 wheel
python -m build

# 發布到 PyPI
python -m twine upload dist/*
```

## Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .

ENTRYPOINT ["stealth-browser"]
CMD ["--help"]
```

```bash
# 建構映像檔
docker build -t stealth-browser .

# 執行掃描
docker run --rm stealth-browser scan --format json
```

## 在 CI/CD 中使用

```yaml
# GitHub Actions 範例
- name: Install StealthBrowser
  run: pip install stealth-browser

- name: Run Fingerprint Scan
  run: stealth-browser scan --format json --output fingerprint.json

- name: Run Anti-Detection Score
  run: stealth-browser score --summary
```

---

# 🤝 貢獻指南

我們歡迎並感謝所有形式的貢獻！無論是提交 Bug 回報、改進文件，還是提交程式碼 PR。

## 提交 Issue

1. 在提交 Issue 前，請先搜尋已有 Issue 列表，確認問題未被提出
2. 使用清晰的標題描述問題
3. 附上完整的重現步驟、環境資訊和錯誤日誌
4. 如有可能，附上最小化的重現程式碼

## 提交 Pull Request

1. **Fork** 本儲存庫並建立你的特性分支：`git checkout -b feature/your-feature-name`
2. 確保所有**現有測試通過**：`python -m pytest tests/`
3. 為新功能**編寫測試案例**，保持測試覆蓋率
4. 確保程式碼通過 **lint 檢查**：`python -m flake8 src/`
5. **提交** 並撰寫清晰的 Commit Message（遵循 [Conventional Commits](https://www.conventionalcommits.org/) 規範）
6. **推送** 到你的 Fork 並建立 Pull Request

## 程式碼規範

- 遵循 PEP 8 編碼規範
- 函式和類別需包含完整的 docstring
- 型別註解覆蓋所有公共 API
- 單一函式不超過 50 行

---

# 📄 開源協議

本專案基於 [MIT License](https://opensource.org/licenses/MIT) 開源。

```
MIT License

Copyright (c) 2024 StealthBrowser Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**[回到頂部 ⬆](#stealthbrowser)**

</div>

---
---

<a id="english"></a>

# 🎉 Introduction

**StealthBrowser** is a **lightweight anti-detection browser fingerprint analysis CLI engine** built for security researchers, web scraping engineers, and privacy enthusiasts.

## Problems It Solves

In everyday web automation, data collection, and privacy protection scenarios, browser fingerprinting technology is widely used to detect and block automated tools. Existing fingerprint detection solutions often suffer from the following issues:

| Pain Point | Description |
|------------|-------------|
| **Heavy Dependencies** | Most tools rely on Selenium, Playwright, or other heavyweight frameworks, resulting in high deployment costs |
| **Insufficient Coverage** | Only a few dimensions (Canvas/WebGL) are covered, making them easy to bypass |
| **No Scoring System** | Unable to quantitatively evaluate anti-detection effectiveness for targeted optimization |
| **Rigid Configuration** | Lacks preset profiles, requiring manual parameter tuning every time |

## Core Value

- **Zero External Dependencies** — Built entirely on the Python standard library; just `pip install` and go, no browser drivers needed
- **50+ Fingerprint Dimensions** — Comprehensive coverage of Canvas, WebGL, Audio, Fonts, Hardware, Network, Behavior, Storage, Screen, Timezone, HTTP Headers, and more
- **Anti-Detection Scoring System** — Quantified 0-100 scoring across four dimensions: Consistency, Uniqueness, Entropy, and Stability
- **6 Preset Fingerprint Profiles** — Chrome / Firefox / Safari / Mobile / Crawler / Max Stealth, switch with a single command
- **Multi-Format Export** — Supports JSON, YAML, and HTML output formats
- **TUI Terminal Dashboard** — Visualize analysis results directly in your terminal

## What Makes It Different

The key distinction between StealthBrowser and similar tools is that **it is not a browser automation tool, but a fingerprint analysis engine**. It focuses on fingerprint collection, scoring, and profile generation. It can work alongside any browser automation framework or run independently for environment detection.

---

# ✨ Core Features

- **🔍 50+ Fingerprint Dimensions** — Deep coverage of Canvas, WebGL (renderer/vendor/extensions), AudioContext, font enumeration, hardware concurrency/memory/GPU, network info/connection type, behavioral patterns (mouse/keyboard/touch), storage detection (Cookie/LocalStorage/IndexedDB), screen resolution/color depth/pixel ratio, timezone/language/locale, HTTP header analysis, and more

- **📊 Four-Dimension Anti-Detection Scoring** — Quantified 0-100 scoring across **Consistency** (contradictions between dimensions), **Uniqueness** (rarity within the population), **Entropy** (randomness of information), and **Stability** (variance across multiple collections)

- **🎭 6 Preset Fingerprint Profiles** — Built-in Chrome, Firefox, Safari, Mobile (iOS/Android), Crawler (low resource footprint), and Max Stealth (maximum anonymity) profiles, with support for custom extensions

- **📋 Multi-Format Export** — JSON (structured data), YAML (human-readable configuration), and HTML (visual report) output formats to suit different use cases

- **🖥️ TUI Terminal Dashboard** — A `curses`-based terminal UI for real-time fingerprint analysis visualization with keyboard-driven navigation across dimension details

- **🧪 53 Unit Tests** — Comprehensive test coverage ensuring accuracy of collection logic and scoring algorithms

- **📦 Zero External Dependencies** — Entirely built on the Python standard library (`json`, `yaml`, `urllib`, `curses`, `hashlib`, `subprocess`, etc.), no third-party packages required

- **⚡ High-Performance Collection** — Parallelized fingerprint collection pipeline, full scan completes in under 3 seconds

---

# 🚀 Quick Start

## Requirements

| Item | Requirement |
|------|-------------|
| **Python** | 3.8 or later |
| **Operating System** | Windows / macOS / Linux |
| **Terminal** | ANSI escape sequence or `curses`-capable terminal (required for TUI features) |

## Installation

```bash
# Install from PyPI (recommended)
pip install stealth-browser

# Or install from source
git clone https://github.com/your-username/stealth-browser.git
cd stealth-browser
pip install .
```

## Getting Started

```bash
# View help information
stealth-browser --help

# Quick scan of current browser environment fingerprint
stealth-browser scan

# Run anti-detection scoring
stealth-browser score

# Launch TUI visual dashboard
stealth-browser report --tui
```

---

# 📖 Detailed Usage Guide

## 1. `scan` — Fingerprint Scanning

Collects complete browser fingerprint data from the current environment.

```bash
# Full scan across all dimensions
stealth-browser scan

# Specify output format
stealth-browser scan --format json     # JSON format
stealth-browser scan --format yaml     # YAML format
stealth-browser scan --format html     # HTML format

# Specify output file
stealth-browser scan --output result.json

# Scan specific dimensions only
stealth-browser scan --dimensions canvas,webgl,audio,fonts

# Quiet mode (data output only, no progress info)
stealth-browser scan --quiet
```

**Sample Output (JSON):**

```json
{
  "canvas": {
    "hash": "a1b2c3d4e5f6...",
    "text_metrics": true,
    "image_data": true
  },
  "webgl": {
    "renderer": "ANGLE (Intel, Mesa Intel(R) UHD Graphics...)",
    "vendor": "Google Inc. (Intel)",
    "extensions": ["ANGLE_instanced_arrays", "OES_texture_float", "..."],
    "parameters": {
      "MAX_TEXTURE_SIZE": 16384,
      "MAX_RENDERBUFFER_SIZE": 16384
    }
  },
  "audio": {
    "sample_rate": 44100,
    "channel_count": 2,
    "hash": "f6e5d4c3b2a1..."
  }
}
```

## 2. `score` — Anti-Detection Scoring

Scores the current environment's anti-detection capabilities.

```bash
# Run full scoring
stealth-browser score

# View detailed scores per dimension
stealth-browser score --verbose

# View total score only
stealth-browser score --summary
```

**Scoring Dimensions:**

| Dimension | Max Score | Description |
|-----------|-----------|-------------|
| **Consistency** | 25 | Whether contradictions exist between fingerprint dimensions (e.g., claiming macOS but using Windows fonts) |
| **Uniqueness** | 25 | How rare the fingerprint is in the global fingerprint database; more common means harder to track |
| **Entropy** | 25 | Randomness of fingerprint data; artificially forged fingerprints often have abnormal entropy |
| **Stability** | 25 | Variance across multiple collections; real browser fingerprints should be highly stable |

**Sample Output:**

```
╔══════════════════════════════════════════════╗
║     StealthBrowser Anti-Detection Score      ║
╠══════════════════════════════════════════════╣
║                                              ║
║  Consistency         ████████████░░░░  82    ║
║  Uniqueness          ██████████████░░  88    ║
║  Entropy             ████████████████  95    ║
║  Stability           █████████████░░░  79    ║
║                                              ║
║  ═════════════════════════════════════════    ║
║  Overall Score: 86 / 100  [Excellent]        ║
║                                              ║
╚══════════════════════════════════════════════╝
```

## 3. `generate` — Fingerprint Profile Generation

Generates fingerprint configuration files based on presets or custom parameters.

```bash
# Generate using preset profiles
stealth-browser generate --preset chrome
stealth-browser generate --preset firefox
stealth-browser generate --preset safari
stealth-browser generate --preset mobile
stealth-browser generate --preset crawler
stealth-browser generate --preset max-stealth

# Custom generation
stealth-browser generate --custom --os windows --browser chrome --screen 1920x1080

# Export to a specific format
stealth-browser generate --preset chrome --format yaml --output chrome-profile.yaml
```

**Available Presets:**

| Preset | Description | Use Case |
|--------|-------------|----------|
| `chrome` | Simulates Chrome browser fingerprint | General use, best compatibility |
| `firefox` | Simulates Firefox browser fingerprint | General use, better privacy |
| `safari` | Simulates Safari browser fingerprint | macOS-specific scenarios |
| `mobile` | Simulates mobile browser fingerprint | Mobile emulation, in-app WebView |
| `crawler` | Crawler-specific low-resource fingerprint | Large-scale data collection, reduced detection risk |
| `max-stealth` | Maximum stealth configuration | High anonymity requirements, some compatibility trade-offs |

## 4. `report` — Visual Reports

Generates and displays fingerprint analysis reports.

```bash
# Generate HTML report
stealth-browser report --format html --output report.html

# Launch TUI terminal dashboard
stealth-browser report --tui

# Generate Markdown report
stealth-browser report --format markdown --output report.md
```

## 5. `compare` — Fingerprint Comparison

Compares differences between two fingerprint profiles or two scan results.

```bash
# Compare two fingerprint files
stealth-browser compare profile-a.json profile-b.json

# Compare current environment against a preset
stealth-browser compare --preset chrome

# Compare specific dimensions only
stealth-browser compare profile-a.json profile-b.json --dimensions canvas,webgl
```

**Sample Output:**

```
Fingerprint Comparison Report
═══════════════════════════════════════════════════

Dimension       │ Profile A          │ Profile B          │ Status
────────────────┼────────────────────┼────────────────────┼───────
Canvas Hash     │ a1b2c3d4...        │ e5f6a7b8...        │ Differs
WebGL Renderer  │ NVIDIA GeForce...  │ AMD Radeon...      │ Differs
Audio Sample    │ 44100              │ 44100              │ Match
Screen Res      │ 1920x1080          │ 1920x1080          │ Match
Timezone        │ Asia/Shanghai      │ America/New_York   │ Differs

Divergence: 40% (2/5 dimensions match)
```

## 6. `presets` — Preset Management

Manages built-in and custom fingerprint preset profiles.

```bash
# List all available presets
stealth-browser presets list

# View preset details
stealth-browser presets show chrome

# Import a custom preset
stealth-browser presets import my-preset.yaml

# Export a preset
stealth-browser presets export chrome --output chrome-export.yaml
```

---

# 💡 Design Philosophy & Roadmap

## Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Language** | Python | Richest ecosystem in security research; excellent scripting capabilities |
| **Dependency Strategy** | Zero external deps | Lowers deployment barrier, avoids dependency conflicts, ideal for CI/CD and containerized environments |
| **Output Formats** | JSON/YAML/HTML | JSON for programmatic processing, YAML for human readability, HTML for sharing and presentation |
| **Terminal UI** | `curses` | Natively supported in Python standard library, cross-platform compatible |
| **Scoring Algorithm** | Weighted multi-dimensional | Simple, intuitive, easy to understand and extend |

## Roadmap

- [ ] **v0.2** — Browser automation integration module (Selenium/Playwright adapter layer)
- [ ] **v0.3** — Fingerprint history trend tracking and baseline comparison
- [ ] **v0.4** — Proxy fingerprint detection (VPN/Proxy/Tor exit node identification)
- [ ] **v0.5** — Web API service mode for remote invocation
- [ ] **v1.0** — Stable release with comprehensive documentation and plugin system

---

# 📦 Packaging & Deployment Guide

## Install from PyPI

```bash
pip install stealth-browser
```

## Install from Source

```bash
git clone https://github.com/your-username/stealth-browser.git
cd stealth-browser
pip install -e .    # Development mode
# or
pip install .       # Production install
```

## Build Release Packages

```bash
# Install build tools
pip install build

# Build sdist and wheel
python -m build

# Publish to PyPI
python -m twine upload dist/*
```

## Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir .

ENTRYPOINT ["stealth-browser"]
CMD ["--help"]
```

```bash
# Build image
docker build -t stealth-browser .

# Run scan
docker run --rm stealth-browser scan --format json
```

## CI/CD Integration

```yaml
# GitHub Actions example
- name: Install StealthBrowser
  run: pip install stealth-browser

- name: Run Fingerprint Scan
  run: stealth-browser scan --format json --output fingerprint.json

- name: Run Anti-Detection Score
  run: stealth-browser score --summary
```

---

# 🤝 Contributing Guide

We welcome and appreciate contributions of all kinds — whether it's filing bug reports, improving documentation, or submitting code PRs.

## Filing Issues

1. Before filing an issue, please search the existing issue list to confirm it hasn't already been reported
2. Use a clear, descriptive title
3. Include complete reproduction steps, environment details, and error logs
4. If possible, attach a minimal reproduction code snippet

## Submitting Pull Requests

1. **Fork** this repository and create your feature branch: `git checkout -b feature/your-feature-name`
2. Ensure all **existing tests pass**: `python -m pytest tests/`
3. **Write test cases** for new features to maintain test coverage
4. Ensure code passes **lint checks**: `python -m flake8 src/`
5. **Commit** with a clear commit message (following the [Conventional Commits](https://www.conventionalcommits.org/) specification)
6. **Push** to your fork and create a Pull Request

## Code Standards

- Follow PEP 8 coding conventions
- All functions and classes must include complete docstrings
- Type annotations required for all public APIs
- Individual functions should not exceed 50 lines

---

# 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

```
MIT License

Copyright (c) 2024 StealthBrowser Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**[Back to Top ⬆](#stealthbrowser)**

</div>
