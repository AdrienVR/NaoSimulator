# -*- coding: utf-8 -*-
import sys, time
sys.path.append("..")
from nao_training.NaoStructure import Nao;
from nao_training.NaoEvent import EventManagerAbstractModule;


class NaoControle:
    
    def __init__(self, nao):
        self.__nao = nao;

    def stop(self):
        self.__nao.stop();

    ################################################################
    #       Fonctions permettant de manipuler la voix de Nao       #
    ################################################################

    #test OK
    def dire(self, texte):
        self.__nao.getVoice().say(texte);

    #test OK
    def reglerVolume(self, volume):
        self.__nao.getVoice().setVolume(volume);

    #test OK
    def reglerLangageActuel(self, langage):
        self.__nao.getVoice().setLanguage(langage);

    #test OK
    def recupererVolume(self):
        return self.__nao.getVoice().getVolume();

    #test OK
    def recupererLangageActuel(self):
        return self.__nao.getVoice().getLanguage();

    #test OK
    def recupererLangagesDisponibles(self):
        return self.__nao.getVoice().getAvailableLanguages();

    #test OK
    def afficherLangagesDisponibles(self):
        for language in self.__nao.getVoice().getAvailableLanguages():
            print language;

    ################################################################
    #     Fonctions permettant de manipuler les moteurs de Nao     #
    ################################################################

    #test OK
    def afficherNumeroMoteurs(self):
        #self.__nao.getMotors().displayMotorsNumber(); #TODO à enlever après les tests
        joints = self.__nao.getMotors().getJointNames();
        frenchMotors = self.__recupererNomMoteurs();
        for i in range(len(joints)):
            numeroMoteur = joints[i];
            label = "Moteur %s" %(i);
            label = self.__nao.getMotors().addSpaces(label, 9);
            frenchMotorName = "%s : %s" %(label, frenchMotors[numeroMoteur]);
            print frenchMotorName;

    #test OK
    def afficherPositionMoteurs(self):
        joints = self.__nao.getMotors().getJointNames();
        for i in range(len(joints)):
            normPosition = self.recupererPositionMoteur(i);
            joint = "Moteur %s" %(i);
            joint = self.__nao.getMotors().addSpaces(joint, 9);
            data = "%s : %s" %(joint, normPosition);
            print data
    #test OK
    def bloquerTousMoteurs(self):
        self.__nao.getMotors().setStiffnesses(1);

    #test OK
    def bloquerMoteur(self, numeroMoteur):
        self.__nao.getMotors().setStiffness(numeroMoteur, 1);

    #test OK
    def libererTousMoteurs(self):
        self.__nao.getMotors().setStiffnesses(0);

    #test OK
    def libererMoteur(self, numeroMoteur):
        self.__nao.getMotors().setStiffness(numeroMoteur, 0);

    #test OK
    def bougerMoteur(self, numeroMoteur, position, temps):
        #position est une position normalisée entre 0 et 1.
        #il faut récupérer la vraie valeur.
        minPosition, maxPosition = self.__recupererMinMaxMoteur(numeroMoteur);
        vraiPosition = minPosition;
        if position!=0:
            rate = 100 / float(position);
            vraiPosition = (maxPosition - minPosition) / rate + minPosition;
        print "Vrai position de %s : %s" %(position, vraiPosition); #TODO à enlever après les tests
        self.__nao.getMotors().setMotorAngle(numeroMoteur, vraiPosition, temps);

    #test OK
    def recupererPositionMoteur(self, numeroMoteur):
        minPosition, maxPosition = self.__recupererMinMaxMoteur(numeroMoteur);
        motorAngle = self.__nao.getMotors().getMotorAngle(numeroMoteur);
        normPosition = 0;
        denominateur = motorAngle-minPosition;
        if denominateur !=0:
            rate = (maxPosition - minPosition) /(denominateur);
            normPosition = 100/rate;
        #return normPosition, minPosition, maxPosition, motorAngle;
        return normPosition; #TODO à remettre après les tests

    #test OK
    def effacerAnimationMoteur(self):
        self.__nao.getMotors().resetAnimation();

    #test OK
    def ajouterMouvementAnimationMoteur(self, numeroMoteur, position, temps):
        minPosition, maxPosition = self.__recupererMinMaxMoteur(numeroMoteur);
        vraiPosition = minPosition;
        if position!=0:
            rate = 100 / float(position);
            vraiPosition = (maxPosition - minPosition) / rate + minPosition;
        self.__nao.getMotors().addMotionAnimation(numeroMoteur, vraiPosition, temps);

    #test OK
    def jouerAnimationMoteur(self):
        self.__nao.getMotors().playAnimation();

    #test OK
    #Cette fonction contient une grosse partie de la fonction recupererPositionMoteur
    def afficherAnimationMoteur(self):
        names, angles, times = self.__nao.getMotors().getAnimationData();
        joints = self.__nao.getMotors().getJointNames();

        for i in range(len(names)):
            motorNumber = joints.index(names[i]);
            print "Moteur : %s" %(motorNumber);
            for j in range(len(angles[i])):
                minPosition, maxPosition = self.__recupererMinMaxMoteur(motorNumber);
                motorAngle = angles[i][j];
                normPosition = 0;
                denominateur = motorAngle-minPosition;
                if denominateur !=0:
                    rate = (maxPosition - minPosition) /(denominateur);
                    normPosition = 100/rate;
                string = "    position : %s" %(normPosition);
                string = self.__nao.getMotors().addSpaces(string, 20); 
                print string,"- temps :",times[i][j];

    #test OK
    def __recupererMinMaxMoteur(self, numeroMoteur):
        minPosition = self.__nao.getMotors().getMinAngle(numeroMoteur);
        maxPosition = self.__nao.getMotors().getMaxAngle(numeroMoteur);
        return minPosition, maxPosition;

    #test OK
    def __recupererNomMoteurs(self):
        moteurs = {};

        availableMotors = {
            "HeadYaw" : "TETE DROITE GAUCHE",
            "HeadPitch" : "TETE HAUT BAS",
            "LShoulderPitch" : "EPAULE GAUCHE HAUT BAS",
            "RShoulderPitch" : "EPAULE DROITE HAUT BAS",
            "LShoulderRoll" : "EPAULE GAUCHE ROTATION DROITE GAUCHE",
            "RShoulderRoll" : "EPAULE DROITE ROTATION DROITE GAUCHE",
            "LElbowYaw" : "COUDE GAUCHE ROTATION GAUCHE DROITE",
            "RElbowYaw" : "COUDE DROITE ROTATION GAUCHE DROITE",
            "LElbowRoll" : "COUDE GAUCHE ROTATION HAUT BAS",
            "RElbowRoll" : "COUDE DROITE ROTATION BAS HAUT",
            "LWristYaw" : "POIGNET GAUCHE ROTATION GAUCHE DROITE",
            "RWristYaw" : "POIGNET DROITE ROTATION GAUCHE DROITE",
            "LHand" : "MAIN GAUCHE FERMEE OUVERTE",             
            "RHand" : "MAIN DROITE FERMEE OUVERTE",
            "LHipYawPitch" : "HANCHE_GAUCHE",
            "RHipYawPitch" : "HANCHE_DROITE",
            "LHipRoll" : "HANCHE_GAUCHE_ROTATION",
            "RHipRoll" : "HANCHE_DROITE_ROTATION",
            "LHipPitch" : "HANCHE_GAUCHE_HAUT_BAS",
            "RHipPitch" : "HANCHE_DROITE_HAUT_BAS",
            "LKneePitch" : "GENOU_GAUCHE_HAUT_BAS",
            "RKneePitch" : "GENOU_DROITE_HAUT_BAS",
            "LAnklePitch" : "CHEVILLE_GAUCHE_HAUT_BAS",
            "RAnklePitch" : "CHEVILLE_DROITE_HAUT_BAS",
            "LAnkleRoll" : "CHEVILLE_GAUCHE_ROTATION",
            "RAnkleRoll" : "CHEVILLE_DROITE_ROTATION"
            }

        for motor in self.__nao.getMotors().getJointNames():
            moteur = availableMotors.get(motor);

            moteurs[motor] = moteur;

        return moteurs;

    ################################################################
    #       Fonctions permettant de manipuler les leds de Nao      #
    ################################################################

    #test OK
    #doublon avec afficherNumeroMoteurs
    def afficherNumeroLeds(self):
        leds = self.__nao.getLeds().getLedsNames();
        frenchLeds = self.__recupererNomLeds();
        for i in range(len(leds)):
            numeroLed = leds[i];
            label = "Led %s" %(i);
            label = self.__nao.getLeds().addSpaces(label, 6);
            frenchLedName = "%s : %s" %(label, frenchLeds[numeroLed]);
            print frenchLedName;

    #test OK
    def allumerLeds(self):
        self.__nao.getLeds().allLedsOn();
    #test OK
    def allumerOeilDroite(self):
        self.__nao.getLeds().rightLedsOn();

    #test OK
    def allumerOeilGauche(self):
        self.__nao.getLeds().leftLedsOn();

    def allumerLed(self, numeroLed):
        self.__nao.getLeds().setIntensity(numeroLed, 1);
        
    #test OK
    def eteindreLeds(self):
        self.__nao.getLeds().allLedsOff();

    #test OK
    def eteindreOeilDroite(self):
        self.__nao.getLeds().rightLedsOff();

    #test OK
    def eteindreOeilGauche(self):
        self.__nao.getLeds().leftLedsOff();

    #test OK
    def eteindreLed(self, numeroLed):
        self.__nao.getLeds().setIntensity(numeroLed, 0);

    #test OK
    def estAllume(self, numeroLed):
        estAllume = False;
        
        tabIntensity = self.__nao.getLeds().getIntensity(numeroLed);
        if len(tabIntensity) == 3:
            if tabIntensity[0]>0.06 and tabIntensity[1]>0.06 and tabIntensity[2]>0.06 :
                estAllume = True;
        
        return estAllume;

    #test OK
    def reglerCouleur(self, numeroLed, rouge, vert, bleu):
        self.__nao.getLeds().setColor(numeroLed, rouge, vert, bleu);

    #test OK
    def recupererCouleur(self, numeroLed):
        return self.__nao.getLeds().getColor(numeroLed);

    #test OK
    def apparitionCouleur(self, numeroLed, rouge, vert, bleu, temps):
        self.__nao.getLeds().fadeColor(numeroLed, rouge, vert, bleu, temps);

    
    def effacerAnimationLed(self):
        self.__nao.getLeds().resetAnimation();


    def ajouterAnimationLed(self, numeroLed, rouge, vert, bleu, temps):
        self.__nao.getLeds().addLedAnimation(numeroLed, rouge, vert, bleu, temps);


    def jouerAnimationLed(self):
        self.__nao.getLeds().playAnimation();


    def afficherAnimationLed(self):
        self.__nao.getLeds().displayAnimation("Led", "Couleur", "Temps", 15);
                
    def __recupererIntensite(self, numeroLed):
        return self.__nao.getLeds().getIntensity(numeroLed);

    #test OK
    def __recupererNomLeds(self):

        leds = {
            "RightFaceLed1" : "OEIL DROIT 1",
            "RightFaceLed2" : "OEIL DROIT 2",
            "RightFaceLed3" : "OEIL DROIT 3",
            "RightFaceLed4" : "OEIL DROIT 4",
            "RightFaceLed5" : "OEIL DROIT 5",
            "RightFaceLed6" : "OEIL DROIT 6",
            "RightFaceLed7" : "OEIL DROIT 7",
            "RightFaceLed8" : "OEIL DROIT 8",
            "LeftFaceLed1" : "OEIL GAUCHE 1",
            "LeftFaceLed2" : "OEIL GAUCHE 2",
            "LeftFaceLed3" : "OEIL GAUCHE 3",
            "LeftFaceLed4" : "OEIL GAUCHE 4",
            "LeftFaceLed5" : "OEIL GAUCHE 5",
            "LeftFaceLed6" : "OEIL GAUCHE 6",
            "LeftFaceLed7" : "OEIL GAUCHE 7",
            "LeftFaceLed8" : "OEIL GAUCHE 8"
            }

        return leds;

    ################################################################
    #     Fonction permettant de gérer la reconnaissance vocale    #
    ################################################################

    #test OK
    def attribuerVocabulaire(self, *args):
        vocabulaire = [];
        for arg in args:
            vocabulaire.append(arg);
        self.__nao.getSpeechReco().setPreciseVocabulary(vocabulaire);

    #test OK
    def recupererRecoLangagesDisponibles(self):
        return self.__nao.getSpeechReco().getAvailableLanguages();

    #test OK
    def afficherRecoLangagesDisponibles(self):
        languages = self.__nao.getSpeechReco().getAvailableLanguages();
        for language in languages:
            print language;
    #test OK
    def recupererRecoLangage(self):
        return self.__nao.getSpeechReco().getLanguage();

    #test OK
    def reglerRecoLangage(self, langage):
        self.__nao.getSpeechReco().setLanguage(langage);

    #test OK
    def demarrerReconnaissanceVocale(self):
        self.__nao.getSpeechReco().startSpeechRecognition();

    #test OK
    def arreterReconnaissanceVocale(self):
        print "ARRET RECONNAISSANCE VOCALE";
        self.__nao.getSpeechReco().stopSpeechRecognition();

    ################################################################
    #            Fonction permettant d'afficher la vidéo           #
    ################################################################

    #test OK
    def afficherVideo(self):
        print self.__nao.getVisualReco().displayVideo("Vue de Nao", "Nom du visage : ","Enregistrer");


    ################################################################
    #   Fonctions permettant de gérer la reconnaissance visuelle   #
    ################################################################

    #test OK
    def apprendreVisage(self):
        print "TEST";
        self.__nao.getVisualReco().learnFace("Enregistrer visage", "Nom du visage : ", "Enregistrer");

    #test OK
    def recupererNomVisages(self):
        return self.__nao.getVisualReco().getFaces();

    #test pas OK
    def supprimerVisage(self, nomVisage):
        return self.__nao.getVisualReco().removeFace(nomVisage);

    #test OK
    def supprimerTousVisages(self):
        return self.__nao.getVisualReco().removeAllFaces();

    #test OK
    def afficherVisages(self):
        self.__nao.getVisualReco().displayFaces();

    #test OK
    def apprendreObjet(self, nom, cote):
        self.__nao.getVisualReco().learnObject(nom, cote);

    #test OK
    def recupererNomObjets(self):
        return self.__nao.getVisualReco().getObjects();

    #test OK
    def supprimerObjet(self, nom, cote):
        self.__nao.getVisualReco().removeObject(nom, cote);

    #test OK
    def supprimerTousObjets(self):
        self.__nao.getVisualReco().removeAllObjects();

    #test OK
    def afficherObjets(self):
        self.__nao.getVisualReco().displayObjects();

    ################################################################
    #        Classe permettant de gérer les événéments de Nao      #
    ################################################################

