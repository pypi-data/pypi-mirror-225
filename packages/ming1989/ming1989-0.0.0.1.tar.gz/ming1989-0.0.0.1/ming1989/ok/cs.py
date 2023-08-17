import os.path
import time
import re
import json
from xml.dom.minidom import parseString
import xml.dom.minidom
from flask import Flask, request

import requests


# import pyAardio

def infoShow(txt, lv=1, tm=2000):
    # pyAardio.infoShow(lv,txt,tm)
    print(txt)




def postWechat(postType, data, port):
    payload = {"type": postType, "data": data}
    headers = {
        'User-Agent': 'apifox/1.0.0 (https://www.apifox.cn)',
        'Content-Type': 'application/json'
    }
    # 请求url
    url = f'http://127.0.0.1:{port}/DaenWxHook/client/'
    # 请求参数

    # 调用post
    response = requests.post(url, json=payload,
                             headers=headers)  # response 响应对象

    # 获取响应状态码
    print('状态码：', response.status_code)
    # 获取响应头
    print('响应头信息：', response.headers)
    # 获取响应正文
    print('响应正文：', response.text)



app = Flask(__name__)


@app.route('/wechat/', methods=['get', 'post'])
def wechat():
    data = request.stream.read()
    data = data.decode('utf-8')
    data = json.loads(data, strict=False)
    print(data)
    jiexi事件(data)
    return "xx"


if __name__ == '__main__':
    # dic多微信 = {}     # 用于记录多开微信 {wxid = {'wxNum':"xxxx",'nick':"xxx"}}
    dic多微信 = {
        "wxid_gybxqyp6u8wv22": {
            'wxNum': "zixuetang1688",
            'nick': "学习改变命运"
        }
    }

    rs = app.run(debug=True, port=8089)
    print(rs)

    '''
    # 修改下载图片
    url = "http://127.0.0.1:8089/DaenWxHook/client/"

    payload = json.dumps({
        "type": "Q0002",
        "data": {
            "type": "23:30-23:30"
        }
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    '''