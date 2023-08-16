#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Version: 3.11.4
Creator: 孙一凡-莫无煜
Create Date: 2023/7/21

"""
import sys
import time

__all__ = [
    'time_start',
    'time_get_seconds',
    'time_check_interval',
    'time_wait_until',
]


def time_start(key='__default__'):
    MoVoidTimer.start(key)


def time_get_seconds(key, digits=2):
    return MoVoidTimer.get_total_seconds(key, digits)


def time_check_interval(interval=1, key='__default__', refresh=True):
    return MoVoidTimer.check_interval(interval, key, refresh)


def time_wait_until(wait_second=1, key='__default__', refresh=True):
    MoVoidTimer.wait_until(wait_second, key, refresh)


def time_backup(to_key, from_key='__default__'):
    MoVoidTimer.backup(to_key, from_key)


class MoVoidTimer:
    time_dict = {
        '__default__': time.time()
    }

    @classmethod
    def start(cls, key='__default__'):
        if key not in cls.time_dict:
            cls.time_dict[key] = 0
        cls.time_dict[key] = time.time()

    @classmethod
    def get_total_seconds(cls, key, digits=2):
        now_time = time.time()
        if key not in cls.time_dict:
            cls.time_dict[key] = now_time
        return round(now_time - cls.time_dict[key], digits)

    @classmethod
    def check_interval(cls, interval=1, key='__default__', refresh=True):
        now_time = time.time()
        if key in cls.time_dict:
            if now_time - cls.time_dict[key] > interval:
                re_bool = True
            else:
                re_bool = False
        else:
            re_bool = False
        if refresh:
            cls.time_dict[key] = time.time()
        return re_bool

    @classmethod
    def wait_until(cls, wait_second=1, key='__default__', refresh=True):
        now_time = time.time()
        if key in cls.time_dict:
            if now_time - cls.time_dict[key] <= wait_second:
                time.sleep(wait_second + cls.time_dict[key] - now_time)
        else:
            time.sleep(wait_second)
        if refresh:
            cls.time_dict[key] = time.time()

    @classmethod
    def backup(cls, to_key, from_key='__default__'):
        if to_key in cls.time_dict:
            print('backup to_key {} exists.we will cover it.'.format(to_key), file=sys.stderr)
        if from_key not in cls.time_dict:
            raise KeyError('backup from_key {} does not exist.'.format(from_key))
        cls.time_dict[to_key] = cls.time_dict[from_key]


if __name__ == '__main__':
    pass
