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
    return direction
  
  def offset(self):
    if self.third_person:
      return Vector3(-20 * self.twoD_facing() + Vector3(0, 20, 0))
    else:
      return Vector3(0,0,0)
  
  def forward(self, amount):
    """Move the position forward by the given amount

    The lookat point is moved by the same amount to prevent silly
    effects like the position passing the lookat point
    """

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
    """Rotate the current view by the given angle around the y-axis.

    This is done by rotating the lookat point around the eye point by
    the given angle.
    """

    (x, y, z) = self.lookat - self.position
    r = sqrt(x*x + y*y + z*z)
    if self.third_person:
      theta = max(0.01, min(pi - 0.01, acos(y / r) - self.sensitivity * rotation[1]))
      phi = atan2(z, x) - self.sensitivity * rotation[0]
    else:
      theta = max(0.01, min(pi - 0.01, acos(y / r) + self.sensitivity * rotation[1]))
      phi = atan2(z, x) + self.sensitivity * rotation[0]
    (x, y, z) = (r * sin(theta) * cos(phi), r * cos(theta), r * sin(theta) * sin(phi))
    self.lookat = self.position + Vector3(x, y, z)
    glutPostRedisplay()
  
  def attack():
    return null
    
  def gl_init(self):
    None
  
  def innerArm(self):
    """Draws the inner arm in its resting position, vertical with
    centre of base at origin"""
    glColor3f(1, 0, 0)
    glPushMatrix()
    glTranslatef(0, 1, 0)
    glScalef(0.2, 2, 0.2)
    glutSolidCube(1)
    glPopMatrix()


  def outerArm(self):
    """Draws the outer arm in its resting position, vertical with
    centre of base at origin"""
    glColor3f(0, 1, 0)
    glPushMatrix()
    glTranslatef(0, 0.75, 0)
    glScalef(0.1, 1.5, 0.1)
    glutSolidCube(1)
    glPopMatrix()


  def base(self):
    """Draws the base in its rest position, sitting on the ground plane"""
    glPushMatrix()
    glColor3f(1,1,0)
    glTranslatef(0, 0.5, 0)
    glutSolidCube(1)
    glPopMatrix()
    
  
  def display(self):
    glPushMatrix()
    glTranslate(*self.position)
    glTranslate(0, -20, 0)
    angle = asin(dot(self.twoD_facing(), Vector3(1, 0, 0)))
    glRotate(degrees(angle), 0, 1, 0)
    self.base()
    glTranslate(0, 1, 0)
    self.innerArm()
    glTranslate(0, 2, 0)
    self.outerArm()
    glPopMatrix()
  
  def switch_view(self):
    if self.third_person:
      self.third_person = False
      # self.forward(20)
      # self.up(-20)
    else:
      self.third_person = True
      # self.forward(-20)
      # self.up(20)