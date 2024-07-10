import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# 创建主窗口
root = tk.Tk()
root.title("智能测绘作业")

# 定义全局变量
df = None
def load_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    global df
    if file_path:
        try:
            df = pd.read_excel(file_path)
            for col in ['L度', 'L分', 'L秒', 'R度', 'R分', 'R秒']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
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

def calculate_2C_1(df):
    for i in range(2,7):
        randous_L = df["L度"][i] * 3600 + df["L分"][i] *60 + df["L秒"][i]
        randous_R = df["R度"][i] * 3600 + df["R分"][i] *60 + df["R秒"][i]
        dr = randous_L - randous_R
        if dr  < 180*3600:
            df["2C"][i] = dr + 180*3600
        else:
            df["2C"][i] = dr - 180*3600

def calculate_2C_2(df):
    for i in range(8,13):
        randous_L = df["L度"][i] * 3600 + df["L分"][i] *60 + df["L秒"][i]
        randous_R = df["R度"][i] * 3600 + df["R分"][i] *60 + df["R秒"][i]
        dr = randous_L - randous_R
        if dr  < 180*3600:
            df["2C"][i] = dr + 180*3600
        else:
            df["2C"][i] = dr - 180*3600
def calculate_pan(df):
    for i in range(2,7):
        randous_L = df["L度"][i] * 3600 + df["L分"][i] *60 + df["L秒"][i]
        randous_R = df["R度"][i] * 3600 + df["R分"][i] *60 + df["R秒"][i]
        dr = randous_L - randous_R
        if dr < 0 :
            R = ( randous_L + (randous_R - 180 * 3600) ) * 0.5
            pan_du = R//3600
            pan_fen = (R - pan_du*3600)//60
            pan_miao = (R - pan_du*3600 - pan_fen* 60)//1
        else:
            R =( randous_L + (randous_R + 180 * 3600)) * 0.5
            pan_du = R//3600
            pan_fen = (R - pan_du*3600)//60
            pan_miao = (R - pan_du*3600 - pan_fen* 60)//1
        df["盘度"][i] = pan_du
        df["盘分"][i] = pan_miao
        df["盘秒"][i] = pan_miao
    for i in range(8,13):
        randous_L = df["L度"][i] * 3600 + df["L分"][i] *60 + df["L秒"][i]
        randous_R = df["R度"][i] * 3600 + df["R分"][i] *60 + df["R秒"][i]
        dr = randous_L - randous_R
        if dr < 0 :
            R = ( randous_L + (randous_R - 180 * 3600) ) * 0.5
            pan_du = R//3600
            pan_fen = (R - pan_du*3600)//60
            pan_miao = (R - pan_du*3600 - pan_fen* 60)//1
        else:
            R = ( randous_L + (randous_R + 180 * 3600) ) * 0.5
            pan_du = R//3600
            pan_fen = (R - pan_du*3600)//60
            pan_miao = (R - pan_du*3600 - pan_fen* 60)//1
        df["盘度"][i] = pan_du
        df["盘分"][i] = pan_fen
        df["盘秒"][i] = pan_miao
    return df

def calculate_guilin(df):
    i = 2
    j = 6
    a = (df["盘度"][i]*3600 + df["盘分"][i]*60 + df["盘秒"][i] + df["盘度"][j]*3600 + df["盘分"][j]*60 + df["盘秒"][j])/2
    df["盘度"][1] = a//3600
    df["盘分"][1] = (a- df["盘度"][1]*3600)//60
    df["盘秒"][1] = (a- df["盘度"][1]*3600 - df["盘分"][1]*60 )//60
    i = 8
    j = 12
    a = (df["盘度"][i]*3600 + df["盘分"][i]*60 + df["盘秒"][i] + df["盘度"][j]*3600 + df["盘分"][j]*60 + df["盘秒"][j])/2
    df["盘度"][7] = a//3600
    df["盘分"][7] = (a- df["盘度"][7]*3600)//60
    df["盘秒"][7] = a- df["盘度"][7]*3600 - df["盘分"][7]*60

