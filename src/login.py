from .api.aes import aes_encrypt
from . import apiurl
from . import logger
import requests
import json


def get_token(username, password):
    login_headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Host': 'swxg.haust.edu.cn',
        'Origin': 'https://swxg.haust.edu.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://swxg.haust.edu.cn/xgh5/login.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
        'X-Requested-With': 'XMLHttpRequest'
    }
    token_str = ''.join((str(username), '&', str(password)))
    data = {
        'param': json.dumps({
            'cmd': 'longin',
            'longin': aes_encrypt(token_str)
        })
    }
    login_resp = requests.post(apiurl, data=data, headers=login_headers)
    login_resp.raise_for_status()
    logger.debug('[{}]{}'.format(login_resp.status_code, login_resp.text))
    login_resp_json = json.loads(login_resp.text)
    if login_resp_json['result'] == 0:
        token = login_resp_json['data']['token']  
    else:
        logger.error(login_resp_json['message'])
        token = None
    return token
