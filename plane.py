# -*- coding: utf-8 -*-
from __future__ import division

import random, math, numpy
from heightmap import generate_heightmap
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *



def normal(center_point, clockwise, widdershins):
  n = [clockwise[z] - center_point[z] for z in range(3)]
  p = [widdershins[z] - center_point[z] for z in range(3)]
  cross = [p[1] * n[2] - p[2] * n[1], p[2] * n[0] - p[0] * n[2], p[0] * n[1] - p[1] * n[0]]
  length = math.sqrt(cross[0] ** 2 + cross[1] ** 2 + cross[2] ** 2)
  n = [cross[z] / length for z in range(3)]
  return n
  


class Plane(object):
  def __init__(self, config, heightmap):
    self.size = config['size']
    self.scale = config['scale']
    self.height = config['height']
    self.octaves = config['octaves']
    
    self.y = numpy.zeros((self.size, self.size))
    for x in range(self.size):
      for z in range(self.size):
        # self.y[x, z] = self.height * heightmap.value(self.octaves, (x - self.size // 2) * self.scale, (z - self.size // 2) * self.scale)
        self.y[x, z] = self.height * math.cos(math.pi * math.sqrt(x ** 2 + z ** 2) / self.size) * heightmap.value((x - self.size // 2) * self.scale, (z - self.size // 2) * self.scale, octaves=self.octaves)
    
  def display(self):
    glCallList(self.listID)
    
  def gl_init(self):
    print "  Generating models..."
    self.listID = glGenLists(1)
    glNewList(self.listID, GL_COMPILE_AND_EXECUTE)
    glBegin(GL_TRIANGLES)
    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.6,0.3,0))
    n = [[[] for x in range(self.size+1)] for z in range(self.size+1)]
    norms = [[[] for x in range(self.size+1)] for z in range(self.size+1)]
    for x in range(self.size-1):
      for z in range(self.size-1):
        norm = normal(
          ((x   - self.size // 2) * self.scale, self.y[x  ,z  ], (z   - self.size // 2) * self.scale),
          ((x+1 - self.size // 2) * self.scale, self.y[x+1,z  ], (z   - self.size // 2) * self.scale),
          ((x+1 - self.size // 2) * self.scale, self.y[x+1,z+1], (z+1 - self.size // 2) * self.scale))
        norms[x][z].append(norm)
        norms[x+1][z].append(norm)
        norms[x+1][z+1].append(norm)
        norm = normal(
          ((x   - self.size // 2) * self.scale, self.y[x  ,z  ], (z   - self.size // 2) * self.scale),
          ((x+1 - self.size // 2) * self.scale, self.y[x+1,z+1], (z+1 - self.size // 2) * self.scale),
          ((x   - self.size // 2) * self.scale, self.y[x  ,z+1], (z+1 - self.size // 2) * self.scale))
        norms[x][z].append(norm)
        norms[x+1][z+1].append(norm)
        norms[x][z+1].append(norm)
    
    for x in range(self.size):
      for z in range(self.size):
        norm = [0,0,0]
        for k in range(len(norms[x][z])):
          norm[0] += norms[x][z][k][0] / len(norms[x][z])
          norm[1] += norms[x][z][k][1] / len(norms[x][z])
          norm[2] += norms[x][z][k][2] / len(norms[x][z])
        n[x][z] = norm
    for x in range(self.size-1):
      for z in range(self.size-1):
        glNormal(n[x][z][0], n[x][z][1], n[x][z][2])
        glVertex((x   - self.size // 2) * self.scale, self.y[x  ,z  ], (z   - self.size // 2) * self.scale)
        glNormal(n[x+1][z+1][0], n[x+1][z+1][1], n[x+1][z+1][2])
        glVertex((x+1 - self.size // 2) * self.scale, self.y[x+1,z+1], (z+1 - self.size // 2) * self.scale)
        glNormal(n[x+1][z][0], n[x+1][z][1], n[x+1][z][2])
        glVertex((x+1 - self.size // 2) * self.scale, self.y[x+1,z  ], (z   - self.size // 2) * self.scale)
        glNormal(n[x][z][0], n[x][z][1], n[x][z][2])
        glVertex((x   - self.size // 2) * self.scale, self.y[x  ,z  ], (z   - self.size // 2) * self.scale)
        glNormal(n[x][z+1][0], n[x][z+1][1], n[x][z+1][2])
        glVertex((x   - self.size // 2) * self.scale, self.y[x  ,z+1], (z+1 - self.size // 2) * self.scale)
        glNormal(n[x+1][z+1][0], n[x+1][z+1][1], n[x+1][z+1][2])
        glVertex((x+1 - self.size // 2) * self.scale, self.y[x+1,z+1], (z+1 - self.size // 2) * self.scale)
    glEnd()
    glEndList()
    print "  ...Done"

