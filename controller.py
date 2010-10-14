# -*- coding: utf-8 -*-
from __future__ import division

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Controller(object):
  """The Controller class for the OpenGL application."""

  MAX_DRAG_ROTATION = 50   # degrees for a full-width drag
      
  def __init__(self, player, scene, view, config):
    self.scene = scene
    self.view = view
    self.player = player
    self.mousePos = (0, 0)
    self.leftButtonState = GLUT_UP
    
    # Set callback functions
    glutDisplayFunc(self.view.display)
    glutReshapeFunc(self.view.reshape)
    glutMouseFunc(self.mouseButtonFunc)
    glutMotionFunc(self.mouseMotionFunc)
    glutKeyboardFunc(self.keyboardFunc)
    glutKeyboardUpFunc(self.keyboardUpFunc)


  def mouseButtonFunc(self, button, state, x, y):
    """The GLUT mouseFunc handler"""
    if button == GLUT_LEFT_BUTTON:
      self.mousePos = (x, y)
      self.leftButtonState = state
      if state == GLUT_DOWN:
        self.mouseInitialPos = (x, y)
        glutSetCursor(GLUT_CURSOR_NONE)
      else:
        glutWarpPointer(*self.mouseInitialPos)
        glutSetCursor(GLUT_CURSOR_INHERIT)
    elif button == GLUT_RIGHT_BUTTON:
      self.player.action(15)


  def mouseMotionFunc(self, x, y):
    if self.leftButtonState == GLUT_DOWN:
      rotation = [(x - self.mousePos[0]) / self.view.width,
                  (y - self.mousePos[1]) / self.view.height]
      self.player.turn(rotation)
      if x < 0:
        x = self.view.width
        glutWarpPointer(x, y)
      elif x > self.view.width:
        x = 0
        glutWarpPointer(x, y)
      if y < 0:
        y = self.view.height
        glutWarpPointer(x, y)
      elif y > self.view.height:
        y = 0
        glutWarpPointer(x, y)
      self.mousePos = (x, y)
      glutPostRedisplay()
   
  def keyboardFunc(self, key, x, y):
    if key in ['a', 'A']:
      self.player.move('LEFT')
    elif key in ['w', 'W']:
      self.player.move('FORWARD')
    elif key in ['s', 'S']:
      self.player.move('BACK')
    elif key in ['d', 'D']:
      self.player.move('RIGHT')
    elif key == ' ':
      self.player.move('UP')
    elif key in ['z', 'Z']:
      self.player.move('DOWN')
    elif key in ['e', 'E']:
      self.player.switch_third_person()
    elif key in ['q', 'Q']:
      self.player.switch_viewpoint()
    elif key in ['j', 'J']:
      self.player.move('ROBOT_LEFT')
    elif key in ['i', 'I']:
      self.player.move('ROBOT_FORWARD')
    elif key in ['k', 'K']:
      self.player.move('ROBOT_BACK')
    elif key in ['l', 'L']:
      self.player.move('ROBOT_RIGHT')
    elif key in ['t', 'T']:
      self.player.adjust('RAISE_RIGHT')
    elif key in ['g', 'G']:
      self.player.adjust('LOWER_RIGHT')
   
  def keyboardUpFunc(self, key, x, y):
    if key == 'a':
      self.player.stop('LEFT')
    elif key == 'w':
      self.player.stop('FORWARD')
    elif key == 's':
      self.player.stop('BACK')
    elif key == 'd':
      self.player.stop('RIGHT')
    elif key == ' ':
      self.player.stop('UP')
    elif key in ['z', 'Z']:
      self.player.stop('DOWN')
    elif key in ['j', 'J']:
      self.player.stop('ROBOT_LEFT')
    elif key in ['i', 'I']:
      self.player.stop('ROBOT_FORWARD')
    elif key in ['k', 'K']:
      self.player.stop('ROBOT_BACK')
    elif key in ['l', 'L']:
      self.player.stop('ROBOT_RIGHT')

          
  def run(self):
    """Start the app (just runs the GLUT main loop)"""
    glutMainLoop()
