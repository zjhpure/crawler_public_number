# coding: utf-8
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

    def query_public_number(self):
        self.mysql_conn.ping()
        sql_query = 'select * from public_number where is_del = 0 and today_is_crawl = 0'
        self.cursor.execute(sql_query)
        self.print_with_time('query public_number all')
        return self.cursor.fetchall()

    def query_public_number_by_biz(self, public_number_biz):
        self.mysql_conn.ping()
        sql_query = "select * from public_number where is_del = 0 and today_is_crawl = 0 " \
                    "and public_number_biz = '" + public_number_biz + "'"
        self.cursor.execute(sql_query)
        self.print_with_time('query public_number by biz, biz = ' + public_number_biz)
        return self.cursor.fetchall()

    def update_public_number_today_is_crawl(self, public_number_wechat_id, today_is_crawl):
        self.mysql_conn.ping()
        sql = 'update public_number set today_is_crawl = ' + today_is_crawl \
              + " where public_number_wechat_id = '" + public_number_wechat_id \
              + "' and is_del = 0"
        self.cursor.execute(sql)
        self.print_with_time('update public_number today_is_crawl is ' + today_is_crawl)
        self.conn.commit()

    def reset_all_public_number_today_is_crawl(self):
        self.mysql_conn.ping()
        sql = 'update public_number set today_is_crawl = 0'
        self.cursor.execute(sql)
        self.print_with_time('reset all public_number today_is_crawl is 0')
        self.conn.commit()

    def insert_crawl_record(self, public_number_id, crawl_status):
        self.mysql_conn.ping()
        self.cursor.execute(
            'insert into crawl_record'
            '(id, public_number_id, crawl_status) '
            'values(%s, %s, %s)',
            (None, public_number_id, crawl_status))
        self.print_with_time('insert crawl_record')
        self.conn.commit()

    def query_public_number_article(self, public_number_wechat_id, public_number_article_title,
                                    public_number_article_publish_time):
        self.mysql_conn.ping()
        sql_query = "select * from public_number_article where public_number_wechat_id = '" + public_number_wechat_id \
                    + "' and public_number_article_title = '" + public_number_article_title \
                    + "' and public_number_article_publish_time = '" + public_number_article_publish_time + "'"
        count = self.cursor.execute(sql_query)
        self.print_with_time('query public_number article')
        return count

    def insert_public_number_article(self, public_number_wechat_id, public_number_name, public_number_article_title,
                                     public_number_article_publish_time, public_number_article_content_url,
                                     public_number_article_cover):
        self.mysql_conn.ping()
        self.cursor.execute(
            'insert into public_number_article'
            '(id, public_number_wechat_id, public_number_name, public_number_article_title, '
            'public_number_article_publish_time, public_number_article_content_url, public_number_article_cover) '
            'values(%s, %s, %s, %s, %s, %s, %s)',
            (None, public_number_wechat_id, public_number_name, public_number_article_title,
             public_number_article_publish_time, public_number_article_content_url, public_number_article_cover))
        self.print_with_time('insert public_number article')
        self.conn.commit()

    def close(self):
        self.mysql_conn.close()

    @staticmethod
    def print_with_time(content):
        print(strftime('%Y-%m-%d %H:%M:%S'))
        print(content)
