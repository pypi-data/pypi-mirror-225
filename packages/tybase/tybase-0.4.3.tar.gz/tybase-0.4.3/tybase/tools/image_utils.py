# 获取图片的md5文件
import hashlib
import os
import shutil
from urllib.parse import urlparse

import cv2
import loguru
import numpy as np
import requests


def read_image(image_path_or_url: str):
    """
    # 读取图片的功能,可以从本地读取,也可以从url读取
    :param image_path_or_url: 图片地址或是url
    :return: numpy数组
    """
    parsed_url = urlparse(image_path_or_url)
    if bool(parsed_url.netloc) and bool(parsed_url.scheme):  # Check if the input is a url
        response = requests.get(image_path_or_url)
        image = np.asarray(bytearray(response.content), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    else:  # Local file path
        image = cv2.imread(image_path_or_url)
    return image


def resize_image(image: np.ndarray, max_dimension: int = 512) -> np.ndarray:
    """
    # 重置图片大小,把大图变小图
    :param image: 图片的数组
    :param max_dimension: 图片压缩的最大尺寸
    :return: np数组
    """
    scale_factor = max_dimension / max(image.shape)
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized_image


def save_image(image: np.ndarray, output_path: str) -> None:
    cv2.imwrite(output_path, image)


def crop_image_from_url(url: str, save_path: str, max_dimension: int = 512):
    """
    # 从url中裁剪图片
    :param url: 图片的url
    :param max_dimension: 图片的最大尺寸
    :param save_loc: 保存图片的路径
    :return: 返回一个图片的地址
    """
    image = read_image(url)

    if not max_dimension:
        # 如果传递的是0,那么就不需要裁剪直接返回
        save_image(image, save_path)

    if max(image.shape[:2]) <= max_dimension:
        loguru.logger.info("不需要裁剪,直接保存")
        save_image(image, save_path)
    else:
        resized_image = resize_image(image, max_dimension)
        save_image(resized_image, save_path)
    return save_path


def get_md5(img, ext='.jpg'):
    # Convert image to byte array
    is_success, im_buf_arr = cv2.imencode(ext, img)
    byte_im = im_buf_arr.tobytes()

    # Compute MD5
    md5 = hashlib.md5()
    md5.update(byte_im)

    return md5.hexdigest()


def url_to_md5(url):
    # from tybase.tools.image_utils import url_to_md5
    # 对url的md5进行加密
    # 获取文件名（不包括格式）
    filename = url.split("/")[-1].split(".")[0]
    # 获取格式
    ext = url.split(".")[-1]

    # 对文件名进行MD5加密
    m = hashlib.md5()
    m.update(filename.encode('utf-8'))
    md5 = m.hexdigest()
    # 返回MD5哈希值与格式的组合
    return "{}.{}".format(md5, ext)


def url_to_md5_without_ext(url):
    """
    from tybase.tools.image_utils import url_to_md5_without_ext
    对url进行MD5加密，返回不包含扩展名的MD5值。
    """
    # 获取文件名（不包括格式）
    filename = url.split("/")[-1].split(".")[0]

    # 对文件名进行MD5加密
    m = hashlib.md5()
    m.update(filename.encode('utf-8'))
    return m.hexdigest()


def delete_file_or_directory(path):
    """
    from tybase.tools.image_utils import delete_file_or_directory
    删除文件或者文件夹
    :param path: 一个文件或者文件夹的路径
    :return: None
    """
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            print(f"错误: {path} 不是一个文件也不是一个文件夹")
    except FileNotFoundError:
        print(f"警告: {path} 不存在")





if __name__ == '__main__':
    pass
    # 图片裁剪
    # crop_image_from_url
    # get_md5 获取md5
