# -*- coding: utf-8 -*-
# preprocessing.py
"""数据预处理模块： 第二节代码"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)


def preprocess_data(sessions: pd.DataFrame, conversions: pd.DataFrame) -> pd.DataFrame:
    """
    预处理步骤：
        1. 按 user_id 和 session_time 排序
        2. 左关联 conversions (on='user_id')
        3. 筛选 session_time < conversion_time

    参数:
        sessions: 原始会话 DataFrame
        conversions: 原始转化 DataFrame

    返回:
        预处理后的 DataFrame，仅包含转化前会话（仅转化用户）
    """
    # 1. 排序（原地排序，与 notebook 一致）
    sessions_sorted = sessions.sort_values(['user_id', 'session_time'])
    logger.info("已按用户和时间排序")

    # 2. 合并
    full = sessions_sorted.merge(conversions, on='user_id', how='left')
    logger.info(f"合并后共 {len(full)} 条记录")

    # 3. 筛选转化前会话
    full_select = full.query('session_time < conversion_time')
    logger.info(f"筛选后保留 {len(full_select)} 条记录（仅转化前会话）")

    return full_select