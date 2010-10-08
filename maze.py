# -*- coding: utf-8 -*-
from __future__ import division

import random, numpy, math
from collections import deque

from fractal_map import FractalMap
from geom3 import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def cross(a, b):
  return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def normal(center_point, clockwise, widdershins):
  n = numpy.zeros((len(center_point),len(center_point[0]),3))
  for i in range(len(center_point)):
    for j in range(len(center_point[0])):
      n[i,j] = cross((widdershins - center_point)[i,j], (clockwise - center_point)[i,j])
  return n


def smoothed_normals(a, direction):
  # print y
  if direction == 'forward':
    n = (normal(a[1:-2, 1:-2], a[ :-3,1:-2], a[1:-2, :-3]) +
         normal(a[1:-2, 1:-2], a[1:-2, :-3], a[2:-1,1:-2]) +
         normal(a[1:-2, 1:-2], a[2:-1,1:-2], a[1:-2,2:-1]) +
         normal(a[1:-2, 1:-2], a[1:-2,2:-1], a[ :-3,1:-2])) / 4
  elif direction == 'backward':
    n = (normal(a[1:-2, 1:-2], a[1:-2, :-3], a[ :-3,1:-2]) +
         normal(a[1:-2, 1:-2], a[2:-1,1:-2], a[1:-2, :-3]) +
         normal(a[1:-2, 1:-2], a[1:-2,2:-1], a[2:-1,1:-2]) +
         normal(a[1:-2, 1:-2], a[ :-3,1:-2], a[1:-2,2:-1])) / 4
  return n


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



