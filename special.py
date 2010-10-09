# -*- coding: utf-8 -*-
from __future__ import division

import random

from model import Model

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def lamp_pre1():
  glLight(GL_LIGHT1, GL_POSITION, [0, 20, 0, 1])
def lamp_pre2():
  glLight(GL_LIGHT2, GL_POSITION, [0, 20, 0, 1])
def lamp_pre3():
  glLight(GL_LIGHT3, GL_POSITION, [0, 20, 0, 1])

class Special(object):
  @classmethod
  def init(cls):
    cls.models = []
    
    glEnable(GL_LIGHT1)
    glLight(GL_LIGHT1, GL_DIFFUSE, (1, 0.98, 0.8, 1))
    glLight(GL_LIGHT1, GL_SPECULAR, (1, 0.98, 0.8, 1))
    glLight(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 0.6)
    glLight(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.001)
    glLight(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.0001)
    glEnable(GL_LIGHT2)
    glLight(GL_LIGHT2, GL_DIFFUSE, (1, 0.98, 0.8, 1))
    glLight(GL_LIGHT2, GL_SPECULAR, (1, 0.98, 0.8, 1))
    glLight(GL_LIGHT2, GL_CONSTANT_ATTENUATION, 0.6)
    glLight(GL_LIGHT2, GL_LINEAR_ATTENUATION, 0.001)
    glLight(GL_LIGHT2, GL_QUADRATIC_ATTENUATION, 0.0001)
    glEnable(GL_LIGHT3)
    glLight(GL_LIGHT3, GL_DIFFUSE, (1, 0.98, 0.8, 1))
    glLight(GL_LIGHT3, GL_SPECULAR, (1, 0.98, 0.8, 1))
    glLight(GL_LIGHT3, GL_CONSTANT_ATTENUATION, 0.6)
    glLight(GL_LIGHT3, GL_LINEAR_ATTENUATION, 0.001)
    glLight(GL_LIGHT3, GL_QUADRATIC_ATTENUATION, 0.0001)
    lamp1 = Model('models/lamp.obj', lamp_pre1)
    lamp2 = Model('models/lamp.obj', lamp_pre2)
    lamp3 = Model('models/lamp.obj', lamp_pre3)
    cls.models.append(lamp1)
    cls.models.append(lamp1)
    cls.models.append(lamp2)
    cls.models.append(lamp3)
    
  def __init__(self, location):
    self.x = location[0]
    self.z = location[1]

  def gl_init(self):
    self.listID = glGenLists(1); glNewList(self.listID, GL_COMPILE_AND_EXECUTE)
    glPushMatrix()
    glTranslate(self.x, 0, self.z)
    if len(Special.models) > 0:
      model = random.choice(Special.models)
      Special.models.remove(model)
      model.display()
    else:
      glutSolidCube(10)
    glPopMatrix()
    glEndList()

  def display(self):
    glCallList(self.listID)