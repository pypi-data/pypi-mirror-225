import requests
class obj:
    def __init__(
        self,
        headers:dict,      # 请求头
        data:dict,         # 请求参数
        url,                # 请求网址
    ):

        self.json_res = requests.get(url, headers=headers, data=data).json()
