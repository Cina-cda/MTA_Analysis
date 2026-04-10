# main.py
"""主程序：串联所有模块，完整执行归因分析流程，输出 Excel 报告和图片"""

import pandas as pd
from config import EXCEL_FILE, FIGURES_DIR
from data_loader import load_and_explore
from preprocessing import preprocess_data
from attribution_models import (
    first_click_attribution,
    last_click_attribution,
    linear_attribution,
    time_decay_attribution,
)
from advanced_analysis import (
    u_shaped_attribution,
    channel_synergy_analysis,
    path_length_distribution,
    time_decay_sensitivity,
)
from visualization import plot_model_comparison, plot_decay_sensitivity


def main():
    # 1. 数据加载
    print("=" * 50)
    print("1. 加载数据并转换时间列")
    sessions, conversions = load_and_explore()

    # 2. 预处理
    print("\n" + "=" * 50)
    print("2. 预处理：排序、合并、筛选转化前会话")
    full_select = preprocess_data(sessions, conversions)

    # 3. 首次点击归因
    print("\n" + "=" * 50)
    print("3. 首次点击归因")
    first_df = first_click_attribution(full_select)
    print(first_df)

    # 4. 末次点击归因
    print("\n" + "=" * 50)
    print("4. 末次点击归因")
    last_df = last_click_attribution(full_select)
    print(last_df)

    # 5. 线性归因
    print("\n" + "=" * 50)
    print("5. 线性归因")
    linear_df = linear_attribution(full_select)
    print(linear_df)

    # 6. 时间衰减归因（默认半衰期7天）
    print("\n" + "=" * 50)
    print("6. 时间衰减归因（半衰期7天）")
    time_df = time_decay_attribution(full_select, half_life=7.0)
    print(time_df)

    # 7. 合并对比汇总表
    print("\n" + "=" * 50)
    print("7. 合并生成对比汇总表")
    full = (
        first_df[['channel', '人数', '占比（%）']]
        .rename(columns={'人数': '首次点击转化数'})
        .merge(
            last_df[['channel', '人数', '占比（%）']].rename(columns={'人数': '末次点击转化数'}),
            on='channel'
        )
        .merge(
            linear_df[['渠道', '转化数', '占比（%）']].rename(columns={'渠道': 'channel', '转化数': '线性归因转化数'}),
            on='channel'
        )
        .merge(
            time_df[['channel', '总归因转化数', '占比(%)']],
            on='channel'
        )
    )
    full = full.rename(columns={
        '占比（%）_x': '首次点击占比(%)',
        '占比（%）_y': '末次点击占比(%)',
        '占比（%）': '线性归因占比(%)',
        '占比(%)': '时间衰减归因占比(%)',
        '总归因转化数': '时间衰减归因转化数'
    })
    print(full)

    # 8. U型归因（第9节）
    print("\n" + "=" * 50)
    print("8. U型归因（基于位置）")
    u_df = u_shaped_attribution(full_select)
    print(u_df)

    # 9. 渠道协同效应分析（第10节）
    print("\n" + "=" * 50)
    print("9. 渠道协同效应分析")
    pair_counts, ratio = channel_synergy_analysis(full_select)
    print(f"渠道对频次表（前5行）:\n{pair_counts.head()}")

    # 10. 转化路径长度分布（第11节）
    print("\n" + "=" * 50)
    print("10. 转化路径长度分布")
    # 先计算会话次数列（full_select 中没有，需临时计算）
    full_with_count = full_select.copy()
    full_with_count['会话次数'] = full_with_count.groupby('user_id')['session_time'].transform('count')
    session_count_dist, combo_avg_len = path_length_distribution(full_with_count)
    print("会话次数分布:\n", session_count_dist)
    print("渠道组合平均路径长度（前5行）:\n", combo_avg_len.head())

    # 11. 时间窗口敏感性分析（第12节）
    print("\n" + "=" * 50)
    print("11. 时间窗口敏感性分析（半衰期1天、3天、7天、14天）")
    half_lives = [1, 3, 7, 14]
    sensitivity_results = time_decay_sensitivity(full_select, half_lives)
    time_half_time_1 = sensitivity_results[1]
    time_half_time_3 = sensitivity_results[3]
    time_half_time_7 = sensitivity_results[7]
    time_half_time_14 = sensitivity_results[14]
    print("半衰期1天结果:\n", time_half_time_1)
    print("半衰期3天结果:\n", time_half_time_3)
    print("半衰期14天结果:\n", time_half_time_14)

    # 12. 一次性写入 Excel（避免追加模式错误）
    print("\n" + "=" * 50)
    print("12. 保存结果到 Excel（一次性写入所有 sheet）")
    with pd.ExcelWriter(EXCEL_FILE) as writer:
        first_df.to_excel(writer, sheet_name='首次点击', index=False)
        last_df.to_excel(writer, sheet_name='末次点击', index=False)
        linear_df.to_excel(writer, sheet_name='线性归因', index=False)
        time_df.to_excel(writer, sheet_name='时间衰减', index=False)
        full.to_excel(writer, sheet_name='对比汇总', index=False)
        u_df.to_excel(writer, sheet_name='U型归因', index=False)
        pair_counts.to_excel(writer, sheet_name='渠道协同', index=False)
        session_count_dist.to_excel(writer, sheet_name='路径长度分布', index=False)
        combo_avg_len.to_excel(writer, sheet_name='渠道组合平均长度', index=False)
        time_half_time_1.to_excel(writer, sheet_name='衰减半衰期1天', index=False)
        time_half_time_3.to_excel(writer, sheet_name='衰减半衰期3天', index=False)
        time_half_time_7.to_excel(writer, sheet_name='衰减半衰期7天', index=False)
        time_half_time_14.to_excel(writer, sheet_name='衰减半衰期14天', index=False)
    print(f"Excel 已保存至: {EXCEL_FILE}")

    # 13. 绘图
    print("\n" + "=" * 50)
    print("13. 生成图表")
    plot_model_comparison(full, save_path=FIGURES_DIR / "各渠道在不同归因模型下的贡献对比.png")
    plot_decay_sensitivity(sensitivity_results, save_dir=FIGURES_DIR)

    print("\n" + "=" * 50)
    print("分析完成！所有结果已保存至 outputs 目录。")


if __name__ == "__main__":
    main()