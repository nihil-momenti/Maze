# -*- coding: utf-8 -*-
from __future__ import division

from maze import Maze
from special import Special
from tex_plane import Plane

class World(object):
  def __init__(self, config):
    print "  Creating entities..."
    print "    Creating maze..."
    maze = Maze(config['maze'])
    print "    ...Done"
    #ground = Plane(config['ground'], self.heightmap)
    self.contents = set([maze])
    self.config = config
    for cell in maze.specials:
      self.contents.add(Special(*cell))
    print "  ...Done"
    self.start_point = maze.start_point
  
  def gl_init(self):
    Special.init()
    [thing.gl_init() for thing in self.contents]
    
  def display(self):
    [thing.display() for thing in self.contents]
  
  def add(self, thing):
    self.contents.add(thing)
