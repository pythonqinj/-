import random
import numpy as np
import itertools
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import matplotlib.patches as patches


def circle_from_three_points(p1, p2, p3):
    """
    根据三个点计算外接圆的圆心和半径。

    :param p1: 第一个点的坐标
    :param p2: 第二个点的坐标
    :param p3: 第三个点的坐标
    :return: 外接圆的圆心坐标和半径
    """
    A = np.array([
        [p1[0], p1[1], 1],
        [p2[0], p2[1], 1],
        [p3[0], p3[1], 1]
    ])
    B = np.array([
        [-p1[0] ** 2 - p1[1] ** 2],
        [-p2[0] ** 2 - p2[1] ** 2],
        [-p3[0] ** 2 - p3[1] ** 2]
    ])
    X = np.linalg.solve(A, B)
    xc, yc = -0.5 * X[0][0], -0.5 * X[1][0]
    radius = np.sqrt((xc - p1[0]) ** 2 + (yc - p1[1]) ** 2)
    return (xc, yc), radius


def delaunay_triangles(points):
    """
    使用Delaunay三角化算法计算点集的三角网。

    :param points: 点集，每个点为一个元组，包含x和y坐标
    :return: 三角网的三角形列表，每个三角形由三个点的索引组成
    """
    triangles = set()
    for p1, p2, p3 in itertools.combinations(points, 3):
        center, radius = circle_from_three_points(p1, p2, p3)
        if all(((center[0] - p[0]) ** 2 + (center[1] - p[1]) ** 2 > radius ** 2 for p in points if
                p not in (p1, p2, p3))):
            triangles.add(tuple(sorted([p1, p2, p3])))
    return list(triangles)


def generate_and_plot_original():
    """
    生成随机点并绘制原始图。
    """
    global points, triangles
    # 生成n个随机点
    n = int(entry.get())
    points = [(random.random(), random.random()) for _ in range(n)]

    # 找到Delaunay三角形
    triangles = delaunay_triangles(points)

    # 清除前一个绘图
    ax1.clear()
    ax2.clear()

    # 设置原始图
    ax1.set_aspect('equal')
    ax1.set_title('Original Figure')
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

    # 绘制更新后的图
    canvas.draw()


def plot_with_color_scheme():
    """
    绘制带有选择的颜色方案的图。
    """
    # 清除前一个绘图
    ax2.clear()

    # 设置带颜色方案的图
    ax2.set_aspect('equal')
    ax2.set_title('Colored Figure')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.scatter(*zip(*points), color='blue')

    # 获取所选颜色方案
    selected_color_scheme = color_scheme_var.get()
    color_scheme = color_schemes[selected_color_scheme]

    # 使用所选颜色方案绘制每个三角形
    for i, triangle in enumerate(triangles):
        p1, p2, p3 = triangle
        vertices = [p1, p2, p3]
        color = color_scheme[i % len(color_scheme)]
        triangle_patch = patches.Polygon(vertices, closed=True, edgecolor='black', facecolor=color, alpha=0.5)
        ax2.add_patch(triangle_patch)

    # 隐藏带颜色方案图的坐标轴
    ax2.axis('off')

    # 绘制更新后的图
    canvas.draw()


# 定义颜色方案
color_schemes = {
    "Light Colors": ['#ff4d4f', '#ffaf4d', '#ffc53a', '#fffd37', '#c7ff37', '#37d3ff', '#3787ff', '#8636ff'],
    "Forest Greens": ['#3e8e41', '#0e6647', '#2c5d3e', '#2c4d3e', '#3e4e3e', '#4e3e3e', '#3e3e4e'],
    "Tomato Shades": ['#ff6347', '#ffa07a', '#ff4500', '#ff8c00', '#ff7f50', '#ffd700', '#f0e68c', '#f08080'],
    "Steel Blues": ['#4682b4', '#6495ed', '#00bfff', '#1e90ff', '#add8e6', '#87ceeb', '#00bfff', '#e0ffff']
}

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
button_original = tk.Button(frame, text="Generate Original Plot", command=generate_and_plot_original)
button_original.pack(side=tk.LEFT)

# 添加下拉菜单选择颜色方案
color_scheme_var = tk.StringVar(root)
color_scheme_var.set("Light Colors")  # 设置默认颜色方案
color_scheme_menu = tk.OptionMenu(frame, color_scheme_var, *color_schemes.keys())
color_scheme_menu.pack(side=tk.LEFT)

# 添加按钮用于绘制带有颜色方案的图
button_color_scheme = tk.Button(frame, text="Plot with Color Scheme", command=plot_with_color_scheme)
button_color_scheme.pack(side=tk.LEFT)

# 初始化点集和三角形列表
points = []
triangles = []

# 显示窗口
tk.mainloop()
