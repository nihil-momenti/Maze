from __future__ import division

from json import load
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from world import World

try:
  import psyco
  psyco.full()
  print "Psyco Running"
except ImportError:
  print "Psyco not available"

def unload():
  glutSetKeyRepeat(GLUT_KEY_REPEAT_DEFAULT)

def reshape(width, height):
    glMatrixMode ( GL_PROJECTION )
    glLoadIdentity()
    gluPerspective(50, width/height, 1, 2000)
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()
    glViewport(0, 0, width, height)



# Initialise GLUT and create a window

config = load(file('world.config'))

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_MULTISAMPLE)
if config['game_mode']:
  glutEnterGameMode()
  glViewport(0, 0, glutGameModeGet(GLUT_GAME_MODE_WIDTH), glutGameModeGet(GLUT_GAME_MODE_HEIGHT))
else:
  glutInitWindowSize(config['window_width'], config['window_height'])
  glutInitWindowPosition(0, 0)
  glutCreateWindow("Robot")
  glViewport(0, 0, config['window_width'], config['window_height'])
glutSetKeyRepeat(GLUT_KEY_REPEAT_OFF)
glutIgnoreKeyRepeat(1)

# Set up the OpenGL engine into a simple basic state

glClearColor( 1.0, 1.0, 1.0, 1.0 )
glMatrixMode ( GL_PROJECTION )
glLoadIdentity()
if config['game_mode']:
  gluPerspective(config['fov'], (glutGameModeGet(GLUT_GAME_MODE_WIDTH) / glutGameModeGet(GLUT_GAME_MODE_HEIGHT)), 1, 2000)
else:
  gluPerspective(config['fov'], (glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT)), 1, 2000)
glMatrixMode( GL_MODELVIEW )
glLoadIdentity()

glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_CULL_FACE)

world = World(config['world'], unload)

glutDisplayFunc(world.display)
glutReshapeFunc(reshape)
glutIdleFunc(world.display)
glutSpecialFunc(world.special)

glutMainLoop()
