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
print "Creating world..."
world       = World(config['world'])
print "...Done"
print "Loading player..."
player      = Player(config['player'], world.start_point)
world.add(player)
print "...Done"
print "Generating View..."
view        = View(player, world, config['view'])
print "...Done"
print "Loading controller..."
controller  = Controller(player, world, view, config['controller'])
print "...Done"
print
print "Welcome to the Labyrinth"
controller.run()