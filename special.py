# -*- coding: utf-8 -*-
from __future__ import division

import random, math

from model import Model

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from fractal_map import FractalMap

class Ball:
  def __init__(self, x, z):
    self.x = x
    self.y = 0
    self.z = z
    self.bounce(1)
  
  def bounce(self, value):
    self.y += value
    if self.y not in range(-34, 35):
      value = -value
    glutTimerFunc(10, self.bounce, value)
  
  def display(self):
    glPushMatrix()
    glTranslate(self.x, self.y, self.z)
    glutSolidSphere
    glPopMatrix()


def lamp_pre(num):
  def func():
    glLight(GL_LIGHT1 + num, GL_POSITION, [0, 20, 0, 1])
  return func
def torch_pre(num):
  def func():
    glLight(GL_LIGHT1 + num, GL_POSITION, [0, 22, -22, 1])
  return func
  

class Special(object):
  num = 0
  
  @classmethod
  def init(cls):
    cls.num = min(cls.num, 7)
    cls.models = []
    
    cls.map = [FractalMap(8, 0.95) for i in range(Special.num)]
    cls.fire_index = [0 for i in range(Special.num)]
    
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
    cls.flicker(0)
  
  @classmethod
  def flicker(cls, i):
    glLight(GL_LIGHT1 + i, GL_QUADRATIC_ATTENUATION, max(0, 0.00005 * cls.map[i][cls.fire_index[i],] + 0.0001))
    cls.fire_index[i] += 1#; print cls.fire_index[i]
    glutTimerFunc(10, cls.flicker, (i + 1) % cls.num)
    glutPostRedisplay()
    
    
  def __init__(self, location, wall):
    Special.num += 1
    self.x = location[0]
    self.z = location[1]
    self.wall_x = wall[0]
    self.wall_z = wall[1]
    self.balls = set([])

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
      self.balls.add(Ball(self.x, self.z))
    glPopMatrix()
    glEndList()

  def display(self):
    glCallList(self.listID)
    for ball in self.balls:
      ball.display()