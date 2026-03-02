import pandas as pd
import matplotlib.pyplot as plt

# 1. 挂载汉化包
plt.rcParams["font.sans-serif"] = ["Arial Unicode MS"]

# 2. 读取新战报，注意路径
file_path = "/Users/zengqianyi/projects/Retail-Auto-ETL-Pipeline/data/final_business_report.xlsx"
df = pd.read_excel(file_path)

# 升级：把数据按照总营收从高到低排序
df = df.sort_values(by="总营收", ascending=False)

# 3. 告诉机器画多大的图
plt.figure(figsize=(10, 6))

# 4. 画一张柱状图！X轴是门店名称，Y轴是总营收，颜色选高级的数据蓝 (SteelBlue)
bars = plt.bar(df["门店名称"], df["总营收"], color="steelblue", width=0.6)

# 升级：给每个柱子顶上打上具体的金额标签
for bar in bars:
    yval = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2.0,
        yval + 100,
        f"¥{int(yval)}",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
    )

# 5. 加上标题和坐标轴
plt.title("某头部连锁餐饮品牌：各门店真实营收排行榜", fontsize=16, fontweight="bold", pad=20)
plt.ylabel("总营收 (元)", fontsize=12)

# 升级：去掉上边框和右边框，让图表看起来极其干净、极简
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# 6. 一键出图！
plt.tight_layout()
plt.show()
