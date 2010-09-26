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
      k += self.interpolated(octave, *x)
      x = [xn / 2 for xn in x]
    return k

  def interpolated(self, octave, *x):
    fx = [floor(xn) for xn in x]
    cx = [fxn + 1 for fxn in fx]
    return (self.p ** (self.octaves - octave - 1)) * self.int_f(octave, [], x, fx, cx)
    
  def int_f(self, octave, y, x, fx, cx):
    if len(fx) == 0:
      return self.smooth(octave, *y)
    x1 = self.int_f(octave, y + [fx[0]], x[1:], fx[1:], cx[1:])
    x2 = self.int_f(octave, y + [cx[0]], x[1:], fx[1:], cx[1:])
    f = (1 - cos(pi*(cx[0] - x[0]))) / 2
    return x1 * f + x2 * (1 - f)

  def smooth(self, octave, *x):
    den = 2 ** len(x)
    return self.smo_f(octave, [], x, den)
    
    
  def smo_f(self, octave, y, x, den):
    if len(x) == 0:
      return self.noise(octave, *y) * den
    x1 = self.smo_f(octave, y + [x[0]], x[1:], den)
    x2 = self.smo_f(octave, y + [x[0] - 1], x[1:], 2 * den)
    x3 = self.smo_f(octave, y + [x[0] + 1], x[1:], 2 * den)
    return x1 + x2 + x3

    

  def noise(self, octave, *x):
    return self.randomisers[octave].value(*x)
