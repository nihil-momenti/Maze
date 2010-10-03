"""A simple demo of texturing that draws a chequered ground polygon

@author Richard Lobb
@version 28 September 2010"""


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import array
from PIL import Image

LIGHT_POS = (3, 4, 5, 0)
CHECK_1 = (64, 96, 64)    # One of the two chequerboard colours
CHECK_2 = (192, 208, 192) # The other one.


def checkedPattern(imageSize, sqSize, inColour, outColour):
    """Return a chequerboard pattern, packed into a string.

    imageSize is the number of bytes (pixels) across and down
    sqSize is the size of each chequerboard square in pixels
    inColour, outColour are the two (R,G,B) square colours.
    """
    
    result = array.array('B')  # An array of bytes
    inBytes = array.array('B', inColour)
    outBytes = array.array('B', outColour)

    for row in range(imageSize):
        for col in range(imageSize):
            if ((row / sqSize) & 1) ^ ((col / sqSize) & 1):
                result += inBytes
            else:
                result += outBytes
    return result.tostring()



class Scene(object):
    """A scene for display via OpenGL"""

    def __init__(self, textureSize, repetitions):
        """Constructor for a scene with a single textured polygon.
        textureSize is the number of texels along each edge of the 2 x 2
        chequerboard pattern.
        repetitions is the number of times that pattern is repeated over
        the polygon
        """

        self.textureSize = textureSize
        self.repetitions = repetitions
        self.yRotation = 0


    def gl_init(self):
        """Set up OpenGL pipeline stuff needed by this particular scene"""
        
        self.textureID = glGenTextures(1)  # Get 1 texture ID
        pattern = checkedPattern(self.textureSize, self.textureSize/2, CHECK_1, CHECK_2) 
        # Uncomment the next line to inspect the texture image
        # Image.fromstring("RGB", (self.textureSize, self.textureSize), pattern).show()
        w = h = self.textureSize
        glBindTexture(GL_TEXTURE_2D, self.textureID)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB,
                     GL_UNSIGNED_BYTE, pattern)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glTexEnvi(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
        glEnable(GL_TEXTURE_2D)
    

    def display(self):
        """Output the entire scene to the OpenGL pipeline."""
        
        glBindTexture(GL_TEXTURE_2D, self.textureID)
        
        glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POS)
    
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glTexCoord2f(0, 0)
        glVertex3f(-1, 0, 1)
        glTexCoord2f(self.repetitions, 0)
        glVertex3f(1, 0, 1)
        glTexCoord2f(self.repetitions, self.repetitions)
        glVertex3f(1, 0, -1)
        glTexCoord2f(0, self.repetitions)
        glVertex3f(-1, 0, -1)
        glEnd()

