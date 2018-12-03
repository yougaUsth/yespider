# coding=utf-8

from __future__ import unicode_literals

from flask_mongoengine import Document
from mongoengine import StringField, BooleanField, ListField, DictField, DateTimeField, FloatField

from www.utils.time_utils import now_lambda


class BaseTask(Document):
    """
    任务基类
    """

    meta = {
        "collection": "task_config",
        "db_alias": "",
        "strict": False
    }

    task_name = StringField()
    start_url = StringField()
    is_timed = BooleanField(default=False)
    corntab = StringField(default="/* ")

    spider_name = StringField()
    parser_name = StringField()

    title = StringField()
    price = FloatField()

    parser_rules = ListField(DictField())  # 附加字段解析规则

    created_at = DateTimeField(default=now_lambda)
    update_at = DateTimeField()
    deleted_at = DateTimeField()
