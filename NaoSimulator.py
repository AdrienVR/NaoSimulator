# -*- coding: utf-8 -*-

#############################################################
##########           OPEN NAO SIMULATOR               #######
#############################################################

import sys
import os
import time
import threading

## QT libs
from PySide.QtGui import QApplication,  QMainWindow
from PySide.QtGui import QFileDialog, QCursor, QToolTip
from PySide.QtGui import QWidget,QDialog
from PySide.QtGui import QMessageBox,QFont
from PySide import QtCore
from PySide.QtCore import QRect, QUrl
from PySide.QtCore import Qt, SIGNAL, QTimer
from PySide.QtCore import QObject, QThread
from PySide.QtCore import QMutex

#Partie 3D
from Viewer3DWidget import Viewer3DWidget
from Loader import Objet3D
#Affichage accents
from DecoderAll import Decoder
from syntaxColor import *
#API NAO
from Nao3D import Nao3D
from naoqiVirtual import ALProxy
#compilation
from imports import *

#pour activer ou desactiver la redirection des
#affichages de texte vers la console intégrée
DEBUGERR = True
DEBUGERR = False
DEBUGOUT = True
DEBUGOUT = False

ENABLE_SPACES_TO_TAB=True

## Calcul du gris des yeux
FORMAT_COLORS = 255.0
## plus cette valeur grandit plus les couleurs sont ternes
## afin de simuler la faible intensité des leds du robot.
EYES_GREY = 175.0
R_COLOR = EYES_GREY / FORMAT_COLORS

Ssaveout = sys.stdout
Ssaveerr = sys.stderr

Global_repeat = False

from widgets import *

#heritage pour simplifier l'editeur
from Editeur import EditeurPython

