#!/usr/bin/env python3
"""
加密货币网络分析系统启动脚本 - 无Java版本
使用Python原生估计器，无需Java环境

使用方法:
python run_crypto_analysis_no_java.py [--config config_crypto.json] [--output output_dir]
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from crypto_network_analysis_no_java import CryptoNetworkAnalyzerNoJava


def load_config(config_path: str) -> dict:
    """加载配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"❌ 配置文件加载失败: {e}")
        return {}


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='加密货币网络分析系统（无Java版本）')
    parser.add_argument('--config', default='config_crypto.json', 
                       help='配置文件路径 (默认: config_crypto.json)')
    parser.add_argument('--output', default='output_no_java', 
                       help='输出目录 (默认: output_no_java)')
    parser.add_argument('--tokens', type=int, default=20,
                       help='最大分析代币数量 (默认: 20)')
    parser.add_argument('--hours', type=int, default=72,
                       help='分析时间窗口(小时) (默认: 72)')
    parser.add_argument('--correlation', type=float, default=0.6,
                       help='相关性阈值 (默认: 0.6)')
    parser.add_argument('--te', type=float, default=0.05,
                       help='传递熵阈值 (默认: 0.05)')
    parser.add_argument('--estimator', default='PythonKraskovCMI',
                       help='估计器类型 (默认: PythonKraskovCMI)')
    
    args = parser.parse_args()
    
    print("🚀 加密货币市场网络分析系统（无Java版本）")
    print("=" * 50)
    print(f"📁 配置文件: {args.config}")
    print(f"📁 输出目录: {args.output}")
    print(f"🪙 最大代币数: {args.tokens}")
    print(f"⏰ 时间窗口: {args.hours} 小时")
    print(f"📊 相关性阈值: {args.correlation}")
    print(f"🔄 传递熵阈值: {args.te}")
    print(f"🔧 估计器类型: {args.estimator}")
    print("=" * 50)
    
    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # 加载配置
    config = load_config(args.config)
    
    # 更新配置参数
    if 'data_processing' not in config:
        config['data_processing'] = {}
    
    config['data_processing'].update({
        'max_tokens': args.tokens,
        'time_hours': args.hours,
        'correlation_threshold': args.correlation,
        'te_threshold': args.te
    })
    
    # 更新估计器配置
    config['network_analysis'] = config.get('network_analysis', {})
    config['network_analysis']['cmi_estimator'] = args.estimator
    
    # 创建分析器
    analyzer = CryptoNetworkAnalyzerNoJava(config)
    
    try:
        # 获取和预处理数据
        print("\n📊 步骤 1/4: 获取和预处理数据...")
        if not analyzer.fetch_and_preprocess_data():
            print("❌ 数据获取失败")
            return 1
        
        # 执行网络分析
        print("\n🔍 步骤 2/4: 执行网络分析...")
        if not analyzer.analyze_network():
            print("❌ 网络分析失败")
            return 1
        
        # 识别高度关联的资产
        print("\n🎯 步骤 3/4: 识别高度关联的资产组合...")
        results = analyzer.identify_highly_correlated_assets()
        
        if not results:
            print("❌ 资产识别失败")
            return 1
        
        # 生成结果
        print("\n📈 步骤 4/4: 生成结果...")
        
        # 生成可视化
        plot_path = output_dir / 'crypto_network_analysis_no_java.png'
        analyzer.visualize_results(results, str(plot_path))
        
        # 生成报告
        report_path = output_dir / 'crypto_network_report_no_java.md'
        report = analyzer.generate_report(results, str(report_path))
        
        # 保存结果数据
        results_path = output_dir / 'analysis_results_no_java.json'
        import json
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 打印摘要
        print("\n" + "=" * 50)
        print("📊 分析完成！")
        print(f"✅ 分析了 {results['summary']['total_assets']} 个资产")
        print(f"✅ 发现 {results['summary']['highly_correlated_pairs']} 个高相关对")
        print(f"✅ 发现 {results['summary']['te_connections']} 个传递熵连接")
        print(f"✅ 识别出 {results['summary']['asset_combinations']} 个资产组合")
        print(f"✅ 网络密度: {results['summary'].get('network_density', 0):.3f}")
        print(f"\n📁 输出文件保存在: {output_dir.absolute()}")
        print(f"   - crypto_network_analysis_no_java.png (可视化图表)")
        print(f"   - crypto_network_report_no_java.md (分析报告)")
        print(f"   - analysis_results_no_java.json (结果数据)")
        print(f"   - crypto_network_analysis_no_java.log (日志文件)")
        
        # 显示部分结果
        if results.get('correlation_pairs'):
            print(f"\n🔗 高相关资产对 (前5个):")
            for i, pair in enumerate(results['correlation_pairs'][:5], 1):
                print(f"   {i}. {pair['asset1']} ↔ {pair['asset2']} (相关系数: {pair['correlation']:.4f})")
        
        if results.get('asset_combinations'):
            print(f"\n🎯 资产组合 (前3个):")
            for i, combo in enumerate(results['asset_combinations'][:3], 1):
                print(f"   {i}. {combo['type']} 组合: {', '.join(combo['assets'])} (大小: {combo['size']})")
        
        print(f"\n💡 技术说明:")
        print(f"   - 使用估计器: {args.estimator}")
        print(f"   - 无需Java环境")
        print(f"   - 基于Python原生实现")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断分析")
        return 1
    except Exception as e:
        print(f"\n❌ 分析过程中发生错误: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)