class AbstractNaoEvenement(EventManagerAbstractModule):

    def __init__(self, name, memory, naoControle):
        EventManagerAbstractModule.__init__(self, name, memory);
        self.nao = naoControle;
        self.recoVocale= False
        self.motReconnu = ""
        self.tauxReconnaissance = 0.0
        self.recoVisage= False
        self.visageReconnu = ""
        self.recoObjet = False
        self.objetReconnu = ""
        self.tauxRessemblance = 0.0
        self.ratio = 0.0

    ####### FACE DETECTION #######

    #test OK
    def demarrerDetectionVisage(self):
        self.tauxReconnaissance = 0.0
        self.recoVisage= False
        self.visageReconnu = ""
        self.startFaceDetection();

    #test OK
    
    def traiterDetectionVisage(self, visage, tauxReco):
        pass;
    

    #test OK
    def _faceDetectedEvent(self, visage, tauxReco):
        self.tauxReconnaissance = tauxReco
        self.recoVisage= True
        self.visageReconnu = visage
        self.traiterDetectionVisage(visage, tauxReco);

    #test OK
    def arreterDetectionVisage(self):
        self.tauxReconnaissance = 0.0
        self.recoVisage= False
        self.visageReconnu = ""
        self.stopFaceDetection();

    ####### OBJET DETECTION #######

    #test OK
    def demarrerDetectionObjet(self):
        self.recoObjet = False
        self.objetReconnu = ""
        self.tauxRessemblance = 0.0
        self.ratio = 0.0
        self.startPictureDetection();

    #test OK
    
    def traiterDetectionObjet(self, nomObjet, coteObjet, ressemblance, ratio):
        pass;
    
    
    #test OK
    def _pictureDetectedEvent(self, objectName, objectSide, matching, ratio):
        self.recoObjet = True
        self.objetReconnu = objectName+" "+objectSide
        self.tauxRessemblance = matching
        self.ratio = ratio
        self.traiterDetectionObjet(objectName, objectSide, matching, ratio);

    #test OK
    def arreterDetectionObjet(self):
        self.recoObjet = False
        self.objetReconnu = ""
        self.tauxRessemblance = 0.0
        self.ratio = 0.0
        self.stopPictureDetection();

    ####### SPEECH DETECTION #######

    #test OK
    def demarrerDetectionParole(self):
        self.recoParole = False;
        self.startSpeechDetection();

    #test OK
    
    def traiterDetectionParole(self):
        pass;
    
    
    #test OK
    def _speechDetectedEvent(self):
        self.recoParole = True;
        self.traiterDetectionParole();

    #test OK
    def arreterDetectionParole(self):
        self.recoParole = False;
        self.stopSpeechDetection();

    ####### SPEECH RECOGNITION #######

    def demarrerReconnaissanceVocale(self):
        self.recoVocale= False
        self.motReconnu = ""
        self.tauxReconnaissance = 0.0
        self.startWordRecognition();

    
    def traiterReconnaissanceVocale(self, mot, tauxReco):
        pass;
    
    
    def _wordRecognizedEvent(self, word, rate):
        self.recoVocale= True
        self.motReconnu = word
        self.tauxReconnaissance = rate
        self.traiterReconnaissanceVocale(word, rate);

    def arreterReconnaissanceVocale(self):
        self.recoVocale= False
        self.motReconnu = ""
        self.tauxReconnaissance = 0.0
        self.stopWordRecognition();   

