from __future__ import division
import random
import numpy
from collections import deque
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Point(object):
  def __init__(self, x, z):
    self.x = x
    self.z = z

  def __mul__(self, other):
    return Point(self.x * other, self.z * other)

  def __add__(self, other):
    return Point(self.x + other.x, self.z + other.z)

  def t(self):
    return (self.x, self.z)

  def __repr__(self):
    return "Point: (%d, %d)" % (self.x, self.z)


# 0 - Undefined square
# 1 - Wall
# 2 - Floor
class Maze(object):
  def __init__(self, width, height, scale, yscale, num_runners, dead_end_chance):
    self.width = width
    self.height = height
    self.scale = scale
    self.yscale = yscale
    self.num_runners = num_runners
    self.dead_end_chance = dead_end_chance
    self.map = numpy.zeros((width,height),numpy.int8)
    self.startPoint = Point(random.randint(0, width - 1), random.randint(0, height - 1))
    self.generate_maze()
    self.generate_list()

  def generate_maze(self):
    self.map[self.startPoint.t()] = 2
    runners = deque([self.startPoint])
    while (len(runners) > 0):
      current = runners.popleft()
      next = self.choose_direction(current)
      num = 0
      while len(runners) < self.num_runners and next is not None:
        if random.random() < self.dead_end_chance:
          self.map[next.t()] = 1
        else:
          self.map[next.t()] = 2
          runners.append(next)
        num += 1
        next = self.choose_direction(current)
      for point in self.neighbours(current):
        self.map[point.t()] = 1
    self.draw()
    
    
  def choose_direction(self, point):
    # Generate all neighbouring points
    n = self.neighbours(point)
    # Return None if no possible neighbour
    if len(n) == 0:
      return None
    else:
      return random.choice(list(n))

  
  def neighbours(self, point):
    n = set((Point(point.x - 1, point.z),
             Point(point.x + 1, point.z),
             Point(point.x, point.z - 1),
             Point(point.x, point.z + 1)))
