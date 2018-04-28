# -*- coding: utf-8 -*-
import os
import pandas as pd

from scrapy.exceptions import DropItem
from items import *
from cero_spiders.settings import BASE_DIR


class DateGirlPipeline(object):
    def __init__(self):
        self.date_girl_json_path = os.path.join(BASE_DIR, 'media/date_girl.json')
        if os.path.exists(self.date_girl_json_path):
            self.date_dirl_df = pd.read_json(self.date_girl_json_path, dtype=False)
            self.date_girl_ids = set(self.date_dirl_df['id'])
        else:
            self.date_dirl_df = pd.DataFrame(columns=DateGirlItem.fields.keys())
            self.date_girl_ids = set()
        self.new_date_dirl = []

    def close_spider(self, spider):
        new_date_dirl_df = pd.DataFrame(self.new_date_dirl)
        self.date_dirl_df = pd.concat((self.date_dirl_df, new_date_dirl_df))
        self.date_dirl_df.to_json(self.date_girl_json_path, orient='records')

    def process_item(self, item, spider):
        if item['id'] in self.date_girl_ids:
            raise DropItem('Data already existed!')
        elif u'【' in item['title'] or item['id'] == '4164':
            raise DropItem('Girl not single!')
        else:
            self.new_date_dirl.append(item)
        return item


class IndeedReviewPipeline(object):
    def __init__(self):
        self.review_json_path = os.path.join(BASE_DIR, 'media/indeed_review.json')
        if os.path.exists(self.review_json_path):
            self.df = pd.read_json(self.review_json_path, dtype=False)
            self.ids = set(self.df['id'])
        else:
            self.df = pd.DataFrame(columns=IndeedReviewItem.fields.keys())
            self.ids = set()
        self.new_review = []

    def close_spider(self, spider):
        new_review_df = pd.DataFrame(self.new_review)
        self.df = pd.concat((self.df, new_review_df))
        self.df.to_json(self.review_json_path, orient='records')

    def process_item(self, item, spider):
        if item['id'] in self.ids:
            raise DropItem('Data already existed!')
        else:
            self.new_review.append(item)
        return item


class WeixinSogouPipeline(object):
    def __init__(self):
        self.article_json_path = os.path.join(BASE_DIR, 'media/wexin_sogou.json')
        if os.path.exists(self.article_json_path):
            self.df = pd.read_json(self.article_json_path, dtype=False)
            self.titles = set(self.df['title'])
        else:
            self.df = pd.DataFrame(columns=WeixinSogouItem.fields.keys())
            self.titles = set()
        self.new_article = []

    def close_spider(self, spider):
        new_article_df = pd.DataFrame(self.new_article)
        self.df = pd.concat((self.df, new_article_df))
        self.df.to_json(self.article_json_path, orient='records')

    def process_item(self, item, spider):
        if item['title'] in self.titles:
            raise DropItem('Data already existed!')
        else:
            self.new_article.append(item)
        return item
