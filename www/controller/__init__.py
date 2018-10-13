# coding=utf-8
from __future__ import unicode_literals

import os

import pyaml

database_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.yml")

# load database config
db_config = pyaml.yaml.safe_load(open(database_config))


class SpiderConfig(object):
    # spider constant
    status = db_config["status"]
