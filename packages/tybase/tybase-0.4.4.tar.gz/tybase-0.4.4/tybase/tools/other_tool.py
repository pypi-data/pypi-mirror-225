def save_file_from_url(url, folder):
    """
    from tybase.tools.other_tool import save_file_from_url
    把文件保存到本地,并且返回本地的路径,如果文件已经存在,那么就不会再次下载,会有指定的文件夹

    :param url:  文件的url
    :param folder: 保存的文件夹
    :return: 路径
    """

    # 获取URL内容
    import requests
    import hashlib
    import os
    response = requests.get(url)

    # 创建md5对象
    md5 = hashlib.md5()
    md5.update(response.content)
    md5_hash = md5.hexdigest()

    # 获取文件扩展名
    _, ext = os.path.splitext(url)

    # 定义文件路径
    file_path = os.path.join(folder, md5_hash + ext)

    # 判断文件夹是否存在，如果不存在则创建
    os.makedirs(folder, exist_ok=True)

    # 判断文件是否已存在
    if not os.path.exists(file_path):
        # 如果文件不存在，写入文件
        with open(file_path, 'wb') as f:
            f.write(response.content)

    # 返回文件路径
    return file_path
