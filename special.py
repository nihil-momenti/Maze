# -*- coding: utf-8 -*-
from __future__ import division

import random, math

from model import Model

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def lamp_pre(num):
  return (lambda: glLight(GL_LIGHT1 + num, GL_POSITION, [0, 20, 0, 1]))
def torch_pre(num):
  return (lambda: glLight(GL_LIGHT1 + num, GL_POSITION, [0, 22, -22, 1]))

class Special(object):
  num = 0
  
  @classmethod
  def init(cls):
    cls.models = []
    
    models = [
      (Model('models/lamp.obj'), lamp_pre),
      (Model('models/torch.obj'), torch_pre)]
    for i in range(Special.num):
      glEnable(GL_LIGHT1 + i)
      glLight(GL_LIGHT1 + i, GL_DIFFUSE, (1, 0.98, 0.8, 1))
      glLight(GL_LIGHT1 + i, GL_SPECULAR, (1, 0.98, 0.8, 1))
      glLight(GL_LIGHT1 + i, GL_CONSTANT_ATTENUATION, 1)
      glLight(GL_LIGHT1 + i, GL_LINEAR_ATTENUATION, 0.001)
      glLight(GL_LIGHT1 + i, GL_QUADRATIC_ATTENUATION, 0.0001)
      model = random.choice(models)
      cls.models.append((model[0], model[1](i)))
    
  def __init__(self, location, wall):
    Special.num += 1
    self.x = location[0]
    self.z = location[1]
    self.wall_x = wall[0]
    self.wall_z = wall[1]

  def gl_init(self):
    self.listID = glGenLists(1); glNewList(self.listID, GL_COMPILE_AND_EXECUTE)
    glPushMatrix()
    glTranslate(self.x, 0, self.z)
    angle = math.atan2(self.wall_z - self.z, self.wall_x - self.x)
    glRotate(math.degrees(angle), 0, -1, 0)
    if len(Special.models) > 0:
      model = random.choice(Special.models); Special.models.remove(model)
      model[1](); model[0].display()
      
    else:
      glutSolidCube(10)
    glPopMatrix()
    glEndList()

  def display(self):
    glCallList(self.listID)