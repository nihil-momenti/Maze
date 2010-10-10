# -*- coding: utf-8 -*-
from __future__ import division

from math import floor, ceil, cos, pi

from perlin import Perlin

class FractalMap(object):
  def __init__(self, octaves, persistence):
    self.octaves = octaves
    self.p = persistence
    self.perlins = [Perlin() for i in range(octaves)]
  
  def __getitem__(self, key):
    return self.value(*key)
  
  def value(self, *keys):
    k = 0.0
    x = []
    for key in keys:
      if isinstance(key, slice):
        if key.stop is None:
          raise IndexError, "Cannot use infinite slices"
        step = 1 if key.step is None else key.step
        start = 0 if key.start is None else key.start
        stop = key.stop
        x.append(slice(start, stop, step))
      else:
        x.append(slice(key, key+1, 1))
    for octave in range(self.octaves):
      k += (self.p ** (self.octaves - octave - 1)) * self.noise(octave, *x)
      x = [slice(xn.start / 2, xn.stop / 2, xn.step / 2) for xn in x]
    return k
  
  def noise(self, octave, *x):
    return self.perlins[octave].value(*x)
