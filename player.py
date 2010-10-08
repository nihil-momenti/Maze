from __future__ import division

import time
from math import atan2, sqrt, cos, sin, acos, pi
from geom3 import Point3, Vector3, unit

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Player(object):
  def __init__(self, config):
    self.position = Point3(100, 100, 0)
    self.lookat = Point3(101, 100, 0)
    self.viewup = Point3(0, 1, 0)
    self.rotation = (0, 0)
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
        if direction == 'FORWARD':
          self.forward(self.speed * (time.time() - self.update_time))
        elif direction == 'LEFT':
          self.sideways(-self.speed * (time.time() - self.update_time))
        elif direction == 'RIGHT':
          self.sideways(self.speed * (time.time() - self.update_time))
        elif direction == 'BACK':
          self.forward(-self.speed * (time.time() - self.update_time))
      self.update_time = time.time()
      glutTimerFunc(10, self.update, 0)
    else:
      self.in_motion = False
  
  def forward(self, amount):
    """Move the position forward by the given amount

    The lookat point is moved by the same amount to prevent silly
    effects like the position passing the lookat point
    """

    movement = amount * (self.lookat - self.position)
    self.position += movement
    self.lookat += movement
    glutPostRedisplay()
  
  def sideways(self, amount):
    movement = amount * unit((self.lookat - self.position).cross(Vector3(self.viewup)))
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
    theta = max(0.01, min(pi - 0.01, acos(y / r) + self.sensitivity * rotation[1]))
    phi = atan2(z, x) + self.sensitivity * rotation[0]
    (x, y, z) = (r * sin(theta) * cos(phi), r * cos(theta), r * sin(theta) * sin(phi))
    self.lookat = self.position + Vector3(x, y, z)
    glutPostRedisplay()
  
  def attack():
    return null