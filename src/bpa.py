from . import apiurl
from .login import get_token
from .api.aes import aes_encrypt
from . import logger
from requests.sessions import session
from copy import copy
import json


def bpa(username, password):
    logger.info('学号 {} 同学开始报平安'.format(username))
    username = str(username)
    password = str(password)
    token = get_token(username, password)
    if token is None:
        return -2

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

    # 界面请求，虽然没必要
    view_resp = bpa_session.post(apiurl, data={
        'command': 'XGXT',
        'param': json.dumps({
            'cmd': 'checkApplyConditionInst',
            'xh': username,
            'code': 'xsyqsbApplyView',
            'token': token
        })
    }, headers=index_headers)
    logger.debug('[{}]{}'.format(view_resp.status_code, view_resp.text))

    # 检查当日是否已报平安
    stat_resp = bpa_session.post(apiurl, data={
        'command': 'XGXT',
        'param': json.dumps({
            'cmd': 'checkXsYqsbQx',
            'xh': username,
            'token': token
        })
    }, headers=index_headers)
    logger.debug('[{}]{}'.format(stat_resp.status_code, stat_resp.text))
    sm_code = stat_resp.json()['data']['sm']  # 报平安状态
    if sm_code == '1':  # 未报平安
        bpa_uri = 'http://bpa.haust.edu.cn/xgh5/stu/bpa/yq_info.html?' + \
            aes_encrypt('xh={xh}&token={token}'.format(
                xh=username, token=token
            ))
        bpa_headers = copy(index_headers)
        bpa_headers['Referer'] = bpa_uri

        enc_username = aes_encrypt(username)  # 学号你加密个锤子？
        # 请求学生头像，虽然也没必要还耗时间
        stupic_resp = bpa_session.post(apiurl, data={
            'command': 'XGXT',
            'param': json.dumps({
                'cmd': 'stuPicView',
                'xh': enc_username,
                'token': token
            })
        }, headers=bpa_headers)
        logger.debug('[{}]{}'.format(stupic_resp.status_code, '*** Student profile picture ***'))

        # 获取学生信息
        getdata_resp = bpa_session.get(apiurl, params={
            'command': 'XGXT',
            'customercode': '',
            'param': json.dumps({
                'cmd': 'xsyqsbApplyView',
                'xh': enc_username,
                'token': token
            })
        }, headers=bpa_headers)
        logger.debug('[{}]{}'.format(getdata_resp.status_code, getdata_resp.text))
        studata = getdata_resp.json()['data']
        if not studata:
            return -2

        # 报平安
        commit_resp = bpa_session.post(apiurl, data={
            'command': 'XGXT',
            'param': json.dumps({
                    'cmd': 'yqsbFormSave',
                    'xh': studata['xh'],
                    'sbsj': studata['sbsjS'],
                    'nl': studata['nl'],
                    'lxfs': studata['lxdh'],
                    'jzdq': studata['jzdq'],
                    'jzdq_xxdz': studata['jzdqXxdz'],
                    'tw': '36.5',
                    'sflx': '0',
                    'jcbr': '0',
                    'zyzz': '1,',
                    'fbrq': '',
                    'zyzzms': '',
                    'bz': '',
                    'bz1': '',
                    'wcjtgj': '',
                    'wcjtgjxq': '',
                    'wcdq': '',
                    'wcdqxxdz': '',
                    'lkdate': '',
                    'fhdate': '',
                    'zszt': '',
                    'ylzd1': '',
                    'qrblxqdz': '',
                    'qrbltjdz': '',
                    'jcdq': '',
                    'jcxxdz': '',
                    'jcsj': '',
                    'qzsj': '',
                    'zlyy': '',
                    'zysj': '',
                    'token': token
                }
            )
        }, headers=bpa_headers)
        logger.debug('[{}]{}'.format(commit_resp.status_code, commit_resp.text))
        commit_status = commit_resp.json()['result']
        if commit_status == 0:  # 报平安成功
            logger.info('{} 同学已成功报平安'.format(studata['xm']))

            # 请求报平安情况
            bpa_list_uri = 'http://bpa.haust.edu.cn/xgh5/stu/bpa/yq_list.html?' + \
                aes_encrypt('xh={xh}&token={token}'.format(
                    xh=username, token=token
                ))
            bpa_list_headers = copy(index_headers)
            bpa_list_headers['Referer'] = bpa_list_uri

            list_resp = bpa_session.get(apiurl, params={
                'command': 'XGXT',
                'customercode': '',
                'param': json.dumps({
                    'cmd': 'xsyqsbApplyViewList',
                    'xh': enc_username,
                    'rqyf': '',
                    'zsbts': '',
                    'token': token
                })
            }, headers=bpa_list_headers)
            logger.debug('[{}]{}'.format(list_resp.status_code, list_resp.text))
            bpa_count = list_resp.json()['data']['zsbts']
            bpa_mon_count = list_resp.json()['data']['bysbts']
            logger.info('总报平安次数 {} ，本月报平安 {} 次。'.format(
                bpa_count, bpa_mon_count
            ))
            return 0
        else:
            pass
    elif sm_code == '-1':
        logger.warning('{} 今日已报过平安'.format(username))
        return -1
    else:
        pass
    logger.error('报平安失败，请检查')
    return -2
