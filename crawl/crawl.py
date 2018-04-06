# -*- coding: utf-8 -*-
import datetime
import json
import random
import re
import time
import traceback
from time import strftime

import requests
from lxml import etree
from redis import StrictRedis
from cfg.cfg import redis_db
from db.mysql_operate import MysqlOperate


class WechatPubArticleSpider(object):
    headers = {
        'Host': 'mp.weixin.qq.com',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.tencent.mm'
    }
    mysql_operate = MysqlOperate()

    def start_requests(self):
        while True:
            # 每隔5-10s取一次redis数据
            n = random.randint(5, 10)
            self.print_with_time('sleep ' + str(n) + 's')
            time.sleep(n)
            # 从redis获取请求参数和biz值
            x_wechat_key, x_wechat_uin, user_agent, cookie, url = self.operate_redis()
            headers = self.headers
            headers['x-wechat-key'] = x_wechat_key
            headers['x-wechat-uin'] = x_wechat_uin
            headers['User-Agent'] = user_agent
            headers['Cookie'] = cookie
            biz = url.split('&')[1].split('biz=')[1]
            # 通过biz值查询数据库里是否有今天未爬取的此公众号
            result = self.mysql_operate.query_pub_by_biz(biz=biz)
            self.print_with_time(result)
            if len(result) > 0:
                row = result[0]
                pub_id = row[0]
                pub_wx_id = row[1]
                pub_name = row[2]
                try:
                    self.print_with_time('pub_wx_id:' + pub_wx_id + ' pub_name:' + pub_name)
                    response = requests.request('GET', url, headers=headers)
                    meta = {'pub_wx_id': pub_wx_id, 'pub_name': pub_name, 'pub_id': pub_id}
                    article_num = self.parse(response, meta)
                    # 若今天的文章数量为0,可能公众号还没有发表文章
                    if article_num > 0:
                        # 今天已爬取,标记为1,这里一旦有一次今天爬取成功了,就标记为今天已爬取
                        # 大多数公众号一天只能发文一次,除了少数早期的公众号可以发文多次,新申请应该都是一天只能发文一次
                        self.mysql_operate.update_pub_today_is_crawl(pub_wx_id=str(pub_wx_id), today_is_crawl=str(1))
                    # 录入爬取记录,1为爬取成功
                    self.mysql_operate.insert_crawl_record(pub_id=pub_id, crawl_status=1)
                except Exception as e:
                    self.print_with_time(e)
                    traceback.print_exc()
                    self.print_with_time(
                        'crawl failure, ' + 'pub_wx_id:' + pub_wx_id + ', pub_name:' + pub_name)
                    # 录入爬取记录,0为爬取失败
                    self.mysql_operate.insert_crawl_record(pub_id=pub_id, crawl_status=0)

    def parse(self, response, meta):
        # print(response.text)
        if '<h2 class="weui_msg_title">操作频繁，请稍后再试</h2>' in response.text:
            self.print_with_time('操作频繁')
            return 0
        if '<p>请在微信客户端打开链接。</p>' in response.text > 0:
            self.print_with_time('连接失效')
            return 0
        # 今天的文章数量
        article_today_num = 0
        # 获取公众号历史消息第一页
        msg_list = json.loads(re.findall(r'{"list":.*]}', response.text.replace('&quot;', '"'))[0])
        for sel in msg_list['list']:
            if 'app_msg_ext_info' in sel:
                # 获取公众号文章发表时间
                ltime = time.localtime(sel['comm_msg_info']['datetime'])
                day = time.strftime('%Y-%m-%d', ltime)
                # 今天
                today = datetime.date.today()
                # 昨天
                yesterday = today - datetime.timedelta(days=1)
                # 只抓取今天和昨天的文章,抓取昨天的文章是为了避免可能出现在凌晨前发文,而由于爬取的循环刚好在凌晨的前后而错过了爬取
                # 之抓取今天和昨天的文章也是为了减少访问次数,微信对同一个微信号一天访问公众号历史消息的次数是有限制的
                # 若超过了次数,大概需要等待12小时后才能恢复
                if str(yesterday) == day:
                    content_url = sel['app_msg_ext_info']['content_url']
                    # 发表后又删除了的文章content_url会为空
                    if content_url != '':
                        url_temp = content_url.split('/s?')[1]
                        url = 'https://mp.weixin.qq.com/s?' + re.sub('amp;', '', url_temp)
                        meta['cover'] = sel['app_msg_ext_info']['cover'].replace('\\', '')
                        self.print_with_time(url)
                        meta['url'] = url
                        response = requests.request('GET', url, headers=self.headers)
                        self.get_pub_article(response, meta)
                    for s in sel['app_msg_ext_info']['multi_app_msg_item_list']:
                        # 发表后又删除了的文章content_url会为空
                        if s['content_url'] != '':
                            muti_url_temp = s['content_url'].split('/s?')[1]
                            muti_url = 'https://mp.weixin.qq.com/s?' + re.sub('amp;', '', muti_url_temp)
                            meta['cover'] = s['cover'].replace('\\', '')
                            self.print_with_time(muti_url)
                            meta['url'] = muti_url
                            response = requests.request('GET', muti_url, headers=self.headers)
                            self.get_pub_article(response, meta)
                if str(today) == day:
                    content_url = sel['app_msg_ext_info']['content_url']
                    # 发表后又删除了的文章content_url会为空
                    if content_url != '':
                        url_temp = content_url.split('/s?')[1]
                        url = 'https://mp.weixin.qq.com/s?' + re.sub('amp;', '', url_temp)
                        meta['cover'] = sel['app_msg_ext_info']['cover'].replace('\\', '')
                        self.print_with_time(url)
                        meta['url'] = url
                        response = requests.request('GET', url, headers=self.headers)
                        self.get_pub_article(response, meta)
                        article_today_num = article_today_num + 1
                    for s in sel['app_msg_ext_info']['multi_app_msg_item_list']:
                        # 发表后又删除了的文章content_url会为空
                        if s['content_url'] != '':
                            muti_url_temp = s['content_url'].split('/s?')[1]
                            muti_url = 'https://mp.weixin.qq.com/s?' + re.sub('amp;', '', muti_url_temp)
                            meta['cover'] = s['cover'].replace('\\', '')
                            self.print_with_time(muti_url)
                            meta['url'] = muti_url
                            response = requests.request('GET', muti_url, headers=self.headers)
                            self.get_pub_article(response, meta)
                            article_today_num = article_today_num + 1
        return article_today_num

    def get_pub_article(self, response, meta):
        pub_id = meta['pub_id']
        pub_wx_id = meta['pub_wx_id']
        pub_name = meta['pub_name']
        # 把响应返回的文本转换为结点对象,xpath方法要用结点对象
        html = etree.HTML(response.text)
        # 若文章是转载的
        if len(html.xpath('//*[@class="original_page"]')) > 0:
            # 获取原文章的连接,这里的网址是重定向网址
            url = html.xpath('//*[@id="js_share_source"]/@href')[0].strip()
            self.print_with_time('pub_article redirect to: ' + url)
            response = requests.request('GET', url, headers=self.headers)
            self.get_pub_article(response, meta)
        # 若文章不是转载的
        else:
            pub_article_title = html.xpath('//*[@id="activity-name"]/text()')[0].strip()
            self.print_with_time('pub_article_title:' + pub_article_title)
            pub_article_publish_time = html.xpath('//*[@id="post-date"]/text()')[0].strip()
            self.print_with_time('pub_article_publish_time:' + pub_article_publish_time)
            count = self.mysql_operate.query_article(pub_wx_id=pub_wx_id, pub_article_title=pub_article_title,
                                                     pub_article_publish_time=pub_article_publish_time)
            self.print_with_time('pub_wx_id:' + pub_wx_id + ' pub_name:' + pub_name)
            # 通过比较文章的标题和发表时间来判断文章是否已经爬取过,以爬取过的不再爬取
            if count <= 0:
                # 爬取文章封面
                pub_article_cover = meta['cover']
                # 文章链接
                pub_article_content_url = meta['url']
                # 这里说明一下,封面和文章内容,需要下载下来,然后上传到云存储上(比如:七牛云),这里就不详细解说了
                # response.text可以获取到文章内容
                # 文章信息录入数据库
                self.mysql_operate.insert_article(pub_wx_id=pub_wx_id, pub_name=pub_name,
                                                  pub_article_title=pub_article_title,
                                                  pub_article_publish_time=pub_article_publish_time,
                                                  pub_article_content_url=pub_article_content_url,
                                                  pub_article_cover=pub_article_cover)
                self.print_with_time(
                    'pub_id:' + str(pub_id) + ' pub_wx_id:' + pub_wx_id + ' pub_name:' + pub_name +
                    ' pub_article_title:' + pub_article_title +
                    ' pub_article_publish_time:' + pub_article_publish_time +
                    ' pub_article_content_url:' + pub_article_content_url +
                    ' pub_article_cover:' + pub_article_cover)

    def operate_redis(self):
        x_wechat_key = None
        x_wechat_uin = None
        user_agent = None
        cookie = None
        url = None
        flag = True
        while flag:
            self.print_with_time('prepare to connect redis')
            # 连接redis
            redis = StrictRedis(host=redis_db['host'], port=redis_db['port'], password=redis_db['password'])
            # 从左边pop出数据,b表示若没有数据,则会一直堵塞等待
            info = str(redis.blpop('crawl_pub_click')[1], encoding='utf-8')
            info = info.split('&&')
            self.print_with_time(info)
            # 获取从anyproxy拦截公众号历史消息请求时储存在redis上的时间戳
            t = info[4]
            # 获取当前时间戳
            now = int(time.time())
            self.print_with_time('now: ' + str(now))
            # 公众号历史消息请求使用的参数有时效性,为了避免请求失效,这里时间戳不大于当前时间戳500的时间戳,即500秒
            # 还需url包含pass_ticket,因为有些网址不完整,需要去掉,如下:
            # 有时网址是这样:https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={biz值}&scene=124&
            # 有时网址是这样:https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={biz值}&scene=124&devicetype=android-23&version=26060135&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket={pass_ticket值}&wx_header=1
            # 要把前者去掉
            if now - int(t) <= 500 and 'pass_ticket' in info[5]:
                flag = False
                x_wechat_key = info[0]
                x_wechat_uin = info[1]
                user_agent = info[2]
                cookie = info[3]
                url = info[5]
                self.print_with_time('x_wechat_key: ' + x_wechat_key)
                self.print_with_time('x_wechat_uin: ' + x_wechat_uin)
                self.print_with_time('user_agent: ' + user_agent)
                self.print_with_time('cookie: ' + cookie)
                self.print_with_time('time: ' + t)
        self.print_with_time('get pub headers by redis success')
        return x_wechat_key, x_wechat_uin, user_agent, cookie, url

    @staticmethod
    def print_with_time(content):
        print(strftime('%Y-%m-%d %H:%M:%S'))
        print(content)


if __name__ == '__main__':
    wechat_pub_article = WechatPubArticleSpider()
    wechat_pub_article.start_requests()
