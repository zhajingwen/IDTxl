#!/usr/bin/env python3
"""
加密货币市场网络分析系统 - 无Java依赖版本
基于IDTxl的Python原生估计器，无需Java环境

功能：
1. 从Hyperliquid API获取加密货币价格数据
2. 使用Python原生估计器进行网络分析
3. 识别高度关联的资产组合
4. 生成可视化报告

作者: AI Assistant
日期: 2024
"""

import os
import sys
import time
import json
import logging
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# IDTxl imports - 只使用Python原生估计器
from idtxl.data import Data
from idtxl.multivariate_te import MultivariateTE
from idtxl.multivariate_mi import MultivariateMI
from idtxl.visualise_graph import plot_network

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crypto_network_analysis_no_java.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class HyperliquidDataFetcher:
    """Hyperliquid API数据获取器"""
    
    def __init__(self):
        self.base_url = "https://api.hyperliquid.xyz"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoNetworkAnalysis/1.0',
            'Accept': 'application/json'
        })
    
    def get_all_tokens(self) -> List[Dict]:
        """获取所有已上线的代币信息"""
        try:
            url = f"{self.base_url}/info"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            tokens = data.get('universe', [])
            
            logger.info(f"成功获取 {len(tokens)} 个代币信息")
            return tokens
            
        except Exception as e:
            logger.error(f"获取代币信息失败: {e}")
            return []
    
    def get_token_prices(self, tokens: List[str], hours: int = 24) -> pd.DataFrame:
        """获取代币价格数据"""
        try:
            # 获取历史价格数据
            end_time = int(time.time() * 1000)  # 毫秒时间戳
            start_time = end_time - (hours * 60 * 60 * 1000)
            
            url = f"{self.base_url}/info"
            params = {
                'type': 'candleSnapshot',
                'coin': ','.join(tokens),
                'interval': '1h',  # 1小时K线
                'startTime': start_time,
                'endTime': end_time
            }
            
            response = self.session.get(url, params=params, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            
            # 处理价格数据
            price_data = {}
            for token_data in data:
                coin = token_data['coin']
                candles = token_data['candles']
                
                if candles:
                    df = pd.DataFrame(candles)
                    df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
                    df['price'] = df['c'].astype(float)  # 收盘价
                    df = df.set_index('timestamp')
                    price_data[coin] = df['price']
            
            # 合并所有代币价格数据
            price_df = pd.DataFrame(price_data)
            price_df = price_df.dropna()  # 删除缺失值
            
            logger.info(f"成功获取 {len(price_df.columns)} 个代币的 {len(price_df)} 小时价格数据")
            return price_df
            
        except Exception as e:
            logger.error(f"获取价格数据失败: {e}")
            return pd.DataFrame()


class CryptoNetworkAnalyzerNoJava:
    """加密货币网络分析器 - 无Java依赖版本"""
    
    def __init__(self, config: Dict = None):
        self.config = config or self._default_config()
        self.data_fetcher = HyperliquidDataFetcher()
        self.price_data = None
        self.network_results = None
        
    def _default_config(self) -> Dict:
        """默认配置 - 使用Python原生估计器"""
        return {
            'min_price': 0.001,  # 最小价格过滤
            'min_volume': 10000,  # 最小交易量过滤
            'max_tokens': 30,  # 最大分析代币数量（减少以提高性能）
            'time_hours': 72,  # 分析时间窗口（3天，减少以提高性能）
            'cmi_estimator': 'PythonKraskovCMI',  # 使用Python原生估计器
            'max_lag_sources': 6,  # 减少滞后以提高性能
            'min_lag_sources': 1,
            'max_lag_target': 3,
            'tau_sources': 1,
            'tau_target': 1,
            'n_perm_max_stat': 50,  # 减少置换次数以提高速度
            'n_perm_min_stat': 50,
            'n_perm_omnibus': 100,
            'fdr_alpha': 0.05,  # FDR显著性水平
            'correlation_threshold': 0.6,  # 降低相关性阈值
            'te_threshold': 0.05,  # 降低传递熵阈值
            'kraskov_k': 4,  # Kraskov估计器参数
            'num_threads': 'USE_ALL',  # 使用所有可用线程
        }
    
    def fetch_and_preprocess_data(self) -> bool:
        """获取并预处理数据"""
        try:
            logger.info("开始获取加密货币数据...")
            
            # 获取所有代币
            tokens_info = self.data_fetcher.get_all_tokens()
            if not tokens_info:
                logger.error("无法获取代币信息")
                return False
            
            # 过滤代币
            filtered_tokens = self._filter_tokens(tokens_info)
            if not filtered_tokens:
                logger.error("没有符合条件的代币")
                return False
            
            logger.info(f"选择 {len(filtered_tokens)} 个代币进行分析")
            
            # 获取价格数据
            self.price_data = self.data_fetcher.get_token_prices(
                filtered_tokens, 
                self.config['time_hours']
            )
            
            if self.price_data.empty:
                logger.error("无法获取价格数据")
                return False
            
            # 数据预处理
            self._preprocess_data()
            
            logger.info(f"数据预处理完成，最终数据形状: {self.price_data.shape}")
            return True
            
        except Exception as e:
            logger.error(f"数据获取和预处理失败: {e}")
            return False
    
    def _filter_tokens(self, tokens_info: List[Dict]) -> List[str]:
        """过滤代币"""
        filtered = []
        
        for token in tokens_info:
            # 基本过滤条件
            if (token.get('maxLeverage', 0) > 0 and  # 有杠杆
                token.get('onlyIsolated', False) == False and  # 支持交叉保证金
                len(token.get('name', '')) > 0):  # 有名称
                
                filtered.append(token['name'])
                
                if len(filtered) >= self.config['max_tokens']:
                    break
        
        return filtered
    
    def _preprocess_data(self):
        """数据预处理"""
        # 计算收益率
        returns = self.price_data.pct_change().dropna()
        
        # 移除异常值（超过3个标准差）
        returns = returns[np.abs(returns) < 3 * returns.std()]
        
        # 标准化数据
        returns = (returns - returns.mean()) / returns.std()
        
        self.price_data = returns
        
        logger.info("数据预处理完成：计算收益率、移除异常值、标准化")
    
    def analyze_network(self) -> bool:
        """执行网络分析 - 使用Python原生估计器"""
        try:
            logger.info("开始网络分析（使用Python原生估计器）...")
            
            # 准备IDTxl数据格式
            data_array = self.price_data.values.T  # 转置为(processes, samples)格式
            data = Data(data_array, dim_order='ps')
            
            # 配置分析参数 - 使用Python原生估计器
            settings = {
                'cmi_estimator': self.config['cmi_estimator'],
                'max_lag_sources': self.config['max_lag_sources'],
                'min_lag_sources': self.config['min_lag_sources'],
                'max_lag_target': self.config['max_lag_target'],
                'tau_sources': self.config['tau_sources'],
                'tau_target': self.config['tau_target'],
                'n_perm_max_stat': self.config['n_perm_max_stat'],
                'n_perm_min_stat': self.config['n_perm_min_stat'],
                'n_perm_omnibus': self.config['n_perm_omnibus'],
                'fdr_alpha': self.config['fdr_alpha'],
                'kraskov_k': self.config['kraskov_k'],
                'num_threads': self.config['num_threads'],
            }
            
            # 执行多元传递熵分析
            logger.info("执行多元传递熵分析...")
            network_analysis = MultivariateTE()
            self.network_results = network_analysis.analyse_network(
                settings=settings, 
                data=data
            )
            
            logger.info("网络分析完成")
            return True
            
        except Exception as e:
            logger.error(f"网络分析失败: {e}")
            return False
    
    def analyze_correlation_network(self) -> Dict:
        """基于相关性的网络分析 - 作为传递熵的补充"""
        try:
            logger.info("执行相关性网络分析...")
            
            # 计算相关性矩阵
            correlation_matrix = self.price_data.corr()
            
            # 识别高度相关的资产对
            highly_correlated = []
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    corr = correlation_matrix.iloc[i, j]
                    if abs(corr) >= self.config['correlation_threshold']:
                        asset1 = correlation_matrix.columns[i]
                        asset2 = correlation_matrix.columns[j]
                        highly_correlated.append({
                            'asset1': asset1,
                            'asset2': asset2,
                            'correlation': corr,
                            'abs_correlation': abs(corr)
                        })
            
            # 按相关性强度排序
            highly_correlated.sort(key=lambda x: x['abs_correlation'], reverse=True)
            
            # 基于相关性构建网络
            correlation_network = {
                'correlation_matrix': correlation_matrix,
                'highly_correlated_pairs': highly_correlated,
                'network_density': len(highly_correlated) / (len(correlation_matrix.columns) * (len(correlation_matrix.columns) - 1) / 2)
            }
            
            logger.info(f"相关性分析完成：发现 {len(highly_correlated)} 个高相关对")
            return correlation_network
            
        except Exception as e:
            logger.error(f"相关性网络分析失败: {e}")
            return {}
    
    def identify_highly_correlated_assets(self) -> Dict:
        """识别高度关联的资产组合"""
        try:
            logger.info("识别高度关联的资产组合...")
            
            # 获取传递熵网络结果
            te_connections = []
            if self.network_results is not None:
                edge_list = self.network_results.get_edge_list()
                for edge in edge_list:
                    if edge[2] >= self.config['te_threshold']:  # 传递熵阈值
                        te_connections.append({
                            'source': self.price_data.columns[edge[0]],
                            'target': self.price_data.columns[edge[1]],
                            'transfer_entropy': edge[2],
                            'p_value': edge[3] if len(edge) > 3 else None
                        })
                
                # 按传递熵强度排序
                te_connections.sort(key=lambda x: x['transfer_entropy'], reverse=True)
            
            # 执行相关性分析
            correlation_network = self.analyze_correlation_network()
            highly_correlated = correlation_network.get('highly_correlated_pairs', [])
            
            # 识别资产组合
            asset_combinations = self._find_asset_combinations(
                highly_correlated, 
                te_connections
            )
            
            results = {
                'correlation_pairs': highly_correlated,
                'te_connections': te_connections,
                'asset_combinations': asset_combinations,
                'correlation_network': correlation_network,
                'summary': {
                    'total_assets': len(self.price_data.columns),
                    'highly_correlated_pairs': len(highly_correlated),
                    'te_connections': len(te_connections),
                    'asset_combinations': len(asset_combinations),
                    'network_density': correlation_network.get('network_density', 0)
                }
            }
            
            logger.info(f"识别完成：{len(highly_correlated)}个高相关对，{len(te_connections)}个TE连接，{len(asset_combinations)}个资产组合")
            return results
            
        except Exception as e:
            logger.error(f"识别高度关联资产失败: {e}")
            return {}
    
    def _find_asset_combinations(self, correlated_pairs: List, te_connections: List) -> List:
        """寻找资产组合"""
        combinations = []
        
        # 基于相关性的组合
        asset_groups = {}
        for pair in correlated_pairs:
            asset1, asset2 = pair['asset1'], pair['asset2']
            
            # 寻找现有组
            found_group = None
            for group_id, group in asset_groups.items():
                if asset1 in group or asset2 in group:
                    found_group = group_id
                    break
            
            if found_group is not None:
                asset_groups[found_group].update([asset1, asset2])
            else:
                new_group_id = len(asset_groups)
                asset_groups[new_group_id] = {asset1, asset2}
        
        # 转换为列表格式
        for group_id, group in asset_groups.items():
            if len(group) >= 2:  # 至少2个资产
                combinations.append({
                    'type': 'correlation_based',
                    'assets': list(group),
                    'size': len(group),
                    'strength': 'high' if len(group) >= 3 else 'medium'
                })
        
        # 基于传递熵的组合
        te_groups = {}
        for conn in te_connections:
            source, target = conn['source'], conn['target']
            
            # 寻找现有组
            found_group = None
            for group_id, group in te_groups.items():
                if source in group or target in group:
                    found_group = group_id
                    break
            
            if found_group is not None:
                te_groups[found_group].update([source, target])
            else:
                new_group_id = len(te_groups)
                te_groups[new_group_id] = {source, target}
        
        # 添加TE组合
        for group_id, group in te_groups.items():
            if len(group) >= 2:
                combinations.append({
                    'type': 'te_based',
                    'assets': list(group),
                    'size': len(group),
                    'strength': 'high' if len(group) >= 3 else 'medium'
                })
        
        return combinations
    
    def visualize_results(self, results: Dict, save_path: str = None):
        """可视化结果"""
        try:
            logger.info("生成可视化结果...")
            
            # 设置图形样式
            plt.style.use('seaborn-v0_8')
            fig = plt.figure(figsize=(20, 15))
            
            # 1. 相关性热力图
            ax1 = plt.subplot(2, 3, 1)
            correlation_matrix = results.get('correlation_network', {}).get('correlation_matrix', self.price_data.corr())
            sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', center=0, ax=ax1)
            ax1.set_title('资产相关性热力图', fontsize=14, fontweight='bold')
            ax1.set_xlabel('资产')
            ax1.set_ylabel('资产')
            
            # 2. 网络图（如果有传递熵结果）
            ax2 = plt.subplot(2, 3, 2)
            if self.network_results:
                try:
                    plot_network(
                        results=self.network_results, 
                        weights="max_te_lag", 
                        fdr=False, 
                        ax=ax2
                    )
                    ax2.set_title('传递熵网络图', fontsize=14, fontweight='bold')
                except Exception as e:
                    logger.warning(f"网络图绘制失败: {e}")
                    ax2.text(0.5, 0.5, '网络图不可用', ha='center', va='center', transform=ax2.transAxes)
                    ax2.set_title('传递熵网络图（不可用）', fontsize=14, fontweight='bold')
            else:
                ax2.text(0.5, 0.5, '网络图不可用', ha='center', va='center', transform=ax2.transAxes)
                ax2.set_title('传递熵网络图（不可用）', fontsize=14, fontweight='bold')
            
            # 3. 高相关资产对
            ax3 = plt.subplot(2, 3, 3)
            if results.get('correlation_pairs'):
                pairs = results['correlation_pairs'][:10]  # 前10个
                assets = [f"{p['asset1']}-{p['asset2']}" for p in pairs]
                correlations = [p['correlation'] for p in pairs]
                
                bars = ax3.barh(assets, correlations, color='skyblue')
                ax3.set_xlabel('相关系数')
                ax3.set_title('高相关资产对 (Top 10)', fontsize=14, fontweight='bold')
                ax3.grid(True, alpha=0.3)
                
                # 添加数值标签
                for i, bar in enumerate(bars):
                    width = bar.get_width()
                    ax3.text(width, bar.get_y() + bar.get_height()/2, 
                            f'{width:.3f}', ha='left', va='center')
            
            # 4. 传递熵连接
            ax4 = plt.subplot(2, 3, 4)
            if results.get('te_connections'):
                connections = results['te_connections'][:10]  # 前10个
                connections_str = [f"{c['source']}→{c['target']}" for c in connections]
                te_values = [c['transfer_entropy'] for c in connections]
                
                bars = ax4.barh(connections_str, te_values, color='lightcoral')
                ax4.set_xlabel('传递熵')
                ax4.set_title('传递熵连接 (Top 10)', fontsize=14, fontweight='bold')
                ax4.grid(True, alpha=0.3)
                
                # 添加数值标签
                for i, bar in enumerate(bars):
                    width = bar.get_width()
                    ax4.text(width, bar.get_y() + bar.get_height()/2, 
                            f'{width:.3f}', ha='left', va='center')
            else:
                ax4.text(0.5, 0.5, '无传递熵连接', ha='center', va='center', transform=ax4.transAxes)
                ax4.set_title('传递熵连接（无数据）', fontsize=14, fontweight='bold')
            
            # 5. 资产组合分布
            ax5 = plt.subplot(2, 3, 5)
            if results.get('asset_combinations'):
                combinations = results['asset_combinations']
                types = [c['type'] for c in combinations]
                
                # 按类型分组统计
                type_counts = {}
                for t in types:
                    type_counts[t] = type_counts.get(t, 0) + 1
                
                if type_counts:
                    ax5.pie(type_counts.values(), labels=type_counts.keys(), autopct='%1.1f%%')
                    ax5.set_title('资产组合类型分布', fontsize=14, fontweight='bold')
                else:
                    ax5.text(0.5, 0.5, '无组合数据', ha='center', va='center', transform=ax5.transAxes)
                    ax5.set_title('资产组合类型分布（无数据）', fontsize=14, fontweight='bold')
            
            # 6. 组合大小分布
            ax6 = plt.subplot(2, 3, 6)
            if results.get('asset_combinations'):
                combinations = results['asset_combinations']
                sizes = [c['size'] for c in combinations]
                if sizes:
                    ax6.hist(sizes, bins=range(min(sizes), max(sizes)+2), 
                            alpha=0.7, color='lightgreen', edgecolor='black')
                    ax6.set_xlabel('组合大小')
                    ax6.set_ylabel('频次')
                    ax6.set_title('资产组合大小分布', fontsize=14, fontweight='bold')
                    ax6.grid(True, alpha=0.3)
                else:
                    ax6.text(0.5, 0.5, '无组合数据', ha='center', va='center', transform=ax6.transAxes)
                    ax6.set_title('资产组合大小分布（无数据）', fontsize=14, fontweight='bold')
            
            plt.tight_layout()
            
            # 保存图片
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"可视化结果已保存到: {save_path}")
            
            plt.show()
            
        except Exception as e:
            logger.error(f"可视化失败: {e}")
    
    def generate_report(self, results: Dict, save_path: str = None) -> str:
        """生成分析报告"""
        try:
            logger.info("生成分析报告...")
            
            report = []
            report.append("# 加密货币市场网络分析报告（无Java版本）")
            report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("")
            
            # 数据概览
            report.append("## 数据概览")
            report.append(f"- 分析资产数量: {results['summary']['total_assets']}")
            report.append(f"- 时间窗口: {self.config['time_hours']} 小时")
            report.append(f"- 数据点数量: {len(self.price_data)}")
            report.append(f"- 网络密度: {results['summary'].get('network_density', 0):.3f}")
            report.append("")
            
            # 高相关资产对
            report.append("## 高度相关资产对")
            if results.get('correlation_pairs'):
                report.append(f"发现 {len(results['correlation_pairs'])} 个高度相关的资产对:")
                report.append("")
                for i, pair in enumerate(results['correlation_pairs'][:20], 1):
                    report.append(f"{i}. {pair['asset1']} ↔ {pair['asset2']} (相关系数: {pair['correlation']:.4f})")
            else:
                report.append("未发现高度相关的资产对")
            report.append("")
            
            # 传递熵连接
            report.append("## 传递熵连接")
            if results.get('te_connections'):
                report.append(f"发现 {len(results['te_connections'])} 个传递熵连接:")
                report.append("")
                for i, conn in enumerate(results['te_connections'][:20], 1):
                    p_val_str = f" (p值: {conn['p_value']:.4f})" if conn['p_value'] else ""
                    report.append(f"{i}. {conn['source']} → {conn['target']} (TE: {conn['transfer_entropy']:.4f}{p_val_str})")
            else:
                report.append("未发现显著的传递熵连接")
            report.append("")
            
            # 资产组合
            report.append("## 识别出的资产组合")
            if results.get('asset_combinations'):
                report.append(f"发现 {len(results['asset_combinations'])} 个资产组合:")
                report.append("")
                for i, combo in enumerate(results['asset_combinations'], 1):
                    report.append(f"{i}. {combo['type']} 组合: {', '.join(combo['assets'])} (大小: {combo['size']}, 强度: {combo['strength']})")
            else:
                report.append("未发现显著的资产组合")
            report.append("")
            
            # 技术说明
            report.append("## 技术说明")
            report.append("本分析使用Python原生估计器，无需Java环境：")
            report.append(f"- 估计器类型: {self.config['cmi_estimator']}")
            report.append(f"- Kraskov参数k: {self.config['kraskov_k']}")
            report.append(f"- 线程数: {self.config['num_threads']}")
            report.append(f"- 置换次数: {self.config['n_perm_max_stat']}")
            report.append("")
            
            # 投资建议
            report.append("## 投资建议")
            report.append("基于网络分析结果，建议关注以下方面:")
            report.append("")
            report.append("1. **高相关资产**: 这些资产价格变动高度同步，适合配对交易策略")
            report.append("2. **传递熵连接**: 这些连接显示了信息流动方向，可用于预测价格变动")
            report.append("3. **资产组合**: 这些组合可以作为投资组合构建的参考")
            report.append("")
            report.append("**风险提示**: 本分析基于历史数据，不构成投资建议，请谨慎投资。")
            
            # 保存报告
            report_text = "\n".join(report)
            if save_path:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                logger.info(f"分析报告已保存到: {save_path}")
            
            return report_text
            
        except Exception as e:
            logger.error(f"生成报告失败: {e}")
            return ""


