# coding=utf-8
from __future__ import unicode_literals

import re

from lxml import etree
from www.models.task_models import BaseTaskModel


class BaseParser(object):
    # 加载任务基类
    TASK = BaseTaskModel

    def __init__(self, name, task_id):
        self.name = name

    def _parser_article(self, task_id, response):
        """
        解析字段
        :param task_id:任务id
        :param response:html
        :return:
        """
        _article = dict()
        task = self.TASK.objects(id=task_id)
        # 返序列化html
        selector = etree.HTML(response)

        for rule in task.parser_rules:
            # 解析xpath
            if rule.x_path:
                res = selector.xpath('//span//text()')
            # 解析正则模块
            elif rule.re_path:
                res = re.compile(rule.re_path, re.U | re.S)
            else:
                res = "<p><p/>"
            if isinstance(list, res):
                res = ",".join(res)

            _article[rule.name] = res
        self.articles = _article


