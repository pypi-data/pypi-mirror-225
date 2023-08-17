"""
@Time : 2023/8/2 17:58 
@Author : skyoceanchen
@TEL: 18916403796
@项目：multi_media_operations
@File : other.by
@PRODUCT_NAME :PyCharm
"""
import base64
from PIL import Image
import os
import sys

from file_operations.file_operation import FileOperation
import numpy as np


class ImageMidOperation(object):
    def __init__(self, path=None):
        self.path = path
        self.get_img()

    def get_img(self):
        if os.path.exists(self.path):
            self.img = Image.open(self.path)

    # <editor-fold desc="图片转字符画">
    def get_char(self, r, g, b, alpha=256):
        char = list('M3NB6Q#OC?7>!:–;. ')
        if alpha == 0:
            return ' '
        grey = (2126 * r + 7152 * g + 722 * b) / 10000

        char_idx = int((grey / (alpha + 1.0)) * len(char))
        return char[char_idx]

    def img_to_char_draw(self, img, width=100):
        text = ''
        width1, height1 = img.size
        height = int(height1 / (width1 / width))
        self.img = self.img.resize((width, height), Image.NEAREST)
        for i in range(height):
            for j in range(width):
                text += self.get_char(*self.img.getpixel((j, i)))
            text += '\n'
        return text

    # </editor-fold>
    # <editor-fold desc="将图片填充为正方形">
    def fill_image(self, col=3, row=3, save_path=None):
        width, height = self.img.size
        # 选取长和宽中较大值作为新图片的
        new_image_width = new_image_height = width if width > height else height
        if col > row:
            new_image_width = int(new_image_width * col / row)
        else:
            new_image_height = int(new_image_height * row / col)
        # 生成新图片[白底]
        print(new_image_width, new_image_height, )
        new_image = Image.new(self.img.mode, (new_image_width, new_image_height), color='white')
        # 将之前的图粘贴在新图上，居中
        new_image.paste(self.img,
                        (int((new_image_width - width) / 2),
                         int((new_image_height - height) / 2),
                         )
                        )
        if save_path:
            new_image.save(save_path)
        self.img = new_image

    # </editor-fold>
    # <editor-fold desc="切割图片">
    def cut_image(self, to_dir='', col=3, row=3, ):
        self.fill_image(col=col, row=row)
        width, height = self.img.size
        item_width = int(width / col)
        item_height = int(height / row)
        box_list = []
        # (left, upper, right, lower)
        for i in range(0, row):
            for j in range(0, col):
                box = (j * item_width, i * item_height, (j + 1) * item_width, (i + 1) * item_height)
                box_list.append(box)
        image_list = [self.img.crop(box) for box in box_list]
        index = 1
        for image in image_list:
            image.save(os.path.join(to_dir, str(index) + '.png'), 'PNG')
            index += 1
        return True

    # </editor-fold>
    # <editor-fold desc="把切割的图片进行拼起来">
    def compose_image(self, img_dir, save_path, row, col, size=256, endswith="png"):
        # 获取图片集地址下的所有图片名称
        # filelist = os.listdir(img_dir)
        filelist = FileOperation.file_sort_absolute(img_dir, endswith)
        image_names = np.array([file for file in filelist if file.endswith('.png')], dtype=object)
        to_image = Image.new('RGB', (col * size, row * size))  # 创建一个新图
        # to_image.show()
        # 循环遍历，把每张图片按顺序粘贴到对应位置上
        for y in range(1, row + 1):
            for x in range(1, col + 1):
                from_image = Image.open(image_names[col * (y - 1) + x - 1]).resize(
                    (size, size), Image.LANCZOS)
                to_image.paste(from_image, ((x - 1) * size, (y - 1) * size))
        return to_image.save(save_path)

    # </editor-fold>

    def img_light(self, light=0.5, save_path=None):
        # multiply each pixel by 0.9 (makes the image darker)
        # works best with .jpg and .png files, darker < 1.0 < lighter
        # (.bmp and .gif files give goofy results)
        # note that lambda is akin to a one-line function
        self.img = self.img.point(lambda p: p * light)
        # brings up the modified image in a viewer, simply saves the image as
        # a bitmap to a temporary file and calls viewer associated with .bmp
        # make certain you have associated an image viewer with this file type
        # save modified image to working folder as Audi2.jpg
        if save_path:
            self.img.save(save_path)
        else:
            self.img.save(self.path)
