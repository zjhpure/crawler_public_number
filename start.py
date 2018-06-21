# coding: utf-8
import multiprocessing

from public_number.get_public_number import GetPublicNumber
from crawler.reset_crawl import ResetCrawler
from crawler.crawler import PublicNumberSpider


def start_get_public_number():
    get_public_number = GetPublicNumber()
    get_public_number.query_public_number_count()


def start_reset_crawler():
    reset_crawler = ResetCrawler()
    reset_crawler.run()


def start_crawler():
    public_number_spider = PublicNumberSpider()
    public_number_spider.start_requests()


if __name__ == '__main__':
    multiprocessing.Process(target=start_reset_crawler, name='process: start_reset_crawler').start()
    multiprocessing.Process(target=start_get_public_number, name='process: start_get_public_number').start()
    multiprocessing.Process(target=start_crawler, name='process: start_crawler').start()
