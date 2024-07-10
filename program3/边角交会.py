import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import math
import matplotlib.pyplot as plt

# Use a font that supports CJK characters
plt.rcParams['font.sans-serif'] = ['SimHei']  # Use SimHei font
plt.rcParams['axes.unicode_minus'] = False  # Ensure minus sign is shown correctly

def edge_intersection(x1, y1, x2, y2, angle1, angle2):
    # Convert angles to radians
    angle1 = math.radians(angle1)
    angle2 = math.radians(angle2)

    # Calculate slopes
    m1 = math.tan(angle1)
    m2 = math.tan(angle2)

    # Define unknown point coordinates (x, y)
    x, y = sp.symbols('x y')

    # Create the system of equations
    eq1 = sp.Eq(y - y1, m1 * (x - x1))
    eq2 = sp.Eq(y - y2, m2 * (x - x2))

    # Solve the system of equations
    solution = sp.solve((eq1, eq2), (x, y))

    return solution

def plot_results(x1, y1, x2, y2, solution):
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')

    # Plot known points
    ax.plot(x1, y1, 'bo', label='点 A')
    ax.plot(x2, y2, 'go', label='点 B')

    # Annotate known points
    ax.text(x1, y1, f'A ({x1}, {y1})', fontsize=12, ha='right')
    ax.text(x2, y2, f'B ({x2}, {y2})', fontsize=12, ha='right')

    # Plot the solution
    px, py = solution[sp.symbols('x')], solution[sp.symbols('y')]
    ax.plot(px, py, 'ro', label='解')
    ax.plot([x1, px], [y1, py], 'b--')
    ax.plot([x2, px], [y2, py], 'g--')

    # Annotate the solution
    ax.text(px, py, f'P ({px:.2f}, {py:.2f})', fontsize=12, ha='right')

    # Set labels and legend
    ax.set_xlabel('X 轴')
    ax.set_ylabel('Y 轴')
    ax.legend()
    ax.set_title('边角交会结果')

    plt.grid(True)

    return fig

def calculate():
    try:
        # Get user input values
        x1 = float(entry_x1.get())
        y1 = float(entry_y1.get())
        x2 = float(entry_x2.get())
        y2 = float(entry_y2.get())
        angle1 = float(entry_angle1.get())
        angle2 = float(entry_angle2.get())

        # Calculate the coordinates of the unknown point
        solution = edge_intersection(x1, y1, x2, y2, angle1, angle2)

        # Plot the results
        fig = plot_results(x1, y1, x2, y2, solution)

        # Display the plot in the Tkinter interface
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=2, rowspan=10, padx=10, pady=10, columnspan=2)

    except ValueError:
        # Show error message if the input is invalid
        messagebox.showerror("输入错误", "请输入有效的数字")

# Create the main window
root = tk.Tk()
root.title("边角交会计算器")

# Create and place input fields and labels
tk.Label(root, text="点 A (x1, y1)").grid(row=0, column=0, padx=10, pady=10)
tk.Label(root, text="x1:").grid(row=1, column=0, padx=10, pady=5)
entry_x1 = tk.Entry(root)
entry_x1.grid(row=1, column=1, padx=10, pady=5)
entry_x1.insert(0, "1")  # Set default value

tk.Label(root, text="y1:").grid(row=2, column=0, padx=10, pady=5)
entry_y1 = tk.Entry(root)
entry_y1.grid(row=2, column=1, padx=10, pady=5)
entry_y1.insert(0, "1")  # Set default value

tk.Label(root, text="点 B (x2, y2)").grid(row=3, column=0, padx=10, pady=10)
tk.Label(root, text="x2:").grid(row=4, column=0, padx=10, pady=5)
entry_x2 = tk.Entry(root)
entry_x2.grid(row=4, column=1, padx=10, pady=5)
entry_x2.insert(0, "4")  # Set default value

tk.Label(root, text="y2:").grid(row=5, column=0, padx=10, pady=5)
entry_y2 = tk.Entry(root)
entry_y2.grid(row=5, column=1, padx=10, pady=5)
entry_y2.insert(0, "1")  # Set default value

tk.Label(root, text="角度").grid(row=6, column=0, padx=10, pady=10)
tk.Label(root, text="angle1 (A点到目标点的角度):").grid(row=7, column=0, padx=10, pady=5)
entry_angle1 = tk.Entry(root)
entry_angle1.grid(row=7, column=1, padx=10, pady=5)
entry_angle1.insert(0, "45")  # Set default value

tk.Label(root, text="angle2 (B点到目标点的角度):").grid(row=8, column=0, padx=10, pady=5)
entry_angle2 = tk.Entry(root)
entry_angle2.grid(row=8, column=1, padx=10, pady=5)
entry_angle2.insert(0, "135")  # Set default value

# Create and place the calculate button
calculate_button = tk.Button(root, text="计算", command=calculate)
calculate_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()
