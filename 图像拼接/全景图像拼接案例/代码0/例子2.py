from PIL import Image
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

if __name__ == '__main__':
    folder_path = r"D:\Pycharm\Code\Intelligent mapping\图像拼接\全景图像拼接案例\场景(5张)"

    images = read_images_from_folder(folder_path)
    print(images)
    for img in images:
        print(img)
    panorama = stitch_images_in_folder(folder_path)
    if panorama is not None:
        cv.imshow("全景图", panorama)
        cv.imwrite("./panorama.jpg", panorama)
        cv.waitKey(0)
        cv.destroyAllWindows()
