#!/usr/bin/env python3

'''
COPYRIGHT Dazzy Ding, Peter Zhang 2015-2016
'''

import math
from PIL import Image
from utils import Point, random_point


# Setting
TIMES = 3000
IMAGE_SIZE = 500


# Produce point count
prob = [[0 for x in range(IMAGE_SIZE)] for y in range(IMAGE_SIZE)]
p1 = Point(0, 0)
p2 = Point(IMAGE_SIZE, IMAGE_SIZE)
for i in range(TIMES):
    p = random_point(p1, p2)
    x = math.floor(p.x)
    y = math.floor(p.y)
    prob[x][y] += 1

# Normalization of point probability
max_c = 0
for x in range(IMAGE_SIZE):
    for y in range(IMAGE_SIZE):
        if prob[x][y] > max_c:
            max_c = prob[x][y]
for x in range(IMAGE_SIZE):
    for y in range(IMAGE_SIZE):
        prob[x][y] = prob[x][y] / max_c


# Render image
im = Image.new('L', (IMAGE_SIZE, IMAGE_SIZE))
pixels = im.load()
for x in range(IMAGE_SIZE):
    for y in range(IMAGE_SIZE):
        # pixel = (math.floor(255 * prob[x][y]), 255, 255)
        pixel = math.floor(255 * prob[x][y])
        pixels[x, y] = pixel
im.convert('RGB').save("benchmark.png")
