# coding=utf-8

from __future__ import unicode_literals

from flask_mongoengine import Document
from mongoengine import StringField, FloatField, DateTimeField
from www.utils.time_utils import now_lambda


class MqTask(Document):

    meta = {
        "collection": "mq_job",
        "db_alias": "",
        "strict": False
    }

    func_name = StringField()  # 方法名称
    module_name = StringField()
    status = StringField()  # 状态
    execute_time = FloatField()  # 执行时间
    exception = StringField()  # 异常信息

    created_at = DateTimeField(default=now_lambda)
    update_at = DateTimeField()
