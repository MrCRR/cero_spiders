# coding=utf-8
"""
title: 
author: cero
Create on: 2018/4/27
"""
import scrapy
from cero_spiders.items import WeixinSogouItem


class WeixinSogouSpider(scrapy.Spider):
    name = 'WeixinSogou'

    start_urls = [
        'http://weixin.sogou.com/weixin?type=2&s_from=input&query=%E5%85%A5%E7%BE%A4&ie=utf8&_sug_=n&_sug_type_=&w=01019900&sut=3389&sst0=1524878374117&lkt=1%2C1524878374013%2C1524878374013'
    ]

    def parse(self, response):
        for box in response.css('.txt-box'):
            article = box.css('a::attr(href)').extract_first()
            if article:
                yield scrapy.Request(article, callback=self.parse_article)

        next_page = response.css('#sogou_next').css('a::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_article(self, response):
        item = WeixinSogouItem()
        item['title'] = response.css('.rich_media_title').css('h2::text').extract_first()
        item['image_urls'] = response.css('img::attr(data-src)').extract()
        yield item
