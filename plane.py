from __future__ import division
import numpy, random, math, copy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def powerOf2(size):
  if abs(math.log(size, 2) - round(math.log(size, 2))) < 0.0000001:
    return True
  else:
    return False

def normal(center_point, clockwise, widdershins):
  n = [clockwise[z] - center_point[z] for z in range(3)]
  p = [widdershins[z] - center_point[z] for z in range(3)]
  cross = [p[1] * n[2] - p[2] * n[1], p[2] * n[0] - p[0] * n[2], p[0] * n[1] - p[1] * n[0]]
  length = math.sqrt(cross[0] ** 2 + cross[1] ** 2 + cross[2] ** 2)
  n = [cross[z] / length for z in range(3)]
  return n

class FlatPlane(object):
  def __init__(self, size, height, scale):
    self.size = size
    self.height = height
    self.scale = scale
    self.generate_list()
  
  def generate_list(self):
    self.listID = glGenLists(1)
    glNewList(self.listID, GL_COMPILE_AND_EXECUTE)
    glBegin(GL_QUADS)
    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.6,0.3,0))
    glNormal(0,1,0)
    glVertex(-self.size / 2 * self.scale, self.height, -self.size / 2 * self.scale)
    glVertex(-self.size / 2 * self.scale, self.height,  self.size / 2 * self.scale)
    glVertex( self.size / 2 * self.scale, self.height,  self.size / 2 * self.scale)
    glVertex( self.size / 2 * self.scale, self.height, -self.size / 2 * self.scale)
    glEnd()
    glEndList()
    
  def display(self):
    glCallList(self.listID)