class MainWindow(QMainWindow,  Ui_MainWindow, EditeurPython):
    def __init__(self,  conteneur=None):
        if conteneur is None : conteneur = self
        QMainWindow.__init__(conteneur)
        self.setupUi(conteneur)
        EditeurPython.__init__(self)
        self.setCentralWidget(self.centralwidget)

        ######################## ATTRIBUTS ################################

        self.colors = ColorWindow()

        #Python Shell like
        self.textBrowserConsole = PyShell(self.tabConsole)

        #fenetre a propos
        self.aProposWindow=ApWindow()

        #fenetre configuration reseau
        self.config=Configuration()
        self.runReal=False

        #fenetre documentation
        if QWEB_ENABLE:
            self.doc=Documentation()
            self.doc.webView.load(QUrl(os.path.join("doc","index.html")))
            self.doc.webView.show()
        else :
            self.actionDocumentation.setEnabled(False)

        #stop ne marche pas ...
        self.actionStop.setEnabled(False)

        #on enregistre les redirections systemes vers le nouveau "shell"
        self.saveout = sys.stdout
        self.saveerr = sys.stderr

        #Pour l'animation : utilisation d'un timer pour le framerate
        self.timer=QTimer()

        #Pour afficher infos angles sur les mouvements des sliders.
        self.cursor=QCursor()

        #utilisé lors de la vérification du nombre de membre : obsolete avec referencement du modele(h21,t14)
        self.initTabLength=self.tabWidget2.count()

        ########## VIRTUAL NAO ##############
        self.virtualNao=Nao3D()
        #association au FakeALProxy
        ALProxy.associateVirtualRobot(self.virtualNao)

        self.Viewer3DWidget=Viewer3DWidget(self.widgetGLContainer)
        self.Viewer3DWidget.virtualNao=self.virtualNao
        ##########

        self.buttonNames = [self.pushButtonTeteGD,self.pushButtonTeteHB,
                            self.pushButtonBicepsG,self.pushButtonCoudeG,self.pushButtonMainG,self.pushButtonDoigtsG,
                            self.pushButtonHanche,
                            self.pushButtonCuisseG, self.pushButtonMolletG, self.pushButtonPiedG,
                            self.pushButtonCuisseD, self.pushButtonMolletD, self.pushButtonPiedD,
                            self.pushButtonBicepsD,self.pushButtonCoudeD,self.pushButtonMainD,self.pushButtonDoigtsD
                            ]

        self.sliders=[
        ## Haut
                      self.horizontalSliderTete0,self.horizontalSliderTete2,
                      self.horizontalSliderBicepsG0,self.horizontalSliderBicepsG2,
                      self.horizontalSliderCoudeG0,self.horizontalSliderCoudeG1,
                      self.horizontalSliderMainG1,
                      self.horizontalSliderDoigtsG0,
        ## Bas
                      self.horizontalSliderHanche15,
                      self.horizontalSliderCuisseG0,self.horizontalSliderCuisseG1,
                      self.horizontalSliderMolletG0,
                      self.horizontalSliderPiedG0,self.horizontalSliderPiedG1,
        ## Partie Droite Bas
                      self.horizontalSliderHanche15,
                      self.horizontalSliderCuisseD0,self.horizontalSliderCuisseD1,
                      self.horizontalSliderMolletD0,
                      self.horizontalSliderPiedD0,self.horizontalSliderPiedD1,
        ## Haut
                      self.horizontalSliderBicepsD0,self.horizontalSliderBicepsD2,
                      self.horizontalSliderCoudeD0,self.horizontalSliderCoudeD1,
                      self.horizontalSliderMainD1,
                      self.horizontalSliderDoigtsD0]

        #permet de savoir quel slider a changé de valeur (= old)
        self.valueList=[]
        for a in range(len(self.sliders)):
            self.valueList.append(self.sliders[a].value())

        self.sliderAxis=[0,2,0,2,2,1,1,0,3,0,1,0,0,1,3,0,1,0,0,1,0,2,2,1,1,0]

        self.target=0
        self.targets={self.pushButtonTeteHB:("teteG","teteD"),self.pushButtonTeteGD:("teteG","teteD"),
                      self.pushButtonBicepsG:("epauleG","bicepsG","epauleBicepsG"),self.pushButtonBicepsD:("epauleD","bicepsD","epauleBicepsD"),
                      self.pushButtonCoudeG:("coudeG"),self.pushButtonCoudeD:("coudeD"),
                      self.pushButtonMainG:("mainG"),self.pushButtonMainD:("mainD"),
                      self.pushButtonDoigtsG:("doigt1G","doigt2G","doigt3G"),self.pushButtonDoigtsD:("doigt1D","doigt2D","doigt3D"),
                      self.pushButtonHanche:("hancheD","hancheG"),
                      self.pushButtonCuisseG:("cuisseG"),self.pushButtonCuisseD:("cuisseD"),
                      self.pushButtonMolletG:("molletG"),self.pushButtonMolletD:("molletD"),
                      self.pushButtonPiedG:("piedG"),self.pushButtonPiedD:("piedD")}

        self.checkLedBoxes={self.checkBoxLed1:"eye1",self.checkBoxLed2:"eye2",self.checkBoxLed3:"eye3",
                            self.checkBoxLed4:"eye4",self.checkBoxLed5:"eye5",self.checkBoxLed6:"eye6",
                            self.checkBoxLed7:"eye7",self.checkBoxLed8:"eye8"}
        self.selectedAll=True

        self.modified = False
        self.name="Nao Simulator 2014"
        self.fileName=""

        self.boolOmbre = False
        self.running=True
        self.htmlSet=True

        self.thread = Worker(self)
        self.thread_code = Worker(self)

        self.thread_both_terminated = False

        self.printer = Printer()
        self.printer.target = self

        self.materials=[self.actionOrange,self.actionGris,self.actionBleu,self.actionNoir]
        self.eqMtlNames={self.actionOrange:(FORMAT_COLORS/FORMAT_COLORS,30.0/FORMAT_COLORS,1.0/FORMAT_COLORS),self.actionGris:(200.0/FORMAT_COLORS,200.0/FORMAT_COLORS,200.0/FORMAT_COLORS),
                         self.actionBleu:(20.0/FORMAT_COLORS,20.0/FORMAT_COLORS,FORMAT_COLORS/FORMAT_COLORS),self.actionNoir:(0.0/FORMAT_COLORS,0.0/FORMAT_COLORS,0.0/FORMAT_COLORS)}


        self.differenceRobots=[self.horizontalSliderMainG1,
                                self.horizontalSliderMainD1,
                                self.horizontalSliderDoigtsG0,
                                self.horizontalSliderDoigtsD0,
                                self.pushButtonMainG,
                                self.pushButtonMainD,
                                self.pushButtonDoigtsG,
                                self.pushButtonDoigtsD]

        self.currentIndex = 0

        self.syntaxColor = PythonHighlighter(self.textEdit.document())

        #self._pool = CallbackThreadPool(4)
        self.touchSensor = -1

        self.touchSensors = [self.pushButtonMainDDevant, self.pushButtonMainDDessus, self.pushButtonMainDArriere,
        self.pushButtonMainGDevant, self.pushButtonMainGDessus, self.pushButtonMainGArriere,
        self.pushButtonTeteDevant, self.pushButtonTeteDessus, self.pushButtonTeteArriere]

        ################# INITIALISATION #####################################

        self.initName()
        self.actionStop_2.setShortcut(None)

        self.colors.setColorVar("wallpaper",self.Viewer3DWidget.background)

        self.initTextEdit()

        self.createConnexions()
        self.show()

        self.setIO()

        self.tabWidget.setCurrentIndex(0)

        #Pour la maj, il y a une connexion directe avec le compteur, pour l'animation
        self.connect(self.timer,  SIGNAL("timeout()"), self.animate)
        self.connect(self.timer,  SIGNAL("timeout()"), self.updateSliders)
        self.connect(self.timer,  SIGNAL("timeout()"), self.updatePhysics)
        self.oldTime=0.0
        #pour le reste une surcharge des fonctions WheelEvent et MouseEvent permet
        #le controle des mouvements
        self.resizeViewer3DWidget()

        self.motor()
        self.resizeShell()

        #stocke la partie jambes retirées
        self.pop=[0,0]
        self.hideLegs()
        self.oldMaterial=self.actionOrange

        self.selectAll()
        self.stopLights()
        self.selectAll()
        self.updateSliders()
        self.updatePhysics()
        self.running=False

    def __del__(self):
         sys.stdout = self.saveout
         sys.stderr = self.saveerr
         print "goodbye"

    #def OnCloseEvent(self):
    #todo

    def setIO(self):
        if not DEBUGOUT :
            sys.stdout = self.textBrowserConsole
            if not DEBUGERR:
                sys.stderr = self.textBrowserConsole
            else :
                sys.stderr = self.saveerr
        else :
            self.setOffIO()

    def setOffIO(self):
        sys.stdout = self.saveout
        sys.stderr = self.saveerr

