# -*- coding: utf-8 -*-

from Loader import *

from OpenGL.arrays import vbo
from OpenGL.GL import *

import numpy
import time

import operator

"""
Permet de charger chaque membre à partir de chaque
fichier .obj les décrivant.

Utilisé dans Viewer3DWidget via Nao3D.
Utilisé dans naoqiVirtual via Nao3D.
utilisé dans NaoSimulator
"""

class Membre():
    dt=0.02
    membres={}#dictionnaire des VBO créées par typeMembre
    membresRecup={}#recup des obj par name
    print "Chargement des objets 3D en cours..."

    extrema = {"teteG":[(-38.5,29.5),(.0,.0),(-119.5,119.5)],
                     "bicepsG":[(-119.5,119.5),(.0,.0),(-18.0,76.0)],
                     "coudeG":[(.0,.0),(-119.5,119.5),(-88.5,-2.0)],
                     "mainG":[(.0,.0),(-119.5,119.5),(.0,.0)],
               "teteD":[(-38.5,29.5),(0,0),(-119.5,119.5)],
                     "bicepsD":[(-119.5,119.5),(.0,.0),(-18.0,76.0)],
                     "coudeD":[(.0,.0),(-119.5,119.5),(-88.5,-2.0)],
                     "mainD":[(.0,.0),(-119.5,119.5),(.0,.0)],
               "hanche":[(-32.81,21.22),(.0,.0),(-32.81,21.22)],
               "hancheD":[(-32.81,21.22),(.0,.0),(-32.81,21.22)],
               "hancheG":[(-32.81,21.22),(.0,.0),(-32.81,21.22)],
                     "cuisseG":[(-88.0,27.73),(-21.74,45.29),(.0,.0)],
                     "molletG":[(-5.29,121.04),(.0,.0),(.0,.0)],
                     "piedG":[(-68.15,52.86),(-22.79,44.06),(.0,.0)],
               "cuisseD":[(-88.0,27.73),(-21.74,45.29),(.0,.0)],
                     "molletD":[(-5.29,121.04),(.0,.0),(.0,.0)],
                     "piedD":[(-68.15,52.86),(-22.79,44.06),(.0,.0)],
                     "epauleBicepsG":[(-119.5,119.5),(.0,.0),(-18.0,76.0)],
                     "epauleBicepsD":[(-119.5,119.5),(.0,.0),(-18.0,76.0)],
                     "epauleG":[(-119.5,119.5),(.0,.0),(-18.0,76.0)],
                     "doigt3D":[(.0,90.0),(.0,.0),(.0,.0)],
                     "doigt3G":[(.0,90.0),(.0,.0),(.0,.0)],
                     "doigt1D":[(-90.0,.0),(.0,.0),(.0,.0)],
                     "doigt1G":[(-90.0,.0),(.0,.0),(.0,.0)],
                     "doigt2D":[(.0,90.0),(.0,.0),(.0,.0)],
                     "doigt2G":[(.0,90.0),(.0,.0),(.0,.0)],
                     "epauleD":[(-119.5,119.5),(.0,.0),(-18.0,76.0)]}

    def __init__(self,partie,name):

        self.isFirst=False
        self.boolText=False
        self.replaceColor=False

        self.multipleColors=False
        self.changeColor={}

        self.membre=partie

        if partie not in Membre.membres.keys():
            self.construct()
        else :
            self.recopy(Membre.membresRecup[partie+"G"])
            if partie=="torseS" : print "25 %"
            elif partie=="torse" : print "50 %"
            elif partie=="tete" : print "75 %"
            elif partie=="pied" : print "100 %"

        self.size=[1.0,1.0,1.0]
        self.rotate=[0.0,0.0,0.0]

        self.vitesse=[0.0,0.0,0.0]

        self.stiffness= 0.0
        #angle : différentiel à appliquer aux angles, en degré par milliseconde
        self.angle= [.0,.0,.0]
        self.timeMove = [.0,.0,.0]

        self.pos=[0.0,0.0,0.0]

        if name in self.extrema.keys():
            self.min=[self.extrema[name][0][0],self.extrema[name][1][0],self.extrema[name][2][0]]
            self.max=[self.extrema[name][0][1],self.extrema[name][1][1],self.extrema[name][2][1]]
        else:
            self.min=[.0,.0,.0]
            self.max=[.0,.0,.0]

        self.name=name

        self.underObjects={}
        #on ajoute cet objet dans la 'liste' des objets existant
        #pour y avoir accès facilement.
        Membre.membresRecup[name]=self

    def setAngle(self, axe, angleDegre, time):
        self.timeMove[axe]=1000*time
        self.angle[axe] = (angleDegre-self.rotate[axe])/float(self.timeMove[axe])

    def updateDt(self, dt):
        dt*=1000#ms
        for x in range(3):
            if self.timeMove[x]>=dt:
                self.timeMove[x]-=dt
                self.rotate[x]+=(self.angle[x]*dt*self.stiffness)
            #self.rotate[x]+=1

    def getPercentFromAxis(self, axe):
        #print self.max[axe]==self.min[axe],self.max[axe],self.min[axe],self.max[axe]-self.min[axe]
        if (self.max[axe]==self.min[axe]): return .0
        return (self.rotate[axe]-self.min[axe])/(self.max[axe]-self.min[axe])*100.0

    def setAngleFromPercent(self, axe, p):
        self.rotate[axe]= p/100.0 *((self.max[axe]-self.min[axe]))+self.min[axe]
        #print self.rotate[axe], "axe "+str(axe)

    def setAngleFromPercentList(self, pl):
        for x in range(len(pl)):
            self.rotate[x]= pl[x]/100.0 *((self.max[x]-self.min[x]))+self.min[x]

    def calculateAngle(self,axe,p,time):
        rotFin=self.get()
        rotAxe=self.rotate[axe]
        angle=(rotFin-rotAxe)/(1000.0*time)

    def addUnder(self,partie,name):
        self.underObjects[name]=Membre(partie,name)

    def draw(self,rot=False):
        if self.membre[:3]=="eye":
            glDisable(GL_LIGHTING)
        if self.isFirst:
            glPushMatrix()

        glTranslatef(self.pos[0],self.pos[2],self.pos[1])
        glScalef(self.size[0],self.size[2],self.size[1])

