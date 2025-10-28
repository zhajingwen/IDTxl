#!/usr/bin/env python3
"""
加密货币网络分析系统测试脚本
用于验证系统功能和性能
"""

import sys
import time
import numpy as np
import pandas as pd
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from crypto_network_analysis import CryptoNetworkAnalyzer


def test_data_fetcher():
    """测试数据获取器"""
    print("🧪 测试数据获取器...")
    
    from crypto_network_analysis import HyperliquidDataFetcher
    
    fetcher = HyperliquidDataFetcher()
    
    # 测试获取代币信息
    tokens = fetcher.get_all_tokens()
    print(f"✅ 获取到 {len(tokens)} 个代币")
    
    if tokens:
        # 测试获取价格数据（小规模）
        test_tokens = [token['name'] for token in tokens[:5]]  # 只测试前5个
        prices = fetcher.get_token_prices(test_tokens, hours=24)
        print(f"✅ 获取到 {len(prices.columns)} 个代币的价格数据，形状: {prices.shape}")
        return True
    else:
        print("❌ 无法获取代币信息")
        return False


def test_analyzer_with_synthetic_data():
    """使用合成数据测试分析器"""
    print("🧪 测试分析器（合成数据）...")
    
    # 创建合成数据
    np.random.seed(42)
    n_assets = 10
    n_samples = 100
    
    # 生成相关的价格数据
    base_prices = np.random.randn(n_samples)
    price_data = {}
    
    for i in range(n_assets):
        if i < 3:  # 前3个资产高度相关
            noise = np.random.randn(n_samples) * 0.1
            price_data[f'ASSET_{i}'] = base_prices + noise
        elif i < 6:  # 中间3个资产中等相关
            noise = np.random.randn(n_samples) * 0.3
            price_data[f'ASSET_{i}'] = base_prices * 0.5 + noise
        else:  # 后4个资产独立
            price_data[f'ASSET_{i}'] = np.random.randn(n_samples)
    
    # 创建DataFrame
    df = pd.DataFrame(price_data)
    
    # 创建分析器
    config = {
        'max_tokens': 10,
        'time_hours': 24,
        'correlation_threshold': 0.5,
        'te_threshold': 0.05,
        'cmi_estimator': 'JidtKraskovCMI',  # 使用Kraskov CMI估计器
        'n_perm_max_stat': 20,  # 减少置换次数以加快测试
        'n_perm_min_stat': 20,
        'n_perm_omnibus': 50,
    }
    
    analyzer = CryptoNetworkAnalyzer(config)
    analyzer.price_data = df
    
    # 测试网络分析
    print("  执行网络分析...")
    start_time = time.time()
    success = analyzer.analyze_network()
    analysis_time = time.time() - start_time
    
    if success:
        print(f"✅ 网络分析完成，耗时: {analysis_time:.2f}秒")
        
        # 测试资产识别
        print("  识别高度关联资产...")
        results = analyzer.identify_highly_correlated_assets()
        
        if results:
            print(f"✅ 识别完成:")
            print(f"    - 高相关对: {results['summary']['highly_correlated_pairs']}")
            print(f"    - TE连接: {results['summary']['te_connections']}")
            print(f"    - 资产组合: {results['summary']['asset_combinations']}")
            
            # 显示部分结果
            if results.get('correlation_pairs'):
                print("   高相关对示例:")
                for pair in results['correlation_pairs'][:3]:
                    print(f"     {pair['asset1']} ↔ {pair['asset2']}: {pair['correlation']:.3f}")
            
            return True
        else:
            print("❌ 资产识别失败")
            return False
    else:
        print("❌ 网络分析失败")
        return False


def test_performance():
    """性能测试"""
    print("🧪 性能测试...")
    
    # 测试不同规模的数据
    test_cases = [
        (5, 50, "小规模"),
        (10, 100, "中规模"),
        (20, 200, "大规模"),
    ]
    
    for n_assets, n_samples, scale_name in test_cases:
        print(f"  测试 {scale_name} ({n_assets}个资产, {n_samples}个样本)...")
        
        # 生成测试数据
        np.random.seed(42)
        data = np.random.randn(n_assets, n_samples)
        
        # 创建分析器
        config = {
            'max_tokens': n_assets,
            'n_perm_max_stat': 10,  # 减少置换次数
            'n_perm_min_stat': 10,
            'n_perm_omnibus': 20,
        }
        
        analyzer = CryptoNetworkAnalyzer(config)
        
        # 准备数据
        data_array = data
        from idtxl.data import Data
        idtxl_data = Data(data_array, dim_order='ps')
        
        # 测试网络分析性能
        start_time = time.time()
        try:
            from idtxl.multivariate_te import MultivariateTE
            network_analysis = MultivariateTE()
            settings = {
                'cmi_estimator': 'JidtKraskovCMI',
                'max_lag_sources': 5,
                'min_lag_sources': 1,
                'max_lag_target': 3,
                'tau_sources': 1,
                'tau_target': 1,
                'n_perm_max_stat': 10,
                'n_perm_min_stat': 10,
                'n_perm_omnibus': 20,
            }
            
            results = network_analysis.analyse_network(settings=settings, data=idtxl_data)
            analysis_time = time.time() - start_time
            
            print(f"    ✅ 完成，耗时: {analysis_time:.2f}秒")
            
        except Exception as e:
            print(f"    ❌ 失败: {e}")


def test_configuration():
    """测试配置系统"""
    print("🧪 测试配置系统...")
    
    # 测试默认配置
    analyzer1 = CryptoNetworkAnalyzer()
    print(f"✅ 默认配置加载成功")
    
    # 测试自定义配置
    custom_config = {
        'max_tokens': 15,
        'time_hours': 72,
        'correlation_threshold': 0.8,
    }
    analyzer2 = CryptoNetworkAnalyzer(custom_config)
    print(f"✅ 自定义配置加载成功")
    
    # 验证配置合并
    assert analyzer2.config['max_tokens'] == 15
    assert analyzer2.config['time_hours'] == 72
    assert analyzer2.config['correlation_threshold'] == 0.8
    print(f"✅ 配置合并正确")


def main():
    """主测试函数"""
    print("🚀 加密货币网络分析系统测试")
    print("=" * 50)
    
    test_results = []
    
    # 测试1: 数据获取器
    try:
        result = test_data_fetcher()
        test_results.append(("数据获取器", result))
    except Exception as e:
        print(f"❌ 数据获取器测试失败: {e}")
        test_results.append(("数据获取器", False))
    
    # 测试2: 分析器（合成数据）
    try:
        result = test_analyzer_with_synthetic_data()
        test_results.append(("分析器（合成数据）", result))
    except Exception as e:
        print(f"❌ 分析器测试失败: {e}")
        test_results.append(("分析器（合成数据）", False))
    
    # 测试3: 性能测试
    try:
        test_performance()
        test_results.append(("性能测试", True))
    except Exception as e:
        print(f"❌ 性能测试失败: {e}")
        test_results.append(("性能测试", False))
    
    # 测试4: 配置系统
    try:
        test_configuration()
        test_results.append(("配置系统", True))
    except Exception as e:
        print(f"❌ 配置系统测试失败: {e}")
        test_results.append(("配置系统", False))
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常。")
        return 0
    else:
        print("⚠️ 部分测试失败，请检查系统配置。")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)