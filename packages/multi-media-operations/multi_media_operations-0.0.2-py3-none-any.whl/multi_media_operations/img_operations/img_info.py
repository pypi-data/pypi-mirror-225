"""
@Time : 2023/8/2 14:01 
@Author : skyoceanchen
@TEL: 18916403796
@项目：multi_media_operations
@File : img_info.by
@PRODUCT_NAME :PyCharm
"""
from PIL import Image
import cv2  # pip install opencv-python==4.4.0.46
import exifread  # exifread-3.0.0
from pyexiv2 import Image  # pyexiv2-2.8.2
import re


# 获取图片信息
class ImageInfo(object):
    def __init__(self, path):
        self.path = path
        self.img = Image.open(path)

    def size(self):
        return self.img.size

    def format(self):
        return self.img.format

    def width(self):
        return self.img.width

    def height(self):
        return self.img.height

    def shape(self):
        self.cv_img = cv2.imread(self.path)  # 读取图片信息
        return self.cv_img.shape  # [高|宽|像素值由三种原色构成]

    def change_img_size(self, size, to_path):
        """

        :param size: 尺寸 如(12840, 12370)
        :param to_path: 存储地址
        :return:
        """
        self.cv_img = cv2.imread(self.path)  # 读取图片信息
        # 如：要将一个图片变为32*32大小的
        # import cv2
        # img=cv2.imread('picture.jpg',cv2.IMREAD_COLOR)
        # img1 = cv2.imread('picture.jpg', 1)
        # img=cv2.imread('picture.jpg',cv2.IMREAD_GRAYSCALE)
        # img2 = cv2.imread('picture.jpg', 0)
        res = cv2.resize(self.cv_img, size, interpolation=cv2.INTER_CUBIC)  # (12840, 12370) 宽，长
        # da = imread(res)
        # print(da)
        # cv2.startWindowThread()  # 加在这个位置
        # cv2.imshow('iker', res)
        # cv2.imshow('image', image)
        cv2.imwrite(to_path, res)
        cv2.waitKey(0)
        # cv2.destoryAllWindows()

    def lati_long_date(self, data):
        """
        对经纬度进行处理，保留６位小数
        """
        # 删除左右括号，最后以逗号分隔为一个列表
        data_list_tmp = str(data).replace('[', '').replace(']', '').split(',')
        # 循环取出每个元素，删除元素两边的空格，得到一个新列表
        data_list = [date.strip() for date in data_list_tmp]
        # 替换秒的值
        data_tmp = data_list[-1].split('/')
        # 秒的值
        data_sec = int(data_tmp[0]) / int(data_tmp[1]) / 3600
        # 替换分的值
        data_tmp = data_list[-2]
        # 分的值
        data_minute = int(data_tmp) / 60
        # 度的值
        data_degree = int(data_list[0])
        # 由于高德API只能识别到小数点后的6位
        # 需要转换为浮点数，并保留为6位小数
        result = "%.6f" % (data_degree + data_minute + data_sec)
        return float(result)

    def info_exifread(self, stop_tag=exifread.DEFAULT_STOP_TAG, details=True, strict=True, debug=False,
                      truncate_tags=True, auto_seek=True):
        f = open(self.path, "rb")
        tags = exifread.process_file(f, stop_tag=stop_tag, details=details, strict=strict, debug=debug,
                                     truncate_tags=truncate_tags, auto_seek=auto_seek)
        f.close()
        # GPS信息
        img_info = {}
        for tag, IfdTag_obj in tags.items():
            print(tag, "*" * 10, IfdTag_obj, IfdTag_obj.values)
            # print(tag, "*" * 10, IfdTag_obj, type(IfdTag_obj), dir(IfdTag_obj))
            # print(IfdTag_obj.field_length)
            # print(IfdTag_obj.field_offset)
            # print(IfdTag_obj.field_type)
            # print(IfdTag_obj.printable)
            # print(IfdTag_obj.tag)
            if re.search("YResolution", tag):
                img_info["YResolution"] = IfdTag_obj.values[0] if IfdTag_obj.values else None  # Y 分辨率
            elif re.search("XResolution", tag):
                img_info["XResolution"] = IfdTag_obj.values[0] if IfdTag_obj.values else None  # X 分辨率
            elif re.search("ImageWidth", tag):
                img_info["ImageWidth"] = IfdTag_obj.values[0] if IfdTag_obj.values else None  # 图像宽度
            elif re.search("ImageLength", tag):
                img_info["ImageLength"] = IfdTag_obj.values[0] if IfdTag_obj.values else None  # 图像长度
            elif re.search("Model", tag):
                img_info["Model"] = IfdTag_obj.values if IfdTag_obj.values else None  # 图像来源
            elif re.search("Make", tag):
                img_info["Make"] = IfdTag_obj.values if IfdTag_obj.values else None  # 图像来源
            elif re.search("UserComment", tag):
                # img_info["UserComment"] = IfdTag_obj.values if IfdTag_obj.values else None  # 备注
                pass
            elif re.search("YCbCrPositioning", tag):
                img_info["YCbCrPositioning"] = IfdTag_obj.values[0] if IfdTag_obj.values else None  # Y Cb 铬定位
            elif "GPS GPSLatitude" == tag:
                img_info["GPSLatitude"] = IfdTag_obj.values if IfdTag_obj.values else None  # 全球定位系统纬度
                img_info["GPSLatitude"] = self.lati_long_date(img_info["GPSLatitude"])
            elif "GPS GPSLatitudeRef" == tag:
                img_info["GPSLatitudeRef"] = IfdTag_obj.values if IfdTag_obj.values else None  # 全球定位系统纬度参考
            elif "GPS GPSLongitude" == tag:
                img_info["GPSLongitude"] = IfdTag_obj.values if IfdTag_obj.values else None  # 全球定位系统纬度
                img_info["GPSLongitude"] = self.lati_long_date(img_info["GPSLongitude"])
            elif "GPS GPSLongitudeRef" == tag:
                img_info["GPSLongitudeRef"] = IfdTag_obj.values if IfdTag_obj.values else None  # 全球定位系统纬度参考
            elif re.search("GPSAltitude", tag):
                img_info["GPSAltitude"] = IfdTag_obj.values[0] if IfdTag_obj.values else None  # 全球定位系统高度
            # # 获取纬度信息
            # if re.match('GPS GPSLatitude', tag):
            #     try:
            #         match_result = re.match('\[(\w*), (\w*), (\w.*)/(\w.*)\]', str(value)).groups()
            #         img_info['纬度'] = str(int(match_result[0])) + " " + str(int(match_result[1])) + " " + str(
            #             int(match_result[2]) / int(match_result[3]))
            #     except:
            #         img_info['纬度'] = str(value)
            # # 获取纬度信息
            # elif re.match('GPS GPSLongitude', tag):
            #     try:
            #         match_result = re.match('\[(\w*), (\w*), (\w.*)/(\w.*)\]', str(value)).groups()
            #         img_info['经度'] = str(int(match_result[0])) + " " + str(int(match_result[1])) + " " + str(
            #             int(match_result[2]) / int(match_result[3]))
            #     except:
            #         img_info['经度'] = str(value)
            # # 获取高度
            # elif re.match('GPS GPSAltitude', tag):
            #     img_info['高度'] = str(value)
            # # 获取拍摄时间
            # elif re.match('EXIF DateTimeOriginal', tag):
            #     img_info['拍摄时间'] = str(value)
            # elif re.match('Image Software', tag):
            #     img_info['图像软件'] = str(value)
            # elif re.match('Image ExifOffset', tag):
            #     img_info['Image ExifOffset'] = str(value)
            # elif re.match('GPS Tag 0xEA1C', tag):
            #     img_info['GPS Tag 0xEA1C'] = str(value)
            # elif re.match('Image GPSInfo', tag):
            #     img_info['Image GPSInfo'] = str(value)
            # elif re.match('Image Padding', tag):
            #     img_info['Image Padding'] = str(value)
            # elif re.match('EXIF Padding', tag):
            #     img_info['EXIF Padding'] = str(value)
        return img_info


