# coding=utf-8

from __future__ import unicode_literals

from urllib2 import Request


class BaseSpider(object):

    def __init__(self, parser, task_id, task_name, custom_article=None, subscribe=None, anchor=None, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.task_id = task_id
        self.parser = parser
        self._extra = {'task_id': task_id, 'task_name': task_name}
        self.custom_article = custom_article
        self.subscribe = subscribe
        if anchor:
            self.anchor = anchor  # 相当于重新生成url 再次被调度
        else:
            self.anchor = self.parser.front_url.split('#')[-1] if '#' in self.parser.front_url else None  # for filter

    def _parse_index(self, response, callback=None):
        callback = callback if callable(callback) else self._parse_article
        _extra_url = self._extra.copy()
        # 解析response 获取链接列表
        for i, url in enumerate(self.parser.parse_index(response)):
            _meta = {}
            if isinstance(url, tuple):
                url, _meta = url
            if self.custom_article:
                url = self.custom_article

            if not url:
                continue
            _meta['_index'] = i + 1
            url = response.urljoin(url.replace('\\/', '/'))
            url = url.replace(':80/', '/')  
            if self.task_id == 'test_index':
                yield {"url": url}
                continue
            _extra_url['url'] = url
            request = Request(url, callback)
            request.meta.update(_meta)

            request.meta['dupefilter'] = None
            if self.anchor:
                request.meta['anchor'] = self.anchor

            yield request
            if self.task_id in {'test_article', 'test_subscribe'}:
                break

    def _parse_article(self, response):
        items = self.parser.parse_article(response)
        for item in items:
            if isinstance(item, Request):
                item.callback = self._parse_article
                yield item
            elif not item:
                yield None
            else:
                _extra_url = self._extra.copy()
                url = item.get('url', '')
                if url.startswith('http'):
                    _extra_url['url'] = url
                yield item