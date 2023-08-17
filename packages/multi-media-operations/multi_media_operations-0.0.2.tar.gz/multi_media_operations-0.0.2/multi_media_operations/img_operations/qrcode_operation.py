"""
@Time : 2023/8/2 13:24 
@Author : skyoceanchen
@TEL: 18916403796
@项目：multi_media_operations
@File : qrcode_operations.by
@PRODUCT_NAME :PyCharm
"""
import qrcode
from PIL import Image


class QRCodeOperations(object):
    @staticmethod
    def basic_qrcode(text, file_path):
        # text = r"http://139.224.52.79:8089/media/report\\embed_report\\1648622788.pdf"  # 设置URL必须添加http://
        img = qrcode.make(text)
        img.save(file_path)  # 保存图片至本地目录，可以设定路径

    @staticmethod
    def qrcode(text, file_path, version=1, box_size=10, border=4, error_correction=qrcode.constants.ERROR_CORRECT_H, ):
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border
        )
        # 传入数据
        qr.add_data(text)
        qr.make(fit=True)
        # 生成二维码
        img = qr.make_image()
        # 保存二维码
        img.save(file_path)

    @staticmethod
    def logo_qrcode(text, file_path, img_path=None, version=1, fill_color="green", back_color="white", box_size=5,
                    border=4, factor=6, error_correction=qrcode.constants.ERROR_CORRECT_H, ):
        """
        :param text: 文本内容
        :param to_path: 输出文件地址
        :param img_path: 添加logo图片地址
        :param version: 版本
        :param box_size: 二维码大小
        :param border: 边框大修
        :param error_correction:
        :param fill_color: 填充颜色
        :param back_color: 背景颜色
        :param factor: 参数设置logo的大小
        :return:
        """
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        # 添加数据
        qr.add_data(text)
        # 填充数据
        qr.make(fit=True)
        # 生成图片
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        # 添加logo，打开logo照片
        # icon = Image.open("test.png")
        if img_path:
            icon = Image.open(img_path)
            # 获取图片的宽高
            img_w, img_h = img.size
            size_w = int(img_w / factor)
            size_h = int(img_h / factor)
            icon_w, icon_h = icon.size
            if icon_w > size_w:
                icon_w = size_w
            if icon_h > size_h:
                icon_h = size_h
            # 重新设置logo的尺寸
            icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
            # 得到画图的x，y坐标，居中显示
            w = int((img_w - icon_w) / 2)
            h = int((img_h - icon_h) / 2)
            # 黏贴logo照
            img.paste(icon, (w, h), mask=None)
        img.save(file_path)
        return img
