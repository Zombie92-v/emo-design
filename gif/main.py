import requests
from emoGenral import general
from PIL import Image

def download_mp4(url, save_dir='downloads',out=""):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    response = requests.get(url, stream=True)
    filename = os.path.join(save_dir,out)

    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return os.path.abspath(filename)


from moviepy.editor import VideoFileClip
import os

def convert_to_gif(source,output_path=None, max_size=500, crop_size=(240, 240),output_dir="gif"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        clip = VideoFileClip(source)
        # 获取原始宽高比
        original_width, original_height = clip.size
        original_ratio = original_width / original_height
        crop_width, crop_height = crop_size
        crop_ratio = crop_width / crop_height

        # 按比例调整尺寸
        if original_ratio > crop_ratio:
            # 如果原图比裁剪区域宽，按高度缩放
            clip = clip.resize(height=crop_height)
        else:
            # 如果原图比裁剪区域窄，按宽度缩放
            clip = clip.resize(width=crop_width)

        # 计算裁剪区域 (中心裁剪)
        x1 = (clip.w - crop_width) // 2
        y1 = (clip.h - crop_height) // 2
        x2 = (clip.w + crop_width) // 2
        y2 = (clip.h + crop_height) // 2

        # 中心裁剪
        clip = clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)

        # 调整GIF大小并控制文件大小
        scale = 1.0
        while True:
            gif_path = os.path.join(output_dir,output_path)
            clip_resized = clip.resize(scale)
            clip_resized.write_gif(gif_path, fps=8)  # 可以调整帧率
            if os.path.getsize(gif_path) <= max_size * 1024:  # 限制文件大小
                break
            scale *= 0.9  # 缩小GIF尺寸以减小文件大小

    except Exception as e:
        raise ValueError(f"转换为GIF时出错: {e}")
    finally:
        clip.close()  # 确保关闭文件


def send_request(api_url="http://8.134.205.36:8000/red/context", message=None, request_type="all"):
    # 定义请求的 URL 和头部信息
    headers = {
        'Content-Type': 'application/json'
    }

    # 定义请求数据
    data = {
        "url": message,
        "type": request_type
    }

    # 发送 POST 请求
    response = requests.post(api_url, headers=headers, json=data)

    # 返回响应结果
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}"}


def save_first_frame_as_png(mp4_file, output_image,output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        # 读取视频文件
        clip = VideoFileClip(mp4_file)

        # 获取第一帧 (0秒处的帧)
        first_frame = clip.get_frame(0)

        # 保存为 PNG 格式
        image = Image.fromarray(first_frame)
        image.save(output_image, format='PNG')

        # 获取文件的绝对路径
        # absolute_path = os.path.abspath(output_image)
        absolute_path = os.path.join(output_dir, output_image)
        print(f"第一帧保存为 {absolute_path}")

        return absolute_path  # 返回绝对路径
    except Exception as e:
        print(f"读取或保存第一帧时出错: {e}")
        return None
    finally:
        clip.close()  # 确保关闭视频文件

if __name__ == '__main__':
    mp4Data = send_request(message="59 困困熊.发布了一篇小红书笔记，快来看吧！ 😆 j1sIXHYzB4Uj2dA 😆 http://xhslink.com/a/DmPRkCmDOT2X，复制本条信息，打开【小红书】App查看精彩内容！")
    mp4List = mp4Data["result"].get("mp4List", [])
    updated_urls = [url.replace('https', 'http') for url in mp4List]
    # 保存文件第一帧路径
    imgPath = "img-first"
    imgList = []
    for i,mp4 in enumerate(updated_urls):
        print(mp4)
        video_path = download_mp4(mp4,save_dir="downloads/mp4",out=f"{i}-2.mp4")
        print(video_path)
        imgList.append(save_first_frame_as_png(video_path,f"{i}.png","downloads/img"))
        convert_to_gif(video_path, f"{i}-2.gif",output_dir="downloads/gif")
    # 生成横幅
    # masterImgList = mp4Data["result"].get("masterImgList", [])
    general(path=r"D:\project\emo-design\gif\downloads",imgList=imgList,dir="target",title="搞笑日常",firstWord="发疯",font_path=r"D:\project\emo-design\font\鼠标仿手写体.ttf")
