# -*- coding: utf-8 -*-
import multiprocessing

from pub.get_pub import GetPub
from crawl.reset_crawl import ResetCrawl
from crawl.crawl import WechatPubArticleSpider


def start_get_pub():
    get_pub = GetPub()
    get_pub.query_pub_count()


def start_reset_crawl():
    reset_crawl = ResetCrawl()
    reset_crawl.run()


def start_crawl():
    wechat_pub_article = WechatPubArticleSpider()
    wechat_pub_article.start_requests()


if __name__ == '__main__':
    multiprocessing.Process(target=start_reset_crawl, name='process: start_reset_crawl').start()
    multiprocessing.Process(target=start_get_pub, name='process: get_pub').start()
    multiprocessing.Process(target=start_crawl, name='process: start_crawl').start()
