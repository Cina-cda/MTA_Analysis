# 多渠道归因分析项目

## 项目简介
本项目实现了一套完整的归因分析流程，用于评估不同营销渠道对用户转化的贡献。支持以下归因模型：
- 首次点击归因
- 末次点击归因
- 线性归因
- 时间衰减归因（默认半衰期7天）
- U型归因（基于位置，首次40%、末次40%、中间20%）

此外，还提供了进阶分析功能：
- 渠道协同效应（渠道组合频次）
- 转化路径长度分布
- 时间窗口敏感性分析（半衰期1、3、7、14天）
- 可视化对比柱状图及敏感性折线图

## 项目结构
### attribution_project/
### ├── data/ # 原始数据目录（需自行放入CSV文件）
### │ ├── user_sessions.csv
### │ └── conversions.csv
### ├── outputs/ # 运行后自动生成
### │ ├── attribution_analysis.xlsx # 所有结果汇总
### │ └── figures/ # 图表
### ├── logs/ # 日志目录（自动创建）
### ├── config.py # 配置文件（路径、参数）
### ├── data_loader.py # 数据加载模块
### ├── preprocessing.py # 预处理模块
### ├── attribution_models.py # 归因模型实现
### ├── advanced_analysis.py # 进阶分析
### ├── visualization.py # 可视化模块
### ├── main.py # 主程序入口
### ├── requirements.txt # Python依赖
### └── README.md # 本文件


## 环境要求
- Python 3.12
- 依赖包：pandas, numpy, matplotlib

## 快速开始

### 1. 安装依赖
pip install -r requirements.txt

### 2. 准备数据

将原始数据文件 user_sessions.csv 和 conversions.csv 放入 data/ 目录下。

数据格式要求：

user_sessions.csv：包含列 user_id, session_time, channel

conversions.csv：包含列 user_id, conversion_time

### 3. 运行分析
python main.py

### 4. 查看结果

Excel 汇总文件：outputs/attribution_analysis.xlsx（包含所有模型结果及进阶分析）

图表：outputs/figures/ 目录下

## 输出说明

Excel 文件中包含以下工作表：

首次点击、末次点击、线性归因、时间衰减、U型归因：各模型的渠道贡献及占比

对比汇总：四个基础模型的对比表

渠道协同：各渠道组合的出现频次

路径长度分布：用户转化前会话次数分布

渠道组合平均长度：不同渠道序列的平均路径长度

衰减半衰期X天：不同半衰期下的时间衰减归因结果

## 注意事项

预处理阶段仅保留转化前会话，未转化的用户会被自动过滤。

时间衰减归因的默认半衰期为7天，可通过 config.py 中的 TIME_DECAY_HALF_LIFE 修改。

    绘图时会自动设置中文字体，若系统缺少指定字体，可能显示方框，可自行调整 visualization.py 中的字体列表。

## 扩展与定制

    修改 config.py 中的路径、半衰期、U型权重等参数。

    若要增加新的归因模型，在 attribution_models.py 中添加函数，并在 main.py 中调用。

## 许可证

本项目仅供学习交流使用。