"""
图片元数据是什么？
图片元数据（metadata）是嵌入到图片文件中的一些标签。比较像文件属性，但是种类繁多。常见的几种标准有：
EXIF：通常被数码相机在拍摄照片时自动添加，比如相机型号、镜头、曝光、图片尺寸等信息。
IPTC：比如图片标题、关键字、说明、作者、版权等信息。
XMP：由Adobe公司制定标准，以XML格式保存。用PhotoShop等Adobe公司的软件制作的图片通常会携带这种信息。
Exiv2的网站：https://www.exiv2.org/index.html
Exiv2支持的元数据列表：https://www.exiv2.org/metadata.html
Exiv2支持的图片格式：https://dev.exiv2.org/projects/exiv2/wiki/Supported_image_formats
2009年，有team开始开发基于Exiv2的Python库——pyexiv2：https://launchpad.net/pyexiv2
但是2011年之后就停止更新了。
笔者没找到如今可用的版本，于是做了一个简单的基于Exiv2的Python库——还是叫pyexiv2，使用pip install pyexiv2即可安装。
详细说明请看github页面。https://github.com/LeoHsiao1/pyexiv2
中文教程 https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md
# https://blog.csdn.net/qq_35952638/article/details/95088227
"""


# 修改图片信息
class ModifyImageInfo(object):
    def __init__(self, path):
        self.path = path
        self.img = Image(self.path)

    # EXIF：通常被数码相机在拍摄照片时自动添加，比如相机型号、镜头、曝光、图片尺寸等信息。
    def read_exif(self):
        return self.img.read_exif()

    # IPTC：比如图片标题、关键字、说明、作者、版权等信息。
    def read_iptc(self):
        return self.img.read_iptc()

    # XMP：由Adobe公司制定标准，以XML格式保存。用PhotoShop等Adobe公司的软件制作的图片通常会携带这种信息。
    def read_xmp(self):
        return self.img.read_xmp()

    def modify_xmp(self, dic):
        self.img.modify_xmp(dic)
        return self.read_xmp()

    def modify_exif(self, dic):
        self.img.modify_exif(dic)
        return self.read_exif()

    def modify_iptc(self, dic):
        self.img.modify_iptc(dic)
        return self.read_iptc()

    def close(self):
        self.img.close()  # 操作完之后，记得关闭图片，释放内存
