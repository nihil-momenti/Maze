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
      norm = numpy.cross((widdershins - center_point)[i,j], (clockwise - center_point)[i,j])
      n[i,j] = norm / numpy.linalg.norm(norm)
  # print n
  return n


def smoothed_normals(a, direction):
  if direction == 'forward':
    n = (normal(a[1:-1, 1:-1], a[ :-2,1:-1], a[1:-1, :-2]) +
         normal(a[1:-1, 1:-1], a[1:-1, :-2], a[2:  ,1:-1]) +
         normal(a[1:-1, 1:-1], a[2:  ,1:-1], a[1:-1,2:  ]) +
         normal(a[1:-1, 1:-1], a[1:-1,2:  ], a[ :-2,1:-1])) / 4
  elif direction == 'backward':
    n = (normal(a[1:-1, 1:-1], a[1:-1, :-2], a[ :-2,1:-1]) +
         normal(a[1:-1, 1:-1], a[2:  ,1:-1], a[1:-1, :-2]) +
         normal(a[1:-1, 1:-1], a[1:-1,2:  ], a[2:  ,1:-1]) +
         normal(a[1:-1, 1:-1], a[ :-2,1:-1], a[1:-1,2:  ])) / 4
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
    
    roof = -self.y_scale * self.scale / 2
    flor = +self.y_scale * self.scale / 2
    rite =  self.x * self.scale + self.scale / 2
    left =  self.x * self.scale - self.scale / 2
    ford =  self.z * self.scale + self.scale / 2
    back =  self.z * self.scale - self.scale / 2
    
    self.generate_wall(left, rite, flor, roof, back, ford, 1, 'forward') # floor
    self.generate_wall(left, rite, flor, roof, back, ford, 1, 'backward') # roof
    for wall in self.walls:
      if   wall == 'right':   self.generate_wall(left, rite, flor, roof, back, ford, 0, 'forward')
      elif wall == 'left':    self.generate_wall(left, rite, flor, roof, back, ford, 0, 'backward')
      elif wall == 'forward': self.generate_wall(left, rite, flor, roof, back, ford, 2, 'forward')
      elif wall == 'back':    self.generate_wall(left, rite, flor, roof, back, ford, 2, 'backward')
    
    glEnd(); glEndList()
  
  def generate_wall(self, left, rite, flor, roof, back, ford, xyz, direction):
    size = self.res + 3
    scales = [(rite - left) / self.res, (roof - flor) / self.res, (ford - back) / self.res]
    scales[xyz] = self.dist
    
    frnts = [rite, roof, ford]
    backs = [left, flor, back]
    
    disp = numpy.zeros((size, size))
    for i in range(size):
      a = backs[xyz - 1] + (i - 1) * scales[xyz - 1]
      for j in range(size):
        b = backs[xyz + 1 - 3] + (j - 1) * scales[xyz + 1 - 3]
        c = [backs[xyz], b, a] if xyz == 0 else [a, backs[xyz], b] if xyz == 1 else [b, a, backs[xyz]]
        disp[i, j] = self.disp_map[c[0], c[1], c[2]] * scales[xyz]
    #disp[(1,-2), 1:-1] = numpy.zeros((2,size-2))
    #disp[1:-1, (1,-2)] = numpy.zeros((size-2,2))
    
    a = numpy.asarray(
      [
        [
          [disp[a, b], b * scales[xyz + 1 - 3], a * scales[xyz - 1]] if xyz == 0 else
          [a * scales[xyz - 1], disp[a, b], b * scales[xyz + 1 - 3]] if xyz == 1 else
          [b * scales[xyz + 1 - 3], a * scales[xyz - 1], disp[a, b]]
        for b in range(size)
        ]
      for a in range(size)
      ]
    )
    n = smoothed_normals(a, direction)
    
    for i in range(1, size - 2):
      a1 = backs[xyz - 1] + (i - 1) * scales[xyz - 1]; a2 = a1 + scales[xyz - 1]
      for j in range(1, size - 2):
        b1 = backs[xyz + 1 - 3] + (j - 1) * scales[xyz + 1 - 3]; b2 = b1 + scales[xyz + 1 - 3]
        
        
        if direction == 'forward':
          c = [frnts[xyz], b1, a1]; [c.insert(0, c.pop()) for k in range(xyz)]
          t = [
            ((c[0] + self.scale / 2) / self.scale + self.size / 2) / self.size,
            (c[1] / self.scale + self.y_scale / 2) / self.y_scale,
            ((c[2] + self.scale / 2) / self.scale + self.size / 2) / self.size
          ]
          glNormal(*n[i-1][j-1]); glTexCoord3f(*t); glVertex(*c)
          
          c = [frnts[xyz], b2, a2]; [c.insert(0, c.pop()) for k in range(xyz)]
          t = [
            ((c[0] + self.scale / 2) / self.scale + self.size / 2) / self.size,
            (c[1] / self.scale + self.y_scale / 2) / self.y_scale,
            ((c[2] + self.scale / 2) / self.scale + self.size / 2) / self.size
          ]
          glNormal(*n[i][j]); glTexCoord3f(*t); glVertex(*c)
          
          c = [frnts[xyz], b1, a2]; [c.insert(0, c.pop()) for k in range(xyz)]
          t = [
            ((c[0] + self.scale / 2) / self.scale + self.size / 2) / self.size,
            (c[1] / self.scale + self.y_scale / 2) / self.y_scale,
            ((c[2] + self.scale / 2) / self.scale + self.size / 2) / self.size
          ]
          glNormal(*n[i][j-1]); glTexCoord3f(*t); glVertex(*c)
        else:
          c = [backs[xyz], b1, a1]; [c.insert(0, c.pop()) for k in range(xyz)]
          t = [
            ((c[0] + self.scale / 2) / self.scale + self.size / 2) / self.size,
            (c[1] / self.scale + self.y_scale / 2) / self.y_scale,
            ((c[2] + self.scale / 2) / self.scale + self.size / 2) / self.size
          ]
          glNormal(*n[i-1][j-1]); glTexCoord3f(*t); glVertex(*c)
          
          c = [backs[xyz], b1, a2]; [c.insert(0, c.pop()) for k in range(xyz)]
          t = [
            ((c[0] + self.scale / 2) / self.scale + self.size / 2) / self.size,
            (c[1] / self.scale + self.y_scale / 2) / self.y_scale,
            ((c[2] + self.scale / 2) / self.scale + self.size / 2) / self.size
          ]
          glNormal(*n[i][j-1]); glTexCoord3f(*t); glVertex(*c)
          
          c = [backs[xyz], b2, a2]; [c.insert(0, c.pop()) for k in range(xyz)]
          t = [
            ((c[0] + self.scale / 2) / self.scale + self.size / 2) / self.size,
            (c[1] / self.scale + self.y_scale / 2) / self.y_scale,
            ((c[2] + self.scale / 2) / self.scale + self.size / 2) / self.size
          ]
          glNormal(*n[i][j]); glTexCoord3f(*t); glVertex(*c)
          
        
        if direction == 'forward':
          c = [frnts[xyz], b1, a1]; [c.insert(0, c.pop()) for k in range(xyz)]
          t = [
            ((c[0] + self.scale / 2) / self.scale + self.size / 2) / self.size,
            (c[1] / self.scale + self.y_scale / 2) / self.y_scale,
            ((c[2] + self.scale / 2) / self.scale + self.size / 2) / self.size
          ]
          glNormal(*n[i-1][j-1]); glTexCoord3f(*t); glVertex(*c)
          
          c = [frnts[xyz], b2, a1]; [c.insert(0, c.pop()) for k in range(xyz)]
          t = [
            ((c[0] + self.scale / 2) / self.scale + self.size / 2) / self.size,
            (c[1] / self.scale + self.y_scale / 2) / self.y_scale,
            ((c[2] + self.scale / 2) / self.scale + self.size / 2) / self.size
          ]
          glNormal(*n[i-1][j]); glTexCoord3f(*t); glVertex(*c)
          
          c = [frnts[xyz], b2, a2]; [c.insert(0, c.pop()) for k in range(xyz)]
          t = [
            ((c[0] + self.scale / 2) / self.scale + self.size / 2) / self.size,
            (c[1] / self.scale + self.y_scale / 2) / self.y_scale,
            ((c[2] + self.scale / 2) / self.scale + self.size / 2) / self.size
          ]
          glNormal(*n[i][j]); glTexCoord3f(*t); glVertex(*c)
        else:
          c = [backs[xyz], b1, a1]; [c.insert(0, c.pop()) for k in range(xyz)]
          t = [
            ((c[0] + self.scale / 2) / self.scale + self.size / 2) / self.size,
            (c[1] / self.scale + self.y_scale / 2) / self.y_scale,
            ((c[2] + self.scale / 2) / self.scale + self.size / 2) / self.size
          ]
          glNormal(*n[i-1][j-1]); glTexCoord3f(*t); glVertex(*c)
          
          c = [backs[xyz], b2, a2]; [c.insert(0, c.pop()) for k in range(xyz)]
          t = [
            ((c[0] + self.scale / 2) / self.scale + self.size / 2) / self.size,
            (c[1] / self.scale + self.y_scale / 2) / self.y_scale,
            ((c[2] + self.scale / 2) / self.scale + self.size / 2) / self.size
          ]
          glNormal(*n[i][j]); glTexCoord3f(*t); glVertex(*c)
          
          c = [backs[xyz], b2, a1]; [c.insert(0, c.pop()) for k in range(xyz)]
          t = [
            ((c[0] + self.scale / 2) / self.scale + self.size / 2) / self.size,
            (c[1] / self.scale + self.y_scale / 2) / self.y_scale,
            ((c[2] + self.scale / 2) / self.scale + self.size / 2) / self.size
          ]
          glNormal(*n[i-1][j]); glTexCoord3f(*t); glVertex(*c)
    
  def display(self):
    glCallList(self.listID)
  
  

