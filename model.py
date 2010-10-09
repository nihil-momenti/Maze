from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sqrt

from material import Material

materials = {}

def normal(center_point, clockwise, widdershins):
  n = [clockwise[j] - center_point[j] for j in range(3)]
  p = [widdershins[j] - center_point[j] for j in range(3)]
  cross = [p[1] * n[2] - p[2] * n[1], p[2] * n[0] - p[0] * n[2], p[0] * n[1] - p[1] * n[0]]
  length = sqrt(cross[0] ** 2 + cross[1] ** 2 + cross[2] ** 2)
  n = [cross[j] / length for j in range(3)]
  return n

def decodeTuple(chunks):
  return [float(chunk) for chunk in chunks[1:]]

class Model(object):
  def __init__(self, input_name, pre_func=None, post_func=None):
    input_file = open(input_name)
    vertices = [None]
    textures = [None]
    normals = [None]
    lines = []
    points = []
    tris = []
    quads = []
    faces = []
    currentMaterial = None
    
    for line in input_file.readlines():
      chunks = line.split()
      if len(chunks) > 0:
        if   chunks[0] == 'v':
          vertices.append(decodeTuple(chunks))
        elif chunks[0] == 'vt':
          textures.append(decodeTuple(chunks))
        elif chunks[0] == 'vn':
          normals.append(decodeTuple(chunks))
        elif chunks[0] == 'p':
            points.extend([(vertices[int(chunk)], currentMaterial) for chunk in chunks[1:]])
        elif chunks[0] == 'l':
          line = []
          for chunk in chunks[1:]:
            if chunk.contains('/'):
              v = vertices[int(chunk.split('/')[0])]
              vt = textures[int(chunk.split('/')[1])]
            else:
              v = vertices[int(chunk)]
              vt = None
            line.append((v, vt))
          lines.append((line, currentMaterial))
        elif chunks[0] == 'f':
          face = []
          for chunk in chunks[1:]:
            if len(chunk.split('/')) == 3:
              v = vertices[int(chunk.split('/')[0])]
              vt = textures[int(chunk.split('/')[1])] if chunk.split('/')[1] != '' else None
              vn = normals[int(chunk.split('/')[2])]
            elif len(chunk.split('/')) == 2:
              v = vertices[int(chunk.split('/')[0])]
              vt = textures[int(chunk.split('/')[1])]
              vn = None
            else:
              v = vertices[int(chunk)]
              vt = None
              vn = None
            face.append((v, vt, vn))
          if len(face) == 3:
            tris.append((face, currentMaterial))
          elif len(face) == 4:
            quads.append((face, currentMaterial))
          else:
            faces.append((face, currentMaterial))
        elif chunks[0] == 'mtllib':
          loadMtlLib(input_name.rpartition("/")[0] + "/" + chunks[1])
        elif chunks[0] == 'usemtl':
          currentMaterial = materials[chunks[1]]
    
    currentMaterial = None
    # generate the glGenLists thingy
    self.listID = glGenLists(1); glNewList(self.listID, GL_COMPILE_AND_EXECUTE)
    
    if pre_func is not None: pre_func()
    
    glBegin(GL_POINTS)
    for point in points:
      if point[1] is not None and point[1] != currentMaterial:
        point[1].setMaterial()
        currentMaterial = point[1]
      glVertex(point[0])
    glEnd()
    
    for line in lines:
      glBegin(GL_LINE)
      if line[1] is not None and line[1] != currentMaterial:
        line[1].setMaterial()
        currentMaterial = line[1]
      for vertex in line[0]:
        glVertex(vertex[0])
      glEnd()
    
    glBegin(GL_TRIANGLES)
    for tri in tris:
      if tri[1] is not None and tri[1] != currentMaterial:
        tri[1].setMaterial()
        currentMaterial = tri[1]
      for i in range(len(tri[0])):
        if tri[0][i][1] is not None:
          # Texture
          None
        else:
          # No texture
          None
        if tri[0][i][2] is not None:
          glNormal3f(tri[0][i][2][0], tri[0][i][2][1], tri[0][i][2][2])
        else:
          previous = tri[0][i - 1][0]
          next = tri[0][i + 1 - len(tri[0])][0]
          n = normal(tri[0][i][0], previous, next)
          glNormal(n[0], n[1], n[2])
        glVertex(tri[0][i][0])
    glEnd()
    
    glBegin(GL_QUADS)
    for quad in quads:
      if quad[1] is not None and quad[1] != currentMaterial:
        quad[1].setMaterial()
        currentMaterial = quad[1]
      for i in range(len(quad[0])):
        if quad[0][i][1] is not None:
          # Texture
          None
        else:
          # No texture
          None
        if quad[0][i][2] is not None:
          glNormal3f(quad[0][i][2][0], quad[0][i][2][1], quad[0][i][2][2])
        else:
          previous = quad[0][i - 1][0]
          next = quad[0][i + 1 - len(quad[0])][0]
          n = normal(quad[0][i][0], previous, next)
          glNormal(n[0], n[1], n[2])
        glVertex(quad[0][i][0])
    glEnd()
    
    for face in faces:
      if len(face[0]) == 4:
        glBegin(GL_QUADS)
      elif len(face[0]) == 3:
        glBegin(GL_TRIANGLES)
      else:
        glBegin(GL_POLYGON)
      if face[1] is not None and face[1] != currentMaterial:
        face[1].setMaterial()
        currentMaterial = face[1]
      for i in range(len(face[0])):
        if face[0][i][1] is not None:
          # Texture
          None
        else:
          # No texture
          None
        if face[0][i][2] is not None:
          glNormal3f(face[0][i][2][0], face[0][i][2][1], face[0][i][2][2])
        else:
          previous = face[0][i - 1][0]
          next = face[0][i + 1 - len(face[0])][0]
          n = normal(face[0][i][0], previous, next)
          glNormal(n[0], n[1], n[2])
        glVertex(face[0][i][0])
      glEnd()
    
    if post_func is not None: post_func()
    
    glEndList()
    
  def display(self):
    glCallList(self.listID)
      
def loadMtlLib(lib_name):  
  mtlLib = open(lib_name)
  mtls = mtlLib.read().split("newmtl ")
  for mtl in mtls[1:]:
    lines = mtl.splitlines()
    materials[lines[0]] = Material(lines[1:])
