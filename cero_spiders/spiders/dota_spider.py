import scrapy
from scrapy.http import FormRequest
from cero_spiders.items import BuffItem
import time
import re
import json

markets = [
        'https://www.c5game.com/dota.html',
        'http://www.dotasell.com/Search/',
        'https://www.stmbuy.com/dota2',
        'https://www.igxe.cn/dota2/570',
        'https://buff.163.com/market/?game=dota2#tab=selling&page_num=1',
        'https://dmarket.com/ingame-items/item-list/dota2-skins',
        'https://steamcommunity.com/market/search?appid=570'
    ]


class BuffSpider(scrapy.Spider):
    name = 'buff'
    page_num = 1
    ts = int(time.time() * 1000)

    start_urls = [
         'https://buff.163.com/api/market/goods?game=dota2&page_num={}&_={}',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield FormRequest(url.format(self.page_num, self.ts), method='GET')

    def parse(self, response):
        res = json.loads(response.body)['data']
        item_objs = res['items']
        page_num = res['page_num']
        total_page = res['total_page']
        for item_obj in item_objs:
            item = BuffItem()
            if item_obj['goods_info']['info']['tags'].get('hero'):
                item['hero'] = item_obj['goods_info']['info']['tags']['hero']['localized_name']
            item['name'] = item_obj['name']
            item['buy_max_price'] = item_obj['buy_max_price']
            item['sell_min_price'] = item_obj['sell_min_price']
            item['steam_price_cny'] = item_obj['goods_info']['steam_price_cny']
            yield item

        if page_num < total_page:
            self.page_num = str(page_num + 1)
            yield scrapy.Request(self.start_urls[0].format(self.page_num, self.ts), self.parse)

