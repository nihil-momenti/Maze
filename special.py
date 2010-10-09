# -*- coding: utf-8 -*-
from __future__ import division

#from Model import model

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Special(object):
  @classmethod
  def init(cls, config):
    cls.models = []
    for model in config['models']:
      cls.models.append(Model(model))
    
  def __init__(self, location, config):
    self.x = location[0]
    self.z = location[1]

  def gl_init(self):
    self.listID = glGenLists(1); glNewList(self.listID, GL_COMPILE_AND_EXECUTE)
    glPushMatrix()
    glTranslate(self.x, 0, self.z)
    #random.choice(Special.models).display()
    glutSolidCube(10)
    glPopMatrix()
    glEndList()

  def display(self):
    glCallList(self.listID)