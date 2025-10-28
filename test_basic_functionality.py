#!/usr/bin/env python3
"""
基本功能测试脚本
验证IDTxl和加密货币分析系统的核心功能
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

def test_idtxl_imports():
    """测试IDTxl核心模块导入"""
    print("🧪 测试IDTxl核心模块导入...")
    
    try:
        from idtxl.data import Data
        from idtxl.multivariate_te import MultivariateTE
        from idtxl.multivariate_mi import MultivariateMI
        from idtxl.stats import fdrcorrection
        print("✅ IDTxl核心模块导入成功")
        return True
    except Exception as e:
        print(f"❌ IDTxl导入失败: {e}")
        return False

def test_crypto_analyzer_import():
    """测试加密货币分析器导入"""
    print("🧪 测试加密货币分析器导入...")
    
    try:
        from crypto_network_analysis import CryptoNetworkAnalyzer
        print("✅ 加密货币分析器导入成功")
        return True
    except Exception as e:
        print(f"❌ 加密货币分析器导入失败: {e}")
        return False

def test_basic_idtxl_functionality():
    """测试IDTxl基本功能"""
    print("🧪 测试IDTxl基本功能...")
    
    try:
        from idtxl.data import Data
        from idtxl.multivariate_te import MultivariateTE
        
        # 创建测试数据
        np.random.seed(42)
        data = np.random.randn(3, 100)  # 3个过程，100个样本
        
        # 创建IDTxl数据对象
        idtxl_data = Data(data, dim_order='ps')
        print(f"✅ 数据对象创建成功: {idtxl_data.n_processes}个过程, {idtxl_data.n_samples}个样本")
        
        # 创建分析器
        network_analysis = MultivariateTE()
        print("✅ MultivariateTE分析器创建成功")
        
        return True
    except Exception as e:
        print(f"❌ IDTxl基本功能测试失败: {e}")
        return False

def test_statsmodels_functionality():
    """测试statsmodels功能"""
    print("🧪 测试statsmodels功能...")
    
    try:
        from statsmodels.stats.multitest import fdrcorrection
        
        # 测试FDR校正
        p_values = [0.01, 0.05, 0.1, 0.2, 0.3]
        corrected_p, rejected = fdrcorrection(p_values, alpha=0.05)
        
        print(f"✅ FDR校正测试成功:")
        print(f"   原始p值: {p_values}")
        print(f"   校正后p值: {corrected_p}")
        print(f"   拒绝假设: {rejected}")
        
        return True
    except Exception as e:
        print(f"❌ statsmodels功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 基本功能测试")
    print("=" * 50)
    
    test_results = []
    
    # 测试1: IDTxl导入
    result = test_idtxl_imports()
    test_results.append(("IDTxl导入", result))
    
    # 测试2: 加密货币分析器导入
    result = test_crypto_analyzer_import()
    test_results.append(("加密货币分析器导入", result))
    
    # 测试3: IDTxl基本功能
    result = test_basic_idtxl_functionality()
    test_results.append(("IDTxl基本功能", result))
    
    # 测试4: statsmodels功能
    result = test_statsmodels_functionality()
    test_results.append(("statsmodels功能", result))
    
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
        print("🎉 所有基本功能测试通过！系统可以正常运行。")
        print("\n💡 下一步可以运行:")
        print("   uv run python test_crypto_analysis.py")
        return 0
    else:
        print("⚠️ 部分测试失败，请检查系统配置。")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