#     def close(self):
#         if self.modified:
#             reponse = QMessageBox.question(self, u"Enregistrer",
#                 u"Voulez-vous enregistrer le fichier avant de quitter ?",
#                 QMessageBox.Yes | QMessageBox.No)
#             if reponse==QMessageBox.No:
#                 pass
#             else :
#                 self.save()
#         self.__del__()

    def createConnexions(self):
        """
        Callbacks : signal, slot
        """

        #fenetres
        self.connect(self.actionApropos,  SIGNAL("triggered()"), self.aProposWindow.show)
        if QWEB_ENABLE:
            self.connect(self.actionDocumentation,  SIGNAL("triggered()"), self.doc.show)
        self.connect(self.actionConfiguration,  SIGNAL("triggered()"), self.config.show)

        self.connect(self.actionColors,  SIGNAL("triggered()"), self.colors.show)
        self.connect(self.colors.buttonBox, SIGNAL("accepted ()"), self.applyColor)


        #fentre interface
        self.connect(self.actionReinitialiser_Pupitre,  SIGNAL("triggered()"), self.initPupitre)
        self.connect(self.actionReinitialiser_Editeur,  SIGNAL("triggered()"), self.initEditeur)
        self.connect(self.actionReinitialiser_Vue_3D,  SIGNAL("triggered()"), self.initVue3D)

        self.Viewer3DWidget.signalFullscreenOn.connect(self.setFullScreenOn)
        self.Viewer3DWidget.signalFullscreenOff.connect(self.setFullScreenOff)

        #actions Editeur de texte
        #Fichier Menu
        self.connect(self.actionQuitter, SIGNAL("triggered()"), self.close)
        self.connect(self.actionRelancer, SIGNAL("triggered()"), self.relaunch)
        self.connect(self.actionOuvrir,  SIGNAL("triggered()"), self.openFile)
        self.connect(self.textEdit, SIGNAL("textChanged ()"), self.setStar)
        self.connect(self.textEdit, SIGNAL("textChanged ()"), self.setColors)
        self.connect(self.actionEnregistrer,  SIGNAL("triggered()"), self.save)
        self.connect(self.actionEnregistrer_sous,  SIGNAL("triggered()"), self.saveUnder)
        #Edition Menu
        self.connect(self.actionCouper,  SIGNAL("triggered()"), self.cut)
        self.connect(self.actionColler,  SIGNAL("triggered()"), self.paste)
        self.connect(self.actionCopier,  SIGNAL("triggered()"), self.copy)
        self.connect(self.actionAnnuler,  SIGNAL("triggered()"), self.undo)
        self.connect(self.actionRetablir,  SIGNAL("triggered()"), self.redo)
        #self.connect(self.actionSupprimer,  SIGNAL("triggered()"), self.delete)
        #Format Menu
        self.connect(self.actionCommenter,  SIGNAL("triggered()"), self.comment)
        self.connect(self.actionDecommenter,  SIGNAL("triggered()"), self.uncomment)
        self.connect(self.actionIndenter, SIGNAL("triggered()"), self.indent)
        self.connect(self.actionDedenter, SIGNAL("triggered()"), self.unindent)

        self.connect(self.actionEffacer,  SIGNAL("triggered()"), self.textBrowserConsole.clearTT)

        ## RESEAU
        ##self.connect(self.actionRunReal,  SIGNAL("triggered()"), self.changeReseau)

        #actions boutons menu
        self.connect(self.actionRun,  SIGNAL("triggered()"), self.run)
        self.connect(self.actionRun_2,  SIGNAL("triggered()"), self.run)
        # marche pas
        #self.connect(self.actionStop,  SIGNAL("triggered()"), self.stop)
        #self.connect(self.actionStop_2,  SIGNAL("triggered()"), self.stop)
        self.connect(self.actionStop,  SIGNAL("triggered()"), self.thread_code.stop)
        self.connect(self.actionStop,  SIGNAL("triggered()"), self.thread.stop)

        #Robot Menu
        self.connect(self.actionNaoH25,  SIGNAL("triggered()"), self.showLegs)
        self.connect(self.actionNaoH21,  SIGNAL("triggered()"), self.showLegsH21)
        self.connect(self.actionNaoT14,  SIGNAL("triggered()"), self.hideLegs)
        #Couleur Option
        self.connect(self.actionOrange,  SIGNAL("triggered()"), self.changeMaterial)
        self.connect(self.actionGris,  SIGNAL("triggered()"), self.changeMaterial)
        self.connect(self.actionBleu,  SIGNAL("triggered()"), self.changeMaterial)
        self.connect(self.actionNoir,  SIGNAL("triggered()"), self.changeMaterial)

        #corrections affichage du pupitre
        self.connect(self.tabWidget, SIGNAL("currentChanged(int)"), self.resizeShell)
        self.connect(self.tabWidget, SIGNAL("currentChanged(int)"), self.stopSimu)

        #sliders des membres du robot
        for a in self.sliders:
            self.connect(a, SIGNAL("valueChanged (int)"), self.motor)

        #correction affichage widgets sur la réorganisation des widgets
        self.connect(self.splitter, SIGNAL("splitterMoved (int,int)"), self.resizeEvent)
        self.connect(self.splitterHB, SIGNAL("splitterMoved (int,int)"), self.resizeEvent)

        #Changement couleur des yeux
        self.connect(self.pushButtonChangeColors, SIGNAL("released ()"), self.changeColors)
        self.connect(self.pushButtonStopLights, SIGNAL("released ()"), self.stopLights)
        self.connect(self.checkBoxSelectAll, SIGNAL("stateChanged (int)"), self.selectAll)

        #led sliders     spins
        ledsSpins=[self.spinBoxRouge,self.spinBoxVert,self.spinBoxBleu]
        ledsSliders=[self.horizontalSliderRouge,self.horizontalSliderVert,self.horizontalSliderBleu]
        for a in ledsSpins:
            self.connect(a, SIGNAL("valueChanged (int)"), self.updateLedsSliders)
        for a in ledsSliders:
            self.connect(a, SIGNAL("valueChanged (int)"), self.updateLedsSpins)

        #Boutons de reset des moteurs
        for a in self.targets.keys():
            self.connect(a, SIGNAL("pressed()"), self.armReset)
            self.connect(a, SIGNAL("released()"), self.reset)

        #Reinitialisation Position Nao
        self.connect( self.actionInitPosition, SIGNAL("triggered()"), self.resetAll)

        self.connect( self.actionAfficherPosition, SIGNAL("triggered()"), self.afficherPosition)

        self.connect(self.thread, SIGNAL("finished ()"), self.finishCode)
        self.connect(self.thread_code, SIGNAL("finished ()"), self.finishCode)

        ### EVENEMENTIEL
        self.connect(self.pushButtonValidSpeak, SIGNAL("released()"), self.speakToRobot)
        self.connect(self.tabWidget, SIGNAL("currentChanged (int)"), self.protectRunning)
        self.connect(self.lineEditSpeak, SIGNAL("returnPressed ()"), self.speakToRobot)
        self.connect(self.lineEditObjet, SIGNAL("returnPressed ()"), self.objetToRobot)
        self.connect(self.pushButtonObjet, SIGNAL("released()"), self.objetToRobot)

        self.connect(self.pushButtonReconnaitre, SIGNAL("released()"), self.recognizeObjet)

        for a in self.touchSensors:
            self.connect(a, SIGNAL("pressed()"), self.armTouch)
            self.connect(a, SIGNAL("released()"), self.touch)

    ####### Main prog --------------------------------------------------------------------- #############

    def afficherPosition(self):
        line = ""
        for a in range(14):
            line+=str(a)+" : "+str(self.sliders[a].value())+"\n"
        self.afficher(line)

    def relaunch(self):
        global Global_repeat
        Global_repeat = True
        self.close()

    def setFullScreenOn(self):
        self.menuBarNaoSimulator.hide()
        self.toolBarNaoSimulator.hide()

        fenX=self.centralwidget.width()
        fenY=self.centralwidget.height()
        sizes=[]
        sizes.append(0);
        sizes.append(fenX);
        self.splitter.setSizes(sizes)
        sizes=[]
        sizes.append(fenY);
        sizes.append(0);
        self.splitterHB.setSizes(sizes)
        self.resizeEvent(0)

        self.showFullScreen()


    def setFullScreenOff(self):
        self.menuBarNaoSimulator.show()
        self.toolBarNaoSimulator.show()
        self.initPupitre()
        self.showNormal()


    def keyPressEvent (self, key_e):
        if (self.Viewer3DWidget.inFullscreen) and key_e.key()==Qt.Key_Escape:
            self.Viewer3DWidget.inFullscreen=False
            self.setFullScreenOff()
        if key_e.key()==Qt.Key_F5 and (not self.thread_code.isRunning()):
            self.run()

    def protectRunning(self):
        pass

    def speakToRobot(self):
        if self.thread_code.isRunning():
            if str(self.lineEditSpeak.text()) != "":
                ALProxy.eventCall( "onWordDetected",(str(self.lineEditSpeak.text()),100) )
                if ALProxy.eventCall( "onWordRecognized",(str(self.lineEditSpeak.text()),100) ):
                    self.lineEditSpeak.clear()

    def objetToRobot(self):
        if str(self.lineEditObjet.text()) != "":
            self.comboBox.addItem( str(self.lineEditObjet.text()) )
            self.lineEditObjet.clear()

    def recognizeObjet(self):
        if self.thread_code.isRunning():
            name=str(self.comboBox.currentText())
            if  name != "":
                #print  str(self.comboBox.currentText())
                ALProxy.eventCall( "onFaceDetected", (name, 100) )
                ALProxy.eventCall( "onPictureDetected", (name, "face", 100, 100) )

    def hasChanged(self):
        """
        Permet de savoir quel moteur a été bougé
        """
        old=self.valueList[:]
        for a in range(len(self.sliders)):
            self.valueList[a]=self.sliders[a].value()
            if self.valueList[a]!=old[a]:
                return a
        return -1

    def updateSliders(self):
        """
        Permet de mettre à jour les sliders selon leur valeur.
        """
        sliderEq = ALProxy.getKeys()
        for a in range(len(sliderEq)):
            #2 slidereq hanche = 1 slider
            if (a in [8,14]):
                self.sliders[a].setValue(self.virtualNao.getMembre(sliderEq[a][:-1]).getPercentFromAxis(1))
                continue
            #print a
            self.sliders[a].setValue(self.virtualNao.getMembre(sliderEq[a][:-1]).getPercentFromAxis(self.sliderAxis[a]))

    def printState(self):
        """
        debug
        """
        sliderEq = ALProxy.getKeys()
        for a in range(len(self.sliders)):
            print self.sliders[a].value(),sliderEq[a]
        for a in self.virtualNao.getMembreKeys():
            print a, self.virtualNao.getMembre(a).getPercentFromAxis(0),self.virtualNao.getMembre(a).getPercentFromAxis(1),self.virtualNao.getMembre(a).getPercentFromAxis(2)

    def armTouch(self):
        """
        Pour l'utilisation des event touch
        """
        if self.thread_code.isRunning():
            for a in range(len(self.touchSensors)):
                if self.touchSensors[a].isDown():
                    self.touchSensor=a
                    ALProxy.eventCall( "onTactileDetected", (self.touchSensor, 1) )
                    return

    def touch(self):
        """
        Call event for
        """
        #location, state
        if self.thread_code.isRunning():
            ALProxy.eventCall( "onTactileDetected", (self.touchSensor, 0) )


    def armReset(self):
        """
        Pour l'utilisation de reset
        """
        for a in self.targets.keys():
            if a.isDown():
                self.target=a
                return

    ## Reset by pushing button name of the sliders...
    def reset(self):
        """
        Replace le moteur d'un membre (target) à son angle 0
        """
        if self.target:
            #si plusieurs axes a reset en meme tps (biceps)
            if type("a")!=type(self.targets[self.target]):
                for a in self.targets[self.target]:
                    self.virtualNao.getMembre(a).rotate=[0,0,0]
            else:
                self.virtualNao.getMembre(self.targets[self.target]).rotate=[0,0,0]
            self.running=True
            self.updateSliders()

            self.Viewer3DWidget.update()
            self.running=False
            # maj slider


    def resetAll(self):
        for a in self.virtualNao.getMembreKeys():
            self.virtualNao.getMembre(a).rotate=[0,0,0]
            # maj slider
        #self.updateSliders()
        self.Viewer3DWidget.update()

    ############################## MOTEUR #########################

    def motor(self):
        """
        Modifie l'angle des moteurs a partir de ceux qui ont été changé.
        Affiche la valeur de l'angle actuel dans le ToolTip
        """
        #récupère le moteur qui a bougé
        if self.thread_code.isRunning():
             return
        nb=self.hasChanged()

        if not self.boolOmbre:
            self.boolOmbre= not self.boolOmbre
            return

        sliderEq = ALProxy.getKeys()
        if self.sliderAxis[nb]!=3:
            #maj le bon trouvé
            self.virtualNao.getMembre(sliderEq[nb][:-1]).setAngleFromPercent(self.sliderAxis[nb],self.sliders[nb].value())
            QToolTip.showText(self.cursor.pos(),str(self.sliders[nb].value()))
        else :
            self.virtualNao.getMembre("hancheD").setAngleFromPercentList([self.horizontalSliderHanche15.value(),0,self.horizontalSliderHanche15.value()])
            self.virtualNao.getMembre("hancheG").setAngleFromPercentList([self.horizontalSliderHanche15.value(),0,self.horizontalSliderHanche15.value()])
            QToolTip.showText(self.cursor.pos(),str(self.horizontalSliderHanche15.value()))

        self.virtualNao.getMembre("doigt3D").setAngleFromPercent(0,100-self.horizontalSliderDoigtsD0.value())
        self.virtualNao.getMembre("doigt2D").setAngleFromPercent(0,100-self.horizontalSliderDoigtsD0.value())
        self.virtualNao.getMembre("doigt1D").setAngleFromPercent(0,100)#=fixe

        self.virtualNao.getMembre("doigt3G").setAngleFromPercent(0,100-self.horizontalSliderDoigtsG0.value())
        self.virtualNao.getMembre("doigt2G").setAngleFromPercent(0,100-self.horizontalSliderDoigtsG0.value())
        self.virtualNao.getMembre("doigt1G").setAngleFromPercent(0,100)#=fixe

        self.updatePhysics()
        self.Viewer3DWidget.update()


    def updatePhysics(self):
        """
        Modifie l'angle des moteurs qui sont dépendants d'autres : collisions physiques + tete
        """
        self.virtualNao.getMembre("epauleG").rotate[0]=self.virtualNao.getMembre("bicepsG").rotate[0]
        self.virtualNao.getMembre("epauleD").rotate[0]=self.virtualNao.getMembre("bicepsD").rotate[0]
        if (self.virtualNao.getMembre("bicepsG").rotate[2]<30):
            self.virtualNao.getMembre("epauleG").rotate[2]=self.virtualNao.getMembre("bicepsG").rotate[2]