def main():
    """主函数"""
    print("🚀 加密货币市场网络分析系统（无Java版本）")
    print("=" * 50)
    
    # 创建分析器
    analyzer = CryptoNetworkAnalyzerNoJava()
    
    # 获取和预处理数据
    print("📊 正在获取和预处理数据...")
    if not analyzer.fetch_and_preprocess_data():
        print("❌ 数据获取失败")
        return
    
    # 执行网络分析
    print("🔍 正在执行网络分析...")
    if not analyzer.analyze_network():
        print("❌ 网络分析失败")
        return
    
    # 识别高度关联的资产
    print("🎯 正在识别高度关联的资产组合...")
    results = analyzer.identify_highly_correlated_assets()
    
    if not results:
        print("❌ 资产识别失败")
        return
    
    # 生成可视化
    print("📈 正在生成可视化结果...")
    analyzer.visualize_results(results, 'crypto_network_analysis_no_java.png')
    
    # 生成报告
    print("📝 正在生成分析报告...")
    report = analyzer.generate_report(results, 'crypto_network_report_no_java.md')
    
    # 打印摘要
    print("\n" + "=" * 50)
    print("📊 分析完成！")
    print(f"✅ 分析了 {results['summary']['total_assets']} 个资产")
    print(f"✅ 发现 {results['summary']['highly_correlated_pairs']} 个高相关对")
    print(f"✅ 发现 {results['summary']['te_connections']} 个传递熵连接")
    print(f"✅ 识别出 {results['summary']['asset_combinations']} 个资产组合")
    print(f"✅ 网络密度: {results['summary'].get('network_density', 0):.3f}")
    print("\n📁 输出文件:")
    print("- crypto_network_analysis_no_java.png (可视化图表)")
    print("- crypto_network_report_no_java.md (分析报告)")
    print("- crypto_network_analysis_no_java.log (日志文件)")


if __name__ == "__main__":
    main()