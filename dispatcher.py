# coding=utf-8
from __future__ import unicode_literals

import json
import threading
import time

from config import redis_client, STATE_DISPATCH, STATE_PENDING, STATE_WAITING, UID
from www.models.task_models import BaseTask

BEAT_INTERVAL = 5
_state_ = 2


class HeartBeat(threading.Thread):
    """
    调度器心跳检查
    """

    __expire = 5 * BEAT_INTERVAL

    def __init__(self):
        super(HeartBeat, self).__init__()
        self._key = "dispatcher_service"
        self._redis = redis_client
        self._expire = BEAT_INTERVAL * 2

    def _on_beat(self, rmsg):
        print 'rmsg: %s' % rmsg
        # mine = {'status': _state_, 'refresh': time.time()}
        msg = json.loads(rmsg) if rmsg else {}
        _msg = {}
        main_nodes = {}
        pending_nodes = {}

        self.__clear_expire(msg)

        for uid in msg.keys():
            _s = msg[uid].get('status')
            if _s == STATE_DISPATCH:
                main_nodes[uid] = msg.pop(uid)
            elif _s == STATE_PENDING:
                pending_nodes[uid] = msg.pop(uid)
        _len = len(main_nodes)

        # if no working dispatcher
        if _len == 0:
            if _state_ == STATE_WAITING:
                if pending_nodes:
                    # any node is pending already
                    self.__on_keep()
                else:
                    self.__on_pending()
            elif _state_ == STATE_PENDING and _msg.get('status') == STATE_PENDING:
                self.__on_dispatch()
            else:
                self.__on_keep()
        else:
            if _state_ != STATE_WAITING:
                self.__on_waiting()
            else:
                self.__on_keep()

        message = {UID: {'status': _state_, 'refresh': time.time()}}
        message.update(msg)
        message.update(main_nodes)
        message.update(pending_nodes)
        return json.dumps(message)

    @classmethod
    def __clear_expire(cls, nodes):
        """
        clear out dates
        :param nodes:
        """
        for uid in nodes.keys():
            if time.time() - nodes[uid]['refresh'] > cls.__expire:
                nodes.pop(uid)

    @staticmethod
    def __on_waiting():
        pass

    @staticmethod
    def __on_pending():
        pass

    @staticmethod
    def __on_dispatch():
        pass

    def __on_keep(self):
        pass

    def run(self):
        reties = 0
        while 1:
            # replace mc to redis
            rmsg = self._redis.gets(self._key)
            msg = self._on_beat(rmsg)
            if msg:
                if self._redis.append(self._key, msg):
                    reties = 0
                    time.sleep(BEAT_INTERVAL)
                else:
                    reties += 1
            else:
                if self._redis.add(self._key, msg, self._expire):
                    reties = 0
                    time.sleep(BEAT_INTERVAL)
                else:
                    reties += 1
            if reties > 3:
                print 'retries too much, may net error'

                time.sleep(self.__expire + 1)


def load_tasks(task_id=None):
    """
    加载任务池
    :return:
    """
    query = dict()
    if not task_id:
        return

    if isinstance(task_id, list):
        query["id__in"] = task_id
    if isinstance(task_id, basestring):
        query["id"] = task_id
    tasks = BaseTask.objects.filter(**query)

