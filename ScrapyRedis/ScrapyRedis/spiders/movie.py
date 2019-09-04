# -*- coding: utf-8 -*-
# @Time    : 2019-08-30 14:41
# @Author  : Griy
# @Email   : Griy26d@163.com
# @File    : movie.py
# @Software : PyCharm

from urllib.parse import urljoin
from scrapy_redis.spiders import RedisSpider
from ScrapyRedis.items import MovieItemLoader, MovieItem
from ScrapyRedis.utils.common import get_md5
from datetime import datetime
from urllib import parse
from scrapy_splash import SplashRequest
import time


class MovieSpider(RedisSpider):
    name = 'movie'
    allowed_domians = ['https://******.com']
    redis_key = 'movie:start_urls'

    def parse(self, response):
        '''
           1.解析电影列表中的所有url  并交给scrapy 解析每个页面的数据
           2.将下一页的url交给scrapy
           :param response:
           :return:
         '''
        post_nodes = response.xpath('//*[@class="lul"]/li')

        for post_node in post_nodes:
            post_url = urljoin("https://******.com", post_node.xpath('./a/@href').extract_first())
            image_url = post_node.xpath('./a/div/img/@data-original').extract_first()
            title = post_node.xpath('./a/@title').extract_first()
            movie_time = post_node.xpath('./a/span/text()').extract_first()
            # 获取每页列表中的视频链接
            yield SplashRequest(post_url, self.parse_detail,
                                args={'wait': 3},
                                meta={"front-image-url": image_url,
                                      "title": title,
                                      "movie_time": movie_time})

        next_url = response.xpath('//*[@class="span1"]/a/@href').extract()[-1]
        if next_url:
            yield SplashRequest(url=parse.urljoin("https://******.com", next_url),
                                args={'wait': 3},
                                callback=self.parse)

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
