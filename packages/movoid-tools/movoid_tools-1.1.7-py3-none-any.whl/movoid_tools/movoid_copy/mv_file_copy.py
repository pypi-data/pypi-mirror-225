#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Version: 3.11.4
Creator: 孙一凡-莫无煜
Create Date: 2023/7/23

"""
import os
import traceback
from tkinter import filedialog

from ..mv_import import MoVoidImport

try:
    import openpyxl
except ModuleNotFoundError as err:
    MoVoidImport.error(err)
else:
    MoVoidImport.version(openpyxl)


def copy_files():
    names = filedialog.askopenfilenames()
    all_len = len(names)
    for i, v in enumerate(names):
        try:
            path, postfix = os.path.splitext(v)
            new_path = path + '_copy' + postfix
            if postfix == '.xlsx':
                wb = openpyxl.load_workbook(v)
                wb.save(new_path)
                print_text = 'excel file success'
            elif postfix == '.csv':
                with open(v, mode='r', encoding='utf8') as file:
                    temp = file.read()
                with open(new_path, mode='w', encoding='utf8') as file:
                    file.write(temp)
                print_text = 'csv file success'
            else:
                print_text = 'unknown file'
        except:
            print_text = 'error!'
            traceback.print_exc()
        finally:
            print('[{}/{} {:.2%}]{}:{}'.format(i, all_len, i / all_len, print_text, v))


if __name__ == '__main__':
    copy_files()
