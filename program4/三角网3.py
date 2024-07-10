import random
import numpy as np
import itertools
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import matplotlib.patches as patches


# 创建数据点
def create_data_1(n):
    a = 50 * np.random.random(n)
    b = 50 * np.random.random(n)
    list_1 = []
    for i in zip(a, b):
        list_1.append(i)
    z = np.random.randint(40, 65, [n])  # 假设z是一个一维数组
    return np.array(list_1), z


# 创建Delaunay三角剖分并绘制
def create_delaunay_and_lines():
    global points, triangles
    points, z = create_data_1(30)  # 创建数据点

    # 清除前一个绘图
    ax1.clear()
    ax2.clear()

    # 设置原始图
    ax1.set_aspect('equal')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.scatter(*zip(*points), color='blue')

    # 绘制每个三角形在原始图上
    for triangle in triangles:
        p1, p2, p3 = triangle
        vertices = [p1, p2, p3]
        triangle_patch = patches.Polygon(vertices, closed=True, edgecolor='black', facecolor='white', alpha=0.5)
        ax1.add_patch(triangle_patch)

    # 隐藏原始图的坐标轴
    ax1.axis('off')

    # 绘制等高线图
    ax2.set_aspect('equal')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.scatter(*zip(*points), color='blue')

    # 绘制等高线
    xi, yi = np.linspace(0, 1, 100), np.linspace(0, 1, 100)
    xi, yi = np.meshgrid(xi, yi)
    zi = np.interp(xi, points[:, 0], points[:, 1])  # 假设这是 z 值的插值
    ax2.contour(xi, yi, zi)

    # 隐藏等高线图的坐标轴
    ax2.axis('off')

    # 绘制更新后的图
    canvas.draw()


# 主程序
if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    root.title("Delaunay Triangulation")

    # 创建matplotlib图和轴
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # 添加控件框架
    frame = tk.Frame(root)
    frame.pack(side=tk.BOTTOM, fill=tk.X)

    # 添加输入点数的文本框
    label = tk.Label(frame, text="Number of points:")
    label.pack(side=tk.LEFT)
    entry = tk.Entry(frame)
    entry.pack(side=tk.LEFT)
    entry.insert(0, "10")

    # 添加按钮用于生成和绘制原始点和三角形
    button_original = tk.Button(frame, text="Generate Original Plot", command=create_delaunay_and_lines)
    button_original.pack(side=tk.LEFT)

    # 初始化点集和三角形列表
    points = [(random.random(), random.random()) for _ in range(10)]  # 初始化一些随机点
    triangles = list(itertools.combinations(points, 3))

    # 显示窗口
    tk.mainloop()
