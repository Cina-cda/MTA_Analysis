# -*- coding: utf-8 -*-
"""进阶分析模块： 第9-12节代码实现 U型归因、渠道协同效应、路径长度分布、时间窗口敏感性分析"""

import pandas as pd
import numpy as np
from itertools import combinations


def u_shaped_attribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    U型归因（基于位置），第9节
    规则：
        - 只有一次会话：该渠道得100%
        - 只有两次会话：首次和末次各50%
        - 三次及以上：首次40%，末次40%，中间20%平分给所有中间渠道
    返回：
        DataFrame 包含 channel, U型归因转化数, U型归因占比(%)
    """
    # 复制一份避免影响原数据
    df = df.copy()
    # 计算每个用户的会话次数
    df['会话次数'] = df.groupby('user_id')['session_time'].transform('count')
    
    # 筛选不同情况
    single = df[df['会话次数'] == 1].copy()
    double = df[df['会话次数'] == 2].copy()
    multiple = df[df['会话次数'] > 2].copy()
    
    # ---- 单次会话 ----
    if not single.empty:
        single_sum = (
            single.groupby('channel')
            .agg(功劳=('user_id', 'nunique'))
            .reset_index()
        )
        # 功劳为1（100%）
    else:
        single_sum = pd.DataFrame(columns=['channel', '功劳'])
    
    # ---- 两次会话 ----
    if not double.empty:
        # 首次
        double_first = double.sort_values(['user_id', 'session_time']).groupby('user_id').first().reset_index()
        double_first['功劳'] = 0.5
        # 末次
        double_last = double.sort_values(['user_id', 'session_time']).groupby('user_id').last().reset_index()
        double_last['功劳'] = 0.5
        double_combined = pd.concat([double_first, double_last], ignore_index=True)
        double_sum = double_combined.groupby('channel')['功劳'].sum().reset_index()
    else:
        double_sum = pd.DataFrame(columns=['channel', '功劳'])
    
    # ---- 多次会话（>2） ----
    if not multiple.empty:
        # 添加序号
        multiple = multiple.sort_values(['user_id', 'session_time'])
        multiple['序号'] = multiple.groupby('user_id').cumcount()
        # 首次
        multiple_first = multiple.groupby('user_id').first().reset_index()
        multiple_first['功劳'] = 0.4
        # 末次
        multiple_last = multiple.groupby('user_id').last().reset_index()
        multiple_last['功劳'] = 0.4
        # 中间
        multiple_middle = multiple[(multiple['序号'] > 0) & (multiple['序号'] < (multiple['会话次数'] - 1))].copy()
        if not multiple_middle.empty:
            multiple_middle['中间渠道数'] = multiple_middle.groupby('user_id')['channel'].transform('count')
            multiple_middle['功劳'] = 0.2 / multiple_middle['中间渠道数']
        else:
            multiple_middle['功劳'] = 0  # 实际不会出现，但避免空
        multiple_combined = pd.concat([multiple_first, multiple_last, multiple_middle], ignore_index=True)
        multiple_sum = multiple_combined.groupby('channel')['功劳'].sum().reset_index()
    else:
        multiple_sum = pd.DataFrame(columns=['channel', '功劳'])
    
    # 合并三部分
    all_parts = pd.concat([single_sum, double_sum, multiple_sum], ignore_index=True)
    result = all_parts.groupby('channel')['功劳'].sum().reset_index()
    result.rename(columns={'功劳': 'U型归因转化数'}, inplace=True)
    total = result['U型归因转化数'].sum()
    result['U型归因转化数总数'] = total
    result['U型归因占比'] = (result['U型归因转化数'] / total * 100).round(2)
    return result



def channel_synergy_analysis(df: pd.DataFrame):
    """
    渠道协同效应分析（第10节，含补充的比例计算）
    返回：
        pair_counts : DataFrame 各渠道对及人数
        ratio : float 使用两个及以上不同渠道的用户比例(%)
    """
    # 每个用户的不同渠道数
    df['不同渠道数'] = df.groupby('user_id')['channel'].transform('nunique')
    # 筛选至少2个不同渠道的用户
    multi_channel = df[df['不同渠道数'] >= 2].copy()
    # 计算比例
    total_converted_users = df['user_id'].nunique()
    multi_channel_users = multi_channel['user_id'].nunique()
    ratio = multi_channel_users / total_converted_users * 100
    print(f"出现两个及以上不同渠道的用户比例: {ratio:.2f}%")
    # 生成渠道对
    user_channels = (
        multi_channel[['user_id', 'channel']]
        .drop_duplicates(['user_id', 'channel'])
        .groupby('user_id')['channel']
        .apply(lambda x: sorted(set(x)))
        .reset_index(name='不同渠道列表')
    )
    user_channels['不同渠道对'] = user_channels['不同渠道列表'].apply(lambda x: list(combinations(x, 2)))
    # 展开
    channel_pairs = user_channels.explode('不同渠道对')
    # 统计频次
    pair_counts = (
        channel_pairs.groupby('不同渠道对')
        .agg(人数=('user_id', 'nunique'))
        .reset_index()
    )
    return pair_counts, ratio



def path_length_distribution(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    转化路径长度分布，第11节
    返回：
        - session_count_dist: 会话次数分布（每个会话次数对应的人数）
        - channel_combo_avg_len: 各渠道组合的平均路径长度
    """
    # 会话次数分布
    session_count_dist = (
        df.groupby('会话次数')
        .agg(人数=('user_id', 'nunique'))
        .reset_index()
    )
    # 每个用户的渠道组合（去重后转为元组）和会话次数
    user_channels = (
        df.groupby('user_id')
        .agg(会话渠道=('channel', 'unique'), 会话次数=('session_time', 'count'))
        .reset_index()
    )
    user_channels['会话渠道'] = user_channels['会话渠道'].apply(tuple)
    # 平均路径长度
    channel_combo_avg_len = (
        user_channels.groupby('会话渠道')
        .agg(平均路径长度=('会话次数', 'mean'))
        .reset_index()
        .sort_values('平均路径长度', ascending=False)
    )
    return session_count_dist, channel_combo_avg_len



def time_decay_sensitivity(df: pd.DataFrame, half_lives: list) -> dict:
    """
    时间窗口敏感性分析（第12节补充版）
    对每个半衰期，调用 time_decay_attribution 计算，返回字典 {半衰期: result_df}
    """
    from attribution_models import time_decay_attribution
    results = {}
    for hl in half_lives:
        res = time_decay_attribution(df, half_life=hl)
        results[hl] = res
    return results