#    print n
    # Remove neighbours outside map
    outsiders = set(filter(lambda p: p.x not in range(self.width) or p.z not in range(self.height), n))
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
    for z in range(self.height):
      print '#',
      for x in range(self.width):
        if x == self.startPoint.x and z == self.startPoint.z:
          print 'x'
        else:
          print ['?','#',' '][self.map[x,z]],
      print '#'
    for j in range(self.width+1):
      print '#',
    print '#'
  
  def generate_list(self):
    self.listID = glGenLists(1)
    glNewList(self.listID, GL_COMPILE_AND_EXECUTE)
    glBegin(GL_QUADS)
    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.6,0,0.3))
    for x in range(self.width):
      for z in range(self.height):
        if self.map[x,z] != 2:
          # Generate cube centered at x,z
          if x != self.width - 1 and self.map[x+1,z] == 2:
            glNormal( 1, 0, 0)
            glVertex((x + 0.5 - self.width / 2) * self.scale + self.scale / 2, -self.yscale, (z + 0.5 - self.height / 2) * self.scale + self.scale / 2)
            glVertex((x + 0.5 - self.width / 2) * self.scale + self.scale / 2, -self.yscale, (z + 0.5 - self.height / 2) * self.scale - self.scale / 2)
            glVertex((x + 0.5 - self.width / 2) * self.scale + self.scale / 2, self.yscale, (z + 0.5 - self.height / 2) * self.scale - self.scale / 2)
            glVertex((x + 0.5 - self.width / 2) * self.scale + self.scale / 2, self.yscale, (z + 0.5 - self.height / 2) * self.scale + self.scale / 2)
          if x != 0 and self.map[x-1,z] == 2:
            glNormal(-1, 0, 0)
            glVertex((x + 0.5 - self.width / 2) * self.scale - self.scale / 2, -self.yscale, (z + 0.5 - self.height / 2) * self.scale - self.scale / 2)
            glVertex((x + 0.5 - self.width / 2) * self.scale - self.scale / 2, -self.yscale, (z + 0.5 - self.height / 2) * self.scale + self.scale / 2)
            glVertex((x + 0.5 - self.width / 2) * self.scale - self.scale / 2, self.yscale, (z + 0.5 - self.height / 2) * self.scale + self.scale / 2)
            glVertex((x + 0.5 - self.width / 2) * self.scale - self.scale / 2, self.yscale, (z + 0.5 - self.height / 2) * self.scale - self.scale / 2)
          if z != self.height - 1 and self.map[x,z+1] == 2:
            glNormal( 0, 0, 1)
            glVertex((x + 0.5 - self.width / 2) * self.scale - self.scale / 2, -self.yscale, (z + 0.5 - self.height / 2) * self.scale + self.scale / 2)
            glVertex((x + 0.5 - self.width / 2) * self.scale + self.scale / 2, -self.yscale, (z + 0.5 - self.height / 2) * self.scale + self.scale / 2)
            glVertex((x + 0.5 - self.width / 2) * self.scale + self.scale / 2, self.yscale, (z + 0.5 - self.height / 2) * self.scale + self.scale / 2)
            glVertex((x + 0.5 - self.width / 2) * self.scale - self.scale / 2, self.yscale, (z + 0.5 - self.height / 2) * self.scale + self.scale / 2)
          if z != 0 and self.map[x,z-1] == 2:
            glNormal( 0, 0,-1)
            glVertex((x + 0.5 - self.width / 2) * self.scale + self.scale / 2, -self.yscale, (z + 0.5 - self.height / 2) * self.scale - self.scale / 2)
            glVertex((x + 0.5 - self.width / 2) * self.scale - self.scale / 2, -self.yscale, (z + 0.5 - self.height / 2) * self.scale - self.scale / 2)
            glVertex((x + 0.5 - self.width / 2) * self.scale - self.scale / 2, self.yscale, (z + 0.5 - self.height / 2) * self.scale - self.scale / 2)
            glVertex((x + 0.5 - self.width / 2) * self.scale + self.scale / 2, self.yscale, (z + 0.5 - self.height / 2) * self.scale - self.scale / 2)
          glNormal( 0, 1, 0)
          #glVertex((x + 0.5 - self.width / 2) * self.scale + self.scale / 2, self.yscale, (z + 0.5 - self.height / 2) * self.scale + self.scale / 2)
          #glVertex((x + 0.5 - self.width / 2) * self.scale + self.scale / 2, self.yscale, (z + 0.5 - self.height / 2) * self.scale - self.scale / 2)
          #glVertex((x + 0.5 - self.width / 2) * self.scale - self.scale / 2, self.yscale, (z + 0.5 - self.height / 2) * self.scale - self.scale / 2)
          #glVertex((x + 0.5 - self.width / 2) * self.scale - self.scale / 2, self.yscale, (z + 0.5 - self.height / 2) * self.scale + self.scale / 2)
    glNormal( 1, 0, 0)
    glVertex(-self.width / 2 * self.scale, -self.yscale,  self.height / 2 * self.scale)
    glVertex(-self.width / 2 * self.scale, -self.yscale, -self.height / 2 * self.scale)
    glVertex(-self.width / 2 * self.scale, self.yscale, -self.height / 2 * self.scale)
    glVertex(-self.width / 2 * self.scale, self.yscale,  self.height / 2 * self.scale)
    glNormal(-1, 0, 0)
    glVertex( self.width / 2 * self.scale, -self.yscale, -self.height / 2 * self.scale)
    glVertex( self.width / 2 * self.scale, -self.yscale,  self.height / 2 * self.scale)
    glVertex( self.width / 2 * self.scale, self.yscale,  self.height / 2 * self.scale)
    glVertex( self.width / 2 * self.scale, self.yscale, -self.height / 2 * self.scale)
    glNormal( 0, 0, 1)
    glVertex(-self.width / 2 * self.scale, -self.yscale, -self.height / 2 * self.scale)
    glVertex( self.width / 2 * self.scale, -self.yscale, -self.height / 2 * self.scale)
    glVertex( self.width / 2 * self.scale, self.yscale, -self.height / 2 * self.scale)
    glVertex(-self.width / 2 * self.scale, self.yscale, -self.height / 2 * self.scale)
    glNormal( 0, 0,-1)
    glVertex( self.width / 2 * self.scale, -self.yscale,  self.height / 2 * self.scale)
    glVertex(-self.width / 2 * self.scale, -self.yscale,  self.height / 2 * self.scale)
    glVertex(-self.width / 2 * self.scale, self.yscale,  self.height / 2 * self.scale)
    glVertex( self.width / 2 * self.scale, self.yscale,  self.height / 2 * self.scale)
    glEnd()
    glEndList()
    
  def display(self):
    glCallList(self.listID)
    # None
