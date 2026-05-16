# -*- coding: utf-8 -*-
"""StealthBrowser CLI入口

StealthBrowser CLI entry point.
使用argparse实现命令行接口。
"""

import argparse
import json
import sys

from . import __version__
from .engine.collector import FingerprintCollector
from .engine.analyzer import FingerprintAnalyzer
from .engine.scorer import AntiDetectScorer
from .engine.generator import FingerprintGenerator
from .profiles.presets import list_presets, get_preset
from .export.json_export import export_json, load_json
from .export.yaml_export import export_yaml
from .export.html_export import export_html
from .utils.colors import (
    Colors, print_table, print_score_gauge,
    ICON_OK, ICON_FAIL, ICON_WARN, ICON_INFO, ICON_BOX,
)


def create_parser():
    """创建命令行参数解析器

    Create CLI argument parser.

    Returns:
        argparse.ArgumentParser: 参数解析器 / Argument parser
    """
    parser = argparse.ArgumentParser(
        prog="stealth-browser",
        description="StealthBrowser - 轻量级反检测浏览器指纹分析CLI工具",
        epilog="示例: stealth-browser scan --device desktop --os windows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"StealthBrowser v{__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # scan命令 / scan command
    scan_parser = subparsers.add_parser("scan", help="扫描当前环境指纹")
    scan_parser.add_argument(
        "--device", "-d",
        choices=["desktop", "mobile"],
        default="desktop",
        help="设备类型 (默认: desktop)",
    )
    scan_parser.add_argument(
        "--os", "-o",
        choices=["windows", "macos", "linux", "android", "ios"],
        default="windows",
        help="操作系统类型 (默认: windows)",
    )
    scan_parser.add_argument(
        "--locale", "-l",
        default="zh-CN",
        help="地区设置 (默认: zh-CN)",
    )
    scan_parser.add_argument(
        "--seed", "-s",
        type=int,
        default=None,
        help="随机种子 (用于可重复结果)",
    )
    scan_parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="静默模式，只输出JSON",
    )

    # score命令 / score command
    score_parser = subparsers.add_parser("score", help="反检测评分")
    score_parser.add_argument(
        "--input", "-i",
        type=str,
        default=None,
        help="输入指纹JSON文件 (默认使用scan生成)",
    )
    score_parser.add_argument(
        "--device", "-d",
        choices=["desktop", "mobile"],
        default="desktop",
        help="设备类型 (默认: desktop)",
    )
    score_parser.add_argument(
        "--os", "-o",
        default="windows",
        help="操作系统类型 (默认: windows)",
    )
    score_parser.add_argument(
        "--seed", "-s",
        type=int,
        default=None,
        help="随机种子",
    )

    # generate命令 / generate command
    gen_parser = subparsers.add_parser("generate", help="生成指纹配置")
    gen_parser.add_argument(
        "--preset", "-p",
        choices=["desktop", "mobile", "bot", "stealth",
                 "desktop_chrome", "desktop_firefox",
                 "mobile_safari", "mobile_chrome",
                 "bot_friendly", "stealth_max"],
        default=None,
        help="预设模板",
    )
    gen_parser.add_argument(
        "--randomize", "-r",
        action="store_true",
        help="在预设基础上随机化",
    )
    gen_parser.add_argument(
        "--device", "-d",
        choices=["desktop", "mobile"],
        default=None,
        help="设备类型 (随机生成时使用)",
    )
    gen_parser.add_argument(
        "--seed", "-s",
        type=int,
        default=None,
        help="随机种子",
    )
    gen_parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="输出文件路径",
    )
    gen_parser.add_argument(
        "--format", "-f",
        choices=["json", "yaml"],
        default="json",
        help="输出格式 (默认: json)",
    )

    # report命令 / report command
    report_parser = subparsers.add_parser("report", help="导出分析报告")
    report_parser.add_argument(
        "--format", "-f",
        choices=["json", "yaml", "html"],
        default="json",
        help="报告格式 (默认: json)",
    )
    report_parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="输出文件路径",
    )
    report_parser.add_argument(
        "--input", "-i",
        type=str,
        default=None,
        help="输入指纹JSON文件",
    )
    report_parser.add_argument(
        "--device", "-d",
        choices=["desktop", "mobile"],
        default="desktop",
        help="设备类型 (默认: desktop)",
    )
    report_parser.add_argument(
        "--os",
        dest="os_param",
        default="windows",
        help="操作系统类型 (默认: windows)",
    )
    report_parser.add_argument(
        "--seed", "-s",
        type=int,
        default=None,
        help="随机种子",
    )

    # compare命令 / compare command
    compare_parser = subparsers.add_parser("compare", help="对比两个指纹配置")
    compare_parser.add_argument(
        "--profile-a", "-a",
        type=str,
        required=True,
        help="指纹配置A (JSON文件路径或预设名称)",
    )
    compare_parser.add_argument(
        "--profile-b", "-b",
        type=str,
        required=True,
        help="指纹配置B (JSON文件路径或预设名称)",
    )

    # presets命令 / presets command
    subparsers.add_parser("presets", help="列出所有可用预设")

    return parser


