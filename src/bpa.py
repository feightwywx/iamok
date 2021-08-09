from . import apiurl
from .login import get_token
import requests
from requests.sessions import session
import json


def bpa(username, password):
    username = str(username)
    password = str(password)
    token = get_token(username, password)

    index_headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Host': 'bpa.haust.edu.cn',
        'Origin': 'http://bpa.haust.edu.cn',
        'Pragma': 'no-cache',
        'Referer': 'http://bpa.haust.edu.cn/xgh5/stu/index.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
        'X-Requested-With': 'XMLHttpRequest'
    }

    bpa_session = session()

    # 界面请求，虽然没必要但是看起来可以合理一些 也不怎么拖速度（。
    view_resp = bpa_session.post(apiurl, data={
        'command': 'XGXT',
        'param': json.dumps({
            'cmd': 'checkApplyConditionInst',
            'xh': username,
            'code': 'xsyqsbApplyView',
            'token': token
        })
    }, headers=index_headers)
    print(view_resp.status_code, view_resp.text)

    # 检查当日是否已报平安
    stat_resp = bpa_session.post(apiurl, data={
        'command': 'XGXT',
        'param': json.dumps({
            'cmd': 'checkXsYqsbQx',
            'xh': username,
            'token': token
        })
    }, headers=index_headers)
    print(stat_resp.status_code, stat_resp.text)
