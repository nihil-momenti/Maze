from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def decodeK(chunks):
  if len(chunks) == 2:
    return [float(chunks[1]), float(chunks[1]), float(chunks[1])]
  else:
    return [float(chunk) for chunk in chunks[1:]]
    
def decodeD(chunks):
  if chunks[1] == '-halo':
    return (True, float(chunks[2]))
  else:
    return (False, float(chunks[1]))

class Material(object):
  def __init__(self, lines):
    self.d         = (False, 1.0)
    self.Ka        = None
    self.Kd        = None
    self.Ks        = None
    self.Tf        = None
    self.Ns        = None
    self.Ni        = None
    self.illum     = None
    self.sharpness = 60
    
    for line in lines:
      chunks = line.split()
      if len(chunks) > 0:
        if   chunks[0] == 'd':         self.d         = decodeD(chunks)
        elif chunks[0] == 'Ka':        self.Ka        = decodeK(chunks)
        elif chunks[0] == 'Kd':        self.Kd        = decodeK(chunks)
        elif chunks[0] == 'Ks':        self.Ks        = decodeK(chunks)
        elif chunks[0] == 'Tf':        self.Tf        = decodeK(chunks)
        elif chunks[0] == 'Ns':        self.Ns        =   float(chunks[1])
        elif chunks[0] == 'Ni':        self.Ni        =   float(chunks[1])
        elif chunks[0] == 'illum':     self.illum     =     int(chunks[1])
        elif chunks[0] == 'sharpness': self.sharpness =     int(chunks[1])
    
    self.listID = glGenLists(1); glNewList(self.listID, GL_COMPILE_AND_EXECUTE)
    
    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT,   self.Ka)
    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE,   self.Kd)
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR,  self.Ks) 
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, self.Ns) 
    
    glEndList()
    
  def setMaterial(self):
    glCallList(self.listID)
      

# Illumination Models:
# 0  Color on and Ambient off
# 1  Color on and Ambient on
# 2  Highlight on
# 3  Reflection on and Ray trace on
# 4  Transparency: Glass on
#    Reflection: Ray trace on
# 5  Reflection: Fresnel on and Ray trace on
# 6  Transparency: Refraction on
#    Reflection: Fresnel off and Ray trace on
# 7  Transparency: Refraction on
#    Reflection: Fresnel on and Ray trace on
# 8  Reflection on and Ray trace off
# 9  Transparency: Glass on
#    Reflection: Ray trace off
# 10 Casts shadows onto invisible surfaces
 