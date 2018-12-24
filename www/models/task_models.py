# coding=utf-8

from __future__ import unicode_literals

from flask_mongoengine import Document
from mongoengine import StringField, BooleanField, ListField, DateTimeField,EmbeddedDocumentField

from www.utils.time_utils import now_lambda


class RuleModel(Document):
    """
    附加字段的解析规则
    """
    meta = {
        'abstract': True,
        'strict': False
    }
    name = StringField(required=True)  # 解析任务名
    x_path = StringField()  # x-path 解析规则
    re_path = StringField()  # re 解析规则


class BaseTask(Document):
    """
    任务基类
    """

    meta = {
        "collection": "task_config",
        "db_alias": "",
        "strict": False
    }

    id = StringField(required=True)

    task_name = StringField()  # 任务名称
    start_url = StringField(required=True)

    corntab = StringField(default="*/5 * * * * ")
    is_active = BooleanField(default=False)
    spider_name = StringField(required=True)  # 抓取程序
    parser_name = StringField(required=True)  # 解析程序
    parser_rules = ListField(EmbeddedDocumentField(RuleModel))  # 附加字段解析规则
    # creater = EmbeddedDocumentField(User)
    created_at = DateTimeField(default=now_lambda)
    update_at = DateTimeField()
    deleted_at = DateTimeField()



