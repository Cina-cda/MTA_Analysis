# -*- coding: utf-8 -*-
"""归因模型模块： 第3-6节代码实现首次点击、末次点击、线性归因、时间衰减归因"""

import pandas as pd
import numpy as np


def first_click_attribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    首次点击归因（第3节）
    对每个转化用户，找到其第一次会话的渠道，将该转化功劳100%分配给该渠道。
    返回: 
        DataFrame 包含 channel, 人数, 占比(%)
    """
    # 计算每个用户第一次会话的渠道
    first_tap = (
        df.sort_values(['user_id', 'session_time'])
          .groupby('user_id')
          .agg('first')
          .reset_index()
    )
    # 统计各渠道人数
    first_tap_count = (
        first_tap
        .groupby('channel')
        .agg(人数=('user_id', 'nunique'))
        .reset_index()
    )
    # 计算所有渠道人数总数
    total = first_tap_count['人数'].sum()
    # 计算各渠道总人数
    first_tap_count['各渠道汇总人数'] = total
    # 计算各渠道占比
    first_tap_count['占比（%）'] = (first_tap_count['人数'] / total * 100).round(2)
    return first_tap_count


def last_click_attribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    末次点击归因（第4节）
    对每个转化用户，找到其最后一次会话（转化前最后一次）的渠道，将该转化功劳100%分配给该渠道。
    返回: 
        DataFrame 包含 channel, 人数, 占比(%)
    """
    # 计算每个转化的用户，第一次会话的渠道
    last_tap = (
        df.sort_values(['user_id', 'session_time'])
          .groupby('user_id')
          .agg('last')
          .reset_index()
    )
    # 计算各渠道人数
    last_tap_count = (
        last_tap
        .groupby('channel')
        .agg(人数=('user_id', 'nunique'))
        .reset_index()
    )
    # 计算所有渠道人数总数
    total = last_tap_count['人数'].sum()
    # 计算各渠道总人数
    last_tap_count['各渠道汇总人数'] = total
    # 计算各渠道占比
    last_tap_count['占比（%）'] = (last_tap_count['人数'] / total * 100).round(2)
    return last_tap_count


def linear_attribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    线性归因（第5节）
    对每个转化用户，将其转化功劳平均分配给该用户所有转化前会话的渠道。
    返回:
        DataFrame 包含 channel, 转化数, 占比(%)
    """
    # 计算每个用户的渠道列表和渠道数
    line_tap = (
        df.groupby('user_id')
          .agg(渠道=('channel', list), 渠道数=('channel', 'count'))
          .reset_index()
    )
    # 展开列表为行
    line_tap = line_tap.explode('渠道')
    # 计算功劳占比
    line_tap['功劳占比'] = 1 / line_tap['渠道数']
    # 汇总功劳占比（按用户和渠道去重，但 explode 后每行一个渠道，直接 groupby 即可）
    line_tap_sum = (
        line_tap
        .groupby(['user_id', '渠道'])['功劳占比']
        .sum()
        .reset_index()
    )
    # 按渠道汇总
    line_tap_sum_count = (
        line_tap_sum
        .groupby('渠道')
        .agg(转化数=('功劳占比', 'sum'))
        .reset_index()
    )
    # 计算所有渠道人数总数
    total = line_tap_sum_count['转化数'].sum()
    line_tap_sum_count['各渠道汇总数'] = total
    # 计算各渠道占比
    line_tap_sum_count['占比（%）'] = (line_tap_sum_count['转化数'] / total * 100).round(2)
    return line_tap_sum_count


def time_decay_attribution(df: pd.DataFrame, half_life: float = 7.0) -> pd.DataFrame:
    """
    时间衰减归因（第6节）
    权重 = exp(-(转化时间 - 会话时间) / 半衰期)，半衰期设为7天。
    对每个转化用户，归一化权重后作为贡献份额，累加到对应渠道。
    返回:
        DataFrame 包含 channel, 总归因转化数, 占比(%)
    """
    # 计算时间差（天）
    delta_days = (df['conversion_time'] - df['session_time']).dt.total_seconds() / (24 * 3600)
    # 原始权重
    raw_weight = np.exp(-delta_days / half_life)
    # 每个用户的原始权重和
    user_sum = raw_weight.groupby(df['user_id']).transform('sum')
    norm_weight = raw_weight / user_sum
    # 按渠道汇总
    result = (
        df[['channel']].assign(归一化权重=norm_weight)
        .groupby('channel')
        .agg(总归因转化数=('归一化权重', 'sum'))
        .reset_index()
    )
    # 计算总转化数
    total = result['总归因转化数'].sum()
    result['总渠道总转化数'] = total
    # 计算占比
    result['占比(%)'] = (result['总归因转化数'] / total * 100).round(2)
    return result
