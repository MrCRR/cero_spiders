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
    custom_settings = {
        'ITEM_PIPELINES': {
            'cero_spiders.pipelines.BuffPipeline': 300
        }
    }

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
            item['market_name'] = item_obj['market_hash_name']
            item['name'] = item_obj['name']
            item['buy_max_price'] = item_obj['buy_max_price']
            item['sell_min_price'] = item_obj['sell_min_price']
            item['steam_price_cny'] = item_obj['goods_info']['steam_price_cny']
            yield item

        if page_num < total_page:
            self.page_num = str(page_num + 1)
            yield scrapy.Request(self.start_urls[0].format(self.page_num, self.ts), self.parse)


class SteamSpider(scrapy.Spider):
    name = 'steam'
    page_num = 0
    page_size = 100

    start_urls = [
        'https://steamcommunity.com/market/search/render/?query=&start={}&count={}&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=570&norender=1',
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'cero_spiders.pipelines.SteamPipeline': 300
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield FormRequest(url.format(self.page_num*self.page_size, self.page_size), method='GET')

    def parse(self, response):
        res = json.loads(response.body)
        item_objs = res['results']
        start = res['start']
        page_size = res['pagesize']
        total_count = res['total_count']
        for item_obj in item_objs:
            item = BuffItem()
            descs = item_obj['asset_description'].get('descriptions')
            if descs:
                for desc in descs:
                    if 'Used By' in desc['value']:
                        item['hero'] = desc['value'].split(' ')[-1]
                        break
            item['market_name'] = item_obj['hash_name']
            item['buy_max_price'] = item_obj['sale_price_text'].split('$')[-1]
            item['sell_min_price'] = item_obj['sell_price_text'].split('$')[-1]
            yield item

        if start + page_size < total_count:
            yield scrapy.Request(self.start_urls[0].format(start+page_size, self.page_size), callback=self.parse)
