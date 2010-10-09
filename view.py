"""The View class for 363 lab 9.

A further development of the view class from lab 8. This version allows the
camera to move forward and to turn left and right, providing a simple 
way of navigating within a world.
@author Richard Lobb
@version 28 September 2010
"""

from __future__ import division

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from math import sin, cos, atan2, sqrt


class View(object):

    BACKGROUND = (0.95, 0.95, 0.95, 1)
    
    def __init__(self, player, scene, config):
        print "  Loading config..."
        self.scene = scene
        self.player = player
        self.fov = config['fov']
        self.near = config['near']
        self.far = config['far']
        self.aspect = self.width = self.height = 0
        print "  ...Done"
        
        print "  Initialising GLUT..."
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_MULTISAMPLE)
        if config['game_mode']:
          glutEnterGameMode()
        else:
          glutInitWindowSize(config['window_width'], config['window_height'])
          glutInitWindowPosition(0, 0)
          glutCreateWindow("Robot")
        glutSetKeyRepeat(GLUT_KEY_REPEAT_OFF)
        glutIgnoreKeyRepeat(1)
        print "  ...Done"
        
        print "  Setting up the OpenGL engine..."
        glClearColor( *self.BACKGROUND )
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)
        glEnable(GL_CULL_FACE)
        glLight(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.01)
        glLight(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.01)
        glLight(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0)
        glLightModelf(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
        # glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        # glEnable(GL_COLOR_MATERIAL)
        print "  ...Done"
        
        print "  Starting scene's OpenGL init..."
        self.scene.gl_init()
        print "  ...Done"



    def reshape(self, width, height ):
        """ Reshape function, called whenever user resizes window.

        This function is expected to be called directly by OpenGL, as
        a consequence of a setup call of the form glutReshapeFunc(view.reshape)."""
    
        glViewport(0, 0, width, height)
        self.width = width
        self.height = height
        self.aspect = width / height
    

    def display(self):
        """Output this view of the scene to the OpenGL window"""
        
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity( )
        gluPerspective(self.fov, self.aspect, self.near, self.far)
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
        params = []
        params.extend(self.player.position + self.player.offset())
        params.extend(self.player.lookat)
        params.extend(self.player.viewup)
        gluLookAt(*params)
        glLight(GL_LIGHT0, GL_POSITION, list(self.player.position) + [1])
        # glRotate(self.player.rotation[0], 0, 1, 0)
        # glRotate(self.player.rotation[1], 0, 1, 0)
        
        # Call the scene's display method
         
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the frame buffer
        self.scene.display()
        glutSwapBuffers()