##        if rot:
##            rotation=self.addList(self.rotate,rot)
##        else :

        rotation=self.rotate

        glRotatef(rotation[0],1.0,.0,.0)
        glRotatef(rotation[1],.0,.0,1.0)
        glRotatef(rotation[2],.0,1.0,.0)

        if self.replaceColor:
            glColor3f(self.replaceColor[0],self.replaceColor[1],self.replaceColor[2])
        else :
            glColor3f(1.0,1.0,1.0)

        self.drawVBO()

        for x in self.underObjects.keys():
            self.underObjects[x].draw()#rotation)#self.rotate,self.pos)

        if self.isFirst:
            glPopMatrix()
        if self.membre[:3]=="eye":
            glEnable(GL_LIGHTING)

    def addList(self,list1,list2):
        a=[]
        for b in range(len(list1)):
            a.append(list1[b]+list2[b])
        return a

    def subList(self,list1,list2):
        return list([list1[0]-list2[0],list1[1]-list2[1],list1[2]-list2[2]])

    def construct(self):
        Membre.membres[self.membre]={}
        #on ne récupère ici qu'un seul objet.(genre objet blender pas objet reel)
        nao=Loader().load(self.membre)[0]

        self.multipleColors=nao.multipleColors()
        self.changeColor=nao.material#getFaceNbColors()

        Membre.membres[self.membre]["boolText"]=nao.hasTexture
        Membre.membres[self.membre]["len"]=len(nao.tabCoordInd)
        self.boolText=nao.hasTexture

        V=[]
        for a in range(len(nao.tabCoordInd)):
            V.append(nao.tabCoord[nao.tabCoordInd[a]-1])

        VN=[]
        for a in range(len(nao.tabNormInd)):
            VN.append(nao.tabNorm[nao.tabNormInd[a]-1])

        #Create the VBO
        v = numpy.array([V], dtype=numpy.float32)
        Membre.membres[self.membre]["vVBO"] = vbo.VBO(v)

        #Create the VBO
        vn = numpy.array([VN], dtype=numpy.float32)
        Membre.membres[self.membre]["vnVBO"] = vbo.VBO(vn)

        if self.boolText:
            VT=[]
            for a in range(len(nao.tabTextInd)):
                VT.append(nao.tabText[nao.tabTextInd[a]-1])

            #Create the VBO
            vt = numpy.array([VT], dtype=numpy.float32)
            Membre.membres[self.membre]["vtVBO"] = vbo.VBO(vt)

    def drawVBO(self):

        if self.boolText:
            Membre.membres[self.membre]["vtVBO"].bind()
            #self.vtVBO.bind()
            glTexCoordPointer(2, GL_FLOAT, 0, None )

        Membre.membres[self.membre]["vVBO"].bind()
        #self.vVBO.bind()
        glVertexPointer(3, GL_FLOAT, 0, None )

        Membre.membres[self.membre]["vnVBO"].bind()
        #self.vVBO.bind()
        glNormalPointer(GL_FLOAT, 0, None )

        if self.replaceColor:
            glColor3f(self.replaceColor[0],self.replaceColor[1],self.replaceColor[2])
            glDrawArrays(GL_TRIANGLES, 0, Membre.membres[self.membre]["len"]);
        else:
            #eg :a={1:2,2:3,0:6}
            sorted_x = sorted(self.changeColor.iteritems(), key=operator.itemgetter(0))
            #result : [(0, 6), (1, 2), (2, 3)],sachant que le [1] est un material
            for a in range(len(self.changeColor)):
                glColor3f(sorted_x[a][1].getColor()[0],sorted_x[a][1].getColor()[1],sorted_x[a][1].getColor()[2])
                #on affiche toutes les faces de la face n° text actuelle à la face n° text suivante...
                glDrawArrays(GL_TRIANGLES, sorted_x[a][0], self.compteNb(sorted_x,a,Membre.membres[self.membre]["len"]));
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def compteNb(self,liste,a,big):
        if a < len(liste)-1:
            return liste[a+1][0]-liste[a][0]
        else:
            return big-liste[a][0]

    def recopy(self,recopiable):
        self.isFirst=recopiable.isFirst
        self.boolText=recopiable.boolText
        self.replaceColor=recopiable.replaceColor

        self.multipleColors=recopiable.multipleColors
        self.changeColor=recopiable.changeColor.copy()

