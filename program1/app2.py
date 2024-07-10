import tkinter as tk
from tkinter import filedialog, messagebox
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
# 定义选择 Excel 文件的函数
def load_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    global df
    if file_path:
        try:
            df = pd.read_excel(file_path)
            # 将 NaN 值替换为空字符串
            df = df.astype(str)
            display_data(df)
            update_file_path(file_path)
        except Exception as e:
            messagebox.showerror("错误", str(e))

# 更新文件路径显示的函数
def update_file_path(path):
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, path)

# 显示数据的函数
def display_data(data):
    # 清空旧数据
    data_listbox.delete(0, tk.END)
    # 获取列标题
    headers = data.columns.tolist()
    # 将列标题添加到 Listbox
    header_str = " ".join(f"{header:<20}" for header in headers)
    data_listbox.insert(tk.END, header_str)
    # 将每行数据添加到 Listbox，确保每列数据对齐
    for index, row in data.iterrows():
        row_str = " ".join(f"{str(value):<20}" for value in row)
        data_listbox.insert(tk.END, row_str)

# 创建数值输入框
def create_input_boxes():
    global input_values
    input_values = []
    input_frame = tk.Frame(root, borderwidth=2, relief="groove", width=600, height=300)
    input_frame.pack(side="top", fill="both", anchor="ne", expand=True)

    default_values = [80,86,87,90,89,88,85,84]

    for i, default_value in enumerate(default_values):
        row = i // 2
        col = i % 2 * 2
        if i != 7:
            tk.Label(input_frame, text=f"站点{i+1}与站点{i+2}的距离:", padx=5, pady=2).grid(row=row, column=col, sticky="w")
        else:
            tk.Label(input_frame, text=f"站点8与站点1的距离:", padx=5, pady=2).grid(row=row, column=col,sticky="w")
        entry = tk.Entry(input_frame, width=10)
        entry.insert(0, default_value)  # 设置默认值
        entry.grid(row=row, column=col + 1, sticky="ew", padx=20, pady=20)
        input_values.append(entry)

def calculate():
    global fh, fhyun,gaizhen
    excel_file = '测绘数据1.xlsx'
    df = pd.read_excel(excel_file)
    df = df.fillna('')
    for i in range(8):
        # 计算黑面和红面高差
        df.loc[2 + i * 4, "高差"] = (df["后视"][i * 4] - df["前视"][i * 4 + 2]) * 0.001*1000000//1000*0.001
        df.loc[3 + i * 4, "高差"] = (df["后视"][1 + i * 4] - df["前视"][i * 4 + 3]) * 0.001*1000000//1000*0.001
        # 计算平均高差
        df.loc[3 + i * 4, "平均高差"] = ((df["高差"][2 + i * 4] + df["高差"][3 + i * 4]) / 2) * 1000000 // 1000 * 0.001
        # 计算尺常数
        chi_changshu1 = int(df["后视"][1 + i * 4] - df["后视"][0 + i * 4])
        df.loc[2 + i * 4, "后视"] = "({0})".format(chi_changshu1)

        chi_changshu2 = int(df["前视"][3 + i * 4] - df["前视"][2 + i * 4])
        df.loc[1 + i * 4, "前视"] = "({0})".format(chi_changshu2)

    juli = [80, 86, 87, 90, 89, 88, 85, 84]
    L = sum(juli)
    fhyun = 40 * (L*0.001) ** 0.5*1000000//1000*0.001
    fh = 0

    for i in range(8):
        fh = fh + df["高差"][2 + i * 4] + df["高差"][3 + i * 4]
    fh = fh * 1000000 // 1000 * 0.001
    gaizhen = -fh/L

    for i in range(8):
        df.loc[3 + i * 4, "改正后高差"] = (df["平均高差"][3 + i * 4] + (
                    juli[i] * gaizhen) ) * 1000000 // 1000 * 0.001

    # 假定最初点高程为0
    for i in range(8):
        if i == 0:
            df.loc[i * 4, "高程"] = 0
        else:
            df.loc[i * 4, "高程"] = (df["高程"][(i - 1) * 4] + df["改正后高差"][i * 4 - 1]) * 1000000 // 1000 * 0.001

    return display_data(df),fh,fhyun,gaizhen

def show_answer():
    global fh, fhyun,gaizhen
    # 确保计算已经完成
    if fh is not None and fhyun is not None:
        # 创建两个文本框来显示结果
        fh_label = tk.Label(root, text=f"高差闭合差为：{fh}mm")
        fh_label.pack(side="top", padx=5, pady=5)
        fhyun_label = tk.Label(root, text=f"允许高差为：±{fhyun}mm")
        fhyun_label.pack(side="top", padx=5, pady=5)
        gaizhen_label = tk.Label(root, text=f"每米高差改正值为：{gaizhen*1000*1000000//1000*0.001}mm/m")
        gaizhen_label.pack(side="top", padx=5, pady=5)
    else:
        messagebox.showerror("错误", "计算尚未完成，请先计算数据。")



button_frame = tk.Frame(root, height=40)  # 设置按钮框的高度
button1 = tk.Button(button_frame, text="选择数据", command=load_excel, width=15)
button1.pack(side="left", padx=5, pady=5)
file_path_entry = tk.Entry(button_frame, width=50)
file_path_entry.pack(side="left", padx=5, pady=5, fill="x")

button2 = tk.Button(button_frame, text="计算数据", command=calculate, width=15)
button2.pack(side="left", padx=5, pady=5)
button2.place(x=950, y=5)

button3 = tk.Button(button_frame, text="输出答案", command=show_answer, width=15)
button3.pack(side="left", padx=5, pady=5)
button3.place(x=1200, y=5)

button_frame.pack(side="top", fill="x")  # 将按钮框放置在界面上方，并使其水平填充


# 创建数据展示的列表框
data_listbox_frame = tk.Frame(root,width=500)  # 设置列表框的宽度和高度
data_listbox = tk.Listbox(data_listbox_frame, height=15, width=30)  # 设置列表框的高度
data_listbox.pack(side="left", fill="both", expand=True)
data_listbox_frame.pack(side="left", fill="both", expand=True)


# 加载图片
image = tk.PhotoImage(file="测绘作业.png")
image = image.subsample(2)
image_label = tk.Label(root, image=image)
image_label.pack(side="bottom",anchor="se", padx=10, pady=10)




# 创建数值输入框
create_input_boxes()






# 运行主循环
root.mainloop()
