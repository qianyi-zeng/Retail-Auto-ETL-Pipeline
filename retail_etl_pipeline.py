import pandas as pd
import glob
import os

# 1. 获取aming_data文件夹下所有的门店 Excel 报表

file_path = '/Users/zengqianyi/projects/Retail-Auto-ETL-Pipeline/data/*.xlsx'
excel_files = glob.glob(file_path)

print(f"✅雷达扫描完毕，共发现 {len(excel_files)} 家门店的原始数据。")

# 2. 把几十张表合并成一张大表
df_list = []
for file in excel_files:
    # 读取每个表格，包含：订单编号、门店名称、购买金额、订单状态、核销日期
    df = pd.read_excel(file)
    df_list.append(df)

# 将所有门店数据上下拼接到一起
master_df = pd.concat(df_list, ignore_index=True)

# 3. 核心清洗逻辑（干掉脏数据）
# 动作A：干掉没有订单号的“幽灵数据” (去除缺失值)
master_df = master_df.dropna(subset=['订单编号'])

# 动作B：剔除掉那些退款的订单 (只保留核销成功的真实流水)
master_df = master_df[master_df['订单状态'] == '已核销']

# 动作C：把日期格式统一，方便后续按天/周做趋势分析
master_df['核销时间'] = pd.to_datetime(master_df['核销时间']).dt.date

# 4. 商业洞察输出：按门店分组，算出谁在亏钱，谁在赚钱
# 算出每家门店的：总核销单数，以及总入账金额
roi_analysis = master_df.groupby('门店名称').agg(
    核销单数=('订单编号', 'count'),
    总营收=('购买金额', 'sum')
).reset_index()

# 算出客单价 （硬核指标）
roi_analysis['平均客单价'] = round(roi_analysis['总营收'] / roi_analysis['核销单数'], 2)

# 按营收从高到低排序，直接锁定销冠门店
roi_analysis = roi_analysis.sort_values(by='总营收', ascending=False)

print("\n🎯战报生成完毕，各门店真实核销 ROI 如下：")
print(roi_analysis)

# 5. 一键导出成结果，注意路径
output_path = '/Users/zengqianyi/projects/aming_data/final_business_report.xlsx'
roi_analysis.to_excel(output_path, index=False)
print("\n📁最终 Excel 已成功生成！")