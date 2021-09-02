from threading import Timer
import json
import sys
import os.path
import time
from src import logger
from src.bpa import bpa
from random import randint
from src.db import insert_record

def bpa_once(username, password, mailcode, bpatime: tuple =(8, 0), interval=60):
    try:
        stat = bpa(username, password, mailcode)
    except Exception as e:
        logger.critical(str(e))
        stat = -2
    
    now_time = time.time()
    serial_now_time = time.localtime(now_time)
    serial_next_time = time.struct_time((
        serial_now_time[0],
        serial_now_time[1],
        serial_now_time[2],
        bpatime[0],
        bpatime[1],
        serial_now_time[5],
        serial_now_time[6],
        serial_now_time[7],
        serial_now_time[8]
    ))
    next_time = time.mktime(serial_next_time)
    one_day_after = next_time + 86400 - now_time + randint(-3600, 3600)
    half_hr_after = 1800 + randint(-900, 900)

    if stat == 0 or stat == -1:
        offseted_time = now_time + one_day_after
        # 成功执行或已报，延时23~25小时
        Timer(one_day_after, bpa_once, (username, password)).start()
        logger.info('{username} 已报平安。下次报平安时间：{time}'.format(
            username=username,
            time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(offseted_time))
        ))
    else:
        offseted_time = now_time + half_hr_after
        # 失败，延时15~45分钟
        Timer(half_hr_after, bpa_once, (username, password)).start()
        logger.info('{username} 报平安失败，将在一会之后重试。预计报平安时间：{time}'.format(
            username=username,
            time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(offseted_time))
        ))
        
    insert_record(username, now_time, offseted_time, stat)
    # 阻塞60秒 防止高频访问报非法操作
    time.sleep(interval)

def gen_config():
    logger.warning('未找到可用配置文件。')
    config_json = json.dumps({
        'user': [
            {
                'username': '123456',
                'password': '123456',
                'mailcode': '100000'
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
    bpa_once(each['username'], each['password'], each['mailcode'])

        