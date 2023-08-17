import requests
class send_wx_msg:
    def __init__(
        self,
        port = 8055
    ):
        self.url = f'http://127.0.0.1:{port}/DaenWxHook/client/'



    def fetch_group(self,flush=False):
        '''
        获取群聊列表
        :param flush:
        :return:
        '''
        flush = True
        payload = {"type": "Q0006", "data": {"type": "2" if flush else "1"}}
        res = requests.post(self.url, json=payload)
        data = res.json()
        wxid2nick = {}      # {群ID:群名,...}
        nick2wxid = {}      # {群名:群ID,...}
        for row in data["result"]:
            print(row["wxid"],row["nick"])
            wxid2nick[row["wxid"]] = row["nick"]
            nick2wxid[row["nick"]] = row["wxid"]
        return wxid2nick, nick2wxid

    def fetch_firends(self,flush=False):
        payload = {"type": "Q0005", "data": {"type": "2" if flush else "1"}}
        res = requests.post(self.url, json=payload)
        data = res.json()
        wxid2nick = {}
        for row in data["result"]:
            wxid2nick[row["wxid"]] = (row["nick"], row["wxNum"])
        return wxid2nick

    def fetch_group_member(self,wxid):
        payload = {"type": "Q0008", "data": {"wxid": wxid}}
        res = requests.post(self.url, json=payload)
        data = res.json()
        return data["result"]

    def fetch_obj_info(self,wxid):
        payload = {"type": "Q0004", "data": {"wxid": wxid}}
        res = requests.post(self.url, json=payload)
        data = res.json()
        return data["result"]

    def send_mag(self,wxid, msg):
        payload = {"type": "Q0001", "data": {"wxid": wxid, "msg": msg}}
        res = requests.post(self.url, json=payload)
        data = res.json()
        return data["result"]



__author__ = '小小明'
__time__ = '2022/8/16'

import datetime
import json
import time

from flask import Flask, request, jsonify
send_wx_msg = send_wx_msg()


app = Flask(__name__)


def receive_group_msg(from_wxid, wxid, date, msg):
    if wxid:
        if wxid not in wxid2nick:
            row = send_wx_msg.fetch_obj_info(wxid)
            wxid2nick[wxid] = (row["nick"], row["wxNum"])
        nick, wxNum = wxid2nick[wxid]
        print(f"收到来自 {wxid2nick_group[from_wxid]} 群 {nick} 的消息，时间：{date}，微信号：{wxNum}，内容：{msg}")
    else:
        print(f"{wxid2nick_group[from_wxid]} 群{date} 发生{msg}")


def receive_friend_msg(from_wxid, date, msg):
    nick, wxNum = wxid2nick[from_wxid]
    print("收到私聊消息", nick, date, wxNum, msg)


