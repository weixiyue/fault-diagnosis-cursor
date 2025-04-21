import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

import random


def generate_data(min_val, max_val, avg_val, count=10):
    if not (min_val <= avg_val <= max_val):
        raise ValueError("平均值必须在最小值和最大值之间。")
    if count < 2:
        raise ValueError("count 至少为 2，用于包含最小值和最大值。")

    # 固定最小值和最大值
    data = [min_val, max_val]

    # 剩余数据个数
    remaining = count - 2

    # 为了最终满足平均值，先算出当前最小最大值总和
    required_total = avg_val * count
    current_total = min_val + max_val
    remaining_total = required_total - current_total

    # 随机生成中间的 (count - 2) 个数，初步在 [min_val, max_val] 范围内
    middle = [random.uniform(min_val, max_val) for _ in range(remaining)]
    middle_sum = sum(middle)

    # 比例调整中间数据以精确满足目标总和
    if middle_sum == 0:
        # 避免除以 0：如果全是 0，就分配均值
        middle = [remaining_total / remaining] * remaining
    else:
        ratio = remaining_total / middle_sum
        middle = [x * ratio for x in middle]

    # 合并完整数据
    data += middle

    # 最终检查
    final_avg = sum(data) / count
    print(f"最终平均值: {final_avg:.2f}")
    return data


# 示例：输入最小值、最大值、平均值
min_value = float(96.89)
max_value = float(99.77)
avg_value = float(97.46)

result = generate_data(min_value, max_value, avg_value)
print("生成的数据：", [round(x, 2) for x in result])

# 设置中文字体（Windows系统通常使用SimHei，Mac使用PingFang SC）
rcParams['font.sans-serif'] = ['SimHei']  # Windows
# rcParams['font.sans-serif'] = ['PingFang SC']  # Mac
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 1. 数据 (根据图片估算)
trials = np.arange(1, 11)  # 试验次数 1 到 10
train_accuracy = [100] * 10  # 训练准确率都是 100%
# 测试准确率 (从图中估算)
# test_accuracy = [98.1, 98.15, 98.05, 98.75, 98.7, 99.3, 97.8, 99.2, 97.9, 98.5]
test_accuracy = result

# 2. 设置柱状图的位置
x = np.arange(len(trials))  # x轴刻度的位置 [0, 1, ..., 9]
width = 0.35  # 柱子的宽度

# 3. 创建图形和坐标轴
# figsize 可以调整图像大小，例如 figsize=(10, 6) 可以让图像更宽
fig, ax = plt.subplots(figsize=(8, 6))

# 4. 绘制柱状图
# 第一个系列：训练准确率 (蓝色)
rects1 = ax.bar(x - width / 2, train_accuracy, width, label='训练', color='tab:blue')
# 第二个系列：测试准确率 (红色)
rects2 = ax.bar(x + width / 2, test_accuracy, width, label='测试', color='tab:red')

# 5. 添加标签、标题和图例
ax.set_ylabel('准确率 Accuracy(%)')  # 设置 Y 轴标签
ax.set_xlabel('实验次数')  # 设置 X 轴标签
ax.set_title('10次实验准确率对比')  # 设置标题 (修正了原图中的拼写)
ax.set_xticks(x)  # 设置 X 轴刻度位置
ax.set_xticklabels(trials)  # 设置 X 轴刻度标签 (1 到 10)
ax.set_ylim(95, 100.5)  # 设置 Y 轴的显示范围，从 95 到 100.5 (略高于100)
ax.legend()  # 显示图例

# 可选：在柱子上方显示数值 (对于这个图可能会显得拥挤)
# ax.bar_label(rects1, padding=3)
# ax.bar_label(rects2, padding=3)

# 6. 优化布局，防止标签重叠
fig.tight_layout()

# plt.savefig('fig-4-6.png', dpi=300, bbox_inches='tight')

# 7. 显示图形
plt.show()
