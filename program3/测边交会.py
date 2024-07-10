import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import math
import matplotlib.pyplot as plt

# Use a font that supports CJK characters
plt.rcParams['font.sans-serif'] = ['SimHei']  # Use SimHei font
plt.rcParams['axes.unicode_minus'] = False  # Ensure minus sign is shown correctly

def trilateration(x1, y1, x2, y2, d1, d2):
    # 定义未知点的坐标 (x, y)
    x, y = sp.symbols('x y')

    # 建立方程组
    eq1 = sp.Eq((x - x1) ** 2 + (y - y1) ** 2, d1 ** 2)
    eq2 = sp.Eq((x - x2) ** 2 + (y - y2) ** 2, d2 ** 2)

    # 解方程组
    solution = sp.solve((eq1, eq2), (x, y))

    return solution

def calculate_distance(x1, y1, x2, y2):
    # 计算两点间的距离
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def plot_results(x1, y1, x2, y2, solutions, d1, d2):
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')

    # 绘制已知点
    ax.plot(x1, y1, 'bo', label='点 A')
    ax.plot(x2, y2, 'go', label='点 B')

    # 标注已知点
    ax.text(x1, y1, f'A ({x1}, {y1})', fontsize=12, ha='right')
    ax.text(x2, y2, f'B ({x2}, {y2})', fontsize=12, ha='right')

    # 绘制圆
    circle1 = plt.Circle((x1, y1), d1, color='b', fill=False, linestyle='dashed')
    circle2 = plt.Circle((x2, y2), d2, color='g', fill=False, linestyle='dashed')
    ax.add_artist(circle1)
    ax.add_artist(circle2)

    # 绘制解
    for solution in solutions:
        px, py = solution
        ax.plot(px, py, 'ro', label='解')
        ax.plot([x1, px], [y1, py], 'b--')
        ax.plot([x2, px], [y2, py], 'g--')
        # 标注解
        ax.text(px, py, f'P ({px:.2f}, {py:.2f})', fontsize=12, ha='right')

    # 设置标签和图例
    ax.set_xlabel('X 轴')
    ax.set_ylabel('Y 轴')
    ax.legend()
    ax.set_title('测边交会结果')

    plt.grid(True)

    return fig

def calculate():
    try:
        # 获取用户输入的值
        x1 = float(entry_x1.get())
        y1 = float(entry_y1.get())
        x2 = float(entry_x2.get())
        y2 = float(entry_y2.get())
        d1 = float(entry_d1.get())
        d2 = float(entry_d2.get())

        # 计算未知点的坐标
        solutions = trilateration(x1, y1, x2, y2, d1, d2)

        # 核验计算结果
        results = []
        for solution in solutions:
            px, py = solution
            calculated_d1 = calculate_distance(px, py, x1, y1)
            calculated_d2 = calculate_distance(px, py, x2, y2)
            results.append((solution, calculated_d1, calculated_d2))

        # 绘制结果图形
        fig = plot_results(x1, y1, x2, y2, solutions, d1, d2)

        # 在 Tkinter 界面中显示图形
        global canvas
        if 'canvas' in globals():
            canvas.get_tk_widget().grid_forget()
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1, rowspan=10, padx=10, pady=10, sticky='nsew')

    except ValueError:
        # 输入无效时显示错误提示
        messagebox.showerror("输入错误", "请输入有效的数字")

# 创建主窗口
root = tk.Tk()
root.title("测边交会计算器")

# 创建并放置输入字段和标签
input_frame = tk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky='n')

tk.Label(input_frame, text="点 A (x1, y1)").grid(row=0, column=0, columnspan=2, pady=5)
tk.Label(input_frame, text="x1:").grid(row=1, column=0, padx=5, pady=5)
entry_x1 = tk.Entry(input_frame)
entry_x1.grid(row=1, column=1, padx=5, pady=5)
entry_x1.insert(0, "3")  # 设置默认值

tk.Label(input_frame, text="y1:").grid(row=2, column=0, padx=5, pady=5)
entry_y1 = tk.Entry(input_frame)
entry_y1.grid(row=2, column=1, padx=5, pady=5)
entry_y1.insert(0, "0")  # 设置默认值

tk.Label(input_frame, text="点 B (x2, y2)").grid(row=3, column=0, columnspan=2, pady=5)
tk.Label(input_frame, text="x2:").grid(row=4, column=0, padx=5, pady=5)
entry_x2 = tk.Entry(input_frame)
entry_x2.grid(row=4, column=1, padx=5, pady=5)
entry_x2.insert(0, "0")  # 设置默认值

tk.Label(input_frame, text="y2:").grid(row=5, column=0, padx=5, pady=5)
entry_y2 = tk.Entry(input_frame)
entry_y2.grid(row=5, column=1, padx=5, pady=5)
entry_y2.insert(0, "4")  # 设置默认值

tk.Label(input_frame, text="距离").grid(row=6, column=0, columnspan=2, pady=5)
tk.Label(input_frame, text="d1:").grid(row=7, column=0, padx=5, pady=5)
entry_d1 = tk.Entry(input_frame)
entry_d1.grid(row=7, column=1, padx=5, pady=5)
entry_d1.insert(0, "3")  # 设置默认值

tk.Label(input_frame, text="d2:").grid(row=8, column=0, padx=5, pady=5)
entry_d2 = tk.Entry(input_frame)
entry_d2.grid(row=8, column=1, padx=5, pady=5)
entry_d2.insert(0, "4")  # 设置默认值

# 创建并放置计算按钮
calculate_button = tk.Button(input_frame, text="计算", command=calculate)
calculate_button.grid(row=9, column=0, columnspan=2, pady=10)

# 配置列和行的权重
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# 运行应用程序
root.mainloop()
