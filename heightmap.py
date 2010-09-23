from __future__ import division
import numpy, random, math

def powerOf2(size):
  if abs(math.log(size, 2) - round(math.log(size, 2))) < 0.0000001:
    return True
  else:
    return False

def avgDiamondVals(x, y, z, stride, size):
  if x == 0:
    return (y[              x,       z - stride] +
            y[              x,       z + stride] +
            y[size-1 - stride,                z] +
            y[     x + stride,                z]) / 4
  elif x == size-1:
    return (y[               x,      z - stride] +
            y[               x,      z + stride] +
            y[      x - stride,               z] +
            y[      0 + stride,               z]) / 4
  elif z == 0:
    return (y[      x - stride,               z] +
            y[      x + stride,               z] +
            y[               x,      z + stride] +
            y[               x, size-1 - stride]) / 4
  elif z == size-1:
    return (y[      x - stride,               z] +
            y[      x + stride,               z] +
            y[               x,      z - stride] +
            y[               x,      0 + stride]) / 4
  else:
    return (y[      x - stride,               z] +
            y[      x + stride,               z] +
            y[               x,      z - stride] +
            y[               x,      z + stride]) / 4

def avgSquareVals(x, y, z, stride):
  return (y[x - stride, z - stride] + 
          y[x - stride, z + stride] +
          y[x + stride, z - stride] +
          y[x + stride, z + stride]) / 4

def generate_heightmap(size, height_scale, h):
    y = numpy.zeros((size + 1, size + 1))
    if not powerOf2(size) or size == 1:
      print "Size must be a power of two"
      raise Exception
    
    size += 1
    ratio = 2. ** -h
    
    stride = size // 2
    
    while (stride > 0):
      for x in range(stride, size-1, 2*stride):
        for z in range(stride, size-1, 2*stride):
          y[x,z] = height_scale * random.uniform(-0.5,0.5) + avgSquareVals(x, y, z, stride)
      
      oddline = False
      for x in range(0, size, stride):
        oddline = not oddline
        for z in range(stride if oddline else 0, size, 2*stride):
          y[x,z] = height_scale * random.uniform(-0.5,0.5) + avgDiamondVals(x, y, z, stride, size)
          if x == 0:
            y[size-1,z] = y[x,z]
          if z == 0:
            y[x,size-1] = y[x,z]
      height_scale *= ratio
      stride //= 2
    return y