def cmd_scan(args):
    """执行scan命令

    Execute scan command.

    Args:
        args: 命令行参数 / CLI arguments
    """
    if args.quiet:
        Colors.disable()

    # 打印Banner / Print banner
    _print_banner()

    # 创建采集器并采集 / Create collector and collect
    collector = FingerprintCollector(
        device_type=args.device,
        os_type=args.os,
        locale=args.locale,
        seed=args.seed,
    )
    fingerprint_data = collector.collect_all(verbose=not args.quiet)

    # 打印摘要 / Print summary
    summary = collector.get_collection_summary()
    print(f"\n  {Colors.bold('采集摘要:')}")
    print(f"    维度数量: {summary['dimensions_collected']}/{summary['total_dimensions']}")
    print(f"    数据点数: {summary['total_data_points']}")
    print(f"    采集耗时: {summary['collection_time']}s")

    if args.quiet:
        print(json.dumps(fingerprint_data, ensure_ascii=False, default=str, indent=2))

    return fingerprint_data


def cmd_score(args):
    """执行score命令

    Execute score command.

    Args:
        args: 命令行参数 / CLI arguments
    """
    _print_banner()

    # 获取指纹数据 / Get fingerprint data
    if args.input:
        try:
            fingerprint_data = load_json(args.input)
            print(f"  {Colors.info(ICON_INFO)} 从文件加载指纹: {args.input}")
        except Exception as e:
            print(f"  {Colors.error(ICON_FAIL)} 加载文件失败: {e}")
            sys.exit(1)
    else:
        collector = FingerprintCollector(
            device_type=args.device,
            os_type=args.os,
            seed=args.seed,
        )
        fingerprint_data = collector.collect_all(verbose=True)

    # 分析 / Analyze
    analyzer = FingerprintAnalyzer(fingerprint_data)
    analysis_results = analyzer.analyze_all(verbose=True)

    # 评分 / Score
    scorer = AntiDetectScorer(fingerprint_data, analysis_results)
    score_results = scorer.score(verbose=True)

    return score_results


