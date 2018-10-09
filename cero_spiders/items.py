# -*- coding: utf-8 -*-
import scrapy


class DateGirlItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    introduce = scrapy.Field()
    images = scrapy.Field()
    likes = scrapy.Field()


class IndeedReviewItem(scrapy.Item):
    id = scrapy.Field()
    head = scrapy.Field()
    content = scrapy.Field()
    pro = scrapy.Field()
    con = scrapy.Field()


class WeixinSogouItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()


class BuffItem(scrapy.Item):
    hero = scrapy.Field()
    name = scrapy.Field()
    buy_max_price = scrapy.Field()
    sell_min_price = scrapy.Field()
    steam_price_cny = scrapy.Field()
