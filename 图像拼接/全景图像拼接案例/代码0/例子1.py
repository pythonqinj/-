import numpy as np
import cv2
import os
from PIL import Image


class Stitcher:
    def __init__(self):
        self.descriptor = cv2.SIFT_create()

    def stitch(self, images, ratio=0.75, reprojThresh=4.0, showMatches=False):
        if len(images) < 2:
            print("Error: At least two images are required to stitch a panorama.")
            return None

        reference_image = images[0]
        reference_kps, reference_features = self.detectAndDescribe(reference_image)

        result_image = reference_image

        for image in images[1:]:
            kps, features = self.detectAndDescribe(image)
            matches = self.matchKeypoints(reference_features, features, ratio)

            if len(matches) < 4:
                print("Error: Not enough matches found for image.")
                continue

            ptsA = np.float32([reference_kps[m.queryIdx].pt for m in matches])
            ptsB = np.float32([kps[m.trainIdx].pt for m in matches])

            H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)

            if H is None:
                print("Error: Homography estimation failed.")
                continue

            result_image = self.warpAndBlend(result_image, image, H)

            if showMatches:
                vis = self.drawMatches(reference_image, reference_kps, image, kps, matches, status)
                cv2.imshow("Matches", vis)
                cv2.waitKey(0)

            reference_image = result_image
            reference_kps, reference_features = self.detectAndDescribe(result_image)

        return result_image

    def detectAndDescribe(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (kps, features) = self.descriptor.detectAndCompute(gray, None)
        return (kps, features)

    def matchKeypoints(self, featuresA, featuresB, ratio):
        matcher = cv2.BFMatcher()
        rawMatches = matcher.knnMatch(featuresA, featuresB, k=2)
        good_matches = [m[0] for m in rawMatches if len(m) == 2 and m[0].distance < m[1].distance * ratio]
        return good_matches

    def warpAndBlend(self, img1, img2, H):
        # Warp img2 to img1 using the homography matrix H
        warped_image = cv2.warpPerspective(img2, H, (img1.shape[1] + img2.shape[1], img1.shape[0]))

        # Create a canvas that can hold the warped image and img1
        canvas = np.zeros((img1.shape[0], img1.shape[1] + img2.shape[1], 3), dtype=np.uint8)
        canvas[:img1.shape[0], :img1.shape[1]] = img1

        # Blend the warped image and the original image using multi-band blending or simple averaging
        # Here we use simple addition
        result = cv2.addWeighted(canvas, 0.5, warped_image, 0.5, 0)

        return result

    def drawMatches(self, img1, kps1, img2, kps2, matches, status):
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        vis = np.zeros((max(h1, h2), w1 + w2, 3), dtype="uint8")
        vis[:h1, :w1] = img1
        vis[:h2, w1:] = img2

        for (match, s) in zip(matches, status):
            if s:
                pt1 = (int(kps1[match.queryIdx].pt[0]), int(kps1[match.queryIdx].pt[1]))
                pt2 = (int(kps2[match.trainIdx].pt[0] + w1), int(kps2[match.trainIdx].pt[1]))
                cv2.line(vis, pt1, pt2, (0, 255, 0), 1)
        return vis


def load_images_from_folder(folder):
    if not folder.endswith(os.sep):
        folder += os.sep
    filenames = sorted(os.listdir(folder))
    img_paths = [os.path.join(folder, filename) for filename in filenames if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    images = []
    for img_path in img_paths:
        # 使用PIL读取图像并转换为numpy数组
        with Image.open(img_path) as img:
            img_array = np.array(img)
            # 将numpy数组转换为OpenCV格式的图像
            cv_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            images.append(cv_img)

    return images


# 使用示例
folder = r'D:\Pycharm\Code\Intelligent mapping\图像拼接\全景图像拼接案例\场景1'  # 更新为你的文件夹路径
images = load_images_from_folder(folder)

if not images:
    print("错误: 在指定文件夹中未找到图像。")
else:
    stitcher = Stitcher()
    result = stitcher.stitch(images, showMatches=False)
    if result is None:
        print("错误: 拼接失败。")
    else:
        cv2.imshow("全景图", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite("stitched_panorama.png", result)
