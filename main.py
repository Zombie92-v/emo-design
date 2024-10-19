from PIL.Image import Image

import emo
import os

from generalImg import *

# path 是要遍历的根目录，"." 是当前目录
path = 'D:\\img\\cat'
dir = 'target'
title = "小黑喵日常"
firstWord = "喵喵"
guidanceWord = "没有粮食了 喵~"
thinkWord = "感谢大人 打赏~"
def general(path: str, dir="target", title: str=None, firstWord: str=None,guidanceWord:str=None,thinkWord:str=None,imgList=None):
    # files 就是所有文件的绝对路径列表，不包括目录
    if(imgList==None):
        imgList = [os.path.abspath(os.path.join(path, f)) for f in os.listdir(path) if
                   os.path.isfile(os.path.join(path, f))]
    emoList = []
    tb = None
    target_dir = None
    for index, img in enumerate(imgList):
        # 确定目标目录
        target_dir = os.path.join(path, dir)
        # 创建目标目录（如果不存在的话）
        os.makedirs(target_dir, exist_ok=True)
        filename = format_image_filename(os.path.basename(img))
        imgSavePath = os.path.join(target_dir, filename)
        emo.process_image(img, (240, 240), 500, imgSavePath)
        print(f'表情包保存路径：{imgSavePath}')
        emoList.append(imgSavePath)

    # 生成banner JPG 或 PNG 格式，750*400 像素。
    bannerPath = os.path.join(target_dir, "banner.png")
    bannerPath = generalBannerImg(image_paths=emoList[0:3], output_path=bannerPath, title=title, font_size=40,
                                  font_path="font/鼠标仿手写体.ttf")
    # 格式设置
    bannerPath = emo.process_image(bannerPath, (750, 400), 500, bannerPath)
    print(f'横幅生成：{bannerPath}')

    # 封面 PNG 格式，240*240像素。
    firstImg = os.path.join(target_dir, "封面.png")
    firstImg = generalBannerImg(image_paths=emoList[0:-1], output_path=firstImg, title=firstWord, font_size=40,
                                font_path="font/鼠标仿手写体.ttf")
    # 格式设置
    firstImg = emo.process_image(firstImg, (240, 240), 500, firstImg)
    firstImg = make_image_transparent(firstImg,firstImg)
    print(f'封面生成：{firstImg}')
    # 生成图标 PNG 格式，50*50像素。
    icon = os.path.join(target_dir, "图标.png")
    icon = generalBannerImg(image_paths=emoList[0:1], output_path=icon, title=None, font_size=40,
                            font_path="font/鼠标仿手写体.ttf")
    # 格式设置
    icon = emo.process_image(icon, (50, 50), 500, icon)
    icon = make_image_transparent(icon,icon)
    print(f'图标生成：{icon}')

    # 赞赏引导图 750*560 像素（图片上传后将被压缩至500KB以下才可提交）。
    guidance = os.path.join(target_dir, "引导图.png")
    guidance = generalBannerImg(image_paths=emoList[3:6], output_path=guidance, title=guidanceWord, font_size=40,
                                  font_path="font/鼠标仿手写体.ttf")
    # 格式设置
    guidance = emo.process_image(guidance, (750, 560), 500, guidance)
    print(f'引导图生成：{guidance}')
    # 赞赏致谢图 JPG、PNG 或 GIF格式，750*750像素。
    think = os.path.join(target_dir, "致谢图.png")
    think = generalBannerImg(image_paths=emoList[6:7], output_path=think, title=thinkWord, font_size=20,
                                  font_path="font/鼠标仿手写体.ttf")
    # 格式设置
    think = emo.process_image(think, (750, 750), 500, think)
    print(f'致谢图生成：{think}')

def make_image_transparent(input_image_path, output_image_path, color_to_make_transparent=(255, 255, 255)):
    # 打开图片
    img = emo.load_image(input_image_path)
    # 转换为 RGBA 模式，确保图片有 alpha 通道（透明度）
    img = img.convert("RGBA")

    # 获取图片数据
    data = img.getdata()

    # 创建一个新的数据列表
    new_data = []

    # 遍历所有像素
    for item in data:
        # item[:3] 是 RGB 值， item[3] 是 Alpha 值
        if item[:3] == color_to_make_transparent:  # 如果像素是要替换的颜色（例如白色）
            # 将该像素设置为完全透明
            new_data.append((255, 255, 255, 0))
        else:
            # 否则保留原来的像素
            new_data.append(item)

    # 更新图片数据
    img.putdata(new_data)

    # 保存处理后的图片
    img.save(output_image_path, "PNG")
    return output_image_path

from PIL import Image

from PIL import Image
import numpy as np


