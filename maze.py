from __future__ import division
import random
import numpy
from collections import deque

class Point(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def t(self):
    return (self.x, self.y)

  def __repr__(self):
    return "Point: (%d, %d)" % (self.x, self.y)


# 0 - Undefined square
# 1 - Wall
# 2 - Floor
class Maze(object):
  def __init__(self, width, height, num, dead_end_chance):
    self.width = width
    self.height = height
    self.numRunners = num
    self.dead_end_chance = dead_end_chance
    self.map = numpy.zeros((width,height),numpy.int8)
    self.startPoint = Point(random.randint(0, width - 1), random.randint(0, height - 1))
    self.generateMaze()

  def generateMaze(self):
    self.map[self.startPoint.t()] = 2
    runners = deque([self.startPoint])
    while (len(runners) > 0):
      current = runners.popleft()
      next = self.chooseDirection(current)
      while len(runners) < self.numRunners and next is not None:
        if random.random() < self.dead_end_chance:
          self.map[next.t()] = 1
        else:
          self.map[next.t()] = 2
          runners.append(next)
        next = self.chooseDirection(current)
      for point in self.neighbours(current):
        self.map[point.t()] = 1
      self.draw()
    
    
  def chooseDirection(self, point):
    # Generate all neighbouring points
    n = self.neighbours(point)
    # Return None if no possible neighbour
    if len(n) == 0:
      return None
    else:
      return random.choice(list(n))

  
  def neighbours(self, point):
    n = set((Point(point.x - 1, point.y),
             Point(point.x + 1, point.y),
             Point(point.x, point.y - 1),
             Point(point.x, point.y + 1)))
#    print n
    # Remove neighbours outside map
    outsiders = set(filter(lambda p: p.x not in range(self.width) or p.y not in range(self.height), n))
    n -= outsiders
#    print n
#    print self.map
    po = random.choice(list(n))
#    print po
#    print self.map[po.t()]
    # Remove neighbours that have been specified
    specs = set(filter(lambda p: self.map[p.t()] == 1 or self.map[p.t()] == 2, n))
    n -= specs
    return n


  def draw(self):
    for j in range(self.width+1):
      print '#',
    print '#'
    for i in range(self.height):
      print '#',
      for j in range(self.width):
        print ['?','#',' '][self.map[j,i]],
      print '#'
    for j in range(self.width+1):
      print '#',
    print '#'
    raw_input()

Maze(40,40,6,0.4)
