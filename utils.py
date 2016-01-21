#!/usr/bin/env python3

import random
import time

import config
import pyautogui


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point(%d, %d)" % (self.x, self.y)

    def click(self):
        try:
            pyautogui.click(self.x, self.y)
        except pyautogui.FailSafeException:
            print("WARNING:", "FailSafeException", self)

    def moveTo(self):
        pyautogui.moveTo(self.x, self.y)


def random_point(a, b=None):
    if b is None:
        b = a
    x = config.base[0] + random.randint(a.x, b.x)
    y = config.base[1] + random.randint(a.y, b.y)
    return Point(x, y)


def random_click(a, b=None):
    p = random_point(a, b)
    p.click()


def random_sleep(min, max=None):
    if max is None:
        max = 1.1 * min
    seconds = random.uniform(min, max)
    time.sleep(seconds)
