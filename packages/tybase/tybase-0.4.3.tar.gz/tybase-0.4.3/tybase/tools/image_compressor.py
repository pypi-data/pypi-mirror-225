import cv2
from PIL import Image
import numpy as np


class SmartImageCompressor:
    def __init__(self, png_quality=85, jpg_quality=60, default_quality=75):
        """
        from tybase.tools.image_compressor import SmartImageCompressor
        初始化 SmartImageCompressor 类。

        参数:
        - png_quality (int): PNG 图像的压缩质量，默认为 85。
        - jpg_quality (int): JPEG 图像的压缩质量，默认为 60。
        - default_quality (int): 其他类型图像的默认压缩质量，默认为 75。

        示例:
        compressor = SmartImageCompressor(png_quality=90, jpg_quality=65)
        """
        self.png_quality = png_quality
        self.jpg_quality = jpg_quality
        self.default_quality = default_quality

    def compress_from_path(self, input_path, output_path):
        """
        从给定的文件路径读取图像，进行压缩并保存到指定的输出路径。

        参数:
        - input_path (str): 要压缩的图像文件的路径。
        - output_path (str): 压缩后的图像保存的路径。

        示例:
        input_file = '3.png'
        output_file = 'compressed_image.jpg'
        compressor.compress_from_path(input_file, output_file)
        """
        with Image.open(input_path) as img:
            img_format = img.format

            if img_format == "PNG":
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                quality = self.png_quality
            elif img_format in ["JPEG", "JPG"]:
                quality = self.jpg_quality
            else:
                quality = self.default_quality

            img.save(output_path, 'JPEG', quality=quality, optimize=True)

    def compress_from_cv2(self, cv2_img, output_path=None):
        """
        从给定的 OpenCV 图像对象进行压缩。可以选择保存到文件或返回压缩后的图像对象。

        参数:
        - cv2_img (array): OpenCV 格式的图像对象。
        - output_path (str, 可选): 压缩后的图像保存的路径。如果不提供，则不会保存到文件。

        返回:
        - array: 压缩后的 OpenCV 格式的图像对象。

        示例:
        cv2_img = cv2.imread('3.png')
        output_file = 'compressed_image.jpg'
        compressed_img = compressor.compress_from_cv2(cv2_img, output_file)
        """
        img = Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
        img_mode = img.mode

        if img_mode == 'RGBA':
            img = img.convert('RGB')
            quality = self.png_quality
        elif img_mode == "RGB":
            quality = self.jpg_quality
        else:
            quality = self.default_quality

        if output_path:
            img.save(output_path, 'JPEG', quality=quality, optimize=True)

        compressed_cv2_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return compressed_cv2_img
