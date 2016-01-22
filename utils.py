#!/usr/bin/env python3

import random
import time

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
    x = random.randint(a.x, b.x)
    y = random.randint(a.y, b.y)
    return Point(x, y)


def random_click(a, b=None):
    p = random_point(a, b)
    p.click()


def random_sleep(min, max=None):
    if max is None:
        max = 1.1 * min
    seconds = random.uniform(min, max)
    time.sleep(seconds)
