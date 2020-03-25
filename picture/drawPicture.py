# -*- coding: utf-8 -*-

# 使用python画折线图
# pip3 install numpy scipy matplotlib -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

import numpy as np
import matplotlib.pyplot as plt

# X轴，Y轴数据
x = [0, 1, 2, 3, 4, 5, 6]
y = [0.3, 0.4, 2, 5, 3, 4.5, 4]

plt.figure(figsize=(20, 15))  # 创建绘图对象,指定图片大小
plt.plot(x, y, "b--", linewidth=1)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
plt.xlabel("Time")  # X轴标签
plt.ylabel("Value")  # Y轴标签
plt.title("flinkML")  # 图标题
plt.show()  # 显示图
plt.savefig("./flinkML.png")  # 保存图



