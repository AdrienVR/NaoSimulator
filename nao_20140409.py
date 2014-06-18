# -*- coding: utf-8 -*-
import sys, time;

sys.path.insert(0,'/usr/lib/pynaoqi/')
sys.path.append("naoControle/naoTrainingJost");

from nao_training.NaoStructure import Nao;
from nao_training.NaoCommunication import NaoControle;
from nao_training.NaoCommunication import AbstractNaoEvenement;

address = "169.254.16.208"; #A VERIFIER
port = 9559;

naoRobot = Nao(address, port);
nao = NaoControle(naoRobot);
naoEvenement = AbstractNaoEvenement("naoEvenement", naoRobot.getMemory(), nao);

#DEBUT DE LA ZONE DE CODE DES ETUDIANTS
#A éxécuter en saisissant dans une console :
#python nao.py

#tests parole
nao.dire("bonjour")

#tests leds
nao.dire("Tests des leds. Regardez mes yeux.")
nao.allumerLeds()
for i in range(8):
	nao.eteindreLed(i)
	nao.eteindreLed(i+8)
	if i>0:
		nao.allumerLed(i-1)
		nao.allumerLed(i+7)
	time.sleep(0.5)

nao.allumerLed(i)
nao.allumerLed(i+8)


#tests moteur
#moteur 0 : tete droite gauche
#moteur 1 : tete haut bas

nao.dire("Tests des moteurs. Regardez ma tête.")
nao.bloquerMoteur(0)
nao.bloquerMoteur(1)

nao.bougerMoteur(0, 80, 2)
nao.bougerMoteur(1, 80, 2)

nao.bougerMoteur(0, 20, 2)
nao.bougerMoteur(1, 20, 2)

nao.bougerMoteur(0, 50, 2)
nao.bougerMoteur(1, 50, 2)

nao.libererMoteur(0)
nao.libererMoteur(1)

#tests reconnaissance vocale en français
#nao.attribuerVocabulaire("bonjour", "oui", "non");
nao.dire("Demarrage de la detection vocale. Dites bonjour, oui ou non.");
#nao.demarrerReconnaissanceVocale();
naoEvenement.demarrerReconnaissanceVocale();

while not naoEvenement.recoVocale:
	time.sleep(0.5)
if naoEvenement.recoVocale:
	nao.dire("J'ai reconnu %s" %(naoEvenement.motReconnu))
	print "Taux : ", naoEvenement.tauxReconnaissance
	naoEvenement.arreterReconnaissanceVocale(); 
	nao.arreterReconnaissanceVocale();

#tests detection d'objet
nao.afficherVideo();
nao.dire("Demarrage de la detection d'objet. Montrez un objet à la caméra.");
naoEvenement.demarrerDetectionObjet();
while not naoEvenement.recoObjet:
	time.sleep(0.5)
if naoEvenement.recoObjet:
	nao.dire("J'ai reconnu %s" %(naoEvenement.objetReconnu))
	print "Taux : ", naoEvenement.tauxRessemblance
	print "Ratio : ", naoEvenement.ratio
	naoEvenement.arreterDetectionObjet();

#tests detection visage
nao.dire("Demarrage de la detection de visage. Montrez un visage à la caméra.");
naoEvenement.demarrerDetectionVisage();
while not naoEvenement.recoVisage:
	time.sleep(0.5)
if naoEvenement.recoVisage:
	nao.dire("J'ai reconnu %s" %(naoEvenement.visageReconnu))
	#print "Visage reconnu : ", naoEvenement.visageReconnu
	print "Taux : ", naoEvenement.tauxReconnaissance
	naoEvenement.arreterDetectionVisage();

#tests detection parole
nao.attribuerVocabulaire("bonjour", "oui", "non");
nao.dire("Demarrage de la detection de parole. Parlez quand vous voulez.");
nao.demarrerReconnaissanceVocale();
naoEvenement.demarrerDetectionParole();
while not naoEvenement.recoParole:
	time.sleep(0.5)
if naoEvenement.recoParole:
	nao.dire("Quelqu'un parle en ce moment");
	nao.arreterReconnaissanceVocale();
	naoEvenement.arreterDetectionParole();


#tests detection capteurs tactiles
naoEvenement.afficherNumeroCapteursTactiles();
nao.dire("Démarrage de la détection de capteurs. Appuyez sur mes capteurs tactiles. Pour finir l'activité, appuyez sur la partie arrière de ma tête");
naoEvenement.demarrerReconnaissanceTactile();
while not naoEvenement.recoTactile:
    time.sleep(0.5)
while naoEvenement.recoTactile:
    location = naoEvenement.location
    etat = naoEvenement.etat

    print location, etat

    if location==8 and etat==1:
        nao.dire("Fin de la reconnaissance de capteurs")
        naoEvenement.arreterReconnaissanceTactile();

