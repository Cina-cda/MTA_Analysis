# -*- coding: utf-8 -*-
"""可视化模块：严格按照 notebook 补充的绘图代码实现"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def set_chinese_font():
    """设置中文字体，复现 notebook 中的 rcParams 配置"""
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei',
                                        'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False


def plot_model_comparison(full_df: pd.DataFrame, save_path: str = None):
    """
    第7节：各渠道在不同归因模型下的贡献对比柱状图
    full_df 需包含列：channel, 首次点击转化数, 末次点击转化数,
                      线性归因转化数, 时间衰减归因转化数
    """
    set_chinese_font()
    channels = full_df['channel'].tolist()
    x = np.arange(len(channels))
    width = 0.2
    
    first = full_df['首次点击转化数']
    last = full_df['末次点击转化数']
    linear = full_df['线性归因转化数']
    time_decay = full_df['时间衰减归因转化数']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - 1.5*width, first, width, label='首次点击')
    rects2 = ax.bar(x - 0.5*width, last, width, label='末次点击')
    rects3 = ax.bar(x + 0.5*width, linear, width, label='线性归因')
    rects4 = ax.bar(x + 1.5*width, time_decay, width, label='时间衰减')
    
    ax.set_xlabel('渠道', fontsize=12)
    ax.set_ylabel('归因转化数', fontsize=12)
    ax.set_title('各渠道在不同归因模型下的贡献对比', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(channels, rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()


def plot_decay_sensitivity(sensitivity_results: dict, save_dir: str = None):
    """
    第12节：为每个半衰期绘制折线图（使用 .T.plot）
    sensitivity_results: {半衰期: result_df}，其中 result_df 需包含 'channel' 和 '占比(%)' 列
    """
    set_chinese_font()
    for hl, df_res in sensitivity_results.items():
        # 将 channel 设为索引，转置后绘图（与 notebook 一致）
        df_res.set_index('channel').T.plot(kind='line', marker='o')
        plt.title(f'时间衰减归因 - 半衰期 {hl} 天')
        plt.ylabel('占比 (%)')
        plt.tight_layout()
        if save_dir:
            plt.savefig(f"{save_dir}/半衰期{hl}天.png", dpi=150, bbox_inches='tight')
        plt.show()
