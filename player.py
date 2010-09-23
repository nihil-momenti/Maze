class Player(object):
  def __init__(self, x, z):
    self.position = (x, 0, z)
    self.lookat = (x-1, 0, z)
    self.up = (0, 1, 0)
    print self.position
