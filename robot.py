from __future__ import division

import time
from math import atan2, sqrt, cos, sin, acos, asin, pi, degrees
from geom3 import Point3, Vector3, unit, dot

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Robot(object):
  def __init__(self, config, start_point):
    self.position = start_point
    self.lookat = start_point + Vector3(1, 0, 0)
    self.viewup = Point3(0, 1, 0)
    self.sensitivity = config['sensitivity']
    self.speed = config['speed']
    self.moving = set()
    self.in_motion = False
  
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
        if direction == 'ROBOT_FORWARD':
          self.forward(self.speed * (time.time() - self.update_time))
        elif direction == 'ROBOT_LEFT':
          self.turn(-self.sensitivity * (time.time() - self.update_time))
        elif direction == 'ROBOT_RIGHT':
          self.turn(self.sensitivity * (time.time() - self.update_time))
        elif direction == 'ROBOT_BACK':
          self.forward(-self.speed * (time.time() - self.update_time))
      self.update_time = time.time()
      glutTimerFunc(10, self.update, 0)
    else:
      self.in_motion = False
  
  def forward(self, amount):
    movement = amount * unit(self.lookat - self.position)
    self.position += movement
    self.lookat += movement
    glutPostRedisplay()
  
  def right(self, amount):
    movement = amount * unit((self.lookat - self.position).cross(Vector3(self.viewup)))
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
    r = sqrt(x*x + z*z)
    phi = atan2(z, x) + rotation
    (x, z) = (r * cos(phi), r * sin(phi))
    self.lookat = self.position + Vector3(x, y, z)
    glutPostRedisplay()
    
  def gl_init(self):
    glEnable(GL_LIGHT0)
    glLight(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1))
    glLight(GL_LIGHT0, GL_DIFFUSE, (1, 0.89, 0.71, 1))
    glLight(GL_LIGHT0, GL_SPECULAR, (1, 0.89, 0.71, 1))
    glLight(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1)
    #glLight(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.0005)
    #glLight(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.0001)


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
    facing = self.lookat - self.position
    angle = -atan2(facing.dz, facing.dx)
    glRotate(degrees(angle), 0, 1, 0)
    self.base()
    glPopMatrix()