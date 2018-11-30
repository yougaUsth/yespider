# coding=utf-8

from __future__ import unicode_literals

from tornado import httpclient, gen, ioloop


class BaseAsyncCrawler(object):

    def __init__(self, concurrency):
        """

        :param concurrency: 并发数
        """
        self.concurrency = concurrency

    def start_urls(self):
        """
        开始url
        :return:返回起始列表
        """
        pass

    def parse_list(self, response):
        """
        解析列表页
        :param response:
        :return:
        """
        pass

    def parse_item(self, response):
        """
        解析详情页
        :param response:
        :return:
        """
        pass

    def pipe_item(self, item):
        """
        数据存储
        :param item:
        :return:
        """
        pass

    @gen.coroutine
    def request(self, req):
        try:
            response = yield httpclient.AsyncHTTPClient().fetch(req)
            sub_li = self.parse_list(response)
            for sub_list in sub_li:
                sub_res = httpclient.AsyncHTTPClient().fetch(sub_list)
                ret = self.parse_item(sub_res)
                self.pipe_item(ret)
        except Exception as e:
            print e

    @gen.coroutine
    def worker(self):
        try:
            while True:
                req = next(iter(self.start_urls()))
                yield self.request(req)
        except StopIteration:
            pass

    def run(self):
        @gen.coroutine
        def _run():
            yield [self.worker() for i in xrange(self.concurrency)]

        ioloop.IOLoop.current().run_sync(_run)
