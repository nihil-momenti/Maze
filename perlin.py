from __future__ import division

from math import floor, ceil, cos, pi

from randomiser import Randomiser

class Perlin(object):
  def __init__(self, octaves, persistence):
    self.octaves = octaves
    self.p = persistence
    self.randomisers = [Randomiser() for i in range(octaves)]

  def value(self, octaves, *x):
    k = 0.0
    for octave in range(self.octaves - octaves):
      x = [xn / 2 for xn in x]
    for octave in range(self.octaves - octaves, self.octaves):
      k += self.smoothed(octave, *x)
      x = [xn / 2 for xn in x]
    # k = self.smoothed(self.octaves - 1, *x)
    return k

  def smoothed(self, octave, *x):
    fx = [floor(xn) for xn in x]
    cx = [fxn + 1 for fxn in fx]
    return (self.p ** (self.octaves - octave - 1)) * self.f(octave, [], x, fx, cx)
    
  def f(self, octave, y, x, fx, cx):
    if len(fx) == 0:
      return self.unsmoothed(octave, *y)
    x1 = self.f(octave, y + [fx[0]], x[1:], fx[1:], cx[1:])
    x2 = self.f(octave, y + [cx[0]], x[1:], fx[1:], cx[1:])
    f = (1 - cos(pi*(cx[0] - x[0]))) / 2
    return x1 * f + x2 * (1 - f)#* (1 - f) + x2 * f

  def unsmoothed(self, octave, *x):
    return self.randomisers[octave].value(*x)
