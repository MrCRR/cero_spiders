import scrapy
from cero_spiders.items import DateGirlItem

import re


class DotaSpider(scrapy.Spider):
    name = "dota"

    start_urls = [
        'https://www.c5game.com/dota.html',
        'http://www.dotasell.com/Search/',
        'https://www.stmbuy.com/dota2',
        'https://www.igxe.cn/dota2/570',
        'https://buff.163.com/market/?game=dota2#tab=selling&page_num=1',
        'https://dmarket.com/ingame-items/item-list/dota2-skins',
    ]

    def parse(self, response):
        for rec in response.css('h3.p-tit').css('a::attr(href)').extract():
            yield scrapy.Request(rec, callback=self.parse_girl)

        next_page = response.xpath('//li[@id="pagination-next-page"]/a/@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page, self.parse)

    def parse_girl(self, response):
        item = DateGirlItem()
        item['id'] = re.search('\d+', response.url).group()
        item['url'] = response.url
        item['title'] = response.css('.p-tit-single::text').extract_first()
        item['introduce'] = response.css('div.p-entry').css('p::text').extract()
        item['images'] = response.css('.alignnone').xpath('@src').extract()
        item['likes'] = response.css('h10::text').extract_first()
        yield item
