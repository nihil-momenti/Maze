# -*- coding: utf-8 -*-
from __future__ import division

from fractal_map import FractalMap
from PIL import Image
import numpy, time

size = 100
texture = numpy.zeros((size,size,3),'byte')

start = time.time()
tex_map = FractalMap(8, 0.95)
for x in range(size):
  for y in range(size):
    v = tex_map[x,y]
    value = [max(0., min(1., (1 + v * .1) * .60)) * 255,
             max(0., min(1., (1 + v * .1) * .46)) * 255,
             max(0., min(1., (1 + v * .1) * .33)) * 255]
    texture[x,y] = value
end = time.time()

im = Image.fromarray(texture)
im.save('temp.bmp')
print "Time taken: %.4f" % (end - start)
