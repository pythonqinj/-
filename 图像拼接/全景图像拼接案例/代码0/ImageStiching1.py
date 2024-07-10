import os
import cv2
import numpy as np

from Stitcher1 import Stitcher

def load_images_from_folder(folder):
    filenames = os.listdir(folder)
    img_paths = [os.path.join(folder, filename) for filename in filenames]
    images = []
    for img_path in img_paths:
        try:
            img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            if img is not None:
                # Convert RGBA to RGB if the image has 4 channels
                if img.shape[2] == 4:
                    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                images.append(img)
            else:
                print(f"Warning: Can't open/read file: {img_path}")
        except Exception as e:
            print(f"Error: {e} while reading file: {img_path}")
    return images

folder = r'D:\Pycharm\Code\Intelligent mapping\图像拼接\全景图像拼接案例\场景0'

images = load_images_from_folder(folder)

if not images:
    print("Error: No images found in the specified folder.")
else:
    stitcher = Stitcher()
    ordered_images = stitcher.orderImages(images)
    if not ordered_images:
        print("Error: Unable to determine the order of images for stitching.")
    else:
        result = stitcher.stitch(ordered_images, showMatches=True)
        if result is None:
            print("Error: Stitching failed.")
        else:
            # If showMatches is True, result will be a tuple (result, vis)
            if isinstance(result, tuple):
                result, vis = result
                cv2.imshow("Keypoint Matches", vis)
            cv2.imshow("Result", result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
