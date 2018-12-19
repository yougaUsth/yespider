# coding=utf-8

from __future__ import unicode_literals

import os

import pyaml
from rediscluster import StrictRedisCluster
from twisted.pair import ip

from www.utils import ip_utils

config_path = os.path.join(os.path.abspath(__file__), "database.yml")
yaml = pyaml.yaml.safe_load(open(config_path))


redis_config = yaml["redis"]

startup_nodes = [{"host": node.split(":")[0], "port": node.split(":")[1]} for node in redis_config]

redis_client = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

# dispatcher config

DISPATCHER_KEY = 'dispatcher_service'

# internal use
STATE_WAITING = 0  # stand by state
STATE_PENDING = 1  # ready to work
STATE_DISPATCH = 2  # working

# 获取本地IP
UID = ip_utils.get_ip()

STATE_DICT = {
    STATE_WAITING: 'waiting',
    STATE_PENDING: 'pending',
    STATE_DISPATCH: 'dispatch'
}
