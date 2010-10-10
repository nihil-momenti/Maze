# -*- coding: utf-8 -*-
from __future__ import division

from fractal_map import FractalMap
from PIL import Image
import numpy, time

size = 100

zeros = numpy.zeros((size, size))
ones = numpy.ones((size, size))
texture = numpy.zeros((size, size, 3), 'ubyte')

start = time.time()
tex_map = FractalMap(8, 0.95)
v = tex_map[:size,:size]
texture[..., 0] = numpy.maximum(zeros, numpy.minimum(ones, (1 + v * .1) * .60)) * 255
texture[..., 1] = numpy.maximum(zeros, numpy.minimum(ones, (1 + v * .1) * .46)) * 255
texture[..., 2] = numpy.maximum(zeros, numpy.minimum(ones, (1 + v * .1) * .33)) * 255
end = time.time()

im = Image.fromarray(texture)
im.save('temp.bmp')
print "Time taken: %.4f" % (end - start)
