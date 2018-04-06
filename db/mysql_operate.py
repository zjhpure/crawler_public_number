# -*- coding: utf-8 -*-
from db.mysql_conn import MysqlConn
from cfg.cfg import mysql_db
from time import strftime


class MysqlOperate(object):
    def __init__(self):
        self.mysql_conn = MysqlConn(host=mysql_db['host'],
                                    user=mysql_db['user'],
                                    password=mysql_db['password'],
                                    db=mysql_db['db'],
                                    port=mysql_db['port'],
                                    charset='utf8')
        self.mysql_conn.connect()
        self.conn = self.mysql_conn.conn
        self.cursor = self.mysql_conn.cursor

    def query_pub(self):
        self.mysql_conn.ping()
        sql_query = 'select * from pub where is_del = 0 and today_is_crawl = 0'
        self.cursor.execute(sql_query)
        self.print_with_time('query pub all')
        return self.cursor.fetchall()

    def query_pub_by_biz(self, biz):
        self.mysql_conn.ping()
        sql_query = "select * from pub where is_del = 0 and today_is_crawl = 0 " \
                    "and pub_biz = '" + biz + "'"
        self.cursor.execute(sql_query)
        self.print_with_time('query pub by biz, biz = ' + biz)
        return self.cursor.fetchall()

    def update_pub_today_is_crawl(self, pub_wx_id, today_is_crawl):
        self.mysql_conn.ping()
        sql = 'update pub set today_is_crawl = ' + today_is_crawl + " where pub_wx_id = '" + pub_wx_id \
              + "' and is_del = 0"
        self.cursor.execute(sql)
        self.print_with_time('update pub today_is_crawl is ' + today_is_crawl)
        self.conn.commit()

    def reset_all_pub_today_is_crawl(self):
        self.mysql_conn.ping()
        sql = 'update pub set today_is_crawl = 0'
        self.cursor.execute(sql)
        self.print_with_time('reset all pub today_is_crawl is 0')
        self.conn.commit()

    def insert_crawl_record(self, pub_id, crawl_status):
        self.mysql_conn.ping()
        self.cursor.execute(
            'insert into crawl_record'
            '(id, pub_id, crawl_status) '
            'values(%s, %s, %s)',
            (None, pub_id, crawl_status))
        self.print_with_time('insert crawl_record')
        self.conn.commit()

    def query_article(self, pub_wx_id, pub_article_title, pub_article_publish_time):
        self.mysql_conn.ping()
        sql_query = "select * from pub_article where pub_wx_id = '" + pub_wx_id \
                    + "' and pub_article_title = '" + pub_article_title + "' and pub_article_publish_time = '" \
                    + pub_article_publish_time + "'"
        count = self.cursor.execute(sql_query)
        self.print_with_time('query pub article')
        return count

    def insert_article(self, pub_wx_id, pub_name, pub_article_title, pub_article_publish_time,
                       pub_article_content_url, pub_article_cover):
        self.mysql_conn.ping()
        self.cursor.execute(
            'insert into pub_article'
            '(id, pub_wx_id, pub_name, pub_article_title, pub_article_publish_time, pub_article_content_url, '
            'pub_article_cover) '
            'values(%s, %s, %s, %s, %s, %s, %s)',
            (None, pub_wx_id, pub_name, pub_article_title, pub_article_publish_time, pub_article_content_url,
             pub_article_cover))
        self.print_with_time('insert pub article')
        self.conn.commit()

    def close(self):
        self.mysql_conn.close()

    @staticmethod
    def print_with_time(content):
        print(strftime('%Y-%m-%d %H:%M:%S'))
        print(content)
