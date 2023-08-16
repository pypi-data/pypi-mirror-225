#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Version: 3.11.4
Creator: 孙一凡-莫无煜
Create Date: 2023/7/22

"""


if __name__ == '__main__':
    from movoid_log import *

    log_init('config.ini')
    for i in range(100):
        log_print('right')
