
from time import sleep
from Nao import *

address = "169.254.16.208"; #A VERIFIER
port = 9559;

naoRobot = NaoAPI(address, port);
nao = Nao(naoRobot);
naoEvenement = AbstractNaoEvenement("naoEvenement", naoRobot.getMemory(), nao);

#DEBUT DE LA ZONE DE CODE DES ETUDIANTS
#A executer en saisissant dans une console :
#python nao.py

#tests parole
nao.dire("bonjour")



#tests reconnaissance vocale en francais
#nao.attribuerVocabulaire("bonjour", "oui", "non");

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

	#tests detection d'objet
nao.afficherVideo();
nao.dire(u"Demarrage de la detection d'objet. Montrez un objet a la camera.");
naoEvenement.demarrerDetectionObjet();
while not naoEvenement.recoObjet:
	time.sleep(0.5)
if naoEvenement.recoObjet:
	nao.dire("J'ai reconnu %s" %(naoEvenement.objetReconnu))
	print("Taux : ", naoEvenement.tauxRessemblance)
	print("Ratio : ", naoEvenement.ratio)
	naoEvenement.arreterDetectionObjet();

#tests detection visage
nao.dire(u"Demarrage de la detection de visage. Montrez un visage a la camera.");
naoEvenement.demarrerDetectionVisage();
while not naoEvenement.recoVisage:
	time.sleep(0.5)
if naoEvenement.recoVisage:
	nao.dire("J'ai reconnu %s" %(naoEvenement.visageReconnu))
	#print("Visage reconnu : ", naoEvenement.visageReconnu)
	print("Taux : ", naoEvenement.tauxReconnaissance)
	naoEvenement.arreterDetectionVisage();


#tests detection capteurs tactiles
naoEvenement.afficherNumeroCapteursTactiles();
nao.dire("Demarrage de la detection de capteurs.")
nao.dire("Appuyez sur mes capteurs tactiles.")
nao.dire("Pour finir l'activite, appuyez sur la partie arriere de ma tete");
naoEvenement.demarrerReconnaissanceTactile();
while not naoEvenement.recoTactile:
    time.sleep(0.5)
while naoEvenement.recoTactile:
    location = naoEvenement.location
    etat = naoEvenement.etat

    print(str(location)+str(etat))

    if location==8 and etat==1:
        nao.dire("Fin de la reconnaissance de capteurs")
        naoEvenement.arreterReconnaissanceTactile();


