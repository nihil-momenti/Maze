from __future__ import division

import random

class Perlin(object):
  def __init__(self, octaves, h):
    self.octaves = octaves
    self.seeds = [random.random() for i in octaves]

  def value(self, x, y, z):
    k = 0.0
    for octave in range(self.octaves):
      k += self.smoothed(octave, x, y, z)
    return k

  def smoothed(self, octave, x, y, z):
    unsmoothed = self.unsmoothed(octave, x, y, z)
    # smooth

  def unsmoothed(self, octave, x, y, z):
    random.setSeed(self.seeds[octave] + 7 * x + 13 * y + 29 * z)

