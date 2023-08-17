"""
@Time : 2023/4/9 11:52
@Author : skyoceanchen
@TEL: 18916403796
@项目：JYairports
@File : img_operations.by
@PRODUCT_NAME :PyCharm
"""

import base64
from PIL import Image
import os


class ImageBasicOperation(object):
    def __init__(self, path):
        self.path = path
        self.img = Image.open(path)

    @staticmethod
    def base64_to_image(base64_data, img_file, ):
        with open(img_file, "wb") as f:
            f.write(base64_data)

    @staticmethod
    def image_to_base64(img_file, ):
        with open(img_file, "rb") as f:
            base64_data = base64.b64encode(f.read())
        return base64_data

    @staticmethod
    def base64_to_base64(base64_data):
        return base64_data

    # <editor-fold desc="gif转png或者jpg">
    @staticmethod
    def gif_to_png_jpg(gif_path, img_path):
        # im = Image.open("img/a.gif")
        # im.save("img/picture_temp.png")
        img = Image.open(gif_path)
        img.save(img_path)

    # </editor-fold>
    # <editor-fold desc="gif切片处理png">
    @staticmethod
    def gif_to_many_png(gif_path, img_dir):
        im = Image.open(gif_path)
        i = 0
        mypalette = im.getpalette()
        while 1:
            im.putpalette(mypalette)
            new_im = Image.new("RGBA", im.size)
            new_im.paste(im)
            new_im.save(img_dir + str(i) + '.png')
            i += 1
            im.seek(im.tell() + 1)

    # </editor-fold>
    # <editor-fold desc="png或者jpg转gif">
    @staticmethod
    def png_to_gif(gif_path, img_path):
        # im = Image.open("img/a.gif")
        # im.save("img/picture_temp.png")
        # 读取PNG格式图片
        image = Image.open(img_path)
        # 将PNG格式图片保存为GIF格式图片
        image.save(gif_path)

    # </editor-fold>
    # <editor-fold desc="多个png转gif">
    @staticmethod
    def many_png_to_gif(img_folder, gif_path):
        # 图像文件夹路径和输出 GIF 文件名
        # img_folder = '/path/to/images'
        # gif_filename = 'output.gif'
        # 获取所有图像文件名
        img_files = sorted((os.path.join(img_folder, f) for f in os.listdir(img_folder) if f.endswith('.png')))
        # 打开第一张图像
        img = Image.open(img_files[0])
        # 创建 GIF 对象，将第一张图像作为基准帧
        gif_frames = [img]
        # 逐一添加图像帧
        for filename in img_files[1:]:
            img = Image.open(filename)
            gif_frames.append(img)
        # 保存 GIF 动画
        gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:], duration=200, loop=0)

    # </editor-fold>
    # <editor-fold desc="jpg转png">
    @staticmethod
    def jpeg_to_png(jpg_path, img_path):
        # 转换为 PNG 格式
        img = Image.open(jpg_path)
        img = img.convert("RGBA")
        img.save(img_path, format='PNG')

    # </editor-fold>
    # <editor-fold desc="PNG-ico">仅支持png
    @staticmethod
    def png_to_ico(img_path, ico_path):
        img = Image.open(img_path)
        img = img.convert("RGBA")  # .resize((256, 256), Image.LANCZOS)
        img.save(ico_path, format='ICO')

    # </editor-fold>
    # <editor-fold desc="创建空白图片">
    @staticmethod
    def create_white_img(img_file, mode="RGB", size=(256, 256), color=(255, 255, 255)):
        """
            这个函数，需要三个参数。
        mode：图像的模式，一般都用RGB
        size：图像的尺寸，一个二位元组，（宽，高）
        color：如果没有给这个参数，默认是黑色背景。如果需要给出的话，根据图像的模式，给出不同通道数的值。如果是RGB图像，可以使用字符串直接表示
        我们知道，一般彩色图像，是三个通道的，红绿蓝三个通道。所以，我们如果要创建白色图像的话，第三个参数，用元组表示为(255, 255, 255)。
            :return:
        """
        img = Image.new(mode, size, color)
        img.save(img_file)

    # </editor-fold>
