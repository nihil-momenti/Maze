# -*- coding: utf-8 -*-
from __future__ import division

import random, numpy
from math import floor, ceil, cos, pi

class Perlin(object):
  small = numpy.asarray((1, 11, 29, 43, 67, 89, 17, 23, 29), 'int')
  
  def __init__(self):
      self.big1 = random.randint(10000,20000)
      self.big2 = random.randint(750000,1000000)
      self.big3 = random.randint(1000000000,1500000000)
  
  def __getitem__(self, key):
    return self.value(*key)

  def value(self, *x):
    shape = []
    ranges = []
    for xi in x:
      if isinstance(xi, slice):
        step = 1 if xi.step is None else xi.step
        value = xi.stop - xi.start
        value /= step
        shape.append(int(value))
        ranges.append([xi.start + xi.step * i for i in range(int(value))])
      else:
        shape.append(xi)
        ranges.append([xi])
    shape.append(len(x))
    x = numpy.zeros(shape)
    for i in range(len(ranges[0])):
      for j in range(len(ranges[1])):
        x[i,j] = [ranges[0][i], ranges[1][j]]
    fx = numpy.asarray(numpy.floor(x), 'int')
    cx = fx + 1
    y = numpy.zeros(shape)
    return self.int_f(y, x, fx, cx, 0)
  
  # Still needs to be made numpyised
  def int_f(self, y, x, fx, cx, depth):
    if depth == x.ndim - 1:
      return self.smooth(y.astype('int'))
    y[...,depth] = fx[...,depth]
    x1 = self.int_f(y, x, fx, cx, depth + 1)
    y[...,depth] = cx[...,depth]
    x2 = self.int_f(y, x, fx, cx, depth + 1)
    f = (1 - numpy.cos(pi*(x[...,depth] - fx[...,depth]))) / 2
    return x1 * (1 - f) + x2 * f

  def smooth(self, x):
    if x.ndim - 1 == 1:
      return self.noise(x) / 2 + (self.noise(x + 1) + self.noise(x - 1)) / 4
    elif x.ndim - 1 == 2:
      center = self.noise(x)
      sides = (self.noise(x + [ 1, 0]) +
               self.noise(x + [-1, 0]) +
               self.noise(x + [0,  1]) +
               self.noise(x + [0, -1]))
      corners = (self.noise(x + [ 1, 1]) +
                 self.noise(x + [-1, 1]) +
                 self.noise(x + [-1,-1]) +
                 self.noise(x + [ 1,-1]))
      return center / 2 + sides * 3 / 32 + corners / 32
    else:
      return self.noise(x)

  # Crap randomiser, need to find something with less repetition
  # Works okay for fractal generation though
  def noise(self, x):
    n = numpy.sum(x * Perlin.small[:x.ndim-1], x.ndim-1)
    n = numpy.bitwise_xor(numpy.left_shift(n,13), n)
    return (1.0 - numpy.bitwise_and( (n * (n * n * self.big1 + self.big2) + self.big3), 0x7fffffff) / 1073741824.0)
