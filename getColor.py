from PIL import Image
from sklearn.cluster import KMeans


def get_dominant_color(image, k=4):
    # 将图片转换为 RGB 格式
    img = image.convert('RGB')

    # 调整大小，加快计算速度
    img = img.resize((100, 100))

    # 获取像素数据
    pixels = np.array(img).reshape((-1, 3))

    # 使用 KMeans 聚类分析主要颜色
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)

    # 获取主要颜色
    dominant_color = kmeans.cluster_centers_[0].astype(int)
    return tuple(dominant_color)


def get_image_brightness(image):
    # 将图片转换为灰度图像
    grayscale = image.convert('L')

    # 计算图片平均亮度
    hist = grayscale.histogram()
    pixels = sum(hist)
    scale = len(hist)
    avg_brightness = sum(i * hist[i] for i in range(scale)) / pixels

    return avg_brightness


def choose_font_color(image):
    avg_brightness = get_image_brightness(image)

    # 如果图片较亮，使用深色字体；如果图片较暗，使用浅色字体
    if avg_brightness > 128:
        return (0, 0, 0)  # 黑色
    else:
        return (255, 255, 255)  # 白色

import cv2
import numpy as np


def detect_edges(image_path):
    # 加载图像并转换为灰度
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用 Canny 边缘检测
    edges = cv2.Canny(gray, 100, 200)

    # # 显示边缘图像
    # cv2.imshow('Edges', edges)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return edges


def find_non_edge_area(image, edges, text_size):
    # 划分图像为网格
    width, height = image.size
    grid_size = 50
    best_area = None
    min_edges = float('inf')

    for x in range(0, width, grid_size):
        for y in range(0, height, grid_size):
            # 获取当前网格中的边缘数量
            grid_edges = edges[y:y + grid_size, x:x + grid_size]
            num_edges = np.sum(grid_edges)

            # 找到边缘最少的区域
            if num_edges < min_edges and (x + text_size[0] <= width and y + text_size[1] <= height):
                min_edges = num_edges
                best_area = (x, y)

    return best_area


from PIL import ImageDraw, ImageFont


def draw_text_on_image(image_source, text, save_path, font_path, max_size=(240, 60)):
    # Step 1: 加载图片
    image = Image.open(image_source)

    # Step 2: 检测主要颜色和亮度
    dominant_color = get_dominant_color(image)
    font_color = choose_font_color(image)

    # Step 3: 检测边缘，避免遮挡主体
    edges = detect_edges(image_source)
    position = find_non_edge_area(image, edges, max_size)

    if not position:
        raise ValueError("无法找到合适的位置放置文字")

    # Step 4: 绘制文字
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, 80)
    draw.text(position, text, font=font, fill=font_color)

    # Step 5: 保存结果
    image.save(save_path)
    print(f"图片已保存到: {save_path}")

if __name__ == '__main__':
    # 示例调用
    draw_text_on_image("../giphy-5.gif",
                       "Hello!",
                       "giphy-5.gif",
                       "font/鼠标仿手写体.ttf")


