from PIL import Image
import os

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

"""
获取目录文件
"""
def getFiles(path):
    return [os.path.abspath(os.path.join(path, f)) for f in os.listdir(path) if
               os.path.isfile(os.path.join(path, f))]

if __name__ == '__main__':
    path = r"D:\img\gif"
    files = getFiles(path)
    # 输出目录
    target = os.path.join(path, "target")
    # 创建目录
    for f in files:
        resize_gif(input_gif_path=f, output_gif_path="2100.gif")