def cmd_generate(args):
    """执行generate命令

    Execute generate command.

    Args:
        args: 命令行参数 / CLI arguments
    """
    _print_banner()

    generator = FingerprintGenerator()

    # 确定预设名称 / Determine preset name
    preset_map = {
        "desktop": "desktop_chrome",
        "mobile": "mobile_chrome",
        "bot": "bot_friendly",
        "stealth": "stealth_max",
    }

    if args.preset:
        preset_name = preset_map.get(args.preset, args.preset)
        print(f"  {Colors.info(ICON_INFO)} 使用预设: {preset_name}")
        config = generator.from_preset(preset_name, randomize=args.randomize, seed=args.seed)
    elif args.device:
        print(f"  {Colors.info(ICON_INFO)} 随机生成: {args.device}")
        config = generator.random(device_type=args.device, seed=args.seed)
    else:
        print(f"  {Colors.info(ICON_INFO)} 随机生成: desktop")
        config = generator.random(device_type="desktop", seed=args.seed)

    # 导出 / Export
    if args.format == "yaml":
        output_str = export_yaml(config)
    else:
        output_str = export_json(config)

    if args.output:
        if args.format == "yaml":
            export_yaml(config, filepath=args.output)
        else:
            export_json(config, filepath=args.output)
        print(f"\n  {Colors.green(ICON_OK)} 配置已保存到: {args.output}")
    else:
        print(f"\n{output_str}")

    return config


def cmd_report(args):
    """执行report命令

    Execute report command.

    Args:
        args: 命令行参数 / CLI arguments
    """
    _print_banner()

    # 获取指纹数据 / Get fingerprint data
    if args.input:
        try:
            fingerprint_data = load_json(args.input)
            print(f"  {Colors.info(ICON_INFO)} 从文件加载指纹: {args.input}")
        except Exception as e:
            print(f"  {Colors.error(ICON_FAIL)} 加载文件失败: {e}")
            sys.exit(1)
    else:
        collector = FingerprintCollector(
            device_type=args.device,
            os_type=args.os_param,
            seed=args.seed,
        )
        fingerprint_data = collector.collect_all(verbose=True)

    # 分析 / Analyze
    analyzer = FingerprintAnalyzer(fingerprint_data)
    analysis_results = analyzer.analyze_all(verbose=True)

    # 评分 / Score
    scorer = AntiDetectScorer(fingerprint_data, analysis_results)
    score_results = scorer.score(verbose=True)

    # 导出报告 / Export report
    if args.format == "json":
        report_data = {
            "fingerprint": fingerprint_data,
            "analysis": analysis_results,
            "score": score_results,
        }
        output_str = export_json(report_data)
        if args.output:
            export_json(report_data, filepath=args.output)
            print(f"\n  {Colors.green(ICON_OK)} JSON报告已保存到: {args.output}")
        else:
            print(f"\n{output_str}")

    elif args.format == "yaml":
        report_data = {
            "fingerprint": fingerprint_data,
            "analysis": analysis_results,
            "score": score_results,
        }
        output_str = export_yaml(report_data)
        if args.output:
            export_yaml(report_data, filepath=args.output)
            print(f"\n  {Colors.green(ICON_OK)} YAML报告已保存到: {args.output}")
        else:
            print(f"\n{output_str}")

    elif args.format == "html":
        output_str = export_html(fingerprint_data, analysis_results, score_results)
        output_path = args.output or "stealth-browser-report.html"
        export_html(fingerprint_data, analysis_results, score_results, filepath=output_path)
        print(f"\n  {Colors.green(ICON_OK)} HTML报告已保存到: {output_path}")


