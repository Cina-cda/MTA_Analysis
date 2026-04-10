# -*- coding: utf-8 -*-
"""数据加载模块： 第一节代码"""

import pandas as pd
from config import SESSIONS_FILE, CONVERSIONS_FILE


def load_and_explore():
    """
    数据加载与初步探索步骤：
        1. 读取两个 CSV 文件
        2. 将时间列转换为 datetime
    """
    # 读取
    sessions = pd.read_csv(SESSIONS_FILE)
    conversions = pd.read_csv(CONVERSIONS_FILE)

    # 时间列转换
    sessions['session_time'] = pd.to_datetime(sessions['session_time'])
    conversions['conversion_time'] = pd.to_datetime(conversions['conversion_time'])

    return sessions, conversions