class Maze(object):
# 0 - Undefined square
# 1 - Wall
# 2 - Floor
# 3 - Special Floor
  def __init__(self, config):
    print "      Loading config..."
    self.size = config['size']
    self.scale = config['scale']
    self.y_scale = config['y_scale']
    num_runners = config['num_runners']
    special_chance = config['special_chance']
    dead_end_chance = config['dead_end_chance']
    print "      ...Done"
    
    print "      Generating layout..."
    self.start_index = Point(random.randint(0, self.size - 1), random.randint(0, self.size - 1))
    self.gen_maze(num_runners, special_chance, dead_end_chance, self.start_index)
    print "      ...Done"
    
    print "      Generating displacement..."
    disp_map = FractalMap(config['disp_map']['octaves'], config['disp_map']['persistence'])
    self.gen_cells(disp_map, config['disp_map']['res'], config['disp_map']['dist'])
    print "      ...Done"
    
    print "      Generating texture..."
    tex_map = FractalMap(config['tex_map']['octaves'], config['tex_map']['persistence'])
    self.horiz_res = config['tex_map']['horiz_res']
    self.vert_res = config['tex_map']['vert_res']
    self.gen_tex(tex_map, self.horiz_res, self.vert_res, config['tex_map']['variability'])
    print "      ...Done"
    
    self.start_point = Point3((self.start_index.x - self.size / 2) * self.scale, 0, (self.start_index.z - self.size / 2) * self.scale)
    
  def gen_maze(self, num_runners, special_chance, dead_end_chance, start_point):
    self.map = numpy.zeros((self.size,self.size),numpy.int8)
    self.specials = set()
    self.map[start_point.t()] = 2
    runners = deque([start_point])
    while (len(runners) > 0):
      current = runners.popleft()
      next = self.choose_direction(current)
      while len(runners) < num_runners and next is not None:
        if random.random() < dead_end_chance:
          self.map[next.t()] = 1
          if random.random() < special_chance:
            self.specials.add((
              ((current + Point(-self.size/2,-self.size/2)) * self.scale).t(),
              ((next + Point(-self.size/2,-self.size/2)) * self.scale).t()
            ))
        else:
          self.map[next.t()] = 2
          runners.append(next)
        next = self.choose_direction(current)
      for point in self.neighbours(current):
        self.map[point.t()] = 1
    # self.draw()
    
  def gen_cells(self, disp_map, res, dist):
    self.cells = []
    for x in range(self.size):
      for z in range(self.size):
        if self.map[x, z] in (2, 3):
          walls = []
          if x == self.size - 1 or self.map[x+1,z] not in (2, 3): walls.append('right')
          if x == 0 or self.map[x-1,z] not in (2, 3):             walls.append('left')
          if z == self.size - 1 or self.map[x,z+1] not in (2, 3): walls.append('forward')
          if z == 0 or self.map[x,z-1] not in (2, 3):             walls.append('back')
          self.cells.append(Cell(x - self.size/2, z - self.size/2, self.scale, self.y_scale, self.size, disp_map, res, dist, walls))
    
  def gen_tex(self, tex_map, horiz_res, vert_res, var):
    self.texture = numpy.zeros((horiz_res,vert_res,horiz_res,3),'single')
    for x in range(horiz_res):
      for y in range(vert_res):
        for z in range(horiz_res):
          v = tex_map[x,y,z]
          value = [max(0., min(1., (1. + v * var) * .60)),
                   max(0., min(1., (1. + v * var) * .46)),
                   max(0., min(1., (1. + v * var) * .33))]
          # print value
          self.texture[x,y,z] = value
    
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
        if x == self.start_index.x and z == self.start_index.z:
          print 'x',
        else:
          print ['?','#',' '][self.map[x,z]],
      print '#'
    for j in range(self.size+1):
      print '#',
    print '#'
    
  def gl_init(self):
    print "    Initialising maze's OpenGL..."
    print "      Generating walls..."
    [cell.gl_init() for cell in self.cells]
    print "      ...Done"
    print "      Loading texture..."
    self.textureID = glGenTextures(1); glBindTexture(GL_TEXTURE_3D, self.textureID)
    glTexImage3D(GL_TEXTURE_3D, 0, GL_RGB, self.horiz_res, self.vert_res, self.horiz_res, 0, GL_RGB, GL_FLOAT, self.texture)
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glTexEnvi(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
    glEnable(GL_TEXTURE_3D)
    
    self.listID = glGenLists(1); glNewList(self.listID, GL_COMPILE_AND_EXECUTE)
    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT,   (0.2,0.2,0.2,1))
    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE,   (0.8,0.8,0.8,1))
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR,  (0,0,0,1))
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 0)
    [cell.display() for cell in self.cells]
    glBindTexture(GL_TEXTURE_3D, 0)
    glEndList()
    
    
    print "      ...Done"
    print "    ...Done"
    
  def display(self):
    glColor3f(1,1,1)
    glBindTexture(GL_TEXTURE_3D, self.textureID)
    glCallList(self.listID)
    
