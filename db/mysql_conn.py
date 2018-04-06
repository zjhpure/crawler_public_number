# -*- coding: utf-8 -*-
import pymysql
from time import strftime


class MysqlConn(object):
    conn = None
    cursor = None

    def __init__(self, host, user, password, db, port, charset):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.charset = charset

    def connect(self):
        try:
            self.conn = pymysql.connect(host=self.host,
                                        user=self.user,
                                        password=self.password,
                                        db=self.db,
                                        port=self.port,
                                        charset=self.charset,
                                        autocommit=True)
            self.cursor = self.conn.cursor()
            self.print_with_time('mysql connect success')
        except Exception as e:
            self.print_with_time(e)
            self.print_with_time('mysql connect failure')

    def ping(self):
        try:
            self.conn.ping()
            self.print_with_time('mysql ping success')
        except Exception as e:
            self.print_with_time(e)
            self.print_with_time('mysql ping failure')
            try:
                self.connect()
                self.print_with_time('mysql reconnect success')
            except Exception as e:
                self.print_with_time(e)
                self.print_with_time('mysql reconnect failure')

    def close(self):
        try:
            self.conn.close()
            self.print_with_time('mysql close success')
        except Exception as e:
            self.print_with_time(e)
            self.print_with_time('mysql close failure')

    @staticmethod
    def print_with_time(content):
        print(strftime('%Y-%m-%d %H:%M:%S'))
        print(content)
