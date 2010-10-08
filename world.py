# -*- coding: utf-8 -*-
from __future__ import division

# from main import unload
from maze import Maze
from tex_plane import Plane

class World(object):
  def __init__(self, config):
    maze = Maze(config['maze'])
    #ground = Plane(config['ground'], self.heightmap)
    self.contents = set([maze])
  
  def gl_init(self):
    [thing.gl_init() for thing in self.contents]
    
  def display(self):
    [thing.display() for thing in self.contents]