from __future__ import division

from main import unload
from maze import Maze
from plane import *
from player import Player
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class World(object):
  def __init__(self, config):
    coarse_heightmap = generate_heightmap(config['coarse_size'], config['coarse_scale'], config['coarse_h'])
    maze = Maze(config['maze'])
    
#planes = FirstPlane(128, 40, 0.95, True, 10)
maze = Maze(100,100,10,20,6,0.01)
player = Player((maze.startPoint.x - maze.width / 2) * maze.scale, (maze.startPoint.z - maze.height / 2) * maze.scale)

  def display(self):
    self.player.updateAccel()
    self.player.updateView()
    glLoadIdentity()
  #  gluLookAt(0, 100, 200, 0,0,0, 0,1,0)
    gluLookAt(self.player.position[0], self.player.position[1], self.player.position[2],
                self.player.lookat[0],   self.player.lookat[1],   self.player.lookat[2],
                    self.player.up[0],       self.player.up[1],       self.player.up[2])
  #  glRotate(time.time()%360*50, 0, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    [thing.display() for thing in world]
    glutSwapBuffers()
    
  def special(self, key, x, y):
    if key == GLUT_KEY_F10:
      unload()
      exit()