def cmd_compare(args):
    """执行compare命令

    Execute compare command.

    Args:
        args: 命令行参数 / CLI arguments
    """
    _print_banner()

    generator = FingerprintGenerator()

    # 加载配置A / Load config A
    config_a = _load_profile(args.profile_a, generator)
    if config_a is None:
        print(f"  {Colors.error(ICON_FAIL)} 无法加载配置A: {args.profile_a}")
        sys.exit(1)

    # 加载配置B / Load config B
    config_b = _load_profile(args.profile_b, generator)
    if config_b is None:
        print(f"  {Colors.error(ICON_FAIL)} 无法加载配置B: {args.profile_b}")
        sys.exit(1)

    # 对比 / Compare
    results = generator.compare_configs(config_a, config_b)

    # 打印对比结果 / Print comparison results
    print(f"\n  {Colors.bold(Colors.cyan('指纹配置对比'))}")
    print(f"  {Colors.DIM + '─' * 50 + Colors.RESET}")
    print(f"  配置A: {args.profile_a}")
    print(f"  配置B: {args.profile_b}")
    print()

    rows = []
    for dim, data in results.items():
        if isinstance(data, dict):
            if "hash_match" in data:
                match = data["hash_match"]
                icon = ICON_OK if match else ICON_FAIL
                status = Colors.green("匹配") if match else Colors.red("不匹配")
                rows.append([f"  {icon} {dim}", status])
            elif "similarity" in data:
                sim = data["similarity"]
                if sim >= 0.8:
                    icon = ICON_OK
                    status = Colors.green(f"{sim:.1%}")
                elif sim >= 0.5:
                    icon = ICON_WARN
                    status = Colors.yellow(f"{sim:.1%}")
                else:
                    icon = ICON_FAIL
                    status = Colors.red(f"{sim:.1%}")
                rows.append([f"  {icon} {dim}", f"相似度 {status}"])

    if rows:
        print_table(["维度", "对比结果"], rows, col_widths=[30, 20], title="对比详情")
    else:
        print(f"  {Colors.warning(ICON_WARN)} 无可对比的维度")


def cmd_presets(args):
    """执行presets命令

    Execute presets command.

    Args:
        args: 命令行参数 / CLI arguments
    """
    _print_banner()

    presets = list_presets()

    rows = []
    for preset in presets:
        rows.append([
            f"  {ICON_BOX} {preset['name']}",
            preset['device_type'],
            preset['description'],
        ])

    print_table(
        ["预设名称", "设备类型", "描述"],
        rows,
        col_widths=[20, 12, 40],
        title="可用预设配置",
    )


def _load_profile(profile_ref, generator):
    """加载指纹配置(文件或预设名称)

    Load fingerprint profile (file or preset name).

    Args:
        profile_ref (str): 文件路径或预设名称 / File path or preset name
        generator (FingerprintGenerator): 生成器实例 / Generator instance

    Returns:
        dict or None: 指纹配置 / Fingerprint configuration
    """
    # 尝试作为文件加载 / Try loading as file
    try:
        import os
        if os.path.isfile(profile_ref):
            return load_json(profile_ref)
    except Exception:
        pass

    # 尝试作为预设名称 / Try as preset name
    preset_map = {
        "desktop": "desktop_chrome",
        "mobile": "mobile_chrome",
        "bot": "bot_friendly",
        "stealth": "stealth_max",
    }
    preset_name = preset_map.get(profile_ref, profile_ref)
    config = get_preset(preset_name)
    if config:
        return config

    return None


def _print_banner():
    """打印程序Banner

    Print program banner.
    """
    banner = f"""
  {Colors.cyan('╔══════════════════════════════════════════════════╗')}
  {Colors.cyan('║')}  {Colors.BOLD}{Colors.BRIGHT_WHITE}StealthBrowser{Colors.RESET}  {Colors.dim('v' + __version__)}                      {Colors.cyan('║')}
  {Colors.cyan('║')}  {Colors.dim('轻量级反检测浏览器指纹分析工具')}            {Colors.cyan('║')}
  {Colors.cyan('╚══════════════════════════════════════════════════╝')}
"""
    print(banner)


def main():
    """CLI主入口

    CLI main entry point.
    """
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # 命令分发 / Command dispatch
    commands = {
        "scan": cmd_scan,
        "score": cmd_score,
        "generate": cmd_generate,
        "report": cmd_report,
        "compare": cmd_compare,
        "presets": cmd_presets,
    }

    handler = commands.get(args.command)
    if handler:
        try:
            handler(args)
        except KeyboardInterrupt:
            print(f"\n  {Colors.yellow(ICON_WARN)} 用户中断")
            sys.exit(0)
        except Exception as e:
            print(f"\n  {Colors.error(ICON_FAIL)} 错误: {e}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
