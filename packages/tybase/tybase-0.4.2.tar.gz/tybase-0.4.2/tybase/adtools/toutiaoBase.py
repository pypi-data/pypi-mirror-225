from urllib.parse import urlencode, urlunparse
import loguru
import requests
import threading


class APIBaseClient:
    BASE_URL = "https://ad.oceanengine.com/open_api/"
    HEADERS = {"Content-Type": "application/json"}

    def __init__(self, email, token, ad_token_url):
        self.email = email
        self.token = token
        self.ad_token_url = ad_token_url
        self.base_token = self.get_base_token()

    @classmethod
    def _send_request_get(cls, path, params, access_token):
        # Building URL
        scheme, netloc = "https", "ad.oceanengine.com"
        query = urlencode(params or {})
        url = urlunparse((scheme, netloc, path, "", query, ""))
        # Sending request
        headers = {"Access-Token": access_token}
        rsp = requests.get(url, headers=headers)
        return rsp.json()

    def get_base_token(self):
        headers = {"TOKEN": self.token}
        url = f"https://api.bi.tayun365.com/ext/oe/token?account={self.email}"
        r = requests.get(url, headers=headers)
        return r.json()["data"]

    def get_access_token(self):
        """
        获取访问的token。

        :return: 访问的token列表 ( 一般是授权账户 )
        """
        uri = "oauth2/advertiser/get/"
        url = self.BASE_URL + uri
        data = {
            "access_token": self.base_token
        }
        rsp = requests.get(url, json=data)
        return rsp.json()["data"]["list"]


class TouTiaoAdvertiser(APIBaseClient):
    def __init__(self, email, token, ad_token_url):
        super().__init__(email, token, ad_token_url)

    def get_advertiser(self, advertiser_id):
        all_data = []
        page = 1
        loguru.logger.info("getting advertiser {} data".format(advertiser_id))
        while True:
            my_args = {"page": page, "page_size": 100, "cc_account_id": advertiser_id}
            response = self._send_request_get("/open_api/2/customer_center/advertiser/list/", my_args, self.base_token)
            loguru.logger.info("getting page {}".format(page))
            if response['code'] == 0:
                all_data.extend(response['data']['list'])

                if page >= response['data']['page_info']['total_page']:
                    break
                else:
                    page += 1
            else:
                print(f"Error occurred: {response['message']}")
                break
        return all_data

    # 第三步: 根据账户的列表,获取到每个授权账户的具体账户
    def get_all_advertisers(self):
        """
        获取所有的广告商。获取大账户下的所有子账户
        :return: 所有广告商的信息列表
        """
        all_as = self.get_access_token()
        as_data_list = []
        for as_info in all_as:
            advertiser_id = as_info["advertiser_id"]  # 先获取到大账户的id值
            as_data = self.get_advertiser(advertiser_id)  # 通过大账户的id,提取下面所有的字账户
            as_data_list += as_data
        return as_data_list

    # 第三步: 根据账户的列表,获取到每个授权账户的具体账户
    def get_all_advertisers_threading(self):
        """
        获取所有的广告商。获取大账户下的所有子账户
        :return: 所有广告商的信息列表
        """

        all_as = self.get_access_token()
        as_data_list = []  # 将这个变量初始化放到函数开始
        threads = []
        lock = threading.Lock()  # 创建一个锁对象来保护共享资源

        def thread_task(as_info):
            nonlocal as_data_list  # 声明这个变量是外部的，而不是新的局部变量
            advertiser_id = as_info["advertiser_id"]  # 先获取到大账户的id值
            as_data = self.get_advertiser(advertiser_id)  # 通过大账户的id,提取下面所有的字账户
            with lock:  # 保护下面的代码块，确保同一时间只有一个线程可以修改as_data_list
                as_data_list += as_data

        # 为每个授权账户创建并启动一个线程
        for as_info in all_as:
            t = threading.Thread(target=thread_task, args=(as_info,))
            t.start()
            threads.append(t)

        # 等待所有线程完成
        for t in threads:
            t.join()

        return as_data_list
