# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from ScrapyRedis.settings import SQL_DATETIME_FORMAT


class ScrapyredisItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MovieItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class MovieItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    front_image_url = scrapy.Field()
    movie_time = scrapy.Field()
    url_object_id = scrapy.Field()
    movie_link_gao = scrapy.Field()
    movie_link_pu = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
        insert into movie(title,url,url_object_id,front_image_url,movie_link_gao,movie_link_pu,movie_time,crawl_time) 
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """
        params = (
            self['title'],
            self['url'],
            self['url_object_id'],
            self['front_image_url'],
            self['movie_link_gao'],
            self['movie_link_pu'],
            self['movie_time'],
            self['crawl_time'].strftime(SQL_DATETIME_FORMAT),
        )
        return insert_sql, params
