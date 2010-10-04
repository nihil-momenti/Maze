# -*- coding: utf-8 -*-
from __future__ import division

from math import floor, ceil, cos, pi

from randomiser import Randomiser

class Perlin(object):
  def __init__(self, octaves, persistence):
    self.octaves = octaves
    self.p = persistence
    self.randomisers = [Randomiser() for i in range(octaves)]
  
  def __getitem__(self, key):
    return self.value(*key)

  def value(self, *x, **params):
    k = 0.0
    octaves = params['octave'] if 'octave' in params else self.octaves
    for octave in range(self.octaves - octaves):
      x = [xn / 2 for xn in x]
    for octave in range(self.octaves - octaves, self.octaves):
      k += self.interpolated(octave, *x)
      x = [xn / 2 for xn in x]
    return k

  def interpolated(self, octave, *x):
    fx = [floor(xn) for xn in x]
    cx = [fxn + 1 for fxn in fx]
    return (self.p ** (self.octaves - octave - 1)) * self.int_f(octave, [], x, fx, cx)
    
  def int_f(self, octave, y, x, fx, cx):
    if len(fx) == 0:
      # print "( ", y, " : ", self.smooth(octave, *y), " )"
      return self.smooth(octave, *y)
    x1 = self.int_f(octave, y + [fx[0]], x[1:], fx[1:], cx[1:])
    x2 = self.int_f(octave, y + [cx[0]], x[1:], fx[1:], cx[1:])
    f = (1 - cos(pi*(x[0] - fx[0]))) / 2
    return x1 * (1 - f) + x2 * f

  def smooth(self, octave, *x):
    if len(x) == 1:
      return self.noise(octave, x[0]) / 2 + (self.noise(octave, x[0] + 1) + self.noise(octave, x[0] - 1)) / 4
    elif len(x) == 2:
      center = self.noise(octave, *x)
      sides = (self.noise(octave, x[0] + 1, x[1]) + 
               self.noise(octave, x[0] - 1, x[1]) + 
               self.noise(octave, x[0], x[1] + 1) + 
               self.noise(octave, x[0], x[1] - 1))
      corners = (self.noise(octave, x[0] + 1, x[1] + 1) + 
                 self.noise(octave, x[0] + 1, x[1] - 1) + 
                 self.noise(octave, x[0] - 1, x[1] - 1) + 
                 self.noise(octave, x[0] - 1, x[1] + 1))
      return center / 2 + sides * 3 / 32 + corners / 32
    else:
      return self.noise(octave, *x)

  def noise(self, octave, *x):
    return self.randomisers[octave].value(*x)
