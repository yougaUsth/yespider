# coding=utf-8
from __future__ import unicode_literals

import os

import pyaml
from rediscluster import StrictRedisCluster
config_path = os.path.join(os.path.abspath(__file__), "database.yml")
yaml = pyaml.yaml.safe_load(open(config_path))


redis_config = yaml["redis"]

startup_nodes = [{"host": node.split(":")[0], "port": node.split(":")[1]} for node in redis_config]

redis_client = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)