class Cell(object):
  def __init__(self, x, z, scale, y_scale, size, disp_map, res, dist, walls):
    self.x = x
    self.z = z
    self.scale = scale
    self.y_scale = y_scale
    self.size = size
    self.disp_map = disp_map
    self.res = res
    self.dist = dist
    self.walls = walls
    
    
  def gl_init(self):
    self.listID = glGenLists(1)
    self.generate_list()
    
    
  def generate_list(self):
    glNewList(self.listID, GL_COMPILE_AND_EXECUTE); glBegin(GL_TRIANGLES)
    
    # glColor(0.6,0.3,0)
    roof =  self.y_scale * self.scale / 2
    flor = -self.y_scale * self.scale / 2
    rite =  self.x * self.scale + self.scale / 2
    left =  self.x * self.scale - self.scale / 2
    ford =  self.z * self.scale + self.scale / 2
    back =  self.z * self.scale - self.scale / 2
    
    self.generate_flor(left, rite, flor, back, ford)
    self.generate_roof(left, rite, roof, back, ford)
    for wall in self.walls:
      if   wall == 'right':   self.generate_rite(      rite, roof, flor, back, ford)
      elif wall == 'left':    self.generate_left(left,       roof, flor, back, ford)
      elif wall == 'forward': self.generate_ford(left, rite, roof, flor,       ford)
      elif wall == 'back':    self.generate_back(left, rite, roof, flor, back      )
    
    glEnd(); glEndList()
  
  def generate_flor(self, left, rite, flor, back, ford):
    res = self.res
    size = self.res + 4
    y_scale = self.dist
    x_scale = (rite - left) / res
    z_scale = (ford - back) / res
    
    y = numpy.zeros((size, size))
    for i in range(size):
      x = left + (i - 1) * x_scale
      for j in range(size):
        z = back + (j - 1) * z_scale
        y[i, j] = self.disp_map[x, flor, z] * y_scale
    y[(1,-3), 1:-1] = numpy.zeros((2,size-2))
    y[1:-1, (1,-3)] = numpy.zeros((size-2,2))
    
    a = numpy.asarray([[(x * x_scale, y[x,z], z * z_scale) for z in range(size)] for x in range(size)])
    n = smoothed_normals(a, 'forward')
    
    for i in range(1, size - 3):
      x1 = left + (i - 1) * x_scale; x2 = x1 + x_scale
      for j in range(1, size - 3):
        z1 = back + (j - 1) * z_scale; z2 = z1 + z_scale
        
        x = x1; y1 = (flor + y[i  , j  ]); z = z1
        tx = x / self.size / self.scale; ty = y1 / self.size / self.y_scale; tz = z / self.size / self.scale
        glNormal(*n[i-1][j-1]); glTexCoord3f(tx, ty, tz); glVertex(x, y1, z)
        
        x = x2; y1 = (flor + y[i+1, j+1]); z = z2
        tx = x / self.size / self.scale; ty = y1 / self.size / self.y_scale; tz = z / self.size / self.scale
        glNormal(*n[i  ][j  ]); glTexCoord3f(tx, ty, tz); glVertex(x, y1, z)
        
        x = x2; y1 = (flor + y[i+1, j  ]); z = z1
        tx = x / self.size / self.scale; ty = y1 / self.size / self.y_scale; tz = z / self.size / self.scale
        glNormal(*n[i  ][j-1]); glTexCoord3f(tx, ty, tz); glVertex(x, y1, z)
        
        x = x1; y1 = (flor + y[i  , j  ]); z = z1
        tx = x / self.size / self.scale; ty = y1 / self.size / self.y_scale; tz = z / self.size / self.scale
        glNormal(*n[i-1][j-1]); glTexCoord3f(tx, ty, tz); glVertex(x, y1, z)
        
        x = x1; y1 = (flor + y[i  , j+1]); z = z2
        tx = x / self.size / self.scale; ty = y1 / self.size / self.y_scale; tz = z / self.size / self.scale
        glNormal(*n[i-1][j  ]); glTexCoord3f(tx, ty, tz); glVertex(x, y1, z)
        
        x = x2; y1 = (flor + y[i+1, j+1]); z = z2
        tx = x / self.size / self.scale; ty = y1 / self.size / self.y_scale; tz = z / self.size / self.scale
        glNormal(*n[i  ][j  ]); glTexCoord3f(tx, ty, tz); glVertex(x, y1, z)
  
  def generate_roof(self, left, rite, roof, back, ford):
    res = self.res
    size = self.res + 4
    y_scale = self.dist
    x_scale = (rite - left) / res
    z_scale = (ford - back) / res
    
    y = numpy.zeros((size, size))
    for i in range(size):
      x = left + (i - 1) * x_scale
      for j in range(size):
        z = back + (j - 1) * z_scale
        y[i, j] = self.disp_map[x, roof, z] * y_scale
    y[(1,-3), 1:-1] = numpy.zeros((2,size-2))
    y[1:-1, (1,-3)] = numpy.zeros((size-2,2))
    
    a = numpy.asarray([[(x * x_scale, y[x,z], z * z_scale) for z in range(size)] for x in range(size)])
    n = smoothed_normals(a, 'backward')
    
    for i in range(1, size - 3):
      x1 = left + (i - 1) * x_scale
      x2 = x1 + x_scale
      for j in range(1, size - 3):
        z1 = back + (j - 1) * z_scale
        z2 = z1 + z_scale
        glNormal(*n[i-1][j-1]); glVertex(x1, roof + y[i  ,j  ], z1)
        glNormal(*n[i  ][j-1]); glVertex(x2, roof + y[i+1,j  ], z1)
        glNormal(*n[i  ][j  ]); glVertex(x2, roof + y[i+1,j+1], z2)
        
        glNormal(*n[i-1][j-1]); glVertex(x1, roof + y[i  ,j  ], z1)
        glNormal(*n[i  ][j  ]); glVertex(x2, roof + y[i+1,j+1], z2)
        glNormal(*n[i-1][j  ]); glVertex(x1, roof + y[i  ,j+1], z2)
  
  def generate_left(self, left, roof, flor, back, ford):
    res = self.res
    size = self.res + 4
    y_scale = (roof - flor) / res
    x_scale = self.dist
    z_scale = (ford - back) / res
    
    x = numpy.zeros((size, size))
    for i in range(size):
      y = flor + (i - 1) * y_scale
      for j in range(size):
        z = back + (j - 1) * z_scale
        x[i, j] = self.disp_map[left, y, z] * x_scale
    x[(1,-3), 1:-1] = numpy.zeros((2,size-2))
    x[1:-1, (1,-3)] = numpy.zeros((size-2,2))
    
    a = numpy.asarray([[(x[y,z], y * y_scale, z * z_scale) for z in range(size)] for y in range(size)])
    n = smoothed_normals(a, 'backward')
    
    for i in range(1, size - 3):
      y1 = flor + (i - 1) * y_scale
      y2 = y1 + y_scale
      for j in range(1, size - 3):
        z1 = back + (j - 1) * z_scale
        z2 = z1 + z_scale
        glNormal(*n[i-1][j-1]); glVertex(left + x[i  ,j  ], y1, z1)
        glNormal(*n[i  ][j-1]); glVertex(left + x[i+1,j  ], y2, z1)
        glNormal(*n[i  ][j  ]); glVertex(left + x[i+1,j+1], y2, z2)
        
        glNormal(*n[i-1][j-1]); glVertex(left + x[i  ,j  ], y1, z1)
        glNormal(*n[i  ][j  ]); glVertex(left + x[i+1,j+1], y2, z2)
        glNormal(*n[i-1][j  ]); glVertex(left + x[i  ,j+1], y1, z2)
  
  def generate_rite(self, rite, roof, flor, back, ford):
    res = self.res
    size = self.res + 4
    y_scale = (roof - flor) / res
    x_scale = self.dist
    z_scale = (ford - back) / res
    
    x = numpy.zeros((size, size))
    for i in range(size):
      y = flor + (i - 1) * y_scale
      for j in range(size):
        z = back + (j - 1) * z_scale
        x[i, j] = self.disp_map[rite, y, z] * x_scale
    x[(1,-3), 1:-1] = numpy.zeros((2,size-2))
    x[1:-1, (1,-3)] = numpy.zeros((size-2,2))
    
    a = numpy.asarray([[(x[y,z], y * y_scale, z * z_scale) for z in range(size)] for y in range(size)])
    n = smoothed_normals(a, 'forward')
    
    for i in range(1, size - 3):
      y1 = flor + (i - 1) * y_scale
      y2 = y1 + y_scale
      for j in range(1, size - 3):
        z1 = back + (j - 1) * z_scale
        z2 = z1 + z_scale
        glNormal(*n[i-1][j-1]); glVertex(rite + x[i  ,j  ], y1, z1)
        glNormal(*n[i  ][j  ]); glVertex(rite + x[i+1,j+1], y2, z2)
        glNormal(*n[i  ][j-1]); glVertex(rite + x[i+1,j  ], y2, z1)
        
        glNormal(*n[i-1][j-1]); glVertex(rite + x[i  ,j  ], y1, z1)
        glNormal(*n[i-1][j  ]); glVertex(rite + x[i  ,j+1], y1, z2)
        glNormal(*n[i  ][j  ]); glVertex(rite + x[i+1,j+1], y2, z2)
  
  def generate_ford(self, left, rite, roof, flor, ford):
    res = self.res
    size = self.res + 4
    y_scale = (roof - flor) / res
    x_scale = (rite - left) / res
    z_scale = self.dist
    
    z = numpy.zeros((size, size))
    for i in range(size):
      x = left + (i - 1) * x_scale
      for j in range(size):
        y = flor + (j - 1) * y_scale
        z[i, j] = self.disp_map[x, y, ford] * z_scale
    z[(1,-3), 1:-1] = numpy.zeros((2,size-2))
    z[1:-1, (1,-3)] = numpy.zeros((size-2,2))
    
    a = numpy.asarray([[(x * x_scale, y * y_scale, z[x,y]) for y in range(size)] for x in range(size)])
    n = smoothed_normals(a, 'forward')
    
    for i in range(1, size - 3):
      x1 = left + (i - 1) * x_scale
      x2 = x1 + x_scale
      for j in range(1, size - 3):
        y1 = flor + (j - 1) * y_scale
        y2 = y1 + y_scale
        glNormal(*n[i-1][j-1]); glVertex(x1, y1, ford + z[i  ,j  ])
        glNormal(*n[i  ][j  ]); glVertex(x2, y2, ford + z[i+1,j+1])
        glNormal(*n[i  ][j-1]); glVertex(x2, y1, ford + z[i+1,j  ])
        
        glNormal(*n[i-1][j-1]); glVertex(x1, y1, ford + z[i  ,j  ])
        glNormal(*n[i-1][j  ]); glVertex(x1, y2, ford + z[i  ,j+1])
        glNormal(*n[i  ][j  ]); glVertex(x2, y2, ford + z[i+1,j+1])
  
  def generate_back(self, left, rite, roof, flor, back):
    res = self.res
    size = self.res + 4
    y_scale = (roof - flor) / res
    x_scale = (rite - left) / res
    z_scale = self.dist
    
    z = numpy.zeros((size, size))
    for i in range(size):
      x = left + (i - 1) * x_scale
      for j in range(size):
        y = flor + (j - 1) * y_scale
        z[i, j] = self.disp_map[x, y, back] * z_scale
    z[(1,-3), 1:-1] = numpy.zeros((2,size-2))
    z[1:-1, (1,-3)] = numpy.zeros((size-2,2))
    
    a = numpy.asarray([[(x * x_scale, y * y_scale, z[x,y]) for y in range(size)] for x in range(size)])
    n = smoothed_normals(a, 'backward')
    
    for i in range(1, size - 3):
      x1 = left + (i - 1) * x_scale
      x2 = x1 + x_scale
      for j in range(1, size - 3):
        y1 = flor + (j - 1) * y_scale
        y2 = y1 + y_scale
        glNormal(*n[i-1][j-1]); glVertex(x1, y1, back + z[i  ,j  ])
        glNormal(*n[i  ][j-1]); glVertex(x2, y1, back + z[i+1,j  ])
        glNormal(*n[i  ][j  ]); glVertex(x2, y2, back + z[i+1,j+1])
        
        glNormal(*n[i-1][j-1]); glVertex(x1, y1, back + z[i  ,j  ])
        glNormal(*n[i  ][j  ]); glVertex(x2, y2, back + z[i+1,j+1])
        glNormal(*n[i-1][j  ]); glVertex(x1, y2, back + z[i  ,j+1])
  
  def display(self):
    glCallList(self.listID)
  
  
