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
      self.big1 = random.randint(10000,20000)
      self.big2 = random.randint(750000,1000000)
      self.big3 = random.randint(1000000000,1500000000)
      Randomiser.seed += 1
  
  # Crap randomiser, need to find something with less repetition
  # Works okay for fractal generation though
  def value(self, *x):
    n = 0
    for i in range(len(x)):
      n += int(x[i] * Randomiser.small[i])
    n = (n<<13) ^ n;
    return ( 1.0 - ( (n * (n * n * self.big1 + self.big2) + self.big3) & 0x7fffffff) / 1073741824.0)