
"""
创建此对象后，先  .start()
数据格式
# 房间信息
rooms_info = {
    "upd_time": 更新时间
    "room_id": {
        "name": "",             # 房间名,
        state:                  #  L: 锁房 False:空房
        "renter_in": "mid",       # 订房码-入住中或新客人
        "renter_out": "mid",      # 订房码-今离客人
        # 保洁任务
        "clean_task": {
            "task_type": "taskType",     # 任务类型 C 有清洁任务
            "state_name": "stateName",   # 清洁任务状态名  未开始,进行中,已打扫
            "remark"： remark           # 任务备注
            "empl_name": empl_name      # 创建人
        }
    },...
}
# 客户信息（今天开始后2个月的所有客户信息）
renter_info = {
    "upd_time": 更新时间
    phone = [mid,mid,...]                    # 订房码
    mid = {
        wxid = wxid                             # 微信号
        name = infoRealname                     # 客户名,
        phone = infoPhone                       # 入住人手机号
        remark = infoRemark                     # 备注
        room_id = item["roomId"]                 # 房间ID
        date_in = checkIn                       # 入住开始日期 2023-06-22
        date_out = checkOut                     # 入住结束日期
        mid = id                                # 订房码，用于发短信
        cid = contractId                        # 订单id
        price: item["pricePaid"]                # 实收款
        price_agent = item["priceAgent"]        # 佣金
        state = state                           # 今日-入住状态
        # L: 锁房, P: "待入住", S: "入住中", E:"已退房", B: "已取消", D: "已取消",
        tag = tag                               # 标签 钟点房...
    },...
}
# 本月房态
state_month = {
    "upd_time": 更新时间
    "2023-06-01": {
        "room_id": {
            roomName = ,   # 房间名
            modId = ,      # 订房码
            state = ,      # 入住状态      False 未租此房, L 预定
            price =        # 实收价格
        },...
    },...
}
# 订单信息
contract_log = {
    pk = {          # 编号
        "mid": mid,         # 订房码
        "tm": tm,           # 订单时间
        "room": room,       # 房间号
        "date": date,       # 入住日期
        "name": name,       # 姓名
        "phone": phone,     # 手机
        "price": price,     # 价格
    }
}

https://open.feishu.cn/api-explorer/cli_a42d052d8cb01013
123.128.40.7

"""
import datetime

"""


"""
import requests
import time
import json
# 飞书多维表格
class Fs:
    def __init__(self):
        """
        关于多维表格的设置：1. 分享按钮/组织内获得链接的人可编辑 2. 高级权限/关闭
        """
        self.start_time = time.time()

        self.app_id = "cli_a42d052d8cb01013"
        self.app_secret = "X3jpJ2NOps7JmH0bvY2V0b1Hyia7zL2v"

        self.app_token = "Wt0GbvW3XaOkdPslPRJcpOZEnSe"
        self.table_id = "tblmUkx7vjMUw33G"

        self.app_access_token = ""
        self.tenant_access_token = ""
        self.get_access_token()

    # 获取 access_token
    def get_access_token(self):
        run_time = time.time() - self.start_time
        if self.app_access_token and self.tenant_access_token and run_time < 600:
            return
        self.start_time = time.time()

        payload = json.dumps({
            "app_id": self.app_id,
            "app_secret": self.app_secret
        })
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }

        url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
        res = requests.post(url, headers=headers, data=payload)
        self.app_access_token = res.json().get("app_access_token")

        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        res = requests.post(url, headers=headers, data=payload)
        self.tenant_access_token = res.json().get("tenant_access_token")

    def find_sdf(self, room_name, typ, days, page_size=1):
        """
        days: 0 表示今天， 1 昨天  不能是负数
        page_size: 获取条数
        """
        self.get_access_token()
        days = f"= TODAY()-{days}" if days else f"> TODAY()-1"
        filter = f'AND(CurrentValue.[房号] = "{room_name}",CurrentValue.[日期] {days},CurrentValue.[分类] = "{typ}")'
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records?filter={filter}&page_size={page_size}"
        payload = ''

        headers = {
            'Authorization': f'Bearer {self.tenant_access_token}'
        }
        res = requests.get(url, headers=headers, data=payload)
        data = res.json().get("data")
        items = data.get("items") if data else []
        items = items if items else []
        for item in items:
            print(item)
        return items

    # 新增水电记录
    def add_sdf(self, typ, room_name, lj):
        try:
            lj = float(lj)
        except:
            lj = 0
        self.get_access_token()
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        payload = json.dumps({
            "fields": {
                "日期": int(time.time()*1000),
                "分类": typ,
                "房号": room_name,
                "累计": lj,
            }
        })

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {self.tenant_access_token}'
        }
        # headers["Authorization"] = "Bearer u-cHZWrzjUJ0ibWvijCThvBA1hmNmRgh11UMG040.82fjr"
        response = requests.request("POST", url, headers=headers, data=payload)

print()

exit()
fs = Fs()
fs.find_sdf("4-1502", "电", 1)