# 0 - Undefined square
# 1 - Wall
# 2 - Floor
class Maze(object):
  def __init__(self, config):
    self.size = config['size']
    self.scale = config['scale']
    self.y_scale = config['y_scale']
    num_runners = config['num_runners']
    dead_end_chance = config['dead_end_chance']
    
    self.startPoint = Point(random.randint(0, self.size - 1), random.randint(0, self.size - 1))
    self.gen_maze(num_runners, dead_end_chance)
    
    disp_map = FractalMap(config['disp_map']['octaves'], config['disp_map']['persistence'])
    self.gen_cells(disp_map, config['disp_map']['res'], config['disp_map']['dist'])
    
    tex_map = FractalMap(config['tex_map']['octaves'], config['tex_map']['persistence'])
    self.tex_res = config['tex_map']['res']
    self.gen_tex(tex_map, self.tex_res)
    
    
  def gen_maze(self, num_runners, dead_end_chance):
    self.map = numpy.zeros((self.size,self.size),numpy.int8)
    self.map[self.startPoint.t()] = 2
    runners = deque([self.startPoint])
    while (len(runners) > 0):
      current = runners.popleft()
      next = self.choose_direction(current)
      while len(runners) < num_runners and next is not None:
        if random.random() < dead_end_chance:
          self.map[next.t()] = 1
        else:
          self.map[next.t()] = 2
          runners.append(next)
        next = self.choose_direction(current)
      for point in self.neighbours(current):
        self.map[point.t()] = 1
    self.draw()
    
    
  def gen_cells(self, disp_map, res, dist):
    self.cells = []
    for x in range(self.size):
      for z in range(self.size):
        if self.map[x, z] == 2:
          walls = []
          if x == self.size - 1 or self.map[x+1,z] != 2: walls.append('right')
          if x == 0 or self.map[x-1,z] != 2:             walls.append('left')
          if z == self.size - 1 or self.map[x,z+1] != 2: walls.append('forward')
          if z == 0 or self.map[x,z-1] != 2:             walls.append('back')
          self.cells.append(Cell(x - self.size/2, z - self.size/2, self.scale, self.y_scale, self.size, disp_map, res, dist, walls))
    
    
  def gen_tex(self, tex_map, res):
    self.texture = numpy.zeros((res,res,res,3),'ubyte')
    brown = Vector3(0, 0, 0)
    for x in range(res):
      for y in range(res):
        for z in range(res):
          value = int(tex_map[x,y,z] * 255)
          self.texture[x,y,z] = list(Vector3(value, value, value) + brown)
    
    
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
    # Remove neighbours outside map
    outsiders = set(filter(lambda p: p.x not in range(self.size) or p.z not in range(self.size), n))
    n -= outsiders
    po = random.choice(list(n))
    # Remove neighbours that have been specified
    specs = set(filter(lambda p: self.map[p.t()] == 1 or self.map[p.t()] == 2, n))
    n -= specs
    return n
    
    
  def draw(self):
    for j in range(self.size+1):
      print '#',
    print '#'
    for z in range(self.size):
      print '#',
      for x in range(self.size):
        if x == self.startPoint.x and z == self.startPoint.z:
          print 'x',
        else:
          print ['?','#',' '][self.map[x,z]],
      print '#'
    for j in range(self.size+1):
      print '#',
    print '#'
    
    
  def gl_init(self):
    [cell.gl_init() for cell in self.cells]
    self.textureID = glGenTextures(1); glBindTexture(GL_TEXTURE_2D, self.textureID)
    glTexImage3D(GL_TEXTURE_3D, 0, GL_RGB, self.tex_res, self.tex_res, self.tex_res, 0, GL_RGB, GL_UNSIGNED_BYTE, self.texture)
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glTexEnvi(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
    glEnable(GL_TEXTURE_3D)
    
    
  def generate_outer_walls(self, left, rite, roof, flor, back, ford):
    glNormal( 1,  0,  0)
    glVertex(rite, flor, back)
    glVertex(rite, flor, ford)
    glVertex(rite, roof, ford)
    glVertex(rite, roof, back)
    glNormal(-1,  0,  0)
    glVertex(left, flor, ford)
    glVertex(left, flor, back)
    glVertex(left, roof, back)
    glVertex(left, roof, ford)
    glNormal( 0,  0,  1)
    glVertex(rite, flor, ford)
    glVertex(left, flor, ford)
    glVertex(left, roof, ford)
    glVertex(rite, roof, ford)
    glNormal( 0,  0, -1)
    glVertex(left, flor, back)
    glVertex(rite, flor, back)
    glVertex(rite, roof, back)
    glVertex(left, roof, back)
    
    
  def display(self):
    glBindTexture(GL_TEXTURE_2D, self.textureID)
    [cell.display() for cell in self.cells]
    
