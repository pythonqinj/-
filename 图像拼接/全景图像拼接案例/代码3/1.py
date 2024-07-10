import cv2 as cv
import numpy as np
import os
from PIL import Image


# 检测图像的SIFT关键特征点
def sift_keypoints_detect(image):
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    sift = cv.SIFT_create()
    keypoints, features = sift.detectAndCompute(gray_image, None)
    return keypoints, features


# 使用KNN检测来自左右图像的SIFT特征，随后进行匹配
def get_feature_point_ensemble(features_right, features_left):
    bf = cv.BFMatcher()
    matches = bf.knnMatch(features_right, features_left, k=2)
    good_matches = []
    for m, n in matches:
        if m.distance < 0.6 * n.distance:  # 根据Lowe's ratio test
            good_matches.append(m)
    return good_matches


# 计算视角变换矩阵H，用H对右图进行变换并返回全景拼接图像
def Panorama_stitching(image_right, image_left, keypoints_right, keypoints_left, good_matches):
    if len(good_matches) >= 4:
        # 获取匹配点的坐标
        src_pts = np.float32([keypoints_right[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints_left[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # 计算单应性矩阵
        H, _ = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
        if H is not None:
            # 透视变换
            result_image = cv.warpPerspective(image_right, H,
                                              (image_right.shape[1] + image_left.shape[1], image_right.shape[0]))
            result_image[0:image_left.shape[0], 0:image_left.shape[1]] = image_left
            return result_image
    return image_left  # 如果拼接失败，返回左图


# 读取一个文件夹里面的多张图片，拼接后生成全景影像
def stitch_images_in_folder(folder_path):
    images = [os.path.join(folder_path, f) for f in sorted(os.listdir(folder_path)) if f.endswith(('.jpg', '.png'))]
    panorama = None
    for i, image_path in enumerate(images):
        image = Image.open(image_path)
        image = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)

        # 检测SIFT关键特征点
        keypoints, features = sift_keypoints_detect(image)

        if panorama is None:
            panorama = image.copy()
            keypoints_prev = keypoints
            features_prev = features
        else:
            # 使用KNN检测特征并进行匹配
            good_matches = get_feature_point_ensemble(features_prev, features)

            if len(good_matches) >= 4:
                # 拼接全景图
                panorama = Panorama_stitching(panorama, image, keypoints_prev, keypoints, good_matches)
            else:
                print(f"Not enough matches found for {image_path}, skipping...")

            # 更新全景图和特征
            keypoints_prev, features_prev = keypoints, features

    if panorama is not None:
        cv.imshow("Final Panorama", panorama)
        cv.waitKey(0)
        cv.destroyAllWindows()
        cv.imwrite("./全景图.jpg", panorama)
    else:
        print("No panorama image to save.")


if __name__ == '__main__':
    folder_path = 'D:\\Pycharm\\Code\\Intelligent mapping\\图像拼接\\全景图像拼接案例\\场景2'
    stitch_images_in_folder(folder_path)