def change_background(image_path, new_background_color, output_path, bg_color=(255, 255, 255), threshold=60):
    """
    将图片背景替换为指定的颜色。

    参数:
    - image_path: 原始图片的路径
    - new_background_color: 新背景颜色 (R, G, B) 格式
    - output_path: 保存处理后图片的路径
    - bg_color: 需要替换的背景颜色，默认为白色 (255, 255, 255)
    - threshold: 颜色距离的阈值，决定像素是否属于背景色

    """
    # 打开图片并转换为 RGBA（带透明度通道）
    img = Image.open(image_path).convert("RGBA")
    img_array = np.array(img)  # 转换为 numpy 数组

    # 获取宽高尺寸
    width, height = img.size

    # 获取 RGBA 通道
    r, g, b, a = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2], img_array[:, :, 3]

    # 目标背景颜色
    bg_r, bg_g, bg_b = bg_color

    # 计算每个像素与背景色的颜色距离
    distance = np.sqrt((r - bg_r) ** 2 + (g - bg_g) ** 2 + (b - bg_b) ** 2)

    # 创建一个新的透明背景，保持图像主体部分
    mask = distance < threshold  # 判断哪些像素属于背景
    img_array[mask, 3] = 0  # 将背景部分的 alpha 通道设为 0（透明）

    # 将修改后的像素数据重新生成图片
    img_transparent = Image.fromarray(img_array, "RGBA")

    # 创建新背景（填充为指定的新背景颜色）
    new_background = Image.new("RGBA", (width, height), new_background_color + (255,))

    # 将原图粘贴到新背景图上，并使用 alpha 通道进行透明度合成
    new_background.paste(img_transparent, (0, 0), img_transparent)

    # 将 RGBA 转换为 RGB（如果需要保存为 JPG 或 GIF）
    rgb_img = new_background.convert("RGB")

    # 保存图片
    rgb_img.save(output_path)
    print(f"图片背景已成功更换，保存为: {output_path}")
    return output_path

if __name__ == '__main__':
    str = "1040g0083191r94p3ko605p10b5okc0bpho9o468!nd_dft_wlteh_jpg_3"
    masterImgList= [
        "https://sns-webpic-qc.xhscdn.com/202410171617/caee03d935847da9145f156e353927fa/1040g2sg3191r54bh4g805p10b5okc0bpsbcihio!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/3ee8f3314e876471bb2bab3afd040874/1040g2sg3191r54bh4g905p10b5okc0bpu4okhl8!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/030936060cbcac06ab5ed3a319ad8eb5/1040g2sg3191r54bh4gdg5p10b5okc0bps4ogol0!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/226b3265ac3c458e3f5fb845a1e541d3/1040g2sg3191r54bh4g8g5p10b5okc0bp4m2khdg!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/3bc1f35cdb49afcf946d949802a4875b/1040g2sg3191r54bh4gd05p10b5okc0bpou9d4io!nd_dft_wgth_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/b52b01f8bac821c02fd4e27ec2de0446/1040g2sg3191r54bh4g9g5p10b5okc0bpq46qcrg!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/5119eb123242805f20a5028f22151c4d/1040g2sg3191r54bh4g7g5p10b5okc0bpskumadg!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/ec3bdf949bc43a4ed5045156f120c8e4/1040g2sg3191r54bh4gc05p10b5okc0bpshen45o!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/95629b1b1ef04b86ad78b50540077cd0/1040g2sg3191r54bh4g705p10b5okc0bp6p3p2u0!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/18057b8c34a86f292eb7ff1301e4a24d/1040g2sg3191r54bh4gbg5p10b5okc0bpr5i0nng!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/89c9bb04f9ee40faea0b18921b9c31ac/1040g2sg3191r54bh4gag5p10b5okc0bpcoopov0!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/9bf83509e0bd9fa9a84aa4859dd07896/1040g0083191r94p3ko605p10b5okc0bpho9o468!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/f11368336b3503b0a3bc6a3d025f653e/1040g0083191r94p3ko5g5p10b5okc0bpu0cuehg!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/52902663a1cd04efbf5b6c26f551c304/1040g0083191r94p3ko505p10b5okc0bpcc02ju0!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/a41601a69157645b93868102b308c3fc/1040g0083191r94p3ko105p10b5okc0bpllkfrm0!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/b97b704810a845fb4f030c505911f361/1040g0083191r94p3ko305p10b5okc0bprjfaukg!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/f90e80443bfda49cf04faced8e5d705e/1040g0083191r94p3ko205p10b5okc0bpr9s24ao!nd_dft_wlteh_jpg_3",
        "https://sns-webpic-qc.xhscdn.com/202410171617/bc40c7a344abdd5067fbf21094541caa/1040g0083191r94p3ko4g5p10b5okc0bpt8luj58!nd_dft_wlteh_jpg_3"
    ]
    # general(path="D:\\img\\小狮子",dir=dir,
    #         title="可爱小狮子",firstWord="没有脑袋",guidanceWord=guidanceWord, thinkWord=thinkWord)
    # make_image_transparent("D:\\img\\cat\\target\\封面.png",output_image_path="D:\\img\\cat\\target\\封面02.png")
    # make_image_transparent("D:\\img\\cat\\target\\图标.png",output_image_path="D:\\img\\cat\\target\\图标01.png")
    change_background(image_path=r"D:\img\cat\target\致谢图.png",new_background_color=(255,235,205),output_path="test.png")
