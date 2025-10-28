[![DOI](http://joss.theoj.org/papers/10.21105/joss.01081/status.svg)](https://doi.org/10.21105/joss.01081)

# IDTxl

**I**nformation **D**ynamics **T**oolkit **xl** (IDTxl) 是一个基于信息论的综合性软件包，用于从多元时间序列数据中高效推断网络及其节点动力学。IDTxl 提供以下测量功能：

## 🔧 核心功能

### 1. 网络推断 (Network Inference)
- **多元传递熵 (Multivariate Transfer Entropy, TE)** / 格兰杰因果性 (Granger Causality, GC)
- **多元互信息 (Multivariate Mutual Information, MI)**
- **双变量传递熵 (Bivariate TE)** / 格兰杰因果性
- **双变量互信息 (Bivariate MI)**

### 2. 节点动力学分析 (Node Dynamics Analysis)
- **主动信息存储 (Active Information Storage, AIS)**
- **部分信息分解 (Partial Information Decomposition, PID)**

## 🚀 技术特点

- 支持离散和连续数据的估计器
- GPU 和 CPU 平台的并行计算引擎
- 支持 Python 3.4.3+
- 支持 MPI 分布式计算
- 多种高级算法和统计检验

## 📚 快速开始

查看 [Wiki](https://github.com/pwollstadt/IDTxl/wiki) 和 [官方文档](http://pwollstadt.github.io/IDTxl/) 开始使用。如需讨论，请加入 [IDTxl Google 讨论组](https://groups.google.com/forum/#!forum/idtxl)。

### 安装
```bash
pip install idtxl
```

### 基本使用示例
```python
from idtxl.data import Data
from idtxl.multivariate_te import MultivariateTE

# 准备数据
data = Data()
data.generate_mute_data(n_samples=1000, n_replications=5)

# 网络分析
network_analysis = MultivariateTE()
settings = {
    "cmi_estimator": "JidtGaussianCMI",
    "max_lag_sources": 5,
    "min_lag_sources": 1,
}

# 运行分析
results = network_analysis.analyse_network(settings=settings, data=data)
results.print_edge_list(weights="max_te_lag", fdr=False)
```

## 📖 如何引用

P. Wollstadt, J. T. Lizier, R. Vicente, C. Finn, M. Martinez-Zarzuela, P. Mediano, L. Novelli, M. Wibral (2018). _IDTxl: The Information Dynamics Toolkit xl: a Python package for the efficient analysis of multivariate information dynamics in networks._ Journal of Open Source Software, 4(34), 1081. [https://doi.org/10.21105/joss.01081](https://doi.org/10.21105/joss.01081).

## 👥 主要贡献者

- [Patricia Wollstadt](http://patriciawollstadt.de/), 脑成像中心，MEG 单元，歌德大学，德国法兰克福；本田欧洲研究院，德国奥芬巴赫
- [Michael Wibral](http://www.uni-goettingen.de/de/datengetriebene+analyse+biologischer+netzwerke+%28wibral%29/603144.html), 生物网络动力学校园研究所，格奥尔格·奥古斯特大学，德国哥廷根
- [David Alexander Ehrlich](https://www.ds.mpg.de/person/106938), 生物网络动力学校园研究所，格奥尔格·奥古斯特大学，德国哥廷根；马克斯·普朗克动力学与自组织研究所，德国哥廷根
- [Joseph T. Lizier](http://lizier.me/joseph/), 复杂系统中心，悉尼大学，澳大利亚悉尼
- [Raul Vicente](http://neuro.cs.ut.ee/people/), 计算神经科学实验室，计算机科学研究所，塔尔图大学，爱沙尼亚塔尔图
- [Abdullah Makkeh](https://abzinger.github.io/), 生物网络动力学校园研究所，格奥尔格·奥古斯特大学，德国哥廷根
- Conor Finn, 复杂系统中心，悉尼大学，澳大利亚悉尼
- Mario Martinez-Zarzuela, 信号理论与通信和远程信息工程系，巴利亚多利德大学，西班牙巴利亚多利德
- Leonardo Novelli, 复杂系统中心，悉尼大学，澳大利亚悉尼
- [Pedro Mediano](https://www.doc.ic.ac.uk/~pam213/), 计算神经动力学组，帝国理工学院，英国伦敦
- Dr. Michael Lindner, 生物网络动力学校园研究所，格奥尔格·奥古斯特大学，德国哥廷根
- Dr. Aaron J. Gutknecht, 生物网络动力学校园研究所，格奥尔格·奥古斯特大学，德国哥廷根
- [Prof. Viola Priesemann](https://www.uni-goettingen.de/de/priesemann%2C+viola%2C+dr.+-+theorie+neuronaler+systeme+(mpi-ds)/622913.html), 神经系统理论，物理学院，格奥尔格·奥古斯特大学和马克斯·普朗克动力学与自组织研究所，德国哥廷根
- Dr. Lucas Rudelt, 马克斯·普朗克动力学与自组织研究所，德国哥廷根

**如何贡献？** 我们欢迎对 IDTxl 的任何反馈。如果您想贡献，请提交 issue 或发送 pull request 来分享您的功能或改进。请查看 [开发者部分](https://github.com/pwollstadt/IDTxl/wiki#developers-section) 了解详细信息。


## 🙏 致谢

本项目得到了以下资金支持：

- 澳大利亚大学 - 德国学术交流服务 (UA-DAAD) 澳大利亚-德国联合研究合作资助 "测量神经信息合成及其损伤"，Wibral, Lizier, Priesemann, Wollstadt, Finn, 2016-17
- 澳大利亚研究理事会发现早期职业研究员奖 (DECRA) "使用信息论将复杂网络的功能与结构联系起来"，Lizier, 2016-19
- 德国研究基金会 (DFG) 资助 CRC 1193 C04，Wibral
- 下萨克森州科学教育部和大众基金会通过 "Niedersächsisches Vorab" 项目 "生命科学大数据" 的资助 - 项目 "用于转录组和系统动力学在组织形态发生中关联研究的深度学习技术"。

## 📚 主要参考文献

### 核心算法
+ **多元传递熵**: Lizier & Rubinov, 2012, 预印本, 技术报告 25/2012, 马克斯·普朗克数学科学研究所。可从以下地址获取: http://www.mis.mpg.de/preprints/2012/preprint2012_25.pdf
+ **多元传递熵估计的分层统计检验**: [Novelli et al., 2019, Network Neurosci 3(3)](https://www.mitpressjournals.org/doi/full/10.1162/netn_a_00092)
+ **Kraskov 估计器**: [Kraskov et al., 2004, Phys Rev E 69, 066138](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.69.066138)
+ **非均匀嵌入**: [Faes et al., 2011, Phys Rev E 83, 051112](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.83.051112)
+ **Faes 补偿传递熵**: [Faes et al., 2013, Entropy 15, 198-219](https://www.mdpi.com/1099-4300/15/1/198)

### 部分信息分解 (PID)
+ [Williams & Beer, 2010, arXiv:1004.2515 [cs.IT]](http://arxiv.org/abs/1004.2515)
+ [Makkeh et al., 2021, Phys Rev E 103, 032149](https://doi.org/10.1103/PhysRevE.103.032149)
+ [Gutknecht et al., 2021, Proc. R. Soc. A: Math. Phys. Eng, 477(2251), 20210110.](https://royalsocietypublishing.org/doi/full/10.1098/rspa.2021.0110)

### PID 估计器
+ [Bertschinger et al., 2014, Entropy, 16(4)](https://www.mdpi.com/1099-4300/16/4/2161)
+ [Makkeh et al., 2017, Entropy, 19(10)](https://www.mdpi.com/1099-4300/19/10/530)
+ [Makkeh et al., 2018, Entropy, 20(271)](https://www.mdpi.com/1099-4300/20/4/271)
+ [Makkeh et al., 2018, Phys. Rev. E 103, 032149](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.103.032149)

### 专业应用
+ **神经脉冲数据的历史依赖性估计器**: [Rudelt et al., 2021, PLOS Computational Biology, 17(6)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008927)
+ **显著性子图挖掘**: [Gutknecht et al., 2021, bioRxiv](https://doi.org/10.1101/2021.11.03.467050)

## 🔗 相关资源

- **官方文档**: [http://pwollstadt.github.io/IDTxl/](http://pwollstadt.github.io/IDTxl/)
- **GitHub 仓库**: [https://github.com/pwollstadt/IDTxl](https://github.com/pwollstadt/IDTxl)
- **Wiki**: [https://github.com/pwollstadt/IDTxl/wiki](https://github.com/pwollstadt/IDTxl/wiki)
- **Google 讨论组**: [https://groups.google.com/forum/#!forum/idtxl](https://groups.google.com/forum/#!forum/idtxl)

## 🎯 应用领域

- **神经科学**: 脑网络连接分析
- **系统生物学**: 基因调控网络
- **金融**: 市场信息流动分析
- **气候科学**: 气候系统相互作用
- **社会科学**: 复杂社会网络分析

---

*IDTxl 是一个成熟、专业的科学计算工具包，为研究复杂系统中的信息动力学提供了强大而灵活的分析框架。*
