from PIL import Image
import emo

def concatenate_images_centered(image_paths, output_path):
    # 打开所有图片并获取其尺寸
    images = [Image.open(path) for path in image_paths]

    # 计算总宽度和最大高度
    total_width = sum(image.width for image in images)
    max_height = max(image.height for image in images)

    # 创建一个新的空白图像
    new_image = Image.new('RGB', (total_width, max_height), (255, 255, 255))  # 白色背景

    # 将每张图片粘贴到新图像中，确保垂直居中
    x_offset = 0
    for image in images:
        y_offset = (max_height - image.height) // 2  # 计算垂直居中偏移
        new_image.paste(image, (x_offset, y_offset))
        x_offset += image.width  # 更新横向偏移量

    # 保存合并后的图像
    new_image.save(output_path)
    print(f"拼接后的图像已保存到: {output_path}")
    return output_path


from PIL import Image, ImageDraw, ImageFont
def get_text_position(image_url, text, font_size, font_path):

    image = emo.load_image(image_url)

    # 创建绘制对象
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)

    # 计算文本边界框
    bbox = draw.textbbox((0, 0), text, font=font)  # 获取文本的边界框
    text_width = bbox[2] - bbox[0]  # 计算文本的宽度
    text_height = bbox[3] - bbox[1]  # 计算文本的高度
    width, height = image.size
    text_position = (width - text_width - 30, height - text_height - 30)  # 右下角位置，留10像素的边距

    return text_position


from PIL import Image

def resize_image(image_url, target_width, target_height, output_path):
    # 下载图片
    img = emo.load_image(image_url)

    # 获取原始图片的尺寸
    original_width, original_height = img.size

    # 计算等比例缩放后的高度
    aspect_ratio = original_width / original_height
    new_height = int(target_width / aspect_ratio)

    # 如果计算出的新高度大于目标高度，使用目标高度进行缩放
    if new_height > target_height:
        new_height = target_height
        new_width = int(aspect_ratio * new_height)
    else:
        new_width = target_width

    # Step 1: 等比例缩放
    img_resized = img.resize((new_width, new_height), Image.LANCZOS)

    # Step 2: 创建一个新的空白图片，并填充为白色
    new_img = Image.new("RGB", (target_width, target_height), (255, 255, 255))

    # 计算放置缩放后图片的位置，居中
    paste_x = (target_width - new_width) // 2
    paste_y = (target_height - new_height) // 2
    new_img.paste(img_resized, (paste_x, paste_y))

    # 保存处理后的图片
    new_img.save(output_path)
    print(f"处理后的图像已保存到: {output_path}")

def generalBannerImg(image_paths, output_path,title=None,font_size=40,font_path=None):
    img = concatenate_images_centered(image_paths, output_path)
    if(title is not None):
        pos = get_text_position(img, title, font_size, font_path)
        img = emo.add_text_to_image(img, title, img, pos, font_size, font_path)
    return img
def format_image_filename(filename):
    # 如果文件名以 .jpg 结尾，替换为 .png
    if filename.endswith('.jpg'):
        return filename[:-4] + '.png'
    # 如果文件名以 .png 结尾，直接返回
    elif filename.endswith('.png'):
        return filename
    # 如果不以 .jpg 或 .png 结尾，追加 .png
    else:
        return filename + '.png'
if __name__ == '__main__':
    # # # 示例调用
    image_paths = [
        r"D:\img\cat\target\01.png",  # 替换为你的文件路径
        r"D:\img\cat\target\02.png",  # 替换为你的文件路径
        r"D:\img\cat\target\03.png",  # 替换为你的文件路径
    ]
    # output_path = r"./banner.png" # 输出路径
    # img = concatenate_images_centered(image_paths, output_path)
    generalBannerImg(image_paths, output_path="../tool/banner03.png", title="小猫日常", font_size=40, font_path="font/鼠标仿手写体.ttf")
    # resize_image("D:\\img\\cat\\01.png",240,240,"./01.png")
    # img = emo.process_image(img, (750, 400), 500, save_path=output_path)
    #
    # pos = get_text_position("D:\\img\cat\\target\\01-01.png", "小猫日常", 60, "../font/鼠标仿手写体.ttf")
    # emo.add_text_to_image(img, "小猫日常", output_path, pos, 60, "../font/鼠标仿手写体.ttf")
