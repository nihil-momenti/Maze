from __future__ import division
import random
from math import floor

class Randomiser(object):
  big1 = (14867, 15511, 15731, 16477, 16619, 18731)
  big2 = (750413, 755509, 761203, 766039, 770741, 789221)
  big3 = (1000001311, 1002051137 , 1034350277, 1169800543, 1287050543, 1376312589) 
  small = (1, 41, 89, 139, 167)
  tiny = (5, 7, 11, 13, 17, 19)
  c = 12345
  m = 2 ** 32
  z = 2 ** 30
  seed = 0
  def __init__(self):
      self.seed = Randomiser.seed
      Randomiser.seed += 1
  
  # Crap randomiser, need to find something with less repetition
  def value(self, *x):
    n = 0
    for i in range(len(x)):
      n += int(x[i] * Randomiser.small[i])
    # n = (n<<Randomiser.tiny[self.seed]) ^ n;
    # return (1.0 - (((1103515245 * n + 12345) & 0xFFFFFFFF) & 0x3FFFFFFF) / 536870911.0)
    n = (n<<13) ^ n;
    return ( 1.0 - ( (n * (n * n * Randomiser.big1[self.seed] + Randomiser.big2[self.seed]) + Randomiser.big3[self.seed]) & 0x7fffffff) / 1073741824.0)