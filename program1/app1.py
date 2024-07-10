import tkinter as tk
from tkinter import messagebox
import pandas as pd

# 创建主窗口
root = tk.Tk()
root.title("智能测绘作业")

# 定义全局变量
df = None
input_values = []
file_path = None
fh = None
fhyun = None
gaizhen = None
answer = []

def calculate():
    global fh, fhyun, gaizhen, answer
    L = [1.8, 2.0, 1.4, 2.6, 1.2]
    h = [16.310, 13.133, 9.871, -3.112, 13.387]
    H = [36.444, 85.997]

    h_li = H[1] - H[0]
    h_ce = sum(h)
    fh = (h_ce - h_li) * 1000000 // 1000 * 0.001
    fhyun = 40 * (sum(L)) ** 0.5 // 1 + 1
    gaizhen = - (fh / sum(L) * 1000 // 1)

    HBM1 = (H[0] + h[0] + gaizhen * L[0] * 0.001) * 1000000 // 1000 * 0.001
    HBM2 = (HBM1 + h[1] + gaizhen * L[1] * 0.001) * 1000000 // 1000 * 0.001
    HBM3 = (HBM2 + h[2] + gaizhen * L[2] * 0.001) * 1000000 // 1000 * 0.001
    HBM4 = (HBM3 + h[3] + gaizhen * L[3] * 0.001) * 1000000 // 1000 * 0.001

    answer = [H[0], HBM1, HBM2, HBM3, HBM4, H[1]]
    return fh, fhyun, gaizhen, answer

def show_answer():
    global fh, fhyun, gaizhen, answer
    # 确保计算已经完成
    if all([v is not None for v in [fh, fhyun, gaizhen, answer]]):
        # 创建文本框来显示结果
        fh_label = tk.Label(root, text=f"高差闭合差为：{fh:.3f}mm")
        fh_label.pack(side="top", padx=5, pady=5)
        fhyun_label = tk.Label(root, text=f"允许高差为：±{fhyun}mm")
        fhyun_label.pack(side="top", padx=5, pady=5)
        gaizhen_label = tk.Label(root, text=f"每米高差改正值为：{gaizhen} mm/m")
        gaizhen_label.pack(side="top", padx=5, pady=5)

        # 显示BM点的高程
        for i, bm_h in enumerate(answer):
            label = tk.Label(root, text=f"BM{chr(ord('A') + i)}的高程为：{bm_h:.3f}m")
            label.pack(side="top", padx=5, pady=5)
    else:
        messagebox.showerror("错误", "计算尚未完成，请先计算数据。")

# 创建按钮
button_frame = tk.Frame(root, height=200)
button2 = tk.Button(button_frame, text="计算数据", command=calculate)
button2.pack(side="left", padx=10, pady=10)
button3 = tk.Button(button_frame, text="输出答案", command=show_answer)
button3.pack(side="left", padx=10, pady=10)
button2.place(x=600,y=100)
button3.place(x=800,y=100)
button_frame.pack(side="top", fill="x")

# 加载图片
image = tk.PhotoImage(file="D:\Desktop\书上图片（第八题）.png")
image = image.subsample(2)
image_label = tk.Label(root, image=image)
image_label.pack(side="bottom", padx=10, pady=10)

# 运行主循环
root.mainloop()