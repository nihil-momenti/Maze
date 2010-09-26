from __future__ import division

from maze2 import Maze
from perlin import Perlin
from PIL import Image
# m = Maze(20, 40, 5, 0.6)
# m.p()

size = 1024
p = Perlin(6, 0.5)
data = [128 * p.value(2, x, y) + 128 for x in range(size) for y in range(size)]
im = Image.new("L", (size,size))
im.putdata(data)
im.save("test.bmp")