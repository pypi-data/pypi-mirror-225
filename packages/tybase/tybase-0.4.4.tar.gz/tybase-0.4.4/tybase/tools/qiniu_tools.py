import os
from dotenv import load_dotenv
from qiniu import Auth
import time
import uuid
from qiniu import BucketManager

load_dotenv()  # 从.env文件中加载环境变量


def RandomFileName():
    return str(int(time.time())) + "-" + str(uuid.uuid1())  # 取一个随机名气


class MyQiniu:
    def __init__(self, QINIU_AK, QINIU_SK, QINIU_BASE_URL, bucket):
        self.access_key, self.secret_key = QINIU_AK, QINIU_SK
        auth = Auth(QINIU_AK, QINIU_SK)
        self.bucket_manager = BucketManager(auth)
        self.QINIU_BASE_URL = QINIU_BASE_URL
        self.bucket = bucket

    def down_file(self, url, filename):
        ret, info = self.bucket_manager.fetch(url,
                                              self.bucket,
                                              filename)
        if info.status_code == 200:
            file_url = self.QINIU_BASE_URL + filename
            print(file_url)
            return file_url
        else:
            return "err"


def upload_to_qiniu(img_url, base_name="tests/"):
    QINIU_AK = os.getenv('QINIU_AK')
    QINIU_SK = os.getenv("QINIU_SK")
    QINIU_Bucket = os.getenv("QINIU_Bucket")
    QINIU_BASE_URL = os.getenv("QINIU_BASE_URL")
    qi = MyQiniu(QINIU_AK, QINIU_SK, QINIU_BASE_URL, QINIU_Bucket)
    # 远程图片
    qi.down_file(
        img_url,
        base_name + RandomFileName())


if __name__ == '__main__':
    upload_to_qiniu(
        "https://pics0.baidu.com/feed/0b55b319ebc4b745cf5f0eae5ea54a1b8b821520.jpeg@f_auto?token=45c40163494cc309c63c88b7aa86f6ed")
