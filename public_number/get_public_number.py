# coding: utf-8
import time

from time import strftime
from db.mysql_operate import MysqlOperate
from redis import StrictRedis
from cfg.cfg import redis_db


class GetPublicNumber(object):
    mysql_operate = MysqlOperate()

    def query_public_number_count(self):
        # 连接redis
        redis = StrictRedis(host=redis_db['host'], port=redis_db['port'], password=redis_db['password'])
        n = 19
        while True:
            self.print_with_time('sleep 10s')
            time.sleep(10)
            for row in self.mysql_operate.query_public_number():
                self.print_with_time('sleep 2s')
                time.sleep(2)
                public_number_wechat_id = row[1]
                public_number_name = row[2]
                public_number_biz = row[3]
                if redis.llen('public_number') <= 19:
                    redis.rpush('public_number', public_number_name + '&&' + public_number_wechat_id
                                + '&&' + public_number_biz)
                    print('public_number_wechat_id:' + public_number_wechat_id
                          + ' public_number_name:' + public_number_name
                          + ' public_number_biz:' + public_number_biz)
                else:
                    self.print_with_time('public_number size can not more than ' + str(n + 1))
                    self.print_with_time('sleep 2s')
                    time.sleep(2)
                    while redis.llen('public_number') <= 19:
                        if redis.llen('public_number') <= 19:
                            redis.rpush('public_number', public_number_name + '&&' + public_number_wechat_id
                                        + '&&' + public_number_biz)
                            print('public_number_wechat_id:' + public_number_wechat_id
                                  + ' public_number_name:' + public_number_name
                                  + ' public_number_biz:' + public_number_biz)
                        else:
                            self.print_with_time('public_number size can not more than ' + str(n + 1))
                            self.print_with_time('sleep 2s')
                            time.sleep(2)

    @staticmethod
    def print_with_time(content):
        print(strftime('%Y-%m-%d %H:%M:%S'))
        print(content)


if __name__ == '__main__':
    get_public_number = GetPublicNumber()
    get_public_number.query_public_number_count()
