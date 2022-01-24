# iamok
河南科技大学报平安

**由于API更新，该程序已失效**

本程序仅供学习交流使用，下载后请于24小时内删除。请每天按照要求如实上报个人状况信息，否则造成的一切后果自行承担。

## 食用方法

1. 安装Python环境，推荐3.8

2. 建立虚拟环境（可选）并安装依赖

```sh
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

3. 运行`schedule.py`，修改`config.json`，然后再运行一次

4. 完成！搭配`supervisor`等进程管理程序食用效果更佳。如需修改日志粒度，直接编辑src/log.py中的`logger.setLevel()`。
