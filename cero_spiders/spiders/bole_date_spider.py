import scrapy
from cero_spiders.items import DateGirlItem

import re


class BoleDateSpider(scrapy.Spider):
    name = "BoleDate"

    start_urls = [
            'http://date.jobbole.com',
    ]

    def parse(self, response):
        for rec in response.css('h3.p-tit').css('a::attr(href)').extract():
            yield scrapy.Request(rec, callback=self.parse_girl)

        next_page = response.xpath('//li[@id="pagination-next-page"]/a/@href').extract()
        if next_page:
            yield scrapy.Request(next_page[0], self.parse)

    def parse_girl(self, response):
        item = DateGirlItem()
        item['id'] = re.search('\d+', response.url).group()
        item['url'] = response.url
        item['title'] = response.css('.p-tit-single::text').extract_first()
        item['introduce'] = response.css('div.p-entry').css('p::text').extract()
        item['images'] = response.css('.alignnone').xpath('@src').extract()
        yield item
