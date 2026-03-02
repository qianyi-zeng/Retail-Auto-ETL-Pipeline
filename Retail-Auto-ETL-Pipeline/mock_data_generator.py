import pandas as pd
import random
from datetime import datetime, timedelta
import os

# 1. 确切路径
folder_path = '/Users/zengqianyi/projects/Retail-Auto-ETL-Pipeline/data'

# 2. 设定商业模型（人为制造贫富差距）
stores = {
    '上海徐汇店': {'orders': random.randint(180, 250), 'price_min': 80, 'price_max': 350},  # 店王
    '上海静安店': {'orders': random.randint(100, 150), 'price_min': 50, 'price_max': 200},  # 中坚力量
    '上海长宁店': {'orders': random.randint(80, 120), 'price_min': 40, 'price_max': 150},  # 中坚力量
    '上海浦东店': {'orders': random.randint(50, 90), 'price_min': 30, 'price_max': 120} ,  # 腰部
    '上海宝山店': {'orders': random.randint(15, 30), 'price_min': 15, 'price_max': 60}  # 吊车尾
}

# 掺杂20%的"已退款"订单，用来证明清洗脚本的过滤能力！
statuses = ['已核销', '已核销', '已核销', '已核销', '已退款']

print("正在为你生成...")

# 3. 开始生成！
for store, meta in stores.items():
    data = []
    for i in range(meta['orders']):
        # 生成随机订单号
        order_id = f"NO{random.randint(10000000, 99999999)}"
        # 生成随机购买金额
        amount = random.randint(meta['price_min'], meta['price_max'])
        # 随机分配状态
        status = random.choice(statuses)
        # 生成过去3天内的随机时间
        days_ago = random.randint(0, 2)
        hours_ago = random.randint(0, 23)
        trans_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago)

        data.append([order_id, store, amount, status, trans_time.strftime('%Y-%m-%d %H:%M:%S')])

    #  列名
    df = pd.DataFrame(data, columns=['订单编号', '门店名称', '购买金额', '订单状态', '核销时间'])

    # 生成 Excel 并直接塞进 data 文件夹
    file_name = f"{folder_path}/{store}.xlsx"
    df.to_excel(file_name, index=False)
    print(f"✅ {store} 数据生成完毕！共 {meta['orders']} 条记录，已投递至目标文件夹。")

print("🚀任务已完成！")