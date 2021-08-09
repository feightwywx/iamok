import requests
import json

def aes_decrypt(data):
    resp = requests.post('http://tool.chacuo.net/cryptaes', data={
        'data': data,
        'type': 'aes',
        'arg': 'm=ecb_pad=pkcs7_block=128_p=1234567890123456_o=0_s=utf-8_t=1'
    })
    return json.loads(resp.text)['data'][0]

def aes_encrypt(data):
    resp = requests.post('http://tool.chacuo.net/cryptaes', data={
        'data': data,
        'type': 'aes',
        'arg': 'm=ecb_pad=pkcs7_block=128_p=1234567890123456_o=0_s=utf-8_t=0'
    })
    return json.loads(resp.text)['data'][0]
