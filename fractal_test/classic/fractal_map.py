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
  
  def value(self, *x, **params):
    k = 0.0
    octaves = params['octave'] if 'octave' in params else self.octaves
    for octave in range(self.octaves - octaves):
      x = [xn / 2 for xn in x]
    for octave in range(self.octaves - octaves, self.octaves):
      k += (self.p ** (self.octaves - octave - 1)) * self.noise(octave, *x)
      x = [xn / 2 for xn in x]
    return k
  
  def noise(self, octave, *x):
    return self.perlins[octave].value(*x)
