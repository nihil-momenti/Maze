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
    self.right_arm_angle = 20
    self.right_forearm_angle = 80
  
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
  
  def adjust(self, movement):
    if   movement == 'RAISE_RIGHT':
      self.right_arm_angle += 5
    elif movement == 'LOWER_RIGHT':
      self.right_arm_angle -= 5
  
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
    glLight(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.0005)
    glLight(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.0001)
  
  def head(self):
    glPushMatrix()
    glTranslate(0,11.5,0)
    glScale(8,8,8)
    glutSolidCube(1)
    glScale(1/8,1/8,1/8)
    self.eyes()
    glMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (0.96,0.76,0.76,1))
    glPopMatrix()
  
  def eyes(self):
    glPushMatrix()
    glTranslate(4, 2, 2)
    glMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (0,0,0,1))
    glutSolidSphere(1,10,10)
    glTranslate(0, 0,-4)
    glutSolidSphere(1,10,10)
    glPopMatrix()

  def arms(self):
    glPushMatrix()
    glTranslate(0,2.5,0)
    self.left_arm()
    self.right_arm()
    glPopMatrix()
  
  def left_arm(self):
    glPushMatrix()
    glTranslate(0,0,6.5)
    glScale(3, 10, 3)
    glutSolidCube(1)
    glScale(1/3, 1/10, 1/3)
    self.left_forearm()
    glPopMatrix()
  
  def left_forearm(self):
    glPushMatrix()
    glTranslate(0,-10,0)
    glScale(3, 10, 3)
    glutSolidCube(1)
    glScale(1/3, 1/10, 1/3)
    glPopMatrix()
  
  def right_arm(self):
    glPushMatrix()
    glTranslate(0,0,-6.5)
    glTranslate(0,5,0)
    glRotate(self.right_arm_angle, 0, 0, 1)
    glTranslate(0,-5,0)
    glScale(3, 10, 3)
    glutSolidCube(1)
    glScale(1/3, 1/10, 1/3)
    self.right_forearm()
    glPopMatrix()
  
  def right_forearm(self):
    glPushMatrix()
    glTranslate(0,-10,0)
    glTranslate(0,5,0)
    glRotate(self.right_forearm_angle, 0, 0, 1)
    glTranslate(0,-5,0)
    glScale(3, 10, 3)
    glutSolidCube(1)
    glScale(1/3, 1/10, 1/3)
    self.glow_ball()
    glPopMatrix()
  
  def glow_ball(self):
    glPushMatrix()
    glTranslate(2.5, -4, 0)
    glMaterial(GL_FRONT, GL_EMISSION, (1, 0.89, 0.71, 1))
    glutSolidSphere(1, 10, 10)
    glMaterial(GL_FRONT, GL_EMISSION, (0, 0, 0, 1))
    glPopMatrix()
  
  def legs(self):
    glPushMatrix()
    glTranslate(0,-11.5,0)
    self.left_leg()
    self.right_leg()
    glPopMatrix()
  
  def left_leg(self):
    glPushMatrix()
    glTranslate(0,0,3)
    glScale(3, 8, 3)
    glutSolidCube(1)
    glScale(1/3, 1/8, 1/3)
    self.left_shin()
    glPopMatrix()
  
  def left_shin(self):
    glPushMatrix()
    glTranslate(0,-8,0)
    glScale(3, 8, 3)
    glutSolidCube(1)
    glScale(1/3, 1/8, 1/3)
    glPopMatrix()
  
  def right_leg(self):
    glPushMatrix()
    glTranslate(0,0,-3)
    glScale(3, 8, 3)
    glutSolidCube(1)
    glScale(1/3, 1/8, 1/3)
    self.right_shin()
    glPopMatrix()
  
  def right_shin(self):
    glPushMatrix()
    glTranslate(0,-8,0)
    glScale(3, 8, 3)
    glutSolidCube(1)
    glScale(1/3, 1/8, 1/3)
    glPopMatrix()
  
  def base(self):
    glPushMatrix()
    glTranslatef(0, -11.5, 0)
    glScale(1, 3, 2)
    glutSolidCube(5)
    glScale(1/1, 1/3, 1/2)
    self.head()
    self.arms()
    self.legs()
    glPopMatrix()
    
  
  def display(self, show):
    glLight(GL_LIGHT0, GL_POSITION, list(self.position) + [1])
    if show:
      glPushMatrix()
      glTranslate(*self.position)
      facing = self.lookat - self.position
      angle = -atan2(facing.dz, facing.dx)
      glRotate(degrees(angle), 0, 1, 0)
      glMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (0.96,0.76,0.76,1))
      self.base()
      glPopMatrix()
