#!/usr/bin/env python3

'''
COPYRIGHT Dazzy Ding, Peter Zhang 2015-2016
'''

import os
import platform
import math
import random
import time
from datetime import datetime

import config
import pyautogui


class Point():
    ''' Relative position point on game view.
        Assume game view is 800x600.
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point(%d, %d)" % (self.x, self.y)

    @property
    def rx(self):
        return config.base[0] + self.x

    @property
    def ry(self):
        return config.base[1] + self.y

    def click(self):
        try:
            pyautogui.click(self.rx, self.ry)
        except pyautogui.FailSafeException:
            print("WARNING:", "FailSafeException", self)

    def moveTo(self):
        pyautogui.moveTo(self.rx, self.ry)


def random_point(a, b=None):
    if b is None:
        b = a
    method = random.choice((random_point_dd1,
                            random_point_dd2,))
    return method(a, b)


def random_point_dd1(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    x = a.x + dx * random.random()
    y = a.y + dy * random.random()
    return Point(x, y)


def random_point_dd2(a, b, center=Point(400, 240)):
    # TODO: Point tend to center
    dx = b.x - a.x
    dy = b.y - a.y
    x = a.x + dx * random.betavariate(3, 5)
    y = a.y + dy * random.betavariate(3, 5)
    return Point(x, y)


def random_click(a, b=None):
    p = random_point(a, b)
    p.click()


def random_sleep(min, max=None):
    if max is None:
        max = min * 1.1
    seconds = random.uniform(min, max)
    time.sleep(seconds)


def random_sleep_until(min, max=None, floor=0):
    if max is None:
        max = min

    now = time.time()
    if (max - now) <= floor:
        return

    end = random.uniform(min, max)
    seconds = end - now

    end_dt = datetime.fromtimestamp(end)
    print("sleep until:", end_dt.strftime("%I:%M:%S %p"))
    time.sleep(seconds)


def mouse_position():
    pos = pyautogui.position()
    point = Point(pos[0] - config.base[0],
                  pos[1] - config.base[1])
    print("mouse at", point)
    return point
