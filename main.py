from __future__ import division
from maze import Maze
from plane import *
from threading import Thread
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys
try:
  import psyco
  psyco.full()
  print "Psyco Running"
except ImportError:
  print "Psyco not available"

def reshape(width, height):
    glMatrixMode ( GL_PROJECTION )
    glLoadIdentity()
    gluPerspective(50, width/height, 1, 2000)
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()
    glViewport(0, 0, width, height)

    
def special(key, x, y):
  if key == GLUT_KEY_F10:
    exit()

def display():
  glLoadIdentity()
  gluLookAt(0,100,200, 0,0,0, 0,1,0)
  glRotate(time.time()%360*20,0,1,0)
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  [thing.display() for thing in contents]
  glutSwapBuffers()

# Initialise GLUT and create a window

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_MULTISAMPLE)
# glutEnterGameMode()
glutInitWindowSize(900, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow("OpenGL Experiments")
glutIgnoreKeyRepeat(1)

# Set up the OpenGL engine into a simple basic state

glClearColor( 1.0, 1.0, 1.0, 1.0 ) # Background colour			       
glMatrixMode ( GL_PROJECTION )     # Set the projection ...
glLoadIdentity()	               # ... to be ...
gluPerspective(50, 1, 1, 2000)       # ... orthographic.
glMatrixMode( GL_MODELVIEW )       # Set the view matrix ...
glLoadIdentity()	               # ... to identity.

# Enter the main event loop

glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_CULL_FACE)

contents = [FirstPlane(128,10)]#, FlatPlane(128, -20, 10)]
# Maze(32,32,10,6,0.01), 
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutIdleFunc(display)
glutSpecialFunc(special)

glutMainLoop()
