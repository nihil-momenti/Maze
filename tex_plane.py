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
    self.t = numpy.zeros((self.size, self.size), numpy.dtype('3u1'))
    for x in range(self.size):
      for z in range(self.size):
        value = (math.cos(math.pi * math.sqrt((x - self.size // 2) ** 2 + (z - self.size // 2) ** 2) / self.size) + 0.1) * (heightmap.value((x - self.size // 2), (z - self.size // 2), octaves=self.octaves) + 1)
        self.y[x, z] = value * self.height
        if value > 0.5:
          self.t[z, x][1] = 0xFF
        else:
          self.t[z, x][2] = 0xFF
    
  def display(self):
    glCallList(self.listID)
    
  def gl_init(self):
    print "  Generating models..."
    self.textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, self.textureID)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.size, self.size, 0, GL_RGB, GL_UNSIGNED_BYTE, self.t)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glTexEnvi(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
    glEnable(GL_TEXTURE_2D)
    
    
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
    
    
    self.listID = glGenLists(1)
    glNewList(self.listID, GL_COMPILE_AND_EXECUTE)
    glBindTexture(GL_TEXTURE_2D, self.textureID)
    glBegin(GL_TRIANGLES)
    # glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.6,0.3,0))
    for x in range(self.size-1):
      for z in range(self.size-1):
        glNormal(n[x][z][0], n[x][z][1], n[x][z][2])
        glTexCoord2f(x / self.size, z / self.size)
        glVertex((x   - self.size // 2) * self.scale, self.y[x  ,z  ], (z   - self.size // 2) * self.scale)
        glNormal(n[x+1][z+1][0], n[x+1][z+1][1], n[x+1][z+1][2])
        glTexCoord2f((x + 1) / self.size, (z + 1) / self.size)
        glVertex((x+1 - self.size // 2) * self.scale, self.y[x+1,z+1], (z+1 - self.size // 2) * self.scale)
        glNormal(n[x+1][z][0], n[x+1][z][1], n[x+1][z][2])
        glTexCoord2f((x + 1) / self.size, z / self.size)
        glVertex((x+1 - self.size // 2) * self.scale, self.y[x+1,z  ], (z   - self.size // 2) * self.scale)
        glNormal(n[x][z][0], n[x][z][1], n[x][z][2])
        glTexCoord2f(x / self.size, z / self.size)
        glVertex((x   - self.size // 2) * self.scale, self.y[x  ,z  ], (z   - self.size // 2) * self.scale)
        glNormal(n[x][z+1][0], n[x][z+1][1], n[x][z+1][2])
        glTexCoord2f(x / self.size, (z + 1) / self.size)
        glVertex((x   - self.size // 2) * self.scale, self.y[x  ,z+1], (z+1 - self.size // 2) * self.scale)
        glNormal(n[x+1][z+1][0], n[x+1][z+1][1], n[x+1][z+1][2])
        glTexCoord2f((x + 1) / self.size, (z + 1) / self.size)
        glVertex((x+1 - self.size // 2) * self.scale, self.y[x+1,z+1], (z+1 - self.size // 2) * self.scale)
    glEnd()
    glEndList()
    print "  ...Done"

