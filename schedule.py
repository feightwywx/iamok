from os import stat
from threading import Timer
import json
import sys
import os.path
import time
from src import logger
from src.bpa import bpa

def bpa_once(username, password):
    try:
        stat = bpa(username, password)
    except Exception as e:
        logger.critical(str(e))
        stat = -2
    if stat == 0 or stat == -1:
        # 成功执行或已报，延时24小时
        Timer(86400, bpa_once, (username, password)).start()
        logger.info('{username} 已报平安。下次报平安时间：{time}'.format(
            username=username,
            time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 86400))
        ))
    else:
        # 失败，延时半小时
        Timer(1800, bpa_once, (username, password)).start()
        logger.info('{username} 报平安失败，将在30分钟后重试。预计报平安时间：{time}'.format(
            username=username,
            time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 1800))
        ))

def gen_config():
    logger.warning('未找到可用配置文件。')
    config_json = json.dumps({
        'user': [
            {
                'username': 123456,
                'password': 123456
            }
        ]
    }, indent=4)
    with open('config.json', mode='w') as configf:
        configf.write(config_json)
        logger.warning('已生成配置模板。请检查工作目录下的config.json。')
        sys.exit(1)


if not os.path.exists('config.json'):
    gen_config()

with open('config.json', mode='r') as configf:
    config_json = configf.read()
    if config_json:
        config = json.loads(config_json)
    else:
        gen_config()  # 尝试生成模板，结束进程
        
# 存在config.json
for each in config['user']:
    bpa_once(each['username'], each['password'])

        