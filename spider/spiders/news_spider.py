# coding=utf-8
from __future__ import unicode_literals

from spider.spiders.base_spider import BaseSpider


class NewsSpider(BaseSpider):
    def __init__(self, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.start_url = self. _parse_index()
