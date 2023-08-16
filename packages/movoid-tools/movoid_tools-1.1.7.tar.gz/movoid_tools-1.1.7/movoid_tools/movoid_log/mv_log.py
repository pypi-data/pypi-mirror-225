#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Version: 3.11.4
Creator: 孙一凡-莫无煜
Create Date: 2023/7/18

"""
import datetime
import os
import sys
import time
import traceback
from functools import wraps

from ..movoid_config import *

__all__ = [
    'log_init',
    'log_class_label',
    'log_function_label',
    'log_print',
    'log_debug',
    'log_info',
    'log_warning',
    'log_error',
    'log_critical',
]


def log_init(config_path='config.ini', encoding='utf-8'):
    now_config = {}
    config_update_regex_rule(path=config_path, rule_dict=MoVoidLog.config_rule, ori_config=now_config, encoding=encoding)
    for path, kwargs in now_config.items():
        MoVoidLog.new_log_file(**kwargs)


def log_class_label(label: str = '__default__', level=0, error_level=3):
    if label not in MoVoidLog.log_file:
        if '__default__' in MoVoidLog.log_file:
            label = '__default__'
        else:
            if MoVoidLog.log_file:
                key = list(MoVoidLog.log_file.keys())[0]
                MoVoidLog.reset_default(key)
                label = key
            else:
                raise Exception('there is no log file set,please set one log_file to initialize!')

    def decoration(cls):
        for func_name in dir(cls):
            if not (func_name.startswith('__') and func_name.endswith('__')):
                func = getattr(cls, func_name)
                if callable(func):
                    log_level = getattr(func, 'log_level', level)
                    log_error_level = getattr(func, 'log_error_level', error_level)

                    @wraps(func)
                    def wrapping(*args, **kwargs):
                        sign = time.time()
                        log_text = '[{}]<{}><{}>{},{}'.format(sign, cls.__name__, func_name, args, kwargs)
                        MoVoidLog.write(key=label, text=log_text, level=log_level)
                        try:
                            re_func = func(*args, **kwargs)
                        except Exception as err:
                            log_text = '[{}]<{}><{}>{}'.format(sign, cls.__name__, func_name, traceback.print_exc())
                            MoVoidLog.write(key=label, text=log_text, level=log_error_level)
                        else:
                            log_text = '[{}]<{}><{}>{}'.format(sign, cls.__name__, func_name, re_func)
                            MoVoidLog.write(key=label, text=log_text, level=log_level)

                    setattr(cls, func_name, wrapping)

    return decoration


def log_class_function_level(level=1, error_level=3):
    def decoration(func):
        setattr(func, 'log_level', level)
        setattr(func, 'log_error_level', error_level)

    return decoration


def log_function_label(label: str = '__default__', level=0, error_level=3):
    if label not in MoVoidLog.log_file:
        if '__default__' in MoVoidLog.log_file:
            label = '__default__'
        else:
            if MoVoidLog.log_file:
                key = list(MoVoidLog.log_file.keys())[0]
                MoVoidLog.reset_default(key)
                label = key
            else:
                raise Exception('there is no log file set,please set one log_file to initialize!')

    def decoration(func):
        @wraps(func)
        def wrapping(*args, **kwargs):
            sign = time.time()
            log_text = '[{}]<{}>{},{}'.format(sign, func.__name__, args, kwargs)
            MoVoidLog.write(key=label, text=log_text, level=level)
            try:
                re_func = func(*args, **kwargs)
            except Exception as err:
                log_text = '[{}]<{}>{}'.format(sign, func.__name__, traceback.print_exc())
                MoVoidLog.write(key=label, text=log_text, level=error_level)
            else:
                log_text = '[{}]<{}>{}'.format(sign, func.__name__, re_func)
                MoVoidLog.write(key=label, text=log_text, level=level)

        return wrapping

    return decoration


def log_print(text, level=1, label: str = '__default__', print_out=False):
    if label not in MoVoidLog.log_file:
        if '__default__' in MoVoidLog.log_file:
            label = '__default__'
        else:
            if MoVoidLog.log_file:
                key = list(MoVoidLog.log_file.keys())[0]
                MoVoidLog.reset_default(key)
                label = key
            else:
                raise Exception('there is no log file set,please set one log_file to initialize!')
    MoVoidLog.write(label, text, level, print_out)


def log_debug(text, label: str = '__default__', print_out=False):
    log_print(text, 0, label, print_out)


def log_info(text, label: str = '__default__', print_out=False):
    log_print(text, 1, label, print_out)


def log_warning(text, label: str = '__default__', print_out=False):
    log_print(text, 2, label, print_out)


def log_error(text, label: str = '__default__', print_out=False):
    log_print(text, 3, label, print_out)


def log_critical(text, label: str = '__default__', print_out=False):
    log_print(text, 4, label, print_out)


class MoVoidLog:
    log_file = {}
    log_level = {
        0: 'DEBUG',
        1: 'INFO',
        2: 'WARNING',
        3: 'ERROR',
        4: 'CRITICAL',
    }
    config_rule = {
        'log-.*': {
            '__must__': True,
            'path': {
                'type': 'str',
                'default': 'log'
            },
            'alias': {
                'type': 'list-z',
                'default': []
            },
            'default': {
                'type': 'bool',
                'default': True
            },
            'number': {
                'type': 'int',
                'default': 10
            },
            'size': {
                'type': 'int',
                'default': 20
            },
            'day': {
                'type': 'int',
                'default': 7
            },
            'encoding': {
                'type': 'str',
                'default': 'utf-8'
            },
        }
    }

    @classmethod
    def new_log_file(cls, path: str, alias=None, default=True, number=10, size=20, day=7, encoding: str = 'utf-8'):
        if path not in cls.log_file:
            cls.log_file[path] = MoVoidLogOne(path, number=number, size=size, day=day, encoding=encoding)
            try:
                if alias:
                    for i in alias:
                        try:
                            if i and i in cls.log_file:
                                continue
                            else:
                                cls.log_file[i] = cls.log_file[path]
                        except:
                            continue
                if default:
                    cls.log_file['__default__'] = cls.log_file[path]
            except:
                pass

    @classmethod
    def reset_default(cls, key):
        if key in cls.log_file:
            cls.log_file['__default__'] = cls.log_file[key]

    @classmethod
    def write(cls, key, text, level=0, print_out=False):
        if key in cls.log_file:
            cls.log_file[key].write(text, level, print_out)
        else:
            raise Exception('wrong key:<{}>'.format(key))


class MoVoidLogOne:

    def __init__(self, path, number=10, size=20, day=7, encoding='utf-8'):
        self.dir, self.name = os.path.split(os.path.abspath(path))
        self.number = number
        self.size = size
        self.day = day
        self.encoding = encoding
        self.file_path = None
        self.file = None
        self.date = None
        self.index = -1
        self.find_file()

    def check_file_delete(self):
        all_list = os.listdir(self.dir)
        file_list = []
        for i in all_list:
            this_path = os.path.join(self.dir, i)
            if os.path.isfile(this_path) and i.startswith(self.name + '-') and len(i) >= len(self.name) + 17:
                try:
                    this_date = time.mktime(time.strptime(i[len(self.name) + 1:len(self.name) + 11], "%Y-%m-%d"))
                    this_index = int(i[len(self.name) + 12:-4])
                    if this_date > self.day * 86400:
                        os.remove(this_path)
                    else:
                        file_list.append([this_path, this_date, this_index])
                except:
                    continue
        if len(file_list) > self.number:
            file_list.sort(key=lambda x: x[2])
            file_list.sort(key=lambda x: x[1])
            for i in range(len(file_list) - self.number):
                try:
                    os.remove(file_list[i][0])
                except:
                    continue

    def find_file(self):
        all_list = os.listdir(self.dir)
        prefix = '{}-{}'.format(self.name, time.strftime("%Y-%m-%d", time.localtime(time.time())))
        max_index = -1
        last_path = None
        for i in all_list:
            this_path = os.path.join(self.dir, i)
            if os.path.isfile(this_path) and i.startswith(prefix) and i.endswith('.log'):
                if len(prefix) + 5 >= len(i) >= len(prefix) + 4:
                    this_index = 0
                elif len(i) > len(prefix) + 5:
                    try:
                        this_index = int(i[len(prefix) + 1:-4])
                    except:
                        continue
                else:
                    continue
                if this_index > max_index:
                    max_index = this_index
                    last_path = this_path
        if last_path:
            last_size = os.path.getsize(last_path)
            if last_size >= self.size * 1048576:
                self.file_path = '{}.{}.log'.format(prefix, max_index + 1)
                self.file = open(self.file_path, mode='w', encoding=self.encoding)
            else:
                self.file_path = last_path
                self.file = open(self.file_path, mode='a', encoding=self.encoding)
        else:
            self.file_path = '{}.{}.log'.format(prefix, 0)
            self.file = open(self.file_path, mode='w', encoding=self.encoding)
        self.check_file_delete()

    def write(self, text: str = '', level=0, print_out=False):
        now_time = datetime.datetime.now()
        now_date = now_time.strftime("%Y-%m-%d")
        if now_date == self.date:
            this_size = os.path.getsize(self.file_path)
            if this_size >= self.size * 1048576:
                self.index += 1
                self.create_new_file()
        else:
            self.date = now_date
            self.index = 0
            self.create_new_file()
        if text:
            level_text = MoVoidLog.log_level[level] if level in MoVoidLog.log_level else str(level)
            now_second = now_time.strftime("%H:%M:%S.%f")[:-3]
            real_text = '[{}][{}]{}'.format(now_second, level_text, text)
            print(real_text, file=self.file, flush=True)
            if print_out is True:
                print(real_text)
            elif print_out:
                if isinstance(print_out, list):
                    for print_file in print_out:
                        try:
                            print(real_text, file=print_file, flush=True)
                        except:
                            continue
                else:
                    try:
                        print(real_text, file=print_out, flush=True)
                    except:
                        print('we cannot print log text on <{}>:{}'.format(str(print_out), real_text), file=sys.stderr)
        self.check_file_delete()

    def create_new_file(self):
        if self.file is not None and not self.file.closed:
            self.file.close()
        if self.date is None:
            self.date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        if self.index < 0:
            self.index = 0
        new_path = os.path.join(self.dir, '{}-{}.{}.log'.format(self.name, self.date, self.index))
        if os.path.exists(new_path):
            self.find_file()
        else:
            self.file_path = new_path
            self.file = open(self.file_path, mode='w', encoding=self.encoding)


if __name__ == '__main__':
    a = MoVoidLog()
