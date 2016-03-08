#!/usr/bin/env python3

import math
import os
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
    type_ = random.choice((1, 2))
    if type_ == 1:
        dx = b.x - a.x
        dy = b.y - a.y
        x = a.x + dx * random.random()
        y = a.y + dy * random.random()
        return Point(x, y)
    if type_ == 2:
        # Get a point in a circle(a=1, b=1, r=1).
        cr = random.random()
        ca = random.randint(0, 360) / 180 * math.pi
        cx = 1 + cr * math.cos(ca)
        cy = 1 + cr * math.sin(ca)
        # Transform
        dx = b.x - a.x
        dy = b.y - a.y
        x = a.x + dx * cx / 2
        y = a.y + dy * cy / 2
        return Point(x, y)


def random_click(a, b=None):
    p = random_point(a, b)
    p.click()


def random_sleep(min, max=None):
    if max is None:
        max = min * 1.1
    seconds = random.uniform(min, max)
    # print("sleep:", seconds)
    time.sleep(seconds)


def random_sleep_until(min, max=None, floor=0):
    if max is None:
        max = min

    now = time.time()
    end = random.uniform(min, max)
    seconds = end - now
    if seconds <= floor:
        return

    end_dt = datetime.fromtimestamp(end)
    print("sleep until:", end_dt.strftime("%I:%M:%S %p"))
    time.sleep(seconds)


def hotkey_refresh():
    if os.name == 'nt':
        pyautogui.press('f5')
    else:
        pyautogui.hotkey('ctrl', 'r')


def hotkey_switch_panel(panel):
    available = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    if panel in available:
        pyautogui.hotkey('ctrl', panel)
