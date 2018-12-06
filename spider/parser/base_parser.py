# coding=utf-8
from __future__ import unicode_literals

import re

from www.models.task_models import BaseTaskModel


class BaseParser(object):
    # 加载任务基类
    TASK = BaseTaskModel

    def __init__(self, name, task_id):
        self.name = name

    def _parser_article(self, task_id, response):
        """
        解析字段
        :param task_id:
        :param response:
        :return:
        """
        _article = dict()
        task = self.TASK.objects(id=task_id)
        for rule in task.parser_rules:
            # 解析xpath
            if rule.x_path:
                res = response.xpath(rule.x_path)
            # 解析正则模块
            elif rule.re_path:
                res = re.compile(rule.re_path, re.U | re.S)
            else:
                res = "<p><p/>"
            if isinstance(list, res):
                res = ",".join(res)

            _article[rule.name] = res
        self.articles = _article


