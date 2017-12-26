# -*- coding: utf-8 -*-
import os
import pandas as pd

from scrapy.exceptions import DropItem
from items import DateGirlItem
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
