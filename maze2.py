from __future__ import division

import random
from collections import deque

class Cell(object):
  def __init__(self, x, z, wall=True):
    self.x = x
    self.z = z
    self.wall = wall


class Maze(object):
  def __init__(self, height, size, layers, chance):
    self.height = height
    self.size = size
    self.layers = layers
    self.chance = chance
    self.rows = deque()
    start_row = [Cell(0, z, False) for z in range(height)]
    self.start = start_row[height // 2]
    self.start.wall = False
    self.rows.append(start_row)
    for i in range(size // 2):
      self.rows.appendleft(self.generate_row(self.rows[0]))
      self.rows.append(self.generate_row(self.rows[-1]))
    self.rows.remove(start_row)

  def generate_row(self, old_row):
    new_row = [Cell(old_row[0].x - 1, z) for z in range(self.height)]
    cells = deque(filter(lambda cell: not cell.wall, old_row))
    new_cells = deque()
    for i in range(self.layers):
      cell = random.choice(cells)
      cells.remove(cell)
      new_row[cell.z].wall = False
      new_cells.appendleft(new_row[cell.z])
    cells.extendleft(new_cells)

    while len(cells) > 0:
      cell = cells.pop()
      if random.random() < self.chance:
        if cell in old_row:
          new_row[cell.z].wall = False
          cells.appendleft(new_row[cell.z])
        else:
          if random.random() > 0.5 and cell.z > 0:
            new_row[cell.z - 1].wall = False
            cells.appendleft(new_row[cell.z - 1])
          elif cell.z < self.height - 1:
            new_row[cell.z + 1].wall = False
            cells.appendleft(new_row[cell.z + 1])
    return new_row

  def p(self):
    while True:
      for x in range(self.size + 1):
        print '#',
      print

      for z in range(self.height):
        for row in self.rows:
          print ('#' if row[z].wall else ' '),
        print
      for x in range(self.size + 1):
        print '#',
      print
      
      k = raw_input()
      if k == 'a':
        self.rows.appendleft(self.generate_row(self.rows[0]))
        self.rows.pop()
      elif k == 'd':
        self.rows.append(self.generate_row(self.rows[-1]))
        self.rows.popleft()
      elif k == 'k':
        exit()
