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
