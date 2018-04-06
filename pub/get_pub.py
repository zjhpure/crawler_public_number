# -*- coding: utf-8 -*-
import time

from time import strftime
from db.mysql_operate import MysqlOperate
from redis import StrictRedis
from cfg.cfg import redis_db


class GetPub(object):
    mysql_operate = MysqlOperate()

    def query_pub_count(self):
        # 连接redis
        redis = StrictRedis(host=redis_db['host'], port=redis_db['port'], password=redis_db['password'])
        n = 19
        while True:
            self.print_with_time('sleep 10s')
            time.sleep(10)
            for row in self.mysql_operate.query_pub():
                self.print_with_time('sleep 2s')
                time.sleep(2)
                pub_wx_id = row[1]
                pub_name = row[2]
                pub_biz = row[3]
                if redis.llen('crawl_pub') <= 19:
                    redis.rpush('crawl_pub', pub_name + '&&' + pub_wx_id + '&&' + pub_biz)
                    print('pub_wx_id:' + pub_wx_id + ' pub_name:' + pub_name + ' pub_biz:' + pub_biz)
                else:
                    self.print_with_time('crawl_pub size can not more than ' + str(n + 1))
                    self.print_with_time('sleep 2s')
                    time.sleep(2)
                    while redis.llen('crawl_pub') <= 19:
                        if redis.llen('crawl_pub') <= 19:
                            redis.rpush('crawl_pub', pub_name + '&&' + pub_wx_id + '&&' + pub_biz)
                            print('pub_wx_id:' + pub_wx_id + ' pub_name:' + pub_name + ' pub_biz:' + pub_biz)
                        else:
                            self.print_with_time('crawl_pub size can not more than ' + str(n + 1))
                            self.print_with_time('sleep 2s')
                            time.sleep(2)

    @staticmethod
    def print_with_time(content):
        print(strftime('%Y-%m-%d %H:%M:%S'))
        print(content)


if __name__ == '__main__':
    get_pub = GetPub()
    get_pub.query_pub_count()
