#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Version: 3.11.4
Creator: 孙一凡-莫无煜
Create Date: 2023/7/24

"""
__all__ = [
    'file_write_excel_dict_list_list',
    'file_write_excel_dict_dict_list',
    'file_write_excel_dict_list_dict',
    'file_write_excel_dict_dict_dict',
    'file_read_excel_dict_list_list',
    'file_read_excel_dict_dict_list',
    'file_read_excel_dict_list_dict',
    'file_read_excel_dict_dict_dict',
]

from ..mv_import import MoVoidImport

try:
    import xlrd
except ModuleNotFoundError as err:
    MoVoidImport.error(err, '1.2.0')
else:
    MoVoidImport.version(xlrd, '1.2.0')
try:
    import xlwt
except ModuleNotFoundError as err:
    MoVoidImport.error(err)
else:
    MoVoidImport.version(xlwt)


def file_write_excel_dict_list_list(path: str, input_dict: dict):
    wb = xlwt.Workbook()
    for i, v in input_dict.items():
        ws = wb.add_sheet(i)
        for j, w in enumerate(v):
            for k, x in enumerate(w):
                ws.write(j, k, x)
    wb.save(path)


def file_write_excel_dict_dict_list(path: str, input_dict: dict):
    wb = xlwt.Workbook()
    for i, v in input_dict.items():
        ws = wb.add_sheet(i)
        j_index = 0
        for j, w in v.items():
            ws.write(j_index, 0, j)
            for k, x in enumerate(w):
                ws.write(j_index, k + 1, x)
            j_index += 1
    wb.save(path)


def file_write_excel_dict_list_dict(path: str, input_dict: dict, default=''):
    wb = xlwt.Workbook()
    for i, v in input_dict.items():
        ws = wb.add_sheet(i)
        k_list = []
        for j, w in enumerate(v):
            for k, x in w.items():
                if k not in k_list:
                    k_list.append(k)
                k_index = k_list.index(k)
                ws.write(j + 1, k_index, x)
        for j, w in enumerate(v):
            for k, x in enumerate(k_list):
                if x not in w:
                    ws.write(j + 1, k, default)
        for k, x in enumerate(k_list):
            ws.write(0, k, x)
    wb.save(path)


def file_write_excel_dict_dict_dict(path: str, input_dict: dict, default=''):
    wb = xlwt.Workbook()
    for i, v in input_dict.items():
        ws = wb.add_sheet(i)
        j_index = 0
        k_list = []
        for j, w in v.items():
            for k, x in w.items():
                if k not in k_list:
                    k_list.append(k)
                k_index = k_list.index(k)
                ws.write(j_index + 1, k_index + 1, x)
            ws.write(j_index + 1, 0, j)
            j_index += 1
        j_index = 0
        for j, w in v.items():
            for k, x in enumerate(k_list):
                if x not in w:
                    ws.write(j_index + 1, k + 1, default)
            j_index += 1
        ws.write(0, 0, i)
        for k, x in enumerate(k_list):
            ws.write(0, k + 1, x)
    wb.save(path)


def file_read_excel_dict_list_list(path: str):
    re_dict = {}
    wb = xlrd.open_workbook(path)
    wss = wb.sheets()
    for ws in wss:
        ws_name = ws.name
        re_dict[ws_name] = ws._cell_values
    return re_dict


def file_read_excel_dict_dict_list(path: str):
    re_dict = {}
    wb = xlrd.open_workbook(path)
    wss = wb.sheets()
    for ws in wss:
        ws_name = ws.name
        re_dict[ws_name] = {}
        for rows in ws._cell_values:
            re_dict[ws_name][rows[0]] = rows[1:]
    return re_dict


def file_read_excel_dict_list_dict(path: str):
    re_dict = {}
    wb = xlrd.open_workbook(path)
    wss = wb.sheets()
    for ws in wss:
        ws_name = ws.name
        re_dict[ws_name] = []
        keys = ws._cell_values[0]
        for rows in ws._cell_values[1:]:
            temp_dict = {}
            for index, cell in enumerate(rows):
                temp_dict[keys[index]] = cell
            re_dict[ws_name].append(temp_dict)
    return re_dict


def file_read_excel_dict_dict_dict(path: str):
    re_dict = {}
    wb = xlrd.open_workbook(path)
    wss = wb.sheets()
    for ws in wss:
        ws_name = ws.name
        re_dict[ws_name] = {}
        keys = ws._cell_values[0]
        for rows in ws._cell_values[1:]:
            row_key = rows[0]
            re_dict[ws_name][row_key] = {}
            for index, cell in enumerate(rows[1:]):
                re_dict[ws_name][row_key][keys[index + 1]] = cell
    return re_dict


if __name__ == '__main__':
    pass
