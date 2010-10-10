# -*- coding: utf-8 -*-
from __future__ import division

import time
from math import atan2, sqrt, cos, sin, acos, asin, pi, degrees
from geom3 import Point3, Vector3, unit, dot
from robot import Robot

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Player(object):
  def __init__(self, config, start_point):
    self.position = start_point
    self.lookat = start_point + Vector3(1, 0, 0)
    self.viewup = Vector3(0, 1, 0)
    self.sensitivity = config['sensitivity']
    self.speed = config['speed']
    self.moving = set()
    self.in_motion = False
    self.third_person = False
    self.disconnected = False
    self.robot = Robot(config['robot'], start_point)
  
  def move(self, direction):
    if direction in self.moving:
      return
    
    if direction in ['LEFT', 'RIGHT', 'FORWARD', 'BACK'] or self.disconnected and direction in ['UP', 'DOWN']:
      self.moving.add(direction)
      if not self.in_motion:
        self.in_motion = True
        self.update_time = time.time()
        self.update()
    elif self.disconnected:
      self.robot.move(direction)
    
  def stop(self, direction):
    if direction in ['LEFT', 'RIGHT', 'FORWARD', 'BACK'] or self.disconnected and direction in ['UP', 'DOWN']:
      self.moving.remove(direction)
    elif self.disconnected:
      self.robot.stop(direction)
  
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
        elif direction == 'UP':
          self.up(self.speed * (time.time() - self.update_time))
        elif direction == 'DOWN':
          self.up(-self.speed * (time.time() - self.update_time))
      self.update_time = time.time()
      glutTimerFunc(10, self.update, 0)
    else:
      self.in_motion = False
  
  def facing(self):
    direction = self.lookat - self.position
    if not self.disconnected:
      direction.dy = 0
    return unit(direction)
  
  def forward(self, amount):
    movement = amount * unit(self.facing())
    self.position += movement
    self.lookat += movement
    if not self.disconnected:
      self.robot.forward(amount)
    glutPostRedisplay()
  
  def right(self, amount):
    movement = amount * unit(self.facing().cross(self.viewup))
    self.position += movement
    self.lookat += movement
    if not self.disconnected:
      self.robot.right(amount)
    glutPostRedisplay()
  
  def up (self, amount):
    movement = amount * self.viewup
    self.position += movement
    self.lookat += movement
    if not self.disconnected:
      self.robot.up(amount)
    glutPostRedisplay()
      
  def offset(self):
    if self.third_person and not self.disconnected:
      return Vector3(-100 * (self.lookat - self.position))
    else:
      return Vector3(0,0,0)

  def turn(self, rotation):
    (x, y, z) = self.lookat - self.position
    r = sqrt(x*x + y*y + z*z)
    theta = max(0.01, min(pi - 0.01, acos(y / r) + self.sensitivity * rotation[1]))
    phi = atan2(z, x) + self.sensitivity * rotation[0]
    (x, y, z) = (r * sin(theta) * cos(phi), r * cos(theta), r * sin(theta) * sin(phi))
    self.lookat = self.position + Vector3(x, y, z)
    if not self.disconnected:
      self.robot.turn(self.sensitivity * rotation[0])
    glutPostRedisplay()
  
  def attack(self):
    return None
  
  def switch_third_person(self):
    if self.third_person:
      self.third_person = False
    else:
      self.third_person = True
    glutPostRedisplay()
  
  def switch_viewpoint(self):
    if self.disconnected:
      self.disconnected = False
      self.position = self.robot.position
      self.lookat = self.robot.lookat
    else:
      self.disconnected = True
    glutPostRedisplay()
  
  def gl_init(self):
    self.robot.gl_init()
  
  def display(self):
    self.robot.display()