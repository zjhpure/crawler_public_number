# coding: utf-8
import json

from cfg.cfg import redis_db, api_port
from flask import Flask
from redis import StrictRedis

app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello world!'


@app.route('/crawler/public_number/get_click_public_number', methods=['GET', 'POST'])
def get_click_public_number():
    # 连接redis
    redis = StrictRedis(host=redis_db['host'], port=redis_db['port'], password=redis_db['password'])
    if redis.llen('public_number') > 0:
        # redis长度不为0,从左pop出数据,按键精灵可以点击
        info = str(redis.lpop('public_number'), encoding='utf-8')
        info = info.split('&&')
        print(info)
        # data = {"errcode": 0, "msg": "获取公众号成功",
        #         "result": {"public_number_name": info[0],
        #                    "public_number_wechat_id": info[1],
        #                    "public_number_biz": info[2]}}
        data = {"errcode": 0, "msg": "获取公众号成功",
                "result": {"publicNumberName": info[0],
                           "publicNumberWechatId": info[1],
                           "publicNumberBiz": info[2]}}
    else:
        # redis长度为0,按键精灵不用点击
        data = {"errcode": 1, "msg": "无公众号获取"}
    result = json.dumps(data, ensure_ascii=False)
    print(result)
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=api_port, debug=True)