def calculate_gui(df):
    df["归度"][2] = 0
    df["归分"][2] = 0
    df["归秒"][2] = 0
    df["归度"][8] = 0
    df["归分"][8] = 0
    df["归秒"][8] = 0
    randous_guilin1 = df["盘度"][1] * 3600 + df["盘分"][1] *60 + df["盘秒"][1]
    for i in range(3,6):
        randous_pan = df["盘度"][i] * 3600 + df["盘分"][i] *60 + df["盘秒"][i]
        gui1 = randous_pan - randous_guilin1
        df["归度"][i] = gui1//3600
        df["归分"][i] = (gui1 - df["归度"][i]*3600)//60
        df["归秒"][i] = gui1 - df["归度"][i]*3600 - df["归分"][i]*60
    randous_guilin2 = df["盘度"][7] * 3600 + df["盘分"][7] *60 + df["盘秒"][7]
    for i in range(9,12):
        randous_pan = df["盘度"][i] * 3600 + df["盘分"][i] *60 + df["盘秒"][i]
        gui2 = randous_pan - randous_guilin2
        df["归度"][i] = gui2//3600
        df["归分"][i] = (gui2 - df["归度"][i]*3600)//60
        df["归秒"][i] = gui2 - df["归度"][i]*3600 - df["归分"][i]*60
def calculate_ge(df):
    for i in range(2,6):
        junzhi_1 =  df["归度"][i]*3600 +  df["归分"][i]*60 + df["归秒"][i]
        junzhi_2 =  df["归度"][i+6]*3600 +  df["归分"][i+6]*60 + df["归秒"][i+6]
        junzhi = (junzhi_1 + junzhi_2)/2
        df["各度"][i+6] = junzhi//3600
        df["各分"][i+6] = (junzhi - df["各度"][i+6]*3600)//60
        df["各秒"][i+6] = (junzhi - df["各度"][i+6]*3600 - df["各分"][i+6]*60)//1


def calculate():
    global df  # 使用全局变量df
    try:
        calculate_2C_1(df)
        calculate_2C_2(df)
        df = calculate_pan(df)
        calculate_guilin(df)
        calculate_gui(df)
        calculate_ge(df)
        display_data(df)  # 计算结束后刷新显示数据
    except Exception as e:
        messagebox.showerror("计算错误", str(e))

button_frame = tk.Frame(root, height=40)  # 设置按钮框的高度
button1 = tk.Button(button_frame, text="选择数据", command=load_excel, width=15)
button1.pack(side="left", padx=5, pady=5)
file_path_entry = tk.Entry(button_frame, width=50)
file_path_entry.pack(side="left", padx=5, pady=5, fill="x")

button2 = tk.Button(button_frame, text="计算数据", command=calculate, width=15)
button2.pack(side="left", padx=5, pady=5)
button2.place(x=950, y=5)

button_frame.pack(side="top", fill="x")  # 将按钮框放置在界面上方，并使其水平填充


# 创建数据展示的列表框
data_listbox_frame = tk.Frame(root, width=600, height=400)  # 设置列表框的宽度和高度
data_listbox = tk.Listbox(data_listbox_frame, height=30, width=200)  # 设置列表框的高度
data_listbox.pack(side="left", fill="both", expand=True)  # 使Listbox填满其父窗口
data_listbox_frame.pack(side="top", pady=10)  # 将数据展示区域放置在界面顶部，并留出一些间距

window_width = root.winfo_screenwidth()
x_pos = (window_width - data_listbox_frame.winfo_reqwidth()) // 2-400
y_pos = 50  # 可以根据需要调整这个值

data_listbox_frame.place(x=x_pos, y=y_pos)


# 加载图片
image = tk.PhotoImage(file="picture.png")
image = image.subsample(2)# 根据需要调整缩放比例
image_label = tk.Label(root, image=image)
image_label.pack(side="bottom", padx=10, pady=10)

# 运行主循环
root.mainloop()
