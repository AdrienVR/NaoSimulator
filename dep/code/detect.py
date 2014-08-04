
from time import sleep
from Nao import *

nao=Nao(NaoAPI())

naoEvenement = AbstractNaoEvenement("naoEvenement", NaoAPI().getMemory(), nao);
naoEvenement.demarrerReconnaissanceVocale();

#tests parole
nao.dire("bonjour")

nao.dire("Demarrage de la detection d'objet. Montrez un objet a la camera.");
naoEvenement.demarrerDetectionObjet();
while not naoEvenement.recoObjet:
	time.sleep(0.5)
if naoEvenement.recoObjet:
	nao.dire("J'ai reconnu %s" %(naoEvenement.objetReconnu))
	print "Taux : ", naoEvenement.tauxRessemblance
	print "Ratio : ", naoEvenement.ratio
	naoEvenement.arreterDetectionObjet();

#tests detection visage
nao.dire("Demarrage de la detection de visage. Montrez un visage a la camera.");
naoEvenement.demarrerDetectionVisage();
while not naoEvenement.recoVisage:
	time.sleep(0.5)
if naoEvenement.recoVisage:
	nao.dire("J'ai reconnu %s" %(naoEvenement.visageReconnu))
	#print "Visage reconnu : ", naoEvenement.visageReconnu
	print "Taux : ", naoEvenement.tauxReconnaissance
	naoEvenement.arreterDetectionVisage();
