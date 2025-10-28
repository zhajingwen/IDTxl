# 基于IDTxl的加密货币市场网络分析系统

## 🎯 项目简介

本项目基于IDTxl信息动力学工具包，实现了加密货币市场的网络分析系统。通过从Hyperliquid API获取实时价格数据，使用信息论方法（传递熵、互信息）分析资产间的关联性，识别高度关联的资产组合，为量化交易和风险管理提供数据支持。

## 🐍 纯Python实现

本项目采用纯Python实现，无需Java环境：

- **特点**: 使用Python原生估计器，部署简单
- **要求**: 仅需Python环境
- **适用**: 快速部署、各种规模分析
- **优势**: 无Java依赖、内存效率高、维护简单

## 🚀 核心功能

### 1. 数据获取与处理
- **实时数据**: 从Hyperliquid API获取加密货币价格数据
- **智能过滤**: 自动过滤低质量代币，选择有交易价值的资产
- **数据预处理**: 收益率计算、异常值处理、数据标准化

### 2. 网络分析
- **传递熵分析**: 识别资产间的信息流动方向
- **相关性分析**: 发现价格同步变动的资产对
- **统计检验**: FDR校正的显著性检验
- **多变量分析**: 同时分析多个资产间的复杂关系

### 3. 资产组合识别
- **高相关资产对**: 相关系数超过阈值的资产对
- **传递熵连接**: 信息流动显著的连接关系
- **智能组合**: 基于相关性和传递熵的资产组合
- **强度分级**: 高、中、低强度分类

### 4. 可视化与报告
- **综合分析面板**: 6个子图的综合分析视图
- **交互式网络图**: 传递熵网络结构可视化
- **排名图表**: 高相关对和传递熵连接排名
- **详细报告**: Markdown格式的分析报告

## 📁 项目结构

```
IDTxl/
├── crypto_network_analysis.py          # 核心分析模块
├── run_crypto_analysis.py              # 启动脚本
├── test_crypto_analysis.py             # 测试脚本
├── config.json                         # 配置文件
├── requirements.txt                    # 依赖包列表
├── 技术说明.md                         # 技术实现说明
├── 功能对比分析.md                     # 功能对比分析
├── 加密货币网络分析使用指南.md          # 详细使用指南
└── README_加密货币网络分析.md           # 项目说明（本文件）
```

## 🛠️ 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install -r requirements.txt

# 或者手动安装
pip install idtxl numpy pandas matplotlib seaborn requests scipy
```

### 2. 基本使用

```bash
# 使用默认配置运行
python run_crypto_analysis.py

# 自定义参数运行
python run_crypto_analysis.py --tokens 20 --hours 72 --correlation 0.6

# 指定输出目录
python run_crypto_analysis.py --output my_analysis_results
```

### 3. 测试系统

```bash
# 运行测试脚本
python test_crypto_analysis.py
```

## 📊 使用示例

### 示例1: 快速市场扫描
```bash
# 分析前20个代币，24小时数据
python run_crypto_analysis.py --tokens 20 --hours 24 --correlation 0.6
```

### 示例2: 深度关联分析
```bash
# 分析30个代币，72小时数据，高相关性阈值
python run_crypto_analysis.py --tokens 30 --hours 72 --correlation 0.7 --te 0.1
```

### 示例3: Python代码使用
```python
from crypto_network_analysis import CryptoNetworkAnalyzer

# 创建分析器
analyzer = CryptoNetworkAnalyzer()

# 获取数据并分析
analyzer.fetch_and_preprocess_data()
analyzer.analyze_network()
results = analyzer.identify_highly_correlated_assets()

# 生成报告
analyzer.visualize_results(results)
report = analyzer.generate_report(results)
```

## ⚙️ 配置说明

### 主要参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `max_tokens` | 30 | 最大分析代币数量 |
| `time_hours` | 72 | 分析时间窗口(小时) |
| `correlation_threshold` | 0.6 | 相关性阈值 |
| `te_threshold` | 0.05 | 传递熵阈值 |
| `n_perm_max_stat` | 50 | 最大统计置换次数 |
| `cmi_estimator` | PythonKraskovCMI | 估计器类型 |

### 性能优化

```json
{
  "network_analysis": {
    "cmi_estimator": "PythonKraskovCMI", // Python原生估计器
    "max_lag_sources": 6,                // 减少以加快计算
    "n_perm_max_stat": 50,               // 减少置换次数
    "kraskov_k": 4,                      // Kraskov参数
    "num_threads": "USE_ALL"             // 使用所有可用线程
  }
}
```

## 📈 输出结果

### 1. 可视化图表
- **相关性热力图**: 资产间相关性矩阵
- **传递熵网络图**: 信息流动网络结构
- **高相关资产对排名**: 相关系数最高的资产对
- **传递熵连接排名**: 信息流动最强的连接
- **组合类型分布**: 基于相关性和传递熵的组合分布
- **组合大小分布**: 资产组合大小统计

### 2. 分析报告
- **数据概览**: 分析资产数量、时间窗口等
- **高相关资产对**: 详细的相关性分析结果
- **传递熵连接**: 信息流动分析结果
- **资产组合**: 识别出的投资组合
- **投资建议**: 基于分析结果的投资建议

### 3. 数据文件
- **analysis_results.json**: 完整的分析结果数据
- **crypto_network_analysis.log**: 详细的执行日志

## 🔧 高级功能

### 1. 自定义数据源
```python
class CustomDataFetcher:
    def get_token_prices(self, tokens, hours):
        # 实现自定义数据获取逻辑
        pass

