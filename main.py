from __future__ import division

from json import load

from view import View
from world import World
from player import Player
from controller import Controller

try:
  import psyco
  psyco.full()
  print "Psyco Running"
except ImportError:
  print "Psyco not available"

config = load(file('world.config'))
world       = World(config['world'])
player      = Player(world.heightmap, config['player'])
view        = View(player, world, config['view'])
controller  = Controller(player, world, view, config['controller'])
controller.run()