class FirstPlane(object):
  def __init__(self, size, scale):
    self.size = size
    self.scale = scale
    self.generate_plane(size, 40, 0.95)
    self.model_plane(size)
    
  def display(self):
    glCallList(self.listID)
    
  def avgDiamondVals(self, x, z, stride, size):
    if x == 0:
      return (self.y[              x,       z - stride] +
              self.y[              x,       z + stride] +
              self.y[size-1 - stride,                z] +
              self.y[     x + stride,                z]) / 4
    elif x == size-1:
      return (self.y[               x,      z - stride] +
              self.y[               x,      z + stride] +
              self.y[      x - stride,               z] +
              self.y[      0 + stride,               z]) / 4
    elif z == 0:
      return (self.y[      x - stride,               z] +
              self.y[      x + stride,               z] +
              self.y[               x,      z + stride] +
              self.y[               x, size-1 - stride]) / 4
    elif z == size-1:
      return (self.y[      x - stride,               z] +
              self.y[      x + stride,               z] +
              self.y[               x,      z - stride] +
              self.y[               x,      0 + stride]) / 4
    else:
      return (self.y[      x - stride,               z] +
              self.y[      x + stride,               z] +
              self.y[               x,      z - stride] +
              self.y[               x,      z + stride]) / 4
    
  def avgSquareVals(self, x, z, stride):
    return (self.y[x - stride, z - stride] + 
            self.y[x - stride, z + stride] +
            self.y[x + stride, z - stride] +
            self.y[x + stride, z + stride]) / 4

  def generate_plane(self, size, height_scale, h):
    self.y = numpy.zeros((size + 1, size + 1))
    if not powerOf2(size) or size == 1:
      print "Size must be a power of two"
      raise Exception
    
    size += 1
    ratio = 2. ** -h
    
    stride = size // 2
    
    # self.y[0,0] = self.y[0,size-1] = -20
    # self.y[size-1,0] = self.y[size-1,size-1] = 50
    
    while (stride > 0):
    # for i in range(7):
      for x in range(stride, size-1, 2*stride):
        for z in range(stride, size-1, 2*stride):
          self.y[x,z] = height_scale * random.uniform(-0.5,0.5) + self.avgSquareVals(x, z, stride)
      
      oddline = False
      for x in range(0, size, stride):
        oddline = not oddline
        for z in range(stride if oddline else 0, size, 2*stride):
          self.y[x,z] = height_scale * random.uniform(-0.5,0.5) + self.avgDiamondVals(x, z, stride, size)
          # if x == 0:
            # self.y[size-1,z] = self.y[x,z]
          # if z == 0:
            # self.y[x,size-1] = self.y[x,z]
      height_scale *= ratio
      stride //= 2
      # print self.y
    
  def model_plane(self, size):
    self.listID = glGenLists(1)
    glNewList(self.listID, GL_COMPILE_AND_EXECUTE)
    glBegin(GL_TRIANGLES)
    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.6,0.3,0))
    n = [[[] for x in range(size+1)] for z in range(size+1)]
    norms = [[[] for x in range(size+1)] for z in range(size+1)]
    for x in range(size):
      for z in range(size):
        norm = normal(
          (x   - size // 2, self.y[x  ,z  ], z   - size // 2),
          (x+1 - size // 2, self.y[x+1,z  ], z   - size // 2),
          (x+1 - size // 2, self.y[x+1,z+1], z+1 - size // 2))
        norms[x][z].append(norm)
        norms[x+1][z].append(norm)
        norms[x+1][z+1].append(norm)
        norm = normal(
          (x   - size // 2, self.y[x  ,z  ], z   - size // 2),
          (x+1 - size // 2, self.y[x+1,z+1], z+1 - size // 2),
          (x   - size // 2, self.y[x  ,z+1], z+1 - size // 2))
        norms[x][z].append(norm)
        norms[x+1][z+1].append(norm)
        norms[x][z+1].append(norm)
    
    for x in range(size+1):
      for z in range(size+1):
        norm = [0,0,0]
        for k in range(len(norms[x][z])):
          norm[0] += norms[x][z][k][0] / len(norms[x][z])
          norm[1] += norms[x][z][k][1] / len(norms[x][z])
          norm[2] += norms[x][z][k][2] / len(norms[x][z])
        n[x][z] = norm
    for x in range(size):
      for z in range(size):
        glNormal(n[x][z][0], n[x][z][1], n[x][z][2])
        glVertex(x   - size // 2, self.y[x  ,z  ], z   - size // 2)
        glNormal(n[x+1][z+1][0], n[x+1][z+1][1], n[x+1][z+1][2])
        glVertex(x+1 - size // 2, self.y[x+1,z+1], z+1 - size // 2)
        glNormal(n[x+1][z][0], n[x+1][z][1], n[x+1][z][2])
        glVertex(x+1 - size // 2, self.y[x+1,z  ], z   - size // 2)
        glNormal(n[x][z][0], n[x][z][1], n[x][z][2])
        glVertex(x   - size // 2, self.y[x  ,z  ], z   - size // 2)
        glNormal(n[x][z+1][0], n[x][z+1][1], n[x][z+1][2])
        glVertex(x   - size // 2, self.y[x  ,z+1], z+1 - size // 2)
        glNormal(n[x+1][z+1][0], n[x+1][z+1][1], n[x+1][z+1][2])
        glVertex(x+1 - size // 2, self.y[x+1,z+1], z+1 - size // 2)
    glEnd()
    glEndList()

class SecondPlane(object):
  def __init__(self, width, height, scale):
    self.width = width
    self.height = height
    self.scale = scale
    self.generate_plane(10, width, 0, 10)
    self.model_plane(width, height)
    
  def display(self):
    glCallList(self.listID)
  
  def generate_plane(self, velocity, size, avg_height, height_variation):
    if not powerOf2(size) or size == 1:
      print "Size must be a power of two"
      raise Exception
    
    ratio = math.log(size, 2) - 2
    y = numpy.zeros((4,4))
    currentSize = 4
    for x in range(currentSize):
      for z in range(currentSize):
        y[x,z] = random.uniform(avg_height - height_variation,avg_height + height_variation)
    y2 = copy.copy(y)
    while currentSize < size:
      currentSize *= 2
      y = numpy.zeros((currentSize, currentSize))
      for x in range(currentSize):
        for z in range(currentSize):
          y[x,z] = y2[x//2,z//2] + random.uniform(-velocity,velocity)
      y2 = copy.copy(y)
      velocity /= ratio
      ratio /= 2
    self.y = y
    
  def model_plane(self, width, height):
    self.listID = glGenLists(1)
    glNewList(self.listID, GL_COMPILE_AND_EXECUTE)
    glBegin(GL_TRIANGLES)
    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.6,0.3,0))
    n = [[[] for x in range(height+1)] for z in range(width+1)]
    norms = [[[] for x in range(height+1)] for z in range(width+1)]
    for x in range(width - 1):
      for z in range(height - 1):
        norm = normal(
          (x   - width // 2, self.y[x  ,z  ], z   - height // 2),
          (x+1 - width // 2, self.y[x+1,z  ], z   - height // 2),
          (x+1 - width // 2, self.y[x+1,z+1], z+1 - height // 2))
        norms[x][z].append(norm)
        norms[x+1][z].append(norm)
        norms[x+1][z+1].append(norm)
        norm = normal(
          (x   - width // 2, self.y[x  ,z  ], z   - height // 2),
          (x+1 - width // 2, self.y[x+1,z+1], z+1 - height // 2),
          (x   - width // 2, self.y[x  ,z+1], z+1 - height // 2))
        norms[x][z].append(norm)
        norms[x+1][z+1].append(norm)
        norms[x][z+1].append(norm)
    
    for x in range(width - 1):
      for z in range(height - 1):
        norm = [0,0,0]
        for k in range(len(norms[x][z])):
          norm[0] += norms[x][z][k][0] / len(norms[x][z])
          norm[1] += norms[x][z][k][1] / len(norms[x][z])
          norm[2] += norms[x][z][k][2] / len(norms[x][z])
        n[x][z] = norm
    for x in range(width - 2):
      for z in range(height - 2):
        glNormal(n[x][z][0], n[x][z][1], n[x][z][2])
        glVertex(x   - width // 2, self.y[x  ,z  ], z   - height // 2)
        glNormal(n[x+1][z][0], n[x+1][z][1], n[x+1][z][2])
        glVertex(x+1 - width // 2, self.y[x+1,z  ], z   - height // 2)
        glNormal(n[x+1][z+1][0], n[x+1][z+1][1], n[x+1][z+1][2])
        glVertex(x+1 - width // 2, self.y[x+1,z+1], z+1 - height // 2)
        glNormal(n[x][z][0], n[x][z][1], n[x][z][2])
        glVertex(x   - width // 2, self.y[x  ,z  ], z   - height // 2)
        glNormal(n[x+1][z+1][0], n[x+1][z+1][1], n[x+1][z+1][2])
        glVertex(x+1 - width // 2, self.y[x+1,z+1], z+1 - height // 2)
        glNormal(n[x][z+1][0], n[x][z+1][1], n[x][z+1][2])
        glVertex(x   - width // 2, self.y[x  ,z+1], z+1 - height // 2)
    glEnd()
    glEndList()