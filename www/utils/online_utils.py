# coding=utf-8

from __future__ import unicode_literals

from config import redis_client

from www.utils.time_utils import now_lambda, now_timestamp


class OnlineLock(object):
    _redis = redis_client
    """
    red lock 暂时没用
    """
    def __init__(self, key, auto_release=True):
        self._key = "{}:{}".format(self.__class__.__name__, key)
        self._locked = False
        self._auto_release = auto_release

    def lock(self):
        """
        获得锁
        """
        if not self._locked:
            self._redis.watch(self._key)
            try:
                self._locked = self._redis.setnx(self._key, now_timestamp())
            except:
                return False
            if self._locked:
                self._redis.expire(self._key, 10)
            else:
                t = now_lambda() - self._redis.get(self._key)
                # 超时强制释放
                if t > 10:
                    self.release(force=True)
                    self._locked = self._redis.setnx(self._key, now_timestamp())
        return self._locked

    def release(self, force=False):
        """
        释放锁
        """
        if self._locked or force:
            self._locked = False
            self._redis.delete(self._key)

