# coding=utf-8
from __future__ import unicode_literals

import time
from datetime import datetime

import pytz

_utc_tz = pytz.utc


def now_lambda():
    return _utc_tz.localize(datetime.utcnow())


def now_timestamp():
    return time.time()


def main():
    pass

if __name__ == '__main__':
    main()
