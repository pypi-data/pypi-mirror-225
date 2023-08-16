#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Version: 3.11.4
Creator: 孙一凡-莫无煜
Create Date: 2023/7/29

"""
__all__ = [
    'file_write_csv_list_list',
    'file_write_csv_dict_list',
    'file_write_csv_list_dict',
    'file_write_csv_dict_dict',
    'file_read_csv_list_list',
    'file_read_csv_dict_list',
    'file_read_csv_list_dict',
    'file_read_csv_dict_dict',
]


def file_write_csv_list_list(path: str, input_content: list, split=',', split_replace='_', encoding='utf8'):
    split, split_replace, encoding = map(str, [split, split_replace, encoding])
    with open(path, mode='w', encoding=encoding) as file:
        for i, v in enumerate(input_content):
            if i > 0:
                file.write('\n')
            for j, w in enumerate(v):
                if j > 0:
                    file.write(split)
                file.write(str(w).replace(split, split_replace))


def file_write_csv_dict_list(path: str, input_content: dict, split=',', split_replace='_', encoding='utf8'):
    split, split_replace, encoding = map(str, [split, split_replace, encoding])
    with open(path, mode='w', encoding=encoding) as file:
        for i, v in input_content.items():
            if i > 0:
                file.write('\n')
            file.write(str(i))
            for j, w in enumerate(v):
                file.write(split)
                file.write(str(w).replace(split, split_replace))


def file_write_csv_list_dict(path: str, input_content: list, default='', split=',', split_replace='_', encoding='utf8'):
    default, split, split_replace, encoding = map(str, [default, split, split_replace, encoding])
    with open(path, mode='w', encoding=encoding) as file:
        j_list = []
        for i, v in enumerate(input_content):
            for j, w in v.items():
                if j not in j_list:
                    j_list.append(j)
        for i, v in enumerate(input_content):
            if i > 0:
                file.write('\n')
            for j_index, j in j_list:
                if j_index > 0:
                    file.write(split)
                w = v.get(j, default)
                file.write(str(w).replace(split, split_replace))


def file_write_csv_dict_dict(path: str, input_content: dict, default='', title='key', split=',', split_replace='_', encoding='utf8'):
    default, title, split, split_replace, encoding = map(str, [default, title, split, split_replace, encoding])
    with open(path, mode='w', encoding=encoding) as file:
        j_list = []
        for i, v in input_content.items():
            for j, w in v.items():
                if j not in j_list:
                    j_list.append(j)
        file.write(default.join([title] + j_list))
        for i, v in input_content.items():
            file.write('\n' + str(i))
            for j_index, j in j_list:
                file.write(split)
                w = v.get(j, default)
                file.write(str(w).replace(split, split_replace))


def file_read_csv_list_list(path: str, split=',', ignore_blank_row=True, encoding='utf8'):
    re_list = []
    split, encoding = map(str, [split, encoding])
    with open(path, mode='r', encoding=encoding) as file:
        file_lines = file.readlines()
    for line_one in file_lines:
        temp_line = line_one.strip('\n')
        temp_list = temp_line.split(split)
        if len(temp_list) == 1 and temp_list[0] == '':
            if ignore_blank_row:
                continue
            else:
                temp_list = []
        re_list.append(temp_list)
    return re_list


def file_read_csv_dict_list(path: str, split=',', ignore_blank_row=True, encoding='utf8'):
    re_dict = {}
    split, encoding = map(str, [split, encoding])
    with open(path, mode='r', encoding=encoding) as file:
        file_lines = file.readlines()
    for line_one in file_lines:
        temp_line = line_one.strip('\n')
        temp_list = temp_line.split(split)
        if len(temp_list) == 1:
            if ignore_blank_row or temp_list[0] == '':
                continue
        key = str(temp_list.pop(0))
        re_dict[key] = temp_list
    return re_dict


def file_read_csv_list_dict(path: str, split=',', ignore_blank_row=True, ignore_key_value='', encoding='utf8'):
    re_list = []
    split, encoding = map(str, [split, encoding])
    with open(path, mode='r', encoding=encoding) as file:
        file_lines = file.readlines()
    keys = file_lines[0].strip('\n').split(split)
    for line_one in file_lines[1:]:
        temp_list = line_one.strip('\n').split(split)
        if len(temp_list) == 1 and temp_list[0] == '':
            if ignore_blank_row:
                continue
            else:
                temp_list = []
        temp_dict = {}
        for i_key, v_key in enumerate(keys):
            if i_key < len(temp_list):
                v_value = temp_list[i_key]
                if v_value != ignore_key_value:
                    temp_dict[v_key] = v_value
            else:
                break
        re_list.append(temp_dict)
    return re_list


def file_read_csv_dict_dict(path: str, split=',', ignore_blank_row=True, ignore_key_value='', encoding='utf8'):
    re_dict = {}
    split, encoding = map(str, [split, encoding])
    with open(path, mode='r', encoding=encoding) as file:
        file_lines = file.readlines()
    keys = file_lines[0].strip('\n').split(split)[1:]
    for line_one in file_lines[1:]:
        temp_list = line_one.strip('\n').split(split)
        if len(temp_list) == 1 and temp_list[0] == '':
            if ignore_blank_row or temp_list[0] == '':
                continue
        key = str(temp_list.pop(0))
        temp_dict = {}
        for i_key, v_key in enumerate(keys):
            if i_key < len(temp_list):
                v_value = temp_list[i_key]
                if v_value != ignore_key_value:
                    temp_dict[v_key] = v_value
            else:
                break
        re_dict[key] = temp_dict
    return re_dict


if __name__ == '__main__':
    pass
