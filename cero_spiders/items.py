# -*- coding: utf-8 -*-
import scrapy


class DateGirlItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    introduce = scrapy.Field()
    images = scrapy.Field()
    likes = scrapy.Field()
