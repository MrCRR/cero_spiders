# coding=utf-8
"""
title: 
author: cero
Create on: 2018/4/25
"""
import scrapy
from cero_spiders.items import IndeedReviewItem


class IndeedReviewSpider(scrapy.Spider):
    name = 'IndeedReview'

    start_urls = [
        'https://www.indeed.com/cmp/1st-Source-Bank/reviews',
    ]

    def parse(self, response):
        for selector in response.css('.cmp-review-container'):
            item = IndeedReviewItem()
            item['id'] = selector.css('.cmp-review::attr(data-tn-entityid)').extract_first()
            item['head'] = selector.css('.cmp-review-title').css('span::text').extract_first()
            item['content'] = selector.css('.cmp-review-text').css('span::text').extract_first()
            item['pro'] = selector.css('.cmp-review-pro-text::text').extract_first()
            item['con'] = selector.css('.cmp-review-con-text::text').extract_first()
            yield item
            # yield self.parse_review(container)

        next_page = response.css('.cmp-Pagination-link--nav::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_review(self, selector):
        item = IndeedReviewItem()
        item['head'] = selector.css('.cmp-review-title').css('span::text').extract_first()
        item['content'] = selector.css('.cmp-review-text').css('span::text').extract_first()
        item['pro'] = selector.css('.cmp-review-pro-text').extract_first()
        item['con'] = selector.css('.cmp-review-con-text').extract_first()
        yield item
