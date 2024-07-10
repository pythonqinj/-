import random
import numpy as np
import itertools
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import matplotlib.patches as patches

def circle_from_three_points(p1, p2, p3):
    A = np.array([
        [p1[0], p1[1], 1],
        [p2[0], p2[1], 1],
        [p3[0], p3[1], 1]
    ])
    B = np.array([
        [-p1[0]**2 - p1[1]**2],
        [-p2[0]**2 - p2[1]**2],
        [-p3[0]**2 - p3[1]**2]
    ])
    X = np.linalg.solve(A, B)
    xc, yc = -0.5 * X[0][0], -0.5 * X[1][0]
    radius = np.sqrt((xc - p1[0])**2 + (yc - p1[1])**2)
    return (xc, yc), radius

def delaunay_triangles(points):
    triangles = set()
    for p1, p2, p3 in itertools.combinations(points, 3):
        center, radius = circle_from_three_points(p1, p2, p3)
        if all(((center[0] - p[0])**2 + (center[1] - p[1])**2 > radius**2 for p in points if p not in (p1, p2, p3))):
            triangles.add(tuple(sorted([p1, p2, p3])))
    return list(triangles)

def generate_and_plot():
    # Generate n random points
    n = int(entry.get())
    points = [(random.random(), random.random()) for _ in range(n)]

    # Find Delaunay triangles
    triangles = delaunay_triangles(points)

    # Clear the previous plot
    ax1.clear()
    ax2.clear()

    # Set up plots
    ax1.set_aspect('equal')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.scatter(*zip(*points), color='blue')

    ax2.set_aspect('equal')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.scatter(*zip(*points), color='blue')

    # Original plot without color scheme
    for triangle in triangles:
        p1, p2, p3 = triangle
        vertices = [p1, p2, p3]
        triangle_patch = patches.Polygon(vertices, closed=True, edgecolor='black', facecolor='white', alpha=0.5)
        ax1.add_patch(triangle_patch)

    # Get the selected color scheme
    selected_color_scheme = color_scheme_var.get()
    color_scheme = color_schemes[selected_color_scheme]

    # Plot each triangle with the selected color scheme
    for i, triangle in enumerate(triangles):
        p1, p2, p3 = triangle
        vertices = [p1, p2, p3]
        color = color_scheme[i % len(color_scheme)]
        triangle_patch = patches.Polygon(vertices, closed=True, edgecolor='black', facecolor=color, alpha=0.5)
        ax2.add_patch(triangle_patch)

    # Hide the axes
    ax1.axis('off')
    ax2.axis('off')

    # Draw the updated plot
    canvas.draw()

# Define the color schemes
color_schemes = {
    "Light Colors": ['#ff4d4f', '#ffaf4d', '#ffc53a', '#fffd37', '#c7ff37', '#37d3ff', '#3787ff', '#8636ff'],
    "Forest Greens": ['#3e8e41', '#0e6647', '#2c5d3e', '#2c4d3e', '#3e4e3e', '#4e3e3e', '#3e3e4e'],
    "Tomato Shades": ['#ff6347', '#ffa07a', '#ff4500', '#ff8c00', '#ff7f50', '#ffd700', '#f0e68c', '#f08080'],
    "Steel Blues": ['#4682b4', '#6495ed', '#00bfff', '#1e90ff', '#add8e6', '#87ceeb', '#00bfff', '#e0ffff']
}

# Create the main window
root = tk.Tk()
root.title("Delaunay Triangulation")

# Create the matplotlib figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Add a frame for the controls
frame = tk.Frame(root)
frame.pack(side=tk.BOTTOM, fill=tk.X)

# Add an entry to input the number of points
label = tk.Label(frame, text="Number of points:")
label.pack(side=tk.LEFT)
entry = tk.Entry(frame)
entry.pack(side=tk.LEFT)
entry.insert(0, "10")

# Add a dropdown to select the color scheme
color_scheme_var = tk.StringVar(root)
color_scheme_var.set("Light Colors")  # default value
color_scheme_menu = tk.OptionMenu(frame, color_scheme_var, *color_schemes.keys())
color_scheme_menu.pack(side=tk.LEFT)

# Add a button to generate and plot the points and triangles
button = tk.Button(frame, text="Generate and Plot", command=generate_and_plot)
button.pack(side=tk.LEFT)

# Start the Tkinter main loop
root.mainloop()