analyzer = CryptoNetworkAnalyzer()
analyzer.data_fetcher = CustomDataFetcher()
```

### 2. 自定义分析算法
```python
class CustomAnalyzer(CryptoNetworkAnalyzer):
    def identify_highly_correlated_assets(self):
        # 实现自定义识别算法
        pass
```

### 3. 实时监控
```bash
# 每小时运行一次监控
while true; do
    python run_crypto_analysis.py --output "monitor_$(date +%Y%m%d_%H%M%S)"
    sleep 3600
done
```

## 📊 应用场景

### 1. 量化交易
- **配对交易**: 识别高度相关的资产对进行配对交易
- **套利机会**: 发现价格差异和套利机会
- **风险对冲**: 构建相关性较低的投资组合

### 2. 风险管理
- **系统性风险**: 识别系统性风险传播路径
- **组合优化**: 基于相关性优化投资组合
- **压力测试**: 模拟市场冲击对组合的影响

### 3. 市场研究
- **市场结构**: 分析加密货币市场的网络结构
- **信息流动**: 研究市场信息传播机制
- **趋势预测**: 基于网络分析预测市场趋势

## ⚠️ 注意事项

### 1. 数据质量
- API数据可能存在延迟或不完整
- 建议定期验证数据质量
- 某些代币可能因流动性不足而数据异常

### 2. 计算资源
- 大规模分析需要较多内存和计算时间
- 建议在性能较好的机器上运行
- 纯Python实现内存使用较少

### 3. 结果解释
- 相关性不等于因果关系
- 历史数据不代表未来表现
- 建议结合其他分析方法验证结果

### 4. 风险提示
- 本分析仅供研究参考
- 不构成投资建议
- 投资有风险，请谨慎决策

## 🐛 故障排除

### 常见问题

1. **API连接失败**
   - 检查网络连接
   - 确认Hyperliquid API服务状态
   - 增加重试次数和超时时间

2. **内存不足**
   - 减少`max_tokens`参数
   - 缩短`time_hours`时间窗口
   - 增加系统内存

3. **计算时间过长**
   - 减少`n_perm_*`置换次数
   - 减少`max_lag_sources`参数
   - 使用多线程`num_threads`

4. **结果为空**
   - 降低`correlation_threshold`和`te_threshold`
   - 增加`time_hours`时间窗口
   - 检查数据质量和代币选择

5. **估计器错误**
   - 检查数据格式
   - 确保数据无缺失值
   - 调整`kraskov_k`参数
   - 检查数据维度

### 调试模式

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 启用详细日志
analyzer = CryptoNetworkAnalyzer()
analyzer.config['output']['log_level'] = 'DEBUG'
```

## 📚 技术文档

### 核心算法
- **传递熵**: 基于Schreiber (2000)的传递熵理论
- **互信息**: 基于Kraskov等人(2004)的k-近邻估计器
- **统计检验**: 使用FDR校正控制多重比较错误
- **网络分析**: 基于Lizier & Rubinov (2012)的多变量方法

### 估计器说明

| 估计器 | 特点 | 适用场景 |
|--------|------|----------|
| PythonKraskovCMI | k-近邻方法，精度高 | 连续数据，高精度要求 |
| PythonKraskovMI | 互信息估计 | 相关性分析 |

### 依赖库

- **IDTxl**: 信息动力学分析核心库
- **NumPy/Pandas**: 数据处理和计算
- **Matplotlib/Seaborn**: 数据可视化
- **Requests**: API数据获取
- **SciPy**: 科学计算支持

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出改进建议：

1. **Fork** 本项目
2. **创建** 功能分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 更改 (`git commit -m 'Add some AmazingFeature'`)
4. **推送** 到分支 (`git push origin feature/AmazingFeature`)
5. **创建** Pull Request

## 📄 许可证

本项目基于MIT许可证开源。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- **IDTxl项目团队**: 提供强大的信息动力学分析工具
- **Hyperliquid团队**: 提供开放的API服务
- **开源社区**: 提供各种优秀的Python库

## 📞 联系方式

如有问题或建议，请：
1. 查看 [使用指南](加密货币网络分析使用指南.md)
2. 查看 [技术说明](技术说明.md)
3. 查看 [功能对比分析](功能对比分析.md)
4. 运行测试脚本诊断问题
5. 查看日志文件获取详细错误信息
6. 参考IDTxl官方文档

---

*本项目基于IDTxl开发，采用纯Python实现，无需Java环境，部署简单，维护方便。请根据实际需求调整参数和配置，谨慎投资。*