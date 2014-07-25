# -*- coding: utf-8 -*-

import  sys, os
import math

import PyQt4.QtGui as Gui
import PyQt4.QtCore as Core
import PyQt4.QtCore as QtCore
from PyQt4.QtOpenGL import QGLWidget

from OpenGL.arrays import vbo
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

from GLDemo.Camera import Camera
from GLDemo.MyGeom import Point3D
#from Nao3D import Nao3D  #utilise virtualNao

import time


class Viewer3DWidget(QGLWidget):
    """
    Utilise OpenGL pour afficher le robot.
    Utilise Loader pour charger les VBO à partir des fichiers .obj

    Possède un "pointeur" sur le robot virtuel

    WheelEvent et MouseMoveEvent sont des callback qui mettent à jour
    l'affichage 3D (fonction update qui appelle la fonction paintGL)
    """
    signalFullscreenOn = QtCore.pyqtSignal()
    signalFullscreenOff = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        QGLWidget.__init__(self,parent)
        self.setMouseTracking(True)
        # self.setMinimumSize(500, 500)
        self.camera = Camera()
        self.camera.setSceneRadius( 2 )
        self.camera.reset()

        self.isPressed = False
        self.inFullscreen = False
        self.oldx = 0
        self.oldy = 0

        self.decalage=-10

        self.sizef=1.0
        self.taille=0

        self.virtualNao = None#Nao3D()

        self.size(0)
        self.font = Gui.QFont("Helvetica",5)
        self.font_offset=[20,20]

        self.background = Gui.QColor(125,125,255)

    def updateDt(self, dt):
        #animation
        for membre in self.virtualNao.getMembreKeys():
            self.virtualNao.getMembre(membre).updateDt(dt)
        self.update()

    def paintGL(self):
        """
        surcharge de la fonction présente dans GLWidget
        est appelée par update
        """

        glClearColor(self.background.red()/255.0,self.background.green()/255.0,self.background.blue()/255.0,1.0) ;
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity();

        ############################# 3D DRAWING ################

        glEnable(GL_TEXTURE_2D);
        glEnable(GL_DEPTH_TEST);
        glEnable(GL_LIGHTING)
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        self.camera.transform()
        glMatrixMode( GL_MODELVIEW );
        glLoadIdentity();


        glEnableClientState(GL_VERTEX_ARRAY);
        glEnableClientState(GL_NORMAL_ARRAY);

        glTranslatef(0,self.decalage,0)

        glPushMatrix()

        self.virtualNao.getMembre("torseG").draw()
        glScalef(-1.0,1.0,1.0)
        self.virtualNao.getMembre("torseD").draw()

        glPopMatrix()

        glDisableClientState(GL_NORMAL_ARRAY);
        glDisableClientState(GL_VERTEX_ARRAY);

                ######################## NAO SPEAKING ###################
        glLoadIdentity();

        # scene pos and size
        self.renderText(self.font_offset[0],self.font_offset[1],self.virtualNao.speaking, self.font)
        time.sleep(0.015)


    def resizeGL(self, widthInPixels, heightInPixels):
        self.camera.setViewportDimensions(widthInPixels, heightInPixels)
        glViewport(0, 0, widthInPixels, heightInPixels)
        self.font.setPointSize(int(2.5*widthInPixels/100))
        self.font_offset[1] = heightInPixels - (20)

    def initializeGL(self):
        glEnable(GL_BLEND)
        glClearColor(0.5,0.5,1.0,1.0) ;
        glClearDepth(1.0)

        specular = [  .2,.2,.2,1.0 ];
        vert = [  .5,.5,.5,1.0 ];
        l_pos0 = [  10.0,200.0,200.0,1.0 ];
        l_dir0 = [  -10.0,0.0,-20.0,1.0 ];
        glClearColor(0.5,0.5,1.0,1.0) ;
        glMaterialfv(GL_FRONT,GL_SPECULAR,specular);
        glLightfv(GL_LIGHT0,GL_POSITION,l_pos0);
        glLightfv(GL_LIGHT0,GL_SPOT_DIRECTION,l_dir0);
        glLightfv(GL_LIGHT0,GL_DIFFUSE,vert);
        glEnable(GL_LIGHT0);

        glEnable(GL_LIGHTING);
        glEnable(GL_COLOR_MATERIAL)

        glDepthFunc(GL_LESS);
        glEnable(GL_DEPTH_TEST);

    def mouseMoveEvent(self, mouseEvent):
        if int(mouseEvent.buttons()) != Core.Qt.NoButton :
            # user is dragging
            delta_x = mouseEvent.x() - self.oldx
            delta_y = self.oldy - mouseEvent.y()
            if int(mouseEvent.buttons()) & Core.Qt.LeftButton :
                if int(mouseEvent.buttons()) & Core.Qt.MidButton :
                    #pass
                    self.camera.dollyCameraForward( 3*(delta_x+delta_y), False )
                else:
                    self.camera.orbit(self.oldx,self.oldy,mouseEvent.x(),mouseEvent.y())
            elif int(mouseEvent.buttons()) & Core.Qt.MidButton :
                #self.camera.translateSceneRightAndUp( 0, delta_y )
                self.decalage+= delta_y/160.0
                pass
            self.update()
        self.oldx = mouseEvent.x()
        self.oldy = mouseEvent.y()

    def unmiddle(self):
        self.decalage=0

    def middle(self):
        self.decalage=-1.25

    def size(self,t):
        self.sizef=80*t
        self.taille+=self.sizef

    def resizeTo(self,to):
            for x in range(abs(self.taille-to)/80+1):
                if self.taille!=to:
                    self.sizef=80*(to-self.taille)/(abs(to-self.taille))
                    self.taille+=self.sizef
                    self.camera.dollyCameraForward(self.sizef,0)
                    self.update()

    def wheelEvent(self,r):
        self.size(r.delta()/120)
        self.camera.dollyCameraForward(self.sizef,0)
        self.update()

    def mousePressEvent(self, e):
        self.isPressed = True

    def mouseReleaseEvent(self, e):
        self.isPressed = False

    def mouseDoubleClickEvent (self, mouse_e):
        if not self.inFullscreen:
            self.showFullScreen()
            self.inFullscreen=True
            self.signalFullscreenOn.emit()
        else :
            self.inFullscreen=False
            self.signalFullscreenOff.emit()