##        if (self.virtualNao.getMembre("bicepsG").rotate[0]>20):
##            self.virtualNao.getMembre("epauleG").rotate[2]=18
        if (self.virtualNao.getMembre("bicepsD").rotate[2]<30):
            self.virtualNao.getMembre("epauleD").rotate[2]=self.virtualNao.getMembre("bicepsD").rotate[2]
##        if (self.virtualNao.getMembre("bicepsD").rotate[0]<20):
##            self.virtualNao.getMembre("epauleD").rotate[2]=18
        self.virtualNao.getMembre("epauleBicepsG").rotate[0]=self.virtualNao.getMembre("bicepsG").rotate[0]
        self.virtualNao.getMembre("epauleBicepsD").rotate[0]=self.virtualNao.getMembre("bicepsD").rotate[0]

        #correction affichage
        self.virtualNao.getMembre("teteD").rotate[0]=self.virtualNao.getMembre("teteG").rotate[0]
        self.virtualNao.getMembre("teteD").rotate[2]=-self.virtualNao.getMembre("teteG").rotate[2]

        self.Viewer3DWidget.update()

    def changeMaterial(self):
        #print "changing"
        for a in self.materials:
            #print a,self.oldMaterial
            if a!=self.oldMaterial and a.isChecked():
                self.oldMaterial.setChecked(False)
                self.oldMaterial=a
                #print self.eqMtlNames[a],Objet3D.materiaux['Material.002\n'].getColor()
                Objet3D.materiaux['Material.002'].setColor(self.eqMtlNames[a])
                #print self.eqMtlNames[a],Objet3D.materiaux['Material.002\n'].getColor()
                break
        self.Viewer3DWidget.update()
        return

    def applyColor(self):
        dictColor = self.colors.getApplied()
        if "wallpaper" in dictColor.keys():
            self.Viewer3DWidget.background = dictColor["wallpaper"]
        #etc..
        if "background" in dictColor.keys():
            p = self.palette()
            p.setColor( self.backgroundRole(), dictColor["background"])
            self.setPalette(p)

    #######################" LEDS ####################

    def changeColors(self,color=[]):
        """
        Met à jour les parties des yeux sélectionnés avec la couleur choisie.
        """
        eyes=self.getSelectedEyes()
        self.virtualNao.setEyesColoring(self.horizontalSliderRouge.value(),
                                        self.horizontalSliderVert.value(),
                                        self.horizontalSliderBleu.value())
        self.virtualNao.colorEyes(eyes)
        self.Viewer3DWidget.update()

    def stopLights(self):
        """
        remet les leds en gris
        """
        eyes=self.getSelectedEyes()
        self.virtualNao.setEyes(False,eyes)
        self.Viewer3DWidget.update()

    def getSelectedEyes(self):
        """
        Retourne la liste du nom des yeux sélectionnées.
        """
        ret=[]
        gd=(self.checkBoxCoteGauche.isChecked(),self.checkBoxCoteDroit.isChecked())
        lettre="GD"
        for x in range(2):
            if gd[x] :
                for a in self.checkLedBoxes.keys():
                    if a.isChecked():
                        ret.append(self.checkLedBoxes[a]+lettre[x])
        return ret

    def updateLedsSliders(self):
        ledsSpins=[self.spinBoxRouge,self.spinBoxVert,self.spinBoxBleu]
        ledsSliders=[self.horizontalSliderRouge,self.horizontalSliderVert,self.horizontalSliderBleu]
        for a in range(3):
            ledsSliders[a].setValue(ledsSpins[a].value())

    def updateLedsSpins(self):
        ledsSpins=[self.spinBoxRouge,self.spinBoxVert,self.spinBoxBleu]
        ledsSliders=[self.horizontalSliderRouge,self.horizontalSliderVert,self.horizontalSliderBleu]
        for a in range(3):
            ledsSpins[a].setValue(ledsSliders[a].value())

    def selectAll(self):
        """
        coche toutes les cases pour les leds.
        """
        for a in self.checkLedBoxes.keys()+[self.checkBoxCoteGauche,self.checkBoxCoteDroit]:
            a.setChecked(self.selectedAll)
        self.selectedAll = not self.selectedAll

    ###################################" JAMBes ##########

    def showLegs(self):
        """
        Affiche les jambes pour le H25
        """
        ALProxy.setType("H25")
        self.setName("H25")
        for widget in self.differenceRobots:
            widget.setEnabled(True)

        if self.tabWidget2.count()==self.initTabLength-1:
            self.Viewer3DWidget.unmiddle()
            if not "hancheSD" in self.virtualNao.getMembre("torseSD").underObjects.keys():
                self.virtualNao.getMembre("torseSD").underObjects["hancheD"]=self.pop[0]
                self.virtualNao.getMembre("torseSG").underObjects["hancheG"]=self.pop[1]
            self.virtualNao.changeLegs()
            self.Viewer3DWidget.update()
            self.tabWidget2.insertTab(1,self.tab2,"Bas du corps")

    def showLegsH21(self):
        """
        Affiche les jambes pour le H21
        """
        ALProxy.setType("H21")
        self.setName("H21")
        for widget in self.differenceRobots:
            widget.setEnabled(False)

        if self.tabWidget2.count()==self.initTabLength-1:
            self.Viewer3DWidget.unmiddle()
            if not "hancheSD" in self.virtualNao.getMembre("torseSD").underObjects.keys():
                self.virtualNao.getMembre("torseSD").underObjects["hancheD"]=self.pop[0]
                self.virtualNao.getMembre("torseSG").underObjects["hancheG"]=self.pop[1]
            self.virtualNao.changeLegs()
            self.Viewer3DWidget.update()
            self.tabWidget2.insertTab(1,self.tab2,"Bas du corps")

    def hideLegs(self):
        """
        Cache les jambes pour le T14
        """
        ALProxy.setType("T14")
        self.setName("T14")
        for widget in self.differenceRobots:
            widget.setEnabled(True)

        if self.tabWidget2.count()==self.initTabLength:
            self.Viewer3DWidget.middle()
            self.tabWidget2.removeTab(1)

            if "hancheD" in self.virtualNao.getMembre("torseSD").underObjects.keys():
                self.pop[0]=self.virtualNao.getMembre("torseSD").underObjects.pop("hancheD")
                self.pop[1]=self.virtualNao.getMembre("torseSG").underObjects.pop("hancheG")
            self.virtualNao.changeLegs()
            self.Viewer3DWidget.update()

    def initName(self):
        self.buttonTexts = []
        self.buttonNames = [self.pushButtonTeteGD,self.pushButtonTeteHB,
                            self.pushButtonBicepsG,self.pushButtonCoudeG,self.pushButtonMainG,self.pushButtonDoigtsG,
                            self.pushButtonHanche,
                            self.pushButtonCuisseG, self.pushButtonMolletG, self.pushButtonPiedG,
                            self.pushButtonCuisseD, self.pushButtonMolletD, self.pushButtonPiedD,
                            self.pushButtonBicepsD,self.pushButtonCoudeD,self.pushButtonMainD,self.pushButtonDoigtsD
                            ]
        self.buttonNamesY = [self.pushButtonBicepsG,self.pushButtonCoudeG,
                            self.pushButtonCuisseG, self.pushButtonPiedG,
                            self.pushButtonCuisseD, self.pushButtonPiedD,
                            self.pushButtonBicepsD,self.pushButtonCoudeD]
        for a in self.buttonNames:
            self.buttonTexts.append(unicode(a.text()))

        self.numberType={"T14":[0,1,
                               2,3,4,5,6,7,
                               -1,-1,-1,-1,-1,-1,
                               -1,-1,-1,-1,-1,
                               8,9,10,11,12,13],
                        "H21":[0,1,
                               2,3,4,5,-1,-1,
                               6,7,8,9,10,11,
                               12,13,14,15,16,17,
                               18,19,20,21,-1,-1],
                       "H25":range(26)}

    def setName(self, type = "T14"):
        numbers = self.numberType[type]
        iNumberButton = 0
        iNumberEngine = 0
        while True:
            button = self.buttonNames[iNumberButton]
            text = self.buttonTexts[iNumberButton]
            number = numbers[iNumberEngine]
            button.setText(text.replace("XX",str(number)))
            iNumberEngine += 1
            if button in self.buttonNamesY:
                text = unicode(button.text())
                number = numbers[iNumberEngine]
                button.setText(text.replace("YY",str(number)))
                iNumberEngine += 1
            iNumberButton+=1

            if (iNumberEngine >= len(self.numberType[type])) or (iNumberButton >= len(self.buttonNames)):
                break

    ## On doit implémenter le resizement des widgets ajoutés dans le code
    def resizeViewer3DWidget(self):
        """
        Gère la façon dont se resize la vue 3D
        """
        x=self.widgetGLContainer.property("geometry").width()
        y=self.widgetGLContainer.property("geometry").height()
        g=QRect(0,0,x,y)
        self.Viewer3DWidget.setProperty("geometry",g)

    def resizeShell(self):
        """
        Gère la façon dont se resize la console
        """
        x=self.widgetShellContainer.property("geometry").width()
        y=self.widgetShellContainer.property("geometry").height()
        self.textBrowserConsole.setMaximumSize(x,y)
        self.textBrowserConsole.setMinimumSize(x,y)

    def resizeEvent(self,r):
        """
        Appelle les resizers.
        """
        self.resizeViewer3DWidget()
        self.resizeShell()

    ##################################### RUN CODE ###############################

    def animate(self):
        #dt=0.05#self.oldTime-time.time()
        dt=self.oldTime-time.time()
        #if dt>0.05:dt=0.05
        if 1:dt=0.05
        self.oldTime=time.time()
        self.Viewer3DWidget.updateDt(dt)
        self.virtualNao.updateSpeaking(dt)

        if self.virtualNao.finishedSpeaking and self.thread_code.isFinished():
            self.timer.stop()
            self.virtualNao.resetSpeaking()

    def stopSimu(self):
        """
        Assure l'arrêt de la simulation car les sliders ne peuvent
        pas changer d'état pendant une simulation.
        """
        if self.tabWidget.currentIndex()==0:
            self.updateSliders()
            self.stop()

    def stop(self):
        """
        Stoppe rien du tout.
        """
        pass

    def afficher(self,text="blarg"):
        self.textBrowserConsole.write('\n'+text)

    def run(self):
        self.running=self.thread_code.isRunning()
        if (not self.running):
            print "launch"
            self.currentIndex = self.tabWidget2.currentIndex()
            #Démarrage du chrono pour le framerate seulement
            self.timer.start(40)
            self.actionNaoT14.setEnabled(False)
            self.actionNaoH21.setEnabled(False)
            self.actionNaoH25.setEnabled(False)
            self.actionInitPosition.setEnabled(False)
            for x in range(self.tabWidget2.count()-2):
                self.tabWidget2.setTabEnabled(x,False)
            self.running=True
            self.runCode()
        else :
            print "running"

    def runCode(self):
        """
        Démarre le code écrit dans l'éditeur.
        """
        self.tabWidget.setCurrentIndex(0)

        if not DEBUGOUT :
            sys.stdout = self.printer
            if not DEBUGERR:
                sys.stderr = self.printer

        if self.runReal:
            try:
                import naoqi
            except:
                a=QMessageBox()
                s=u"Erreur, NaoQI pour Python n'est pas installé sur cet ordinateur"
                a.information(self,u"Erreur à la connexion au robot",s)
                return

        if self.runReal!=self.actionRunReal.isChecked():
            self.changeReseau()

        p=self.textEdit.toPlainText()#.toUtf8()
        t=Decoder().decode(p)
        t=p#.toUtf8()
        if ENABLE_SPACES_TO_TAB:
            t=t.replace("    ","\t")

        if self.runReal:
            realT=t[:]
            a,b=self.config.getProxy()
            h=str("NaoAPI("+'"'+str(a)+'"'+","+str(b)+")")
            realT = realT.replace("NaoAPI()",h)
        t=t.replace("from Nao import","from NaoVirtual import")

        #try:
        if self.runReal:
            self.thread.setCode(realT)
            self.thread.start()
            time.sleep(1.5)
        self.thread_code.setCode(unicode(t))
        self.thread_code.start()

        return

    def finishCode(self):
        if self.runReal:
            if not self.thread_both_terminated:
                self.thread_both_terminated=True
                return
            else :
                self.thread_both_terminated=False
        #self.thread.stop()
        self.stop()
        self.resizeShell()
        self.textBrowserConsole.finish()
        self.tabWidget.setTabEnabled(0,True)

        self.setIO()
        self.tabWidget.setCurrentIndex(0)
        self.running=False
        #self.printState()
        for x in range(self.tabWidget2.count()-1):
            self.tabWidget2.setTabEnabled(x,True)
        self.tabWidget2.setCurrentIndex (self.currentIndex)
        self.actionNaoT14.setEnabled(True)
        self.actionNaoH21.setEnabled(True)
        self.actionNaoH25.setEnabled(True)
        self.actionInitPosition.setEnabled(True)

    def changeReseau(self):
        """

        """
        self.runReal=self.actionRunReal.isChecked()
        if self.runReal:
            sys.path.remove(os.getcwd())
            os.chdir("nao_api")
            sys.path.append(os.getcwd())
        else :
            sys.path.remove(os.getcwd())
            os.chdir("..")
            sys.path.append(os.getcwd())

    def customEvent(self, e):
        e.callback()



    # Printer for shell
