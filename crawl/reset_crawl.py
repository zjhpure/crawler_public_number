# -*- coding: utf-8 -*-
import datetime
import time

from time import strftime
from db.mysql_operate import MysqlOperate


# 每天凌晨重置所有公众号的今天是否已爬取为0
class ResetCrawl(object):
    mysql_operate = MysqlOperate()

    def run(self):
        while True:
            self.print_with_time('sleep 10s')
            time.sleep(10)
            # 获取当前时间
            now = str(datetime.datetime.now())
            # 获取当前时间的小时数
            hour = now.split(' ')[1].split(':')[0]
            # 若小时数为00,则证明已经到了凌晨
            if '00' == hour:
                # 重置所有公众号的今天是否已爬取为0
                self.mysql_operate.reset_all_pub_today_is_crawl()
                self.print_with_time('sleep 4000s')
                # 执行完就休眠一个小时,一天只重置一次
                time.sleep(4000)

    @staticmethod
    def print_with_time(content):
        print(strftime('%Y-%m-%d %H:%M:%S'))
        print(content)


if __name__ == '__main__':
    reset_crawl = ResetCrawl()
    reset_crawl.run()
