#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Version: 3.11.4
Creator: 孙一凡-莫无煜
Create Date: 2023/7/18

"""
__all__ = [
    'config_update',
    'config_update_regex_rule'
]

import json
import os
import re
from configparser import ConfigParser


def config_update(path: str, ori_config: dict, encoding='utf8'):
    cf1 = ConfigParser()
    if os.path.isfile(path):
        cf1.read(path, encoding)
    cf2 = ConfigParser()
    for i, v in ori_config.items():
        if not cf1.has_section(i):
            cf1.add_section(i)
        cf2.add_section(i)
        for j, w in v.items():
            if cf1.has_option(i, j):
                cf_value = cf1.get(i, j)
                if isinstance(w, int):
                    try:
                        final_str = cf_value
                        final_value = int(cf_value)
                    except:
                        final_str = str(w)
                        final_value = w
                elif isinstance(w, float):
                    try:
                        final_str = cf_value
                        final_value = float(cf_value)
                    except:
                        final_str = str(w)
                        final_value = w
                elif isinstance(w, list):
                    final_str = cf_value
                    final_value = cf_value.split(',')
                elif isinstance(w, dict):
                    final_str = cf_value
                    temp_value = cf_value.split(',')
                    final_value = {}
                    for k in temp_value:
                        k1, k2 = k.split(':')
                        final_value[k1] = k2
                else:
                    final_str = cf_value
                    final_value = cf_value
            else:
                final_str = w
                final_value = w
            cf2.set(i, j, final_str)
            ori_config[i][j] = final_value
    with open(path, 'w', encoding=encoding) as file:
        cf2.write(file)


def config_update_regex_rule(path: str, rule_dict: dict, ori_config: dict, encoding='utf8'):
    cf1 = ConfigParser()
    if os.path.isfile(path):
        cf1.read(path, encoding)
    re_dict = {}
    cf2 = ConfigParser()
    rule_has = {}
    for i_section in cf1.sections():
        v_section = cf1[i_section]
        for i_rule, v_rule in rule_dict.items():
            if re.match(i_rule + '$', i_section):
                re_dict[i_section] = {}
                cf2.add_section(i_section)
                rule_has[i_rule] = True
                for j_rule, w_rule in v_rule.items():
                    if not (j_rule.startswith('__') and j_rule.endswith('__')):
                        temp_str, temp_value = get_value_from_file_rule_ori(v_section.get(j_rule), w_rule, ori_config.get(i_section, {}).get(j_rule))
                        if temp_value is not None:
                            cf2.set(i_section, j_rule, temp_str)
                            re_dict[i_section][j_rule] = temp_value
    for i_rule, v_rule in rule_dict.items():
        if v_rule.get('__must__') and not (i_rule in rule_has and rule_has[i_rule]) and i_rule not in re_dict:
            re_dict[i_rule] = {}
            cf2.add_section(i_rule)
            for j_rule, w_rule in v_rule.items():
                if not (j_rule.startswith('__') and j_rule.endswith('__')):
                    temp_str, temp_value = get_value_from_file_rule_ori(None, w_rule, ori_config.get(i_rule, {}).get(j_rule))
                    if temp_value is not None:
                        cf2.set(i_rule, j_rule, temp_str)
                        re_dict[i_rule][j_rule] = temp_value
    ori_config.clear()
    ori_config.update(re_dict)
    with open(path, mode='w', encoding=encoding) as file:
        cf2.write(file)


def get_value_from_file_rule_ori(file_value, rule, ori_value):
    re_str = None
    re_value = None
    if file_value is None:
        if ori_value is None:
            if rule.get('default') is not None:
                re_value = rule.get('default')
        else:
            re_value = ori_value
    else:
        re_str = file_value
    if re_str is None and re_value is not None:
        re_str = str(re_value)
    if re_str is not None and re_value is None:
        rule_type = rule['type']
        if rule_type == 'int':
            try:
                re_value = int(re_str)
            except:
                re_str, re_value = get_value_from_file_rule_ori(None, rule, ori_value)
        elif rule_type == 'float':
            try:
                re_value = float(re_str)
            except:
                re_str, re_value = get_value_from_file_rule_ori(None, rule, ori_value)
        elif rule_type == 'json':
            try:
                re_value = json.loads(re_str)
            except:
                re_str, re_value = get_value_from_file_rule_ori(None, rule, ori_value)
        elif rule_type == 'bool':
            try:
                re_value = False if re_str.lower() in ('false', 'f', '') else True
            except:
                re_str, re_value = get_value_from_file_rule_ori(None, rule, ori_value)
        elif rule_type == 'list':
            try:
                re_value = re_str.split(',')
            except:
                re_str, re_value = get_value_from_file_rule_ori(None, rule, ori_value)
        elif rule_type == 'list-z':
            try:
                re_value = [_ for _ in re_str.split(',') if _]
            except:
                re_str, re_value = get_value_from_file_rule_ori(None, rule, ori_value)
        elif rule_type == 'dict':
            try:
                temp_list = re_str.split(',')
                re_value = {}
                for i in temp_list:
                    temp_key, temp_value = i.split(':', 1)
                    re_value[temp_key] = temp_value
            except:
                re_str, re_value = get_value_from_file_rule_ori(None, rule, ori_value)
        else:
            re_value = re_str
    return re_str, re_value


if __name__ == '__main__':
    a = {
        'all': {
            '__must__': True,
            'this1': {
                'type': 'str',
                'default': 'doit'
            }
        }
    }
    b = {}
    config_update_regex_rule('config.ini', a, b)
    print('a', a)
    print('b', b)
