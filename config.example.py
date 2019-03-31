#!/usr/bin/env python3

'''
COPYRIGHT Dazzy Ding, Peter Zhang 2015-2016
'''

import sys

# 游戏左上角坐标
if sys.platform == 'darwin':
    base = (0, 23)
if sys.platform == 'linux':
    base = (34, 29)
if sys.platform == 'win32':
    base = (0, 30)

# API 服务器监听端口
host = ("127.0.0.1", 14585)

poi_interaction = False