class Printer(QObject):

        def __init__(self, parent=None):
            super(Printer, self).__init__()
            self.text = ""
            self.target = None
            self.lastTime = time.time()
            self.alert = False
            self.alertCount = 30
            self.alertTime = 8
        def write(self, text):
            if self.alert :
                if time.time()-self.lastTime > 0.5:
                    self.text = text
                    CallbackEvent.post_to(self.target, self.target.afficher, self.text)
                    self.alertTime -= (time.time()-self.lastTime)
                    self.lastTime = time.time()
                if self.alertTime < 0 :
                    self.alert = False
                    self.alertTime = 8
                    CallbackEvent.post_to(self.target, self.target.afficher, "\nAlert : end skipping print frames !\n")
            else :
                self.text = text
                CallbackEvent.post_to(self.target, self.target.afficher, self.text)
                if time.time()-self.lastTime < 0.01:
                    self.alertCount -= 1
                if self.alertCount < 0:
                    self.alert = True
                    self.alertCount = 30
                    CallbackEvent.post_to(self.target, self.target.afficher, "\nAlert : begin skipping print frames !\n")
                else :
                    self.alertCount = 30
                self.lastTime = time.time()


    # Just some random worker
class Worker(QtCore.QThread):

        def __init__(self, parent=None):
            super(Worker, self).__init__(parent)
            self.__quitting = Event()
            self.code=""

        def setCode(self, code):
            self.code = code

        def run(self):
                # And lets just have one happen from this worker thread too
#                 if self.code.strip()!="":
#                     i=0
#                     line = self.code.splitlines()[i]
#                     while (i < len(self.code.splitlines())-1 ):
#                         if line.strip()=="":
#                             i+=1
#                             line = self.code.splitlines()[i]
#                             continue
#                         if line[-1]==":":
#                             bloc=""
#                             while(('\t' in self.code.splitlines()[i+1]) and (i < len(self.code.splitlines())-1 )):
#                                 i+=1
#                                 line = self.code.splitlines()[i]
#                                 bloc+=line+"\n"
#                             exec(bloc)
#                         else :
#                             exec(line)
#                         if self.__quitting.is_set():
#                             return
#                         i+=1
#                         line = self.code.splitlines()[i]
#                     exec(self.code.splitlines()[-1])
            if self.code.strip()!="":
                exec(self.code,{})

        def stop(self):
            self.__quitting.set()
            self.wait()

from threaders import *

a = QApplication(sys.argv)
f = MainWindow()
r = a.exec_()

sys.stdout = Ssaveout
sys.stderr = Ssaveerr

if Global_repeat:
    #os.execv("launch.bat", ['launch.bat'])
    pass
f=None
