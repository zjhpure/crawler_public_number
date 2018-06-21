# coding: utf-8
import datetime
import time
import os

from time import strftime


# 每天凌晨重启anyproxy,anyproxy长时间运行不重启会很卡
class RestartAnyproxy(object):
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
                os.system('sudo pm2 restart anyproxy')
                self.print_with_time('sleep 4000s')
                # 执行完就休眠一个小时,一天只重置一次
                time.sleep(4000)

    @staticmethod
    def print_with_time(content):
        print(strftime('%Y-%m-%d %H:%M:%S'))
        print(content)


if __name__ == '__main__':
    restart_anyproxy = RestartAnyproxy()
    restart_anyproxy.run()
