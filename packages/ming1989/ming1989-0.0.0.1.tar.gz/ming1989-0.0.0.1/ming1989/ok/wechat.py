import atexit

import pandas
from bs4 import BeautifulSoup
import requests
import datetime
import time
import pandas as pd
import re
import json
from xml.dom.minidom import parseString
import xml.dom.minidom
from lib.flask import Flask, request
import os
from pathlib import Path

class Wechat:
    def __init__(
            self,
            port1=8089,
            port2=8055,
            debug=False
    ):
        self.port1 = port1
        self.debug = debug

        self.url = f'http://127.0.0.1:{port2}/DaenWxHook/client/'
        self.root_wxid = None       # 已登录的微信主账号ID

        self.friends_data = None
        self.group_data = None

        self.data_path_root = 'data/'             # 数据根目录
        self.data_path = f'{self.data_path_root}wechat_data.csv'   # 数据路径
        self.data_cols = [              # 数字字段名
            'wxid',                     # 好友或群ID
            'type',                     # str: 1 好友, 2 群, 3 公众号
            'wxNum',
            'nick',
            'remark',
            'nickBrief'
            'nickWhole',
            'remarkBrief',
            'remarkWhole',
            'enBrief',
            'enWhole',
            'v3',
            'sign',
            'country',
            'province',
            'city',
            'momentsBackgroudImgUrl',
            'avatarMinUrl',
            'avatarMaxUrl',
            'sex',
            'memberNum',
        ]               # 数据字段名
        self.data = None
        self.load_data()

        # 注册程序退出前要执行的函数.
        # 程序崩溃和外部中断都会执行。
        atexit.register(self.save_data)

    # 初始化数据 - 好友和群组数据
    def load_data(self):
        if self.data is None:
            if not os.path.exists(self.data_path_root):
                os.makedirs(self.data_path_root)
            # 没有数据文件，则创建数据
            self.data = pd.DataFrame(columns=self.data_cols)
            # 保存数据文件
            self.data.to_csv(self.data_path)

        # 设置索引
        # 用空字符替换所有缺省值
        self.data.fillna("", inplace=True)

        self.upd_group_data()
        self.upd_friends_data()

    # 将数据保存到csv文件
    def save_data(self):
        # 设置索引
        self.data.fillna("", inplace=True)         # 替换空值
        self.data.to_csv(self.data_path)

    def run(self,
            wxfunc  # 函数，处理接收到的数据
            ):
        app = Flask(__name__)

        @app.route('/wechat/', methods=['get', 'post'])
        def wechat():
            data = request.stream.read()
            data = data.decode('utf-8')
            data = json.loads(data, strict=False)
            # data = json.loads(request.data.decode('u8'))
            # date = datetime.datetime.fromtimestamp(int(data["timestamp"]) // 1000)

            rs_data = self.receive_msg(data, debug=True)
            wxfunc(self, rs_data)
            # 需要任意返回点东西
            return "-"
            # return jsonify({"code": 200, "msg": "ok", "timestamp": str(int(time.time()))})

        app.run(port=self.port1)

    # 接收分析事件
    def receive_msg(self, data, debug=None):
        '''
            用途：通过data['type']判断是属于什么事件 D0001 注入成功;D0002 登录成功;D0003 收到消息;D0004 转账事件;D0005 撤回事件;D0006 好友请求
                根据不同的事件，返回不同的参数
            返回：dic 所有事件的所有参数，只有真实的事件才有真实的数据，其它的事件参数都为None
                返回的参数都是后面接口要用到的
        '''

        content = {'title': '解析微信事件'}

        # 收到消息
        self.root_wxid = data.get('wxid', self.root_wxid)
        m_type = data.get("type")
        m_data = data["data"]
        m_type_dict = {
            "D0001": "等待登录",
            "D0002": "登录成功",
            "D0003": "收到消息",
            "D0004": "转账事件",
            "D0005": "撤回事件",
            "D0006": "好友请求",
        }
        content['tips'] = "----"

        res_type = m_type
        # D0001 事件分析————注入成功
        if m_type == "D0001":
            content['tips'] = "检测到微信启动，等待登录..."

        # D0002 事件分析————登录成功
        elif m_type == "D0002":
            content['tips'] = "微信登录成功..."

        # D0003 事件分析————收到消息
        elif m_type == "D0003":
            # 消息示例
            """
            {
                'type': 'D0003',
                'des': '收到消息', 
                'data': {
                    'timeStamp': '1687616564770',
                    'fromType': 1, 
                    'msgType': 10000, 
                    'msgSource': 0, 
                    'fromWxid': 'wxid_9ctpb0b5y95a22', 
                    'finalFromWxid': '', 
                    'atWxidList': [],
                    'silence': 0, 
                    'membercount': 0,
                    'signature': 'v1_nk8lhUDB', 
                    'msg': '你已添加了嘿，芸芸众生，现在可以开始聊天了。', 
                    'msgBase64': '5L2g5bey5re75Yqg5LqG5Zi/77yM6Iq46Iq45LyX55Sf77yM546w5Zyo5Y+v5Lul5byA5aeL6IGK5aSp5LqG44CC'
                },
                'timestamp': '1687616564782', 
                'wxid': 'wxid_mh451po49x8u22', 
                'port': 8055, 
                'pid': 12104,
                'flag': ''
            }
            """

            from_type = m_data["fromType"]                # 来源类型：1|私聊 2|群聊 3|公众号
            # 消息类型：1|文本 3|图片 34|语音 42|名片 43|视频 47|动态表情 48|地理位置 49|分享链接或附件
            # 2001|红包 2002|小程序 2003|群邀请 10000|系统消息|已添加好友，现在可以聊天了
            msg_type = m_data["msgType"]
            msg_source = m_data["msgSource"]              # 消息来源：0|别人发送 1|自己手机发送
            from_wxid = m_data["fromWxid"]                # fromType=1 好友wxid,fromType=2 群wxid, fromType=3 公众号wxid
            final_from_wxid = m_data["finalFromWxid"]     # 仅fromType=2时有效，为群内发言人wxid
            at_wxid_list = m_data["atWxidList"]           # 仅fromType=2，且msgSource=0时有效，为消息中艾特人wxid列表
            silence = m_data["silence"]                   # 仅fromType=2时有效，0
            member_count = m_data["membercount"]          # 仅fromType=2时有效，群成员数量
            signature = m_data["signature"]               # 消息签名
            msg = m_data["msg"]                           # 消息内容
            msg_base64 = m_data["msgBase64"]              # 消息内容的Base64编码

            # 对方通过了我的好友请求
            if from_type == 1 and msg_type == 1 and msg_source == 0 and '我通过了你的朋友验证' in msg:
                i_data = self.fetch_obj_info(wxid=from_wxid)
                self.upd_data_to_df(i_data)

            # 我同意了对方的好友请求
            if msg_type == 10000 and from_type == 1 and "现在可以开始聊天了" in msg:
                i_data = self.fetch_obj_info(wxid=from_wxid)
                self.upd_data_to_df(i_data)

            if from_wxid == 'newsapp':
                m_data["msg"] = '腾讯新闻'
            m_data["msgBase64"] = "太长了..."

            if '<?xml' in msg:
                try:
                    # 打开xml文档
                    xml_item = parseString(msg)
                    # 得到文档元素对象
                    xml_item = xml_item.documentElement
                    des_item = xml_item.getElementsByTagName("des")
                    msg = des_item[0].childNodes[0].data if des_item else ""
                    m_data["msg"] = msg
                except:
                    soup = BeautifulSoup(msg, 'html.parser')
                    text = soup.get_text()
                    text = text.replace(" ", "").replace("\n\n", "").replace("\n\n", "").replace("\n\n", "")
                    print('xml消息解析失败')
                    print(text)
                    print('#'*100)

            from_type_dict = {
                1: "私聊",
                2: "群聊",
                3: "公众号",
            }
            # 消息类型：1|文本 3|图片 34|语音 42|名片 43|视频 47|动态表情 48|地理位置
            # 49|分享链接或附件 2001|红包 2002|小程序 2003|群邀请 10000|系统消息|已添加好友，现在可以聊天了
            msg_type_dict = {
                1: "文本",
                3: "图片",
                34: "语音",
                42: "名片",
                43: "视频",
                47: "动态表情",
                48: "地理位置",
                49: "分享链接或附件",
                2001: "红包",
                2002: "小程序",
                2003: "群邀请",
                10000: "系统消息",
            }
            msg_source_dict = {
                0: "别人发送",
                1: "自己手机发送",
            }

            res_type = f"{m_type}-{from_type}-{msg_type}-{msg_source}"
            msg0 = re.sub(r"\s", '', msg)[:100]
            content['tips'] = f"{m_type_dict[m_type]}|" \
                              f"{from_type_dict[from_type]}|" \
                              f"{msg_type_dict[msg_type]}|" \
                              f"{msg_source_dict[msg_source]}|" \
                              f"{msg0}......"

        # D0004 事件分析————转账事件
        elif m_type == "D0004":
            from_wxid = m_data['fromWxid']             # 对方wxid
            msg_source = m_data['msgSource']           # 1|收到转账 2|对方接收转账 3|发出转账 4|自己接收转账 5|对方退还 6|自己退还
            trans_type = m_data['transType']           # 1|即时到账 2|延时到账

            money = m_data['money']                   # 金额，单位元
            memo = m_data['memo']                     # 转账备注
            transfer_id = m_data['transferid']         # 转账ID
            invalid_time = m_data['invalidtime']       # 10位时间戳

            msg_source_dict = {
                1: "收到转账",
                2: "对方接收转账",
                3: "发出转账",
                4: "自己接收转账",
                5: "对方退还",
                6: "自己退还",
            }
            trans_type_dict = {
                1: "即时到账",
                2: "延时到账",
            }
            res_type = f"{m_type}-{msg_source}-{trans_type}"
            content['tips'] = f"{m_type_dict[m_type]}|" \
                             f"{msg_source_dict[msg_source]}|" \
                             f"{trans_type_dict[trans_type]}"

        # D0005 事件分析————撤回事件
        elif m_type == "D0005":
            from_type = m_data["fromType"]             # 来源类型：1|好友 2|群聊
            msg_source = m_data['msgSource']             # 消息来源：1|别人撤回 2|自己使用手机撤回 3|自己使用电脑撤回

            from_wxid = m_data['fromWxid']              # fromType=1时为好友wxid，fromType=2时为群wxid
            final_from_wxid = m_data['finalFromWxid']     # 仅fromType=2时有效，为群内撤回消息人的wxid
            msg = m_data['msg']  # 撤回的消息内容

            from_type_dict = {
                1: "好友",
                2: "群聊",
            }
            msg_source_dict = {
                1: "别人撤回",
                2: "自己使用手机撤回",
                3: "自己使用电脑撤回",
            }
            res_type = f"{m_type}-{from_type}-{msg_source}"
            msg0 = re.sub(r"\s", '', msg)[:100]
            content['tips'] = f"{m_type_dict[m_type]}|" \
                              f"{from_type_dict[from_type]}|" \
                              f"{msg_source_dict[msg_source]}|" \
                              f"f{msg0}......"

        # D0006 事件分析————好友请求
        elif m_type == "D0006":
            """
            {
                'wxid': 'wxid_3xh9666nle4422',
                'wxNum': 'sdjy6133',
                'nick': '山东京耀',
                'nickBrief': 'SDJY',
                'nickWhole': 'shandongjingyao',
                'v3': 'v3_020b3826fd03010000000000057118a633fe47000000501ea9a3dba12f95f6b60a0536a1adb63075be3043e17053d3e83f99a35a7c415de949f7795d17659c5b79c3714970d33b8e2ed242f56639c05c8c6b0de2eb64cb64c95af8e5df1ba44dc666@stranger',
                'v4': 'v4_000b708f0b0400000100000000009d83413bf5b1bd3d23b56baf93641000000050ded0b020927e3c97896a09d47e6e9e2a00256840b4fb7b6f6ef8b60d471719cbafbe2a739bd3432ce8830769a10becbffd52148cf0f3ed1bf9fff23372c3abc360bc9edd8404fe498cdc2c6d63802f7c243a05a508c85f00e3b21526032f47b4d17d6c20447e40a9fdfb5860a18990f27cdb98a5651d34@stranger',
                'sign': '质量好，利润低，交个朋友。',
                'country': 'CN',
                'province': 'Shandong',
                'city': 'Taian',
                'avatarMinUrl': 'http://wx.qlogo.cn/mmhead/ver_1/AQXIuoI7hicJLa47KtzhRvGibD2nKEkr5pTBj0E00Ygg4Kjtl11j4dsXlbmLOXCmjWictANwplgrgNL2ticJ8CwqQQ/96',
                'avatarMaxUrl': 'http://wx.qlogo.cn/mmhead/ver_1/AQXIuoI7hicJLa47KtzhRvGibD2nKEkr5pTBj0E00Ygg4Kjtl11j4dsXlbmLOXCmjWictANwplgrgNL2ticJ8CwqQQ/0',
                'sex': '1',
                'content': '我是山东京耀',
                'scene': '3'
            },
            """
            wxid = m_data['wxid']
            wx_num = m_data['wxNum']
            nick = m_data['nick']
            sign = m_data['sign']
            cont = m_data['content']
            content['tips'] = f"收到好友请求|{nick}|{cont}"

        content["type"] = res_type


        content['data'] = data
        debug = self.debug if debug is None else debug
        if debug:
            self.log_debug(
                title=content['title'],
                info=content['tips'],
                var=[['data', data]],
                resp=content
            )

        return content

    # 更新数据到pandas
    def upd_data_to_df(self, data):
        root_wxid = data.get('wxid', data.get('rootWxid'))
        result = data.get('result', data.get('data', {}))
        if type(result) != list:
            result = [result]
        for item in result:
            item['rootWxid'] = root_wxid

            wxid = item['wxid']
            if '@chatroom' in wxid:
                item['type'] = '2'
            elif not wxid:
                item['wxid'] = '未知' + str(time.time())
                item['type'] = '0'
            else:
                item['type'] = '1'

        df_i = pd.DataFrame(data=result)
        self.data = pd.concat([self.data, df_i])
        # 删除重复的数据，subset参照手机号，keep保留第一个
        self.data.drop_duplicates(subset=['wxid'], keep='last', inplace=True)
        # 保存数据到文件
        self.save_data()

    # 获取群聊列表
    def upd_group_data(self, flush=True):
        '''
        获取群聊列表
        :param flush:
        :return:

        # 获取到的消息示例 【其中一条】
        {
            'wxid': '5877850803@chatroom',
            'wxNum': '',
            'nick': 'PLC编程，工控交流3群',
            'remark': '',
            'nickBrief': 'PLCBCGKJL3Q',
            'nickWhole': 'PLCbianchenggongkongjiaoliu3qun',
            'remarkBrief': '',
            'remarkWhole': '',
            'enBrief': '',
            'enWhole': '',
            'v3': '',
            'sign': '',
            'country': '',
            'province': '',
            'city': '',
            'momentsBackgroudImgUrl': '',
            'avatarMinUrl': '',
            'avatarMaxUrl': '',
            'sex': '',
            'memberNum': 325
        }
        '''

        content = {'title': '更新群聊列表'}

        payload = {
            "type": "Q0006",
            "data": {
                "type": "2" if flush else "1"  # 2 实时更新, 1 重新获取时不更新
            }
        }
        res = requests.post(self.url, json=payload).text

        # 防止有特殊字符不能转换成Json - 将特殊字符转换成 *
        res = ''.join((i if ord(i) >= 32 else '*' for i in res))
        res = json.loads(res)

        self.upd_data_to_df(res)

        if self.debug:
            self.log_debug(
                content['title'],
                pds=self.data
            )

        content['data'] = self.data
        return content

    # 获取好友列表
    def upd_friends_data(self, flush=True, simpl=True):
        """
        simpl: 简化内容，不必要的内容都略过，反之则获取完整内容

        # 获取到的消息示例 【其中一条】
        {
            'wxid': 'wxid_txlab9keqoq922',
            'wxNum': 'wei15539002190',
            'nick': '故与',
            'remark': '故与',
            'nickBrief': 'GY',
            'nickWhole': 'guyu',
            'remarkBrief': 'GY',
            'remarkWhole': 'guyu',
            'enBrief': '',
            'enWhole': '',
            'v3': 'v3_020b3826fd03010000000000f5b414868e3646000000501',
            'sign': '',
            'country': '',
            'province': '',
            'city': '',
            'momentsBackgroudImgUrl': '',
            'avatarMinUrl': '',
            'avatarMaxUrl': '',
            'sex': '',
            'memberNum': 0
        }
        """

        content = {'title': '更新好友列表'}

        payload = {
            "type": "Q0005",
            "data": {
                "type": "2" if flush else "1"  # 2 实时更新, 1 重新获取时不更新
            }
        }
        res = requests.post(self.url, json=payload).text

        # 防止有特殊字符不能转换成Json - 将特殊字符转换成 *
        res = ''.join((i if ord(i) >= 32 else '*' for i in res))
        res = json.loads(res)

        self.upd_data_to_df(res)

        if self.debug:
            self.log_debug(
                content['title'],
                pds=self.data
            )

        content['data'] = self.data
        return content

    # 检查是好友或群wxid 是否在我的通讯录中
    def check_wxid_is_in_my_record(self, wxid, debug=None):

        content = {}

        df = self.data
        df = df.loc[(df['wxid'] == wxid), :]
        if not df.size:
            if '@chatroom' in wxid:
                content['title'] = '检查群ID是否在我的通讯录中'
                content['err'] = '你没有加入这个群'
            else:
                content['title'] = '检查是不是我的好友'
                content['err'] = 'TA还不是你的好友'

        else:
            content['msg'] = 'Yes'

        debug = self.debug if debug is None else debug
        if debug:
            self.log_debug(
                title=content['title'],
                var=[['wxid', wxid]],
                resp=content
            )

        return content

    # 获取所有群成员
    def upd_group_member(self, wxid):
        content = {'title': '获取所有群成员'}

        payload = {
            "type": "Q0008",
            "data": {
                "wxid": wxid
            }
        }
        res = requests.post(self.url, json=payload)
        data = res.json()
        data = data["result"]

        df = pd.DataFrame(data).fillna('', inplace=False)
        if self.debug:
            self.log_debug(
                content['title'],
                pds=df
            )

        content['data'] = df
        return content

    # 查询对象信息
    def fetch_obj_info(self, wxid, debug=None):
        """
        {
            'code': 200,
            'msg': '操作成功',
            'result': {
                'wxid': 'wgm1016',
                'wxNum': '',
                'nick': '王哈哈[emoji=D83D][emoji=DEB5]',
                'remark': '刘昌録,17664393658',
                'nickBrief': 'WHH?',
                'nickWhole': 'wanghaha?',
                'remarkBrief': 'LCL17664393658',
                'remarkWhole': 'liuchanglu17664393658',
                'enBrief': 'WHH?',
                'enWhole': 'wanghaha?',
                'v3': 'v3_020b3826fd03010000000000b27c3674201a5a000000501ea9a3dba12f95f6b60a0536a1adb63075be3043e17053d3e83f9952684516fc76f26f3bf1ffbaab7fe7a047939376fa2cc0302ab5f9d9cf73c5e8@stranger',
                'v4': '',
                'sign': '',
                'country': 'CN',
                'province': 'Shandong',
                'city': 'Taian',
                'momentsBackgroudImgUrl': 'http://shmmsns.qpic.cn/mmsns/jpAVrBONXapQE9LGqxPCxs1SU68SznM9fianJzrkibPKsia4S7cAMuW9Ua6tpTQaIzIlf8qh12dyAA/0',
                'avatarMinUrl': 'http://wx.qlogo.cn/mmhead/ver_1/22LelxaWW7IsDwKpyIv57j7ibH9WDlzwPKoWC9GYvrMyOKpRhnPP6EYf8t9hHMPPpTowEcMUNFJHlCr05nickmVA/132',
                'avatarMaxUrl': 'http://wx.qlogo.cn/mmhead/ver_1/22LelxaWW7IsDwKpyIv57j7ibH9WDlzwPKoWC9GYvrMyOKpRhnPP6EYf8t9hHMPPpTowEcMUNFJHlCr05nickmVA/0',
                'sex': '',
                'memberNum': 0
            },
            'wxid': 'wxid_mh451po49x8u22',
            'port': 8055,
            'pid': 8672,
            'flag': '',
            'timestamp': '1689224355979'
        }
        """
        content = {}
        payload = {"type": "Q0004", "data": {"wxid": wxid}}
        res = requests.post(self.url, json=payload).text
        # 防止有特殊字符不能转换成Json - 将特殊字符转换成 *
        res = ''.join((i if ord(i) >= 32 else '*' for i in res))
        res = json.loads(res)
        result = res['result']

        content['rootWxid'] = res['wxid']
        content['data'] = result
        debug = debug if debug is not None else self.debug
        if debug:
            result = content['data']
            nick = result.get('nick')
            remark = result.get("remark")
            self.log_debug(
                title='获取微信对象详细信息',
                info=f'{nick}|{remark}',
                var=[["wxid", wxid]],
                resp=content
            )
        return content

    # 发送文本消息
    def send_mag(self, wxid, msg):

        content = {}
        msg = str(msg)
        if not msg:
            content["err"] = "消息是空的"

        # 检测是不是我的好友
        res = self.check_wxid_is_in_my_record(wxid=wxid, debug=False)
        if res.get('err'):
            content['err'] = res.get('err')
        else:
            msg0 = msg.replace("\n", "\r")
            payload = {"type": "Q0001", "data": {"wxid": wxid, "msg": msg0}}
            res = requests.post(self.url, json=payload)
            res = res.json()
            content['data'] = res
            if res['code'] != 200:
                content['err'] = res['msg']

        if self.debug:
            self.log_debug(
                title='发送微信消息-',
                var=[["wxid", wxid], ['msg', msg]],
                resp=content
            )
        return content

    # 发送小程序链接
    def send_app_msg(self, wxid, title, app_content, img_path, jumpPath, gh):
        """
            解决中文不能正常显示
                修改requests文件夹中的models.py文件，大约470行的位置
                在body = complexjson.dumps的括号内参数增加ensure_ascii=False
        """
        content = {}

        # 检测是不是我的好友
        res = self.check_wxid_is_in_my_record(wxid=wxid, debug=False)
        if res.get('err'):
            content['err'] = res.get('err')
        else:
            payload = {
                "type": "Q0013",  # POST 类型
                "data": {
                    "wxid": wxid,  # 好友Id    邀请进群-群组ID|删除好友|修改对象备注-支持好友wxid、群ID
                    #           修改群聊名称|发送名片-要发给谁
                    "title": title,  # 标题：        发送聊天记录|发送分享链接|发送小程序
                    "path": img_path,
                    # 路径：        发送图片|发送本地文件|发送分享链接-缩略图|发送小程序-缩略图
                    "content": app_content,  # 副标题：      发送分享链接|发送小程序|添加好友-请求内容|添加好友_通过wxid
                    "jumpPath": jumpPath,
                    # 跳转地址      发送小程序-点击跳转地址，例如饿了么首页为：pages/index/index.html
                    "gh": gh,  # 小程序地址     发送小程序-例如饿了么为：gh_6506303a12bb
                }
            }

            res = requests.post(self.url, json=payload)
            '''
            # 正确的
            {'code': 200, 'msg': '操作成功', 'result': {}, 'wxid': 'wxid_mh451po49x8u22', 'port': 8055, 'pid': 1908, 'flag': '', 'timestamp': '1689561995370'}
            # 错误的
            {'code': 500, 'msg': '图片不存在或者下载失败', 'result': {}, 'wxid': 'wxid_mh451po49x8u22', 'port': 8055, 'pid': 1908, 'flag': '', 'timestamp': '1689561992232'}
            '''
            res = res.json()
            content['data'] = res
            if res['code'] != 200:
                content['err'] = res['msg']

            if self.debug:
                self.log_debug(
                    title='发送小程序',
                    var=[
                        ["wxid", wxid],
                        ["title", title],
                        ["app_content", app_content],
                        ["img_path", img_path],
                        ["jumpPath", jumpPath]
                    ],
                    resp=content
                )

        return content

    # 发送分享链接
    def send_url(self, wxid, url, path=None, title=None, url_content=None):
        """
            title, content  如果不指定，则会自动获取
            解决中文不能正常显示
                修改requests文件夹中的models.py文件，大约470行的位置
                在body = complexjson.dumps的括号内参数增加ensure_ascii=False
        """
        content = {}
        path = path if path else 'https://p1.itc.cn/q_70/images03/20201026/06d78a60f86a43d8863ec94e49c46b8d.png'

        # 检测是不是我的好友
        res = self.check_wxid_is_in_my_record(wxid=wxid, debug=False)
        if res.get('err'):
            content['err'] = res.get('err')
        else:
            payload = {
                "type": "Q0012",  # POST 类型
                "data": {
                    "wxid": wxid,  # 好友Id    邀请进群-群组ID|删除好友|修改对象备注-支持好友wxid、群ID
                    #           修改群聊名称|发送名片-要发给谁
                    "title": title.strip() if title else title,  # 标题：        发送聊天记录|发送分享链接|发送小程序
                    "path": path.strip(),  # 路径：        发送图片|发送本地文件|发送分享链接-缩略图|发送小程序-缩略图
                    "content": url_content.strip() if url_content else url_content,  # 副标题：      发送分享链接|发送小程序|添加好友-请求内容|添加好友_通过wxid
                    "jumpUrl": url.strip(),  # 跳转链接：     发送分享链接
                }
            }

            res = requests.post(self.url, json=payload)
            res = res.json()
            content['data'] = res
            if res['code'] != 200:
                content['err'] = res['msg']

            if self.debug:
                self.log_debug(
                    title='发送链接消息',
                    var=[
                        ["wxid", wxid],
                        ["url", url],
                        ["path", path],
                        ["title", title],
                        ["url_content", url_content]
                    ],
                    resp=content
                )

        return content

    # 添加好友
    def add_friends(self, wxid, content):
        payload = {
            "type": "Q0019",  # POST 类型
            "data": {
                "wxid": wxid,  # 好友Id    邀请进群-群组ID|删除好友|修改对象备注-支持好友wxid、群ID
                #           修改群聊名称|发送名片-要发给谁
                "content": content,  # 副标题：      发送分享链接|发送小程序|添加好友-请求内容|添加好友_通过wxid
                "scene": 3,
                # 来源            同意好友请求|添加好友|添加好友_通过wxid     (1=qq 3=微信号 6=单向添加 10和13=通讯录 14=群聊 15=手机号 17=名片 30=扫一扫)
            }
        }

        rs = requests.post(self.url, json=payload)
        print(rs.json())
        return

    # 同意好友请求
    def agree_friends_req(self, v3, v4):

        """
        # 收到好友请求
        {
            'type': 'D0006',
            'des': '好友请求',
            'data': {
                'wxid': 'wxid_vb8ag1syrbsr22',
                'wxNum': 'zxcvbnm354061',
                'nick': '星辰[emoji=099E]',
                'nickBrief': 'XC?',
                'nickWhole': 'xingchen?',
                'v3': 'v3_020b3826fd03010000000000193108db3568c5000000501ea9a3dba12f95f6b60a0536a1adb63075be3043e17053d3e83f99fd5b319d908c99f3150d24f191ac2099996b120804999f4a82ebd4a8480bf35831803e4102234b794632e5c74413580b@stranger',
                'v4': 'v4_000b708f0b040000010000000000e6bdf179fddcaa674a62c99f9e641000000050ded0b020927e3c97896a09d47e6e9ec8fdf97c22d46abb2c17694e73e2b8a9a032c409b919ea20c5e4c469d0624b631d8b4b52b62d0a8c3a399aee90295d56865f4e31702ddc39bb1f45162b08a67102a6cd859f6c9bfb03b190a04f9a06efd0c2dc4be292fc58fdb320fe57ff47115d07fa0d66167e10@stranger',
                'sign': '',
                'country': 'CN',
                'province': 'Hunan',
                'city': 'Shaoyang',
                'avatarMinUrl': 'http://wx.qlogo.cn/mmhead/ver_1/8Z04HHsCjERZx4Q35TaDH7U3XUCLbIxcOTibSfePAOCV5SAGmrVA4vw2d7taUKpiadYmqAODJuHicVE1tJr1Aw6hvRzhk1m5fSMLGIhVxMoTx8/96',
                'avatarMaxUrl': 'http://wx.qlogo.cn/mmhead/ver_1/8Z04HHsCjERZx4Q35TaDH7U3XUCLbIxcOTibSfePAOCV5SAGmrVA4vw2d7taUKpiadYmqAODJuHicVE1tJr1Aw6hvRzhk1m5fSMLGIhVxMoTx8/0',
                'sex': '1',
                'content': '我是星辰[emoji=099E]',
                'scene': '1'
            },
            'timestamp': '1688117193541',
            'wxid': 'wxid_mh451po49x8u22',
            'port': 8055,
            'pid': 5356,
            'flag': ''
        }
        """

        content = {}
        payload = {
            "type": "Q0017",  # POST 类型
            "data": {
                "scene": 15,    # 来源  同意好友请求|添加好友|添加好友_通过wxid     (1=qq 3=微信号 6=单向添加 10和13=通讯录 14=群聊 15=手机号 17=名片 30=扫一扫)
                "v3": v3,       # v3 同意好友请求|添加好友_通过V3
                "v4": v4
            }
        }

        res = requests.post(self.url, json=payload)
        res = res.json()
        content['data'] = res
        if res['code'] != 200:
            content['err'] = res['msg']

        if self.debug:
            self.log_debug(
                title='发送微信消息',
                var=[["v3", v3], ["v4", v4]],
                resp=content
            )

        return content

    # 修改好友备注
    def set_friends_remark(self, wxid, remark):

        content = {}
        payload = {
            "type": "Q0023",  # POST 类型
            "data": {
                "type": "2",
                "wxid": wxid,  # 好友Id    邀请进群-群组ID|删除好友|修改对象备注-支持好友wxid、群ID
                #           修改群聊名称|发送名片-要发给谁
                "remark": remark,  # 备注：          修改对象备注-支持emoji、微信表情
            }
        }

        # 检测是不是我的好友
        res = self.check_wxid_is_in_my_record(wxid=wxid, debug=False)
        if res.get('err'):
            content['err'] = res.get('err')
        else:
            res = requests.post(self.url, json=payload)
            res = res.json()
            content['data'] = res

        return content

    def getXmlTxt(self, xmlCode, tagNames, attrs=None):
        '''

        :param xmlCode: xml代码
        :param tagNames: 标签名,可以是字符串，也可以是列表
        :param attrs: []标签的子项，列表
        :return: 返回所有标签或者子项的内容字典
        '''
        vDic = {}
        try:
            # 打开xml文档
            xmlItem = xml.dom.minidom.parseString(xmlCode)
            # 得到文档元素对象
            xmlItem = xmlItem.documentElement
        except:
            return vDic

        if type(tagNames) == str:
            tagNames = [tagNames]

        for tagName in tagNames:
            v = False
            try:
                tagItem = xmlItem.getElementsByTagName(tagName)[0]  # 按标签名获取对象
                if not attrs:
                    v = tagItem.childNodes[0].data  # 获取标签的内容数据
            except:
                pass
            if v:
                vDic[tagName] = v

        if not attrs:
            return vDic

        for attr in attrs:
            try:
                v = tagItem.getAttribute(attr)
            except:
                v = False
            if v:
                vDic[attr] = v
        return vDic

    def decXml(self, dicData, xmlCode):
        xmlType = dicData.get('xmlType', None)
        dicData['内容'] = None

        # 这是游戏 石头剪刀布 掷骰子
        if xmlType == 1:
            rs = self.getXmlTxt(xmlCode, "gameext", ["type", "content", ])

            gameType = int(rs.get("type", 0))
            gameContent = int(rs.get("content", 3))

            dicData['gameType'] = gameType
            dicData['gameContent'] = gameContent

            if gameType == 1:  # 这是石头剪刀布
                itemDic = {1: "剪刀", 2: "石头", 3: "布", }
                dicData['内容'] = f"游戏[石头剪刀布：{itemDic.get(gameContent, None)}]"
            elif gameType == 2:  # 这是 掷骰子
                dicData['内容'] = f"游戏[掷骰子：{gameContent - 3}点]"
        # 这是聊天记录
        elif xmlType == 19:
            rs = self.getXmlTxt(xmlCode, ["title", "des", ])

            title = rs.get("title", None)
            des = rs.get("des", None)

            dicData['title'] = title
            dicData['des'] = des

            dicData['内容'] = f"{title}[{des}]"
        # 这是发起位置共享
        elif xmlType == 17:
            dicData['内容'] = "发起位置共享"
        # 这是表情图片
        elif xmlType == 2:
            rs = self.getXmlTxt(xmlCode, "emoji", ["cdnurl", ])
            rs = rs.get("cdnurl", None)

            if "&" in rs:
                rs = f"<非官方表情包>{rs.split('&')[0]}"
            dicData['内容'] = rs
        # 这是分享链接
        elif xmlType == 5:
            rs = self.getXmlTxt(xmlCode, ["title", "des", "url"])

            title = rs.get("title", None)
            des = rs.get("des", None)
            url = rs.get("url", None)

            dicData["title"] = title
            dicData["des"] = des
            dicData["url"] = url

            dicData['内容'] = f"<{title}>[{des}][{url}]"

        # 这是收藏-笔记
        elif xmlType == 24:
            rs = self.getXmlTxt(xmlCode, "des")

            des = rs.get("des", None)

            dicData["des"] = des

            dicData['内容'] = f"{des}"

        # 未知数据
        else:
            dicData['内容'] = "未知数据"

        return dicData

    def getXmlTxt(self, xmlCode, tagNames, attrs=None):
        '''

        :param xmlCode: xml代码
        :param tagNames: 标签名,可以是字符串，也可以是列表
        :param attrs: []标签的子项，列表
        :return: 返回所有标签或者子项的内容字典
        '''
        vDic = {}
        try:
            # 打开xml文档
            xmlItem = xml.dom.minidom.parseString(xmlCode)
            # 得到文档元素对象
            xmlItem = xmlItem.documentElement
        except:
            return vDic

        if type(tagNames) == str:
            tagNames = [tagNames]

        for tagName in tagNames:
            v = False
            try:
                tagItem = xmlItem.getElementsByTagName(tagName)[0]  # 按标签名获取对象
                if not attrs:
                    v = tagItem.childNodes[0].data  # 获取标签的内容数据
            except:
                pass
            if v:
                vDic[tagName] = v

        if not attrs:
            return vDic

        for attr in attrs:
            try:
                v = tagItem.getAttribute(attr)
            except:
                v = False
            if v:
                vDic[attr] = v
        return vDic

    def getMsg(self, dicData):
        msgType = dicData['msgType']
        msg = dicData["msg"]
        try:
            xmlCode = re.findall(r'<msg>[\d\D]*?</msg>', msg)[0]
        except:
            xmlCode = dicData["msg"]

        # 获取msg中xml中type元素的值，如果没有，则取默认值 99
        rs = self.getXmlTxt(xmlCode, "type")
        if not rs:
            rs = self.getXmlTxt(xmlCode, "emoji", ["type", ])
        xmlType = rs.get("type", 99)

        dicData["xmlType"] = int(xmlType)

        dicData["内容"] = dicData["msg"]
        if msgType == 47:  # 这是动态表情
            dicData = self.decXml(dicData, xmlCode)  # 解析xml

        elif msgType == 34:  # 语音消息
            dicData["内容"] = "语音消息"
        elif msgType == 3:  # 这是图片
            dicData["内容"] = "图片"
        elif msgType == 43:  # 这是视频
            dicData["内容"] = '▶ 视频'
        # 这是分享链接或附件
        elif msgType == 49:
            # 这是文件
            if "file=" in dicData["msg"]:
                dicData["xmlType"] = 96
                msg = dicData["msg"]
                msg = re.findall(r"\[file=(.*?)\]", msg)
                if msg:
                    msg = msg[0]
                dicData["内容"] = msg
            # 其它
            else:
                dicData = self.decXml(dicData, xmlCode)
        # 这是名片
        elif msgType == 42:
            rs = self.getXmlTxt(xmlCode, "msg",
                                ["username", 'nickname', "antispamticket", 'province', 'city', 'openimdesc'])
            v3 = rs.get("username", None)
            nickname = rs.get("nickname", None)  # 昵称
            v4 = rs.get("antispamticket", None)
            province = rs.get("province", None)  # 省份
            city = rs.get("city", None)  # 城市
            openimdesc = rs.get("openimdesc", None)  # 企业微信-企业账号

            dicData['v3'] = v3
            dicData['nickname'] = nickname
            dicData['v4'] = v4
            dicData['province'] = province
            dicData['city'] = city
            dicData['openimdesc'] = openimdesc

            if 'gh_' in v3:
                dicData['xmlType'] = 95
                dicData["内容"] = f"公众号[{nickname}]"
            elif '@openim' in v3:
                dicData['xmlType'] = 94
                dicData["内容"] = f"企业微信号[{openimdesc}[{nickname}]]"
            else:
                dicData['xmlType'] = 93
                dicData["内容"] = f"个人号[{nickname}]]"


        # 这是地理位置
        elif msgType == 48:
            rs = self.getXmlTxt(xmlCode, "location", ["poiname", "label", "x", "y"])
            x = rs["x"]
            y = rs["y"]
            label = rs["label"]
            poiname = rs["poiname"]
            dicData[x] = x
            dicData[y] = y
            dicData[label] = label

            dicData["内容"] = f"x,{x} y,{y} {poiname}[{label}]"
        elif msgType == 10000:

            if '位置共享' in dicData['msg']:
                dicData["xmlType"] = 98
            if '收到红包' in dicData['msg']:
                dicData["xmlType"] = 97
        return dicData

    # 待完善
    def Xpost(self, url, msg_type):
        '''
        获取微信列表（X0000）           POST微信状态检测（Q0000）   POST发送文本消息（Q0001）    POST修改下载图片（Q0002）    POST获取个人信息（Q0003）
        POST查询对象信息（Q0004）       POST获取好友列表（Q0005）   POST获取群聊列表（Q0006）    POST获取公众号列表（Q0007）    POST获取群成员列表（Q0008）
        POST发送聊天记录（Q0009）       POST发送图片（Q0010）      POST发送本地文件（Q0011）    POST发送分享链接（Q0012）    POST发送小程序（Q0013）
        POST发送音乐分享（Q0014）       POST发送XML（Q0015）      POST确认收款（Q0016）       POST同意好友请求（Q0017）    POST添加好友_通过v3（Q0018）
        POST添加好友_通过wxid（Q0019）  POST查询陌生人信息（Q0020） POST邀请进群（Q0021）       POST删除好友（Q0022）    POST修改对象备注（Q0023）
        POST修改群聊名称（Q0024）       POST发送名片（Q0025）

        '''

        payload = {
            "type": msg_type,
            "data": {}
        }

        response = requests.request("POST", url, headers=headers, data=payload)


    # 待完善
    def Qpost(self, wxid, msg_type, msg=None, uWxid=None, picType=None, title=None, dataList=None, path=None, content=None,
              jumpUrl=None, app=None, jumpPath=None,
              gh=None, name=None, author=None, musicUrl=None, imageUrl=None, xml=None, transferid=None, scene=None,
              v3=None, v4=None, pq=None, objWxid=None, remark=None, nick=None):
        url = f"http://127.0.0.1:7777/DaenWxHook/httpapi/?wxid={wxid}"

        payload = {
            "type": msg_type,  # POST 类型
            "data": {
                "type": picType,  # 类型：       修改下载图片-     “23:30-23:30”为全天下载，“00:01-23:59”为全天不下载
                #             添加好友_通过V3-  (1=新朋友，2=互删朋友（2:此时来源将固定死为3）)
                #             邀请进群-         1=直接拉，2=发送邀请链接）
                "wxid": uWxid,  # 好友Id    邀请进群-群组ID|删除好友|修改对象备注-支持好友wxid、群ID
                #           修改群聊名称|发送名片-要发给谁
                "msg": msg,  # 内容：       发送消息
                "title": title,  # 标题：        发送聊天记录|发送分享链接|发送小程序
                "dataList": dataList,  # []内容列表：   发送聊天记录
                "path": path,  # 路径：        发送图片|发送本地文件|发送分享链接-缩略图|发送小程序-缩略图
                "content": content,  # 副标题：      发送分享链接|发送小程序|添加好友-请求内容|添加好友_通过wxid
                "jumpUrl": jumpUrl,  # 跳转链接：     发送分享链接
                "app": app,  # 跳转APP：    发送分享链接-跳转APP(可空，例如QQ浏览器为：wx64f9cf5b17af074d)
                "jumpPath": jumpPath,  # 跳转地址      发送小程序-点击跳转地址，例如饿了么首页为：pages/index/index.html
                "gh": gh,  # 小程序地址     发送小程序-例如饿了么为：gh_6506303a12bb
                "name": name,  # 歌名            发送音乐分享
                "author": author,  # 作者            发送音乐分享
                "musicUrl": musicUrl,  # 网络歌曲直链    发送音乐分享
                "imageUrl": imageUrl,  # 网络图片直链    发送音乐分享
                "xml": xml,  # xml           发送xml
                "transferid": transferid,  # 转账ID          同意收款
                "scene": scene,
                # 来源            同意好友请求|添加好友|添加好友_通过wxid     (1=qq 3=微信号 6=单向添加 10和13=通讯录 14=群聊 15=手机号 17=名片 30=扫一扫)
                "v3": v3,  # v3            同意好友请求|添加好友_通过V3
                "v4": v4,  # v4            同意好友请求
                "pq": pq,  # 手机号或者QQ
                "objWxid": objWxid,  # 好友wxid       邀请进群
                "remark": remark,  # 备注：          修改对象备注-支持emoji、微信表情
                "nick": nick,  # 群名称 支持emoji、微信表情
                #               修改群聊名称

            }
        }

        if msg_type == 'Q0025':  # 发送名片
            # 待完善
            payload = rf'{{\r\n    \"type\": \"{msg_type}\",\r\n    \"data\": {{\r\n        \"wxid\": \"21257217892@chatroom\",\r\n        \"xml\": \"<?xml version=\\\"1.0\\\"?>\r\n<msg bigheadimgurl=\\\"http://wx.qlogo.cn/mmhead/ver_1/qYAC6GgTX4cAqTmzB5Ep8nzeB9RjufAMT02q7PLLEURuLbHlyjibria2LMLBsvqIiaZQmeZPicbRSMQY28zKQGxHTXHz5tg5RQe1UCJkGPVbXSI/0\\\" smallheadimgurl=\\\"http://wx.qlogo.cn/mmhead/ver_1/qYAC6GgTX4cAqTmzB5Ep8nzeB9RjufAMT02q7PLLEURuLbHlyjibria2LMLBsvqIiaZQmeZPicbRSMQY28zKQGxHTXHz5tg5RQe1UCJkGPVbXSI/132\\\" username=\\\"wxid_jah3fozezery22\\\" nickname=\\\"〆无所不能。\\\" fullpy=\\\"wusuobuneng\\\" shortpy=\\\"\\\" alias=\\\"PQAPQB\\\" imagestatus=\\\"3\\\" scene=\\\"17\\\" province=\\\"云南\\\" city=\\\"中国大陆\\\" sign=\\\"\\\" sex=\\\"2\\\" certflag=\\\"0\\\" certinfo=\\\"\\\" brandIconUrl=\\\"\\\" brandHomeUrl=\\\"\\\" brandSubscriptConfigUrl=\\\"\\\" brandFlags=\\\"0\\\" regionCode=\\\"CN_Yunnan_Kunming\\\" biznamecardinfo=\\\"\\\" />\"\r\n    }}\r\n}}'
        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

    # ============================================================================== ***DEBUG***

    # log_debug
    def log_debug(self, title, info=None, var=None, resp=None, pds=None):
        """
        var: ([变量名, 变量值],...)
        """
        print(">" * 100)
        title = f'<ming6131.ok.wechat.py> DEBUG: > {title}'
        print(title)
        print(datetime.datetime.now())
        if info:
            print(info)
        if pds is not None:
            print(pds.head())
            print(f'\n----第一行：')
            print(pd.Series(pds.values[0], pds.columns).to_dict())
        else:
            print(f'\n----参数：')
            if var:
                for item in var:
                    print(f"{item[0]} ->", item[1])
            print(f'\n----返回值：')
            print(resp)
        print("<" * 100, "\n")


if __name__ == '__main__':
    from aaa.api.feishu import Fs

    def receive_msg(wechat, data):
        data = wechat.fetch_obj_info('wxid_3xh9666nle4422')
        wechat.upd_data_to_df(data)


    # 创建飞书多维表格对象
    app_id = "cli_a42d052d8cb01013"
    app_secret = "X3jpJ2NOps7JmH0bvY2V0b1Hyia7zL2v"
    app_token = "Wt0GbvW3XaOkdPslPRJcpOZEnSe"
    fs = Fs(app_id, app_secret, app_token)

    # 获取参数
    num = "H01"
    table_id = "tbljWKjeBUyhKaxf"
    args = fs.get_args(num, table_id)

    # 运行 微信服务端
    port1 = args.get("port1")
    port2 = args.get("port2")
    wechat = Wechat(port1, port2, True)

    wechat.run(receive_msg)

