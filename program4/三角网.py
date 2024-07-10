import random
import numpy as np
import itertools
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

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
    ax.clear()
    ax.set_aspect('equal')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.scatter(*zip(*points), color='red')

    # Plot each triangle
    for triangle in triangles:
        polygon = plt.Polygon(triangle, edgecolor='blue', fill=None)
        ax.add_patch(polygon)

    # Draw the updated plot
    canvas.draw()

# Create the main window
root = tk.Tk()
root.title("Delaunay Triangulation")

# Create the matplotlib figure and axis
fig, ax = plt.subplots()
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

# Add a button to generate and plot the points and triangles
button = tk.Button(frame, text="Generate and Plot", command=generate_and_plot)
button.pack(side=tk.LEFT)

# Start the Tkinter main loop
root.mainloop()
