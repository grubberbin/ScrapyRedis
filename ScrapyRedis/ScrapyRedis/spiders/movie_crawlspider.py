# -*- coding: utf-8 -*-
# @Time    : 2019-08-30 17:32
# @Author  : Griy
# @Email   : Griy26d@163.com
# @File    : movie_crwalspider.py
# @Software : PyCharm

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from ScrapyRedis.items import MovieItemLoader, MovieItem
from ScrapyRedis.utils.common import get_md5
from datetime import datetime


class LagouSpider(CrawlSpider):
    name = 'movie_crawlspider'
    allowed_domains = ['tom727.com']
    start_urls = ['https://tom727.com']

    rules = (
        Rule(LinkExtractor(allow=('relese/.*',)), follow=True),
        Rule(LinkExtractor(allow=('guochanzipai/.*',)), follow=True),
        Rule(LinkExtractor(allow=('yazhouqingse/.*',)), follow=True),
        Rule(LinkExtractor(allow=('oumeixingai/.*',)), follow=True),
        Rule(LinkExtractor(allow=('oumeixingai/.*',)), follow=True),
        Rule(LinkExtractor(allow=('chengrendongman/.*',)), follow=True),
        Rule(LinkExtractor(allow=r'.*/\d+.html'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        '''
            解析页面中的详细数据
            :param response:
            :return:
        '''
        item_loader = MovieItemLoader(item=MovieItem(), response=response)
        title = response.meta.get("title", "")
        movie_time = response.meta.get("movie_time", "")
        front_image_url = response.meta.get("front-image-url", "")
        item_loader.add_value('title', [title])
        item_loader.add_value('movie_time', [movie_time])
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_xpath('movie_link_gao', '//*[@id="xunlei_nr1"]/input/@value')
        item_loader.add_xpath('movie_link_pu', '//*[@id="xunlei_nr2"]/input/@value')
        item_loader.add_value('crawl_time', datetime.now())

        movieItem = item_loader.load_item()

        yield movieItem
