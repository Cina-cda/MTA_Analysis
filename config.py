# -*- coding: utf-8 -*-
"""项目配置文件：路径、参数、常量等"""

import os
from pathlib import Path

# ---------- 路径配置 ----------
# 项目根目录
PROJECT_ROOT = Path(__file__).parent.resolve()

# 数据目录
DATA_DIR = PROJECT_ROOT / "data"
SESSIONS_FILE = DATA_DIR / "user_sessions.csv"
CONVERSIONS_FILE = DATA_DIR / "conversions.csv"

# 输出目录
OUTPUT_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"
EXCEL_FILE = OUTPUT_DIR / "attribution_analysis.xlsx"

# 日志目录
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "attribution.log"

# 自动创建所需目录
os.makedirs(DATA_DIR, exist_ok= True)
os.makedirs(OUTPUT_DIR, exist_ok= True)
os.makedirs(FIGURES_DIR, exist_ok= True)
os.makedirs(LOG_DIR, exist_ok= True)


# ---------- 归因模型参数 ----------
# 时间衰减归因半衰期（天），可单值或列表用于敏感性分析
TIME_DECAY_HALF_LIFE = 7.0               # 半衰期7天
SENSITIVITY_HALF_LIVES = [1, 3, 7, 14]   # 敏感性分析用半衰期列表

# U型归因（基于位置）权重配置：首次、末次、中间总和占比
U_SHAPED_FIRST_WEIGHT = 0.4
U_SHAPED_LAST_WEIGHT = 0.4
U_SHAPED_MIDDLE_WEIGHT = 0.2   # 中间点击平分


# ---------- 其他配置 ----------
# 日志级别：DEBUG, INFO, WARNING, ERROR
LOG_LEVEL = "INFO"

# 是否在控制台同时输出日志
LOG_TO_CONSOLE = True

# 输出Excel时是否包含所有中间DataFrame（调试用）
EXPORT_DEBUG_SHEETS = False
