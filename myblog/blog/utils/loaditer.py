#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/19 11:16
# @Author  : DollA
# @File    : loaditer.py
# @Software: PyCharm


# 提取文件内容
def fileiter(path):
    with open(path, 'r+', encoding='utf8') as f:
        for line in f:
            yield line