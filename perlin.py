# -*- coding: utf-8 -*-
from __future__ import division

import random, numpy
from math import floor, ceil, cos, pi

class Perlin(object):
  small = numpy.asarray((1, 11, 29, 43, 67, 89, 17, 23, 29),'int64')
  
  def __init__(self):
      self.big1 = random.randint(10000,20000)
      self.big2 = random.randint(750000,1000000)
      self.big3 = random.randint(1000000000,1500000000)
  
  def __getitem__(self, key):
    return self.value(*key)

  def value(self, *x):
    fx = [int(xn) for xn in x]
    cx = [fxn + 1 for fxn in fx]
    return self.int_f([], x, fx, cx)
    
  def int_f(self, y, x, fx, cx):
    if len(fx) == 0:
      return self.smooth(*y)
    x1 = self.int_f(y + [fx[0]], x[1:], fx[1:], cx[1:])
    x2 = self.int_f(y + [cx[0]], x[1:], fx[1:], cx[1:])
    f = (1 - cos(pi*(x[0] - fx[0]))) / 2
    return x1 * (1 - f) + x2 * f

  def smooth(self, *x):
    if len(x) == 1:
      return self.noise(x[0]) / 2 + (self.noise(x[0] + 1) + self.noise(x[0] - 1)) / 4
    elif len(x) == 2:
      center = self.noise(*x)
      sides = (self.noise(x[0] + 1, x[1]) + 
               self.noise(x[0] - 1, x[1]) + 
               self.noise(x[0], x[1] + 1) + 
               self.noise(x[0], x[1] - 1))
      corners = (self.noise(x[0] + 1, x[1] + 1) + 
                 self.noise(x[0] + 1, x[1] - 1) + 
                 self.noise(x[0] - 1, x[1] - 1) + 
                 self.noise(x[0] - 1, x[1] + 1))
      return center / 2 + sides * 3 / 32 + corners / 32
    else:
      return self.noise(*x)

  # Crap randomiser, need to find something with less repetition
  # Works okay for fractal generation though
  def noise(self, *x):
    x = numpy.asarray(x,'int64')
    n = numpy.sum(x * Perlin.small[:x.size])
    n = (n<<13) ^ n;
    return ( 1.0 - ( (n * (n * n * self.big1 + self.big2) + self.big3) & 0x7fffffff) / 1073741824.0)
