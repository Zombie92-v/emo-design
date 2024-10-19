import cv2
import numpy as np
from rembg import remove

import emo


def replace_background(image_path, new_bg_color, output_image_path):
    # 读取原始图像
    # image = cv2.imread(image_path)
    image = emo.load_image(image_path)

    # 使用 rembg 去除背景
    image_no_bg = remove(image)

    # 创建一个新背景
    background = np.full(image.ssa, new_bg_color, dtype=np.uint8)

    # 将没有背景的图像转换为 RGB 格式
    image_no_bg = cv2.cvtColor(image_no_bg, cv2.COLOR_RGBA2BGR)

    # 使用 OpenCV 创建掩码
    mask = (image_no_bg != 0).astype(np.uint8)  # 创建掩码，非零表示前景
    mask = cv2.cvtColor(mask * 255, cv2.COLOR_GRAY2BGR)  # 转换为三通道

    # 将前景和背景合成
    foreground = image_no_bg * mask
    background = background * (1 - mask)

    result_image = foreground + background

    # 保存结果图像
    cv2.imwrite(output_image_path, result_image)


# 示例用法
if __name__ == "__main__":
    input_image_path = 'D:\\img\\cat\\target\\致谢图.png'  # 输入图片路径
    output_image_path = 'output_image.png'  # 输出图片路径
    new_background_color = [0, 255, 0]  # 新背景颜色（绿色）

    # 替换背景
    replace_background(input_image_path, new_background_color, output_image_path)

    print(f"背景已替换，输出图片保存为: {output_image_path}")
