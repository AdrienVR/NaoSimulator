
from time import sleep
from NaoCommunication import *

nao=NaoControle(Nao())

naoEvenement = AbstractNaoEvenement("naoEvenement", Nao().getMemory(), nao);
naoEvenement.demarrerReconnaissanceVocale();

#tests parole
nao.dire("bonjour")

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