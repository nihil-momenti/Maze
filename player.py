# -*- coding: utf-8 -*-
from __future__ import division

import time
from math import atan2, sqrt, cos, sin, acos, asin, pi, degrees
from geom3 import Point3, Vector3, unit, dot

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Player(object):
  def __init__(self, config, start_point):
    self.position = start_point
    self.lookat = start_point + Vector3(1, 0, 0)
    self.viewup = Point3(0, 1, 0)
    self.rotation = (0, 0)
    self.sensitivity = config['sensitivity']
    self.speed = config['speed']
    self.moving = set()
    self.in_motion = False
    self.third_person = False
  
  def move(self, direction):
    if direction in self.moving:
      return
    
    self.moving.add(direction)
    if not self.in_motion:
      self.in_motion = True
      self.update_time = time.time()
      self.update()
    
  
  def stop(self, direction):
    self.moving.remove(direction)
  
  def update(self, value=0):
    if len(self.moving) > 0:
      for direction in self.moving:
        if direction == 'FORWARD':
          self.forward(self.speed * (time.time() - self.update_time))
        elif direction == 'LEFT':
          self.right(-self.speed * (time.time() - self.update_time))
        elif direction == 'RIGHT':
          self.right(self.speed * (time.time() - self.update_time))
        elif direction == 'BACK':
          self.forward(-self.speed * (time.time() - self.update_time))
      self.update_time = time.time()
      glutTimerFunc(10, self.update, 0)
    else:
      self.in_motion = False
  
  def twoD_facing(self):
    direction = self.lookat - self.position
    direction.dy = 0
    return unit(direction)
  
  def offset(self):
    if self.third_person:
      return Vector3(-100 * (self.lookat - self.position))
    else:
      return Vector3(0,0,0)
  
  def forward(self, amount):
    movement = amount * unit(self.twoD_facing())
    self.position += movement
    self.lookat += movement
    glutPostRedisplay()
  
  def right(self, amount):
    movement = amount * unit(self.twoD_facing().cross(Vector3(self.viewup)))
    self.position += movement
    self.lookat += movement
    glutPostRedisplay()
  
  def up (self, amount):
    movement = amount * Vector3(0, 1, 0)
    self.position += movement
    self.lookat += movement
    glutPostRedisplay()

  def turn(self, rotation):
    (x, y, z) = self.lookat - self.position
    r = sqrt(x*x + y*y + z*z)
    theta = max(0.01, min(pi - 0.01, acos(y / r) + self.sensitivity * rotation[1]))
    phi = atan2(z, x) + self.sensitivity * rotation[0]
    (x, y, z) = (r * sin(theta) * cos(phi), r * cos(theta), r * sin(theta) * sin(phi))
    self.lookat = self.position + Vector3(x, y, z)
    glutPostRedisplay()
  
  def attack():
    return null
    
  def gl_init(self):
    None


  def base(self):
    glPushMatrix()
    glColor3f(1,1,0)
    glTranslatef(0, 0, 0)
    glScale(20, 28, 20)
    glutSolidCube(1)
    glPopMatrix()
    
  
  def display(self):
    glLight(GL_LIGHT0, GL_POSITION, list(self.position) + [1])
    glPushMatrix()
    glTranslate(*self.position)
    glTranslate(0, -1, 0)
    facing = self.twoD_facing()
    angle = -atan2(facing.dz, facing.dx)
    glRotate(degrees(angle), 0, 1, 0)
    self.base()
    glPopMatrix()
  
  def switch_view(self):
    if self.third_person:
      self.third_person = False
    else:
      self.third_person = True
    glutPostRedisplay()