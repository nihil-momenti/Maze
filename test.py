# -*- coding: utf-8 -*-
from __future__ import division

from maze2 import Maze
from fractal_map import FractalMap
from PIL import Image
from math import cos, pi, sqrt
import numpy
# m = Maze(20, 40, 5, 0.6)
# m.p()

size = 100
tex_map = FractalMap(8, 0.95)
texture = numpy.zeros((size,size,3),'byte')
for x in range(size):
  for y in range(size):
    v = tex_map[x,y]
    value = [max(0., min(1., (1 + v * .1) * .60)) * 255,
             max(0., min(1., (1 + v * .1) * .46)) * 255,
             max(0., min(1., (1 + v * .1) * .33)) * 255]
    texture[x,y] = value
im = Image.fromarray(texture)
im.save('temp.bmp')