# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from redis import StrictRedis
from .settings import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, REDIS_KEY


class PornhubspiderPipeline(object):
    def __init__(self):
        self.conn = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)

    def process_item(self, item, spider):
        data = json.dumps(dict(item), ensure_ascii=False)
        self.conn.lpush(REDIS_KEY, data)
        return item
