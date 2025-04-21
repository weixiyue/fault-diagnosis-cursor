import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# 设置中文字体（Windows系统通常使用SimHei，Mac使用PingFang SC）
rcParams['font.sans-serif'] = ['SimHei']  # Windows
# rcParams['font.sans-serif'] = ['PingFang SC']  # Mac
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# X轴 - Labels
labels = np.arange(10)

# Y轴 - F1-scores (从图中估算的值)
# 注意：这些值是根据图像目测估算的，可能与原始数据略有偏差
f1_scores = {
    'MPINet':        [98, 98, 99, 99, 95, 99, 100, 99, 98, 97],
    'SVM with TD&FD':   [75, 85, 95, 99, 89, 99, 99, 99, 69, 95],
    'KNN with TD&FD':   [62, 68, 88, 98, 75, 95, 100, 100, 48, 94],
    'MLP with TD&FD':   [54, 65, 93, 99, 67, 98, 100, 99, 48, 95],
    'LSTM with TD&FD':  [72, 69, 96, 99, 80, 99, 100, 99, 65, 92],
    'SVM with TD&EMD':  [70, 90, 98, 100, 99, 99, 100, 99, 75, 96],
    'KNN with TD&EMD':  [53, 60, 85, 95, 72, 98, 100, 100, 55, 90],
    'MLP with TD&EMD':  [60, 72, 95, 99, 82, 99, 100, 100, 70, 94],
    'LSTM with TD&EMD': [74, 92, 99, 100, 92, 100, 100, 100, 80, 97],
    'LSTM':             [59, 51, 60, 64, 55, 93, 85, 75, 68, 35]
}

# 获取模型名称列表（用于图例顺序）
model_names = list(f1_scores.keys())

# 创建图形和坐标轴
# 调整 figsize 使其更接近原图的宽高比
plt.figure(figsize=(10, 6)) # 宽度大于高度

# 绘制每一条线
for model in model_names:
    scores = f1_scores[model]
    linestyle = '--' if model == 'MPINet' else '-' # MPINet 使用虚线
    # Matplotlib 会自动选择不同的颜色
    plt.plot(labels, scores, label=model, linestyle=linestyle, marker='') # marker='' 隐藏数据点标记

# 设置坐标轴标签
plt.xlabel("故障标签", fontsize=14)
plt.ylabel("F1值", fontsize=14)

# 设置坐标轴刻度
plt.xticks(labels, fontsize=12) # X 轴显示 0 到 9
plt.yticks(np.arange(20, 101, 10), fontsize=12) # Y 轴从 20 到 100，步长为 10

# 设置 Y 轴范围
plt.ylim(20, 101) # 与原图 Y 轴范围一致

# 添加网格线
plt.grid(True)

# 添加图例
# bbox_to_anchor 将图例放置在绘图区域之外
# loc='upper left' 表示图例的左上角对齐 bbox_to_anchor 指定的点
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0., fontsize=11)

# 调整布局以防止图例或标签被裁剪
plt.tight_layout(rect=[0, 0, 0.85, 1]) # 为图例留出右侧空间 (rect 参数调整)

# 可以选择性地添加标题 (原图标题不完整，这里省略)
plt.title("模型分类F1值", fontsize=16)

plt.savefig('comparison.png', dpi=300, bbox_inches='tight')

# 显示图形
plt.show()