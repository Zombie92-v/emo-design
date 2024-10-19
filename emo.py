import imageio
from io import BytesIO
from getColor import *

def load_image(image_source):
    try:
        # 使用 imageio 读取本地文件或 URL
        image = imageio.imread_v2(image_source)
        img_pil = Image.fromarray(image)  # 转换为 PIL 图像
        return img_pil
    except Exception as e:
        raise ValueError(f"无法加载图片: {e}")


def process_image(image_source, output_size=(240,240), max_file_size_kb=500, save_path=None):
    # Step 1: 使用 imageio 加载图片
    img = load_image(image_source)

    # 获取原始图片的尺寸
    original_width, original_height = img.size

    # 计算等比例缩放后的高度
    target_width = output_size[0]
    target_height = output_size[1]
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


    # Step 3: 保存图片并确保文件大小不超过最大限制
    output_buffer = BytesIO()
    quality = 100  # 初始质量设置 默认不压缩
    while True:
        output_buffer.seek(0)
        new_img.save(output_buffer, format='JPEG', quality=quality)
        size_kb = output_buffer.tell() / 1024  # 获取当前文件大小（KB）

        if size_kb <= max_file_size_kb or quality <= 10:  # 小于最大限制或最低质量
            break
        quality -= 5  # 如果超过最大大小，则降低质量

    # 输出处理后的图片大小和最终质量
    print(f"图片处理完成，最终大小: {size_kb:.2f}KB, 使用质量: {quality}")

    # 保存图片到指定路径
    with open(save_path, "wb") as f:
        f.write(output_buffer.getvalue())
    return save_path



def add_text_to_image(image_source, text, save_path, position=(10, 10), font_size=80,font_path=None,outline_color=(255, 255, 255), outline_width=2):
    # Step 1: 加载图片
    img = load_image(image_source)
    # 计算使用字体颜色
    font_color = choose_font_color(img)

    # Step 2: 创建绘制对象
    draw = ImageDraw.Draw(img)

    # Step 3: 设置字体（默认字体）
    try:
        # 你可以指定自己的字体路径，或者使用默认字体
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()  # 如果找不到字体，使用默认字体


    # Step 4: 在图片上绘制文字
    # 绘制文字的轮廓（多次绘制，实现粗边效果）
    x, y = position
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            draw.text((x + dx, y + dy), text, font=font, fill=outline_color)

    draw.text(position, text, font=font, fill=font_color)

    # Step 5: 保存处理后的图片
    img.save(save_path)
    print(f"图片已保存到: {save_path}")
    return save_path


def resize_gif(input_gif_path, output_gif_path, size=(240, 240)):
    # 打开 GIF 文件
    with Image.open(input_gif_path) as img:
        # 获取 GIF 的每一帧
        frames = []
        for frame in range(img.n_frames):
            img.seek(frame)  # 移动到第 frame 帧
            # 调整每一帧的大小
            resized_frame = img.resize(size, Image.LANCZOS)
            frames.append(resized_frame)

        # 保存调整大小后的 GIF
        frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], loop=0)

if __name__ == '__main__':
    import imageio
    from PIL import Image

    # 输入图片路径
    input_path = r"D:\img\gif\200.webp"

    # 输出图片路径（将扩展名改为 .gif）
    output_path = r"200.gif"

    # 读取 .webp 动图
    webp = imageio.mimread(input_path)

    # 将每一帧保存到 .gif
    imageio.mimsave(output_path, webp, format='GIF', duration=0.1)

    print(f"动图转换完成: {output_path}")
    resize_gif(input_gif_path=output_path, output_gif_path=output_path, size=(240, 240))