@app.route('/wechat/', methods=['get', 'post'])
def wechat():
    data = json.loads(request.data.decode('u8'))
    date = datetime.datetime.fromtimestamp(int(data["timestamp"]) // 1000)

    # 收到消息
    if data['type'] == 'D0003':

        data = data['data']
        msg = data['msg']
        from_wxid = data['fromWxid']
        finalFromWxid = data['finalFromWxid']
        # 消息类型：1|文本 3|图片 34|语音 42|名片 43|视频 47|动态表情 48|地理位置 49|分享链接或附件 2001|红包 2002|小程序 2003|群邀请 10000|系统消息
        if data["msgType"] == 1:
            if "@chatroom" in from_wxid:
                if "暴富" in wxid2nick_group[from_wxid]:
                    receive_group_msg(from_wxid, finalFromWxid, date, msg)
            else:
                receive_friend_msg(from_wxid, date, msg)

    return jsonify({"code": 200, "msg": "ok", "timestamp": str(int(time.time()))})


if __name__ == '__main__':
    app.run(debug=True, port=8089)

'''
{'IdNo': 334285, 'CardType': 820, 'Title': 'MA01-ANSYS2020全套教程', 'RemainingCount': 1000, 'TotalCount': 1001, 'UsedCount': 1, 'CreateTime': '2022-08-04T11:00:04'}, 
{'IdNo': 334258, 'CardType': 820, 'Title': 'DA09-电工基础与电气自动化视频教程', 'RemainingCount': 1000, 'TotalCount': 1002, 'UsedCount': 2, 'CreateTime': '2022-08-04T10:26:35'}, {'IdNo': 333172, 'CardType': 820, 'Title': 'MA03-SolidWorks2020全套视频教程', 'RemainingCount': 999, 'TotalCount': 1000, 'UsedCount': 1, 'CreateTime': '2022-08-03T11:41:04'}, {'IdNo': 332826, 'CardType': 820, 'Title': 'MA02-SolidWorks2021+2022全套视频教程', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-08-02T16:25:51'}, {'IdNo': 322826, 'CardType': 820, 'Title': 'DA08-触摸屏教程[三菱西门子昆仑通态威纶通]', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-07-22T12:13:36'}, {'IdNo': 322575, 'CardType': 820, 'Title': 'MC01-MasterCAM2021/2022全套视频教程', 'RemainingCount': 994, 'TotalCount': 1067, 'UsedCount': 73, 'CreateTime': '2022-07-21T21:25:14'}, {'IdNo': 310662, 'CardType': 820, 'Title': 'DA07-全套西门子变频器视频教程', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-07-04T17:53:25'}, {'IdNo': 310661, 'CardType': 820, 'Title': 'DA06-全套西门子 S7-300 PLC视频教程', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-07-04T17:53:25'}, {'IdNo': 310660, 'CardType': 820, 'Title': 'DA05-全套西门子 S7-200smart PLC视频教程', 'RemainingCount': 1000, 'TotalCount': 1003, 'UsedCount': 3, 'CreateTime': '2022-07-04T17:53:25'}, {'IdNo': 310659, 'CardType': 820, 'Title': 'DA04-全套西门子 S7-200 PLC视频教程', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-07-04T17:53:25'}, {'IdNo': 310658, 'CardType': 820, 'Title': 'DA03-全套西门子 WinCC 视频教程', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-07-04T17:53:25'}, {'IdNo': 310657, 'CardType': 820, 'Title': 'DA02-全套西门子 S7-1500 PLC视频教程', 'RemainingCount': 1000, 'TotalCount': 1002, 'UsedCount': 2, 'CreateTime': '2022-07-04T17:53:25'}, {'IdNo': 310656, 'CardType': 820, 'Title': 'DA01-全套西门子 S7-1200 PLC视频教程', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-07-04T17:53:25'}, {'IdNo': 300542, 'CardType': 820, 'Title': '新MU10-UG10.0全套教程', 'RemainingCount': 900, 'TotalCount': 1158, 'UsedCount': 258, 'CreateTime': '2022-06-16T17:48:29'}, {'IdNo': 298766, 'CardType': 820, 'Title': 'DL82-eplan电气设计视频课程', 'RemainingCount': 998, 'TotalCount': 1011, 'UsedCount': 13, 'CreateTime': '2022-06-13T16:18:52'}, {'IdNo': 298765, 'CardType': 820, 'Title': 'DL81-变频器应用基础-高级模块视频课程', 'RemainingCount': 1000, 'TotalCount': 1001, 'UsedCount': 1, 'CreateTime': '2022-06-13T16:18:52'}, {'IdNo': 298764, 'CardType': 820, 'Title': 'DL80-电工基础视频课程', 'RemainingCount': 1000, 'TotalCount': 1001, 'UsedCount': 1, 'CreateTime': '2022-06-13T16:18:52'}, {'IdNo': 298763, 'CardType': 820, 'Title': 'DL59-工业机器人ABB视频课程', 'RemainingCount': 1000, 'TotalCount': 1013, 'UsedCount': 13, 'CreateTime': '2022-06-13T16:18:52'}, {'IdNo': 298762, 'CardType': 820, 'Title': 'DL58-威纶通触摸屏高级课程', 'RemainingCount': 1000, 'TotalCount': 1001, 'UsedCount': 1, 'CreateTime': '2022-06-13T16:18:52'}, {'IdNo': 298761, 'CardType': 820, 'Title': 'DL57-MCGS昆仑通态触摸屏应用视频课程', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-06-13T16:18:52'}, {'IdNo': 298760, 'CardType': 820, 'Title': 'DL56-新版永宏FBS-mc PLC视频', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-06-13T16:18:52'}, {'IdNo': 298752, 'CardType': 820, 'Title': 'DL55-新版信捷PLC视频教程', 'RemainingCount': 1000, 'TotalCount': 1001, 'UsedCount': 1, 'CreateTime': '2022-06-13T15:59:07'}, {'IdNo': 298751, 'CardType': 820, 'Title': 'DL54-新版威纶触摸屏视频教程', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-06-13T15:59:07'}, {'IdNo': 298750, 'CardType': 820, 'Title': 'DL53-新版台达PLC视频教程', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-06-13T15:59:07'}, {'IdNo': 298749, 'CardType': 820, 'Title': 'DL52-新版松下PLC视频教程', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-06-13T15:59:07'}, {'IdNo': 298748, 'CardType': 820, 'Title': 'DL51-新版欧姆龙CP1HPLC全套视频教程', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-06-13T15:59:07'}, {'IdNo': 284150, 'CardType': 820, 'Title': 'DL50-昆仑通态MCGS触摸屏精讲(10讲)2.5GB', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-05-24T15:21:06'}, {'IdNo': 283282, 'CardType': 820, 'Title': 'DL42-新版三菱触摸屏视频教程（29讲）1.5GB', 'RemainingCount': 1000, 'TotalCount': 1003, 'UsedCount': 3, 'CreateTime': '2022-05-23T16:56:14'}, {'IdNo': 283281, 'CardType': 820, 'Title': 'DL41-新版三菱Q系列PLC视频教程（248讲）35GB', 'RemainingCount': 1000, 'TotalCount': 1015, 'UsedCount': 15, 'CreateTime': '2022-05-23T16:56:14'}, {'IdNo': 283280, 'CardType': 820, 'Title': 'DL40-三菱FX3U系列plc精讲(40讲+240讲) 49GB', 'RemainingCount': 1000, 'TotalCount': 1001, 'UsedCount': 1, 'CreateTime': '2022-05-23T16:56:14'}, {'IdNo': 283279, 'CardType': 820, 'Title': 'DL32-S7-1200-1500应用视频课程（116讲）28G', 'RemainingCount': 1000, 'TotalCount': 1001, 'UsedCount': 1, 'CreateTime': '2022-05-23T16:55:41'}, {'IdNo': 283278, 'CardType': 820, 'Title': 'DL31-200smart编程入门班（综合应用）视频课程（32讲）6G', 'RemainingCount': 1000, 'TotalCount': 1001, 'UsedCount': 1, 'CreateTime': '2022-05-23T16:55:41'}, {'IdNo': 283277, 'CardType': 820, 'Title': 'DL30-西门子S7-1200PLC高级应用视频课程（126讲）12.49G', 'RemainingCount': 1000, 'TotalCount': 1002, 'UsedCount': 2, 'CreateTime': '2022-05-23T16:55:41'}, {'IdNo': 283276, 'CardType': 820, 'Title': 'DL29-S7-200SMART高级应用班智控视频课程（18讲', 'RemainingCount': 1000, 'TotalCount': 1005, 'UsedCount': 5, 'CreateTime': '2022-05-23T16:55:41'}, {'IdNo': 283275, 'CardType': 820, 'Title': 'DL28-wincc7.3应用视频课程（28讲）', 'RemainingCount': 1000, 'TotalCount': 1001, 'UsedCount': 1, 'CreateTime': '2022-05-23T16:55:41'}, {'IdNo': 283274, 'CardType': 820, 'Title': 'DL27-新版西门子Ⅴ90伺服驱系统视频教程', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-05-23T16:55:41'}, {'IdNo': 260056, 'CardType': 820, 'Title': 'DL26-西门子S7-200基础入门到精通', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-04-16T10:31:18'}, {'IdNo': 260055, 'CardType': 820, 'Title': 'DL25-新版西门子S7-200smart 入门到精通', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-04-16T10:31:18'}, {'IdNo': 260054, 'CardType': 820, 'Title': 'DL24-西门子S7-300系列PLC视频教程', 'RemainingCount': 1000, 'TotalCount': 1012, 'UsedCount': 12, 'CreateTime': '2022-04-16T10:31:18'}, {'IdNo': 260053, 'CardType': 820, 'Title': 'DL23-西门子S7-200SMART入门到精通', 'RemainingCount': 1000, 'TotalCount': 1003, 'UsedCount': 3, 'CreateTime': '2022-04-16T10:30:45'}, {'IdNo': 260052, 'CardType': 820, 'Title': 'DL22-西门子S7-300PLC入门到精通', 'RemainingCount': 1000, 'TotalCount': 1001, 'UsedCount': 1, 'CreateTime': '2022-04-16T10:30:45'}, {'IdNo': 260051, 'CardType': 820, 'Title': 'DL20-S7-1200PLC博途', 'RemainingCount': 1000, 'TotalCount': 1002, 'UsedCount': 2, 'CreateTime': '2022-04-16T10:30:45'}, {'IdNo': 260050, 'CardType': 820, 'Title': 'DL19-基于西门子wincc7.5应用教程', 'RemainingCount': 1000, 'TotalCount': 1002, 'UsedCount': 2, 'CreateTime': '2022-04-16T10:30:45'}, {'IdNo': 260049, 'CardType': 820, 'Title': 'DL18-基于西门子触摸屏wincc flexible视频教程', 'RemainingCount': 1000, 'TotalCount': 1000, 'UsedCount': 0, 'CreateTime': '2022-04-16T10:30:45'}, {'IdNo': 260048, 'CardType': 820, 'Title': 'DL17-基于 西门子S7-300PLC 视频教程', 'RemainingCount': 1000, 'TotalCount': 1001, 'UsedCount': 1, 'CreateTime': '2022-04-16T10:30:45'}, {'IdNo': 260047, 'CardType': 820, 'Title': 'DL16-基于西门子S7-1200 PLC的博途触摸屏视频教程', 'RemainingCount': 1000, 'TotalCount': 1002, 'UsedCount': 2, 'CreateTime': '2022-04-16T10:30:45'}, {'IdNo': 260045, 'CardType': 820, 'Title': 'DL15-基于西门子S7-1500 PLC博途触摸屏视频', 'RemainingCount': 1000, 'TotalCount': 1001, 'UsedCount': 1, 'CreateTime': '2022-04-16T10:27:51'}, {'IdNo': 260044, 'CardType': 820, 'Title': 'DL14-新版西门子smart200视频教程', 'RemainingCount': 1000, 'TotalCount': 1001, 'UsedCount': 1, 'CreateTime': '2022-04-16T10:27:51'}, {'IdNo': 260043, 'CardType': 820, 'Title': 'DL13-基于西门子S7-200PLC视频教程', 'RemainingCount': 1000, 'TotalCount': 1004, 'UsedCount': 4, 'CreateTime': '2022-04-16T10:27:51'}, {'IdNo': 260042, 'CardType': 820, 'Title': 'DL12-基于西门子WinCC7.4版本视频教程', 'RemainingCount': 1000, 'TotalCount': 1002, 'UsedCount': 2, 'CreateTime': '2022-04-16T10:27:51'}], 'TotalCount': 123, 'PageNo': 1, 'PageSize': 50}, 'Error_Code': 0, 'Error_Msg': '', 'AllowRetry': None, 'RequestId': '2022112418493314504146'}


'''