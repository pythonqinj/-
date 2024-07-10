import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np
import os

# 调整图片大小和格式
def resize_and_convert(image, size, mode='RGB'):
    image = image.resize(size, Image.Resampling.LANCZOS)
    return image.convert(mode)

# 检测图像的SIFT关键特征点
def sift_keypoints_detect(image):
    gray_image = cv.cvtColor(np.array(image), cv.COLOR_RGB2GRAY)
    sift = cv.SIFT_create()
    keypoints, features = sift.detectAndCompute(gray_image, None)
    keypoints_image = cv.drawKeypoints(
        gray_image, keypoints, None, flags=cv.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
    return keypoints_image, keypoints, features

# 使用KNN检测来自左右图像的SIFT特征，随后进行匹配
def get_feature_point_ensemble(features_right, features_left):
    bf = cv.BFMatcher()
    matches = bf.knnMatch(features_right, features_left, k=2)
    matches = sorted(matches, key=lambda x: x[0].distance / x[1].distance)
    good = []
    for m, n in matches:
        ratio = 0.6
        if m.distance < ratio * n.distance:
            good.append(m)
    return good

# 计算视角变换矩阵H，用H对右图进行变换并返回全景拼接图像
def Panorama_stitching(image_right, image_left):
    _, keypoints_right, features_right = sift_keypoints_detect(image_right)
    _, keypoints_left, features_left = sift_keypoints_detect(image_left)
    goodMatch = get_feature_point_ensemble(features_right, features_left)
    if len(goodMatch) > 4:
        ptsR = np.float32(
            [keypoints_right[m.queryIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
        ptsL = np.float32(
            [keypoints_left[m.trainIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
        ransacReprojThreshold = 4
        Homography, status = cv.findHomography(ptsR, ptsL, cv.RANSAC, ransacReprojThreshold)
        Panorama = cv.warpPerspective(np.array(image_right), Homography, (image_right.size[0] + image_left.size[0], image_right.size[1]))
        Panorama[0:image_left.size[1], 0:image_left.size[0]] = np.array(image_left)
        return Panorama
    else:
        print("没有足够的特征点进行拼接。")
        return None

# Function to read all images from a folder using PIL
def read_images_from_folder(folder_path):
    images = []
    try:
        for filename in os.listdir(folder_path):
            img_path = os.path.join(folder_path, filename)
            if os.path.isfile(img_path):
                images.append(Image.open(img_path))
            else:
                print(f"Skipping non-file: {img_path}")
    except FileNotFoundError:
        print(f"Folder not found: {folder_path}")
    return images

# Function to stitch images in a folder into a panoramic image
def stitch_images_in_folder(folder_path):
    images = read_images_from_folder(folder_path)
    if len(images) < 2:
        print("至少需要两张图片进行拼接。")
        return None
    # Resize all images to the size of the first image and convert them to RGB
    first_image = images[0]
    size = first_image.size
    images = [resize_and_convert(img, size) for img in images]

    panorama = images[0]  # Initialize with the first image
    for i in range(1, len(images)):
        next_image = images[i]
        if next_image is not None:
            panorama = Panorama_stitching(panorama, next_image)
            if panorama is None:
                print(f"拼接失败: {i}和{i+1}张图片")
                return None
        else:
            print(f"无法读取图片: {images[i]}")
    return panorama

class PanoramaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("全景图像拼接")
        self.root.geometry("800x600")  # 设置窗口大小

        self.folder_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="选择图片文件夹:").pack(pady=5)

        path_frame = tk.Frame(self.root)
        path_frame.pack(pady=5)

        self.path_entry = tk.Entry(path_frame, textvariable=self.folder_path, width=50)
        self.path_entry.pack(side=tk.LEFT)

        browse_button = tk.Button(path_frame, text="浏览", command=self.browse_folder)
        browse_button.pack(side=tk.LEFT, padx=5)

        show_images_button = tk.Button(self.root, text="显示图片", command=self.show_images)
        show_images_button.pack(pady=5)

        stitch_button = tk.Button(self.root, text="生成全景图", command=self.stitch_images)
        stitch_button.pack(pady=5)

        self.images_frame = tk.Frame(self.root)
        self.images_frame.pack(pady=10)

        self.panorama_label = tk.Label(self.root)
        self.panorama_label.pack(pady=10)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def show_images(self):
        for widget in self.images_frame.winfo_children():
            widget.destroy()
        folder_path = self.folder_path.get()
        images = read_images_from_folder(folder_path)
        if not images:
            messagebox.showerror("错误", "未找到任何图片。")
            return
        for img in images:
            img.thumbnail((200, 200))  # 更改缩略图大小
            img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(self.images_frame, image=img_tk)
            label.image = img_tk
            label.pack(side=tk.LEFT, padx=5)

    def stitch_images(self):
        folder_path = self.folder_path.get()
        panorama = stitch_images_in_folder(folder_path)
        if panorama is None:
            messagebox.showerror("错误", "拼接失败。")
        else:
            # 将全景图像显示在界面中
            panorama_img = Image.fromarray(panorama)
            panorama_img.thumbnail((600, 400))  # 缩放全景图以适应界面
            panorama_tk = ImageTk.PhotoImage(panorama_img)
            self.panorama_label.config(image=panorama_tk)
            self.panorama_label.image = panorama_tk

if __name__ == '__main__':
    root = tk.Tk()
    app = PanoramaApp(root)
    root.mainloop()
