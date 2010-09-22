from __future__ import division
import random
import numpy

class Point(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)


def neighbours(point):
  n = Set(Point(point.x - 1, point.y),
          Point(point.x + 1, point.y),
          Point(point.x, point.y - 1),
          Point(point.x, point.y + 1))
  # Remove neighbours outside map
  outsiders = set(filter(lambda p: p.x not in range(width) or p.y not in range(height), n))
  n -= outsiders
  # Remove neighbours that have been specified
  specs = set(n.filter(lambda p: self.map[p] == 1 or self.map[p] == 2))
  n -= specs
  return n


# 0 - Undefined square
# 1 - Wall
# 2 - Floor
class Maze(object):
  def __init__(self, width, height, num):
    self.width = width
    self.height = height
    self.numRunners = num
    self.map = numpy.zeros((width,height),numpy.int8)
    self.startPoint = Point(random.randint(0, width - 1), random.randint(0, height - 1))
    self.generateMaze()

  def generateMaze(self):
    self.map.startPoint = 2
    runners = [self.startPoint]
    while (len(runners) > 0):
      current = runners.pop()
      next = chooseDirection(current)
      while len(runners) < self.numRunners - 1 and next is not None:
        self.map[next] = 2
        runners.append(next)
        next = chooseDirection(current)
      [self.map[point] = 1 for point in neighbours(current)]
      self.draw()
    
    
  def chooseDirection(self, point):
    # Generate all neighbouring points
    n = neighbours(point)
    # Return None if no possible neighbour
    if len(n) == 0:
      return None
    else
      return random.choice(n)
  
  def draw(self):
    for i in range(height):
      for j in range(width):
        print ['?','+',' '][self.map[j,i]],
      print ''
    stdio.readline()

Maze(10,10,1)
