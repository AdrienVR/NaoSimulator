
from time import sleep
from Nao import *

nao=Nao(NaoAPI())

naoEvenement = AbstractNaoEvenement("naoEvenement", NaoAPI().getMemory(), nao);
naoEvenement.demarrerReconnaissanceVocale();

nao.demarrerParallelisation()


nao.jouerMusique("Chocobo.mp3")
nao.jouerSon(1,1,1,1)
nao.jouerSi2(1)


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

nao.dire(u"Tests des moteurs. Regardez ma tete.")
nao.activerMoteur(0)
nao.activerMoteur(1)

nao.bougerMoteur(0, 80, 2)
nao.bougerMoteur(1, 80, 2)

sleep(2)
nao.bougerMoteur(0, 50, 2)
nao.bougerMoteur(1, 50, 2)

sleep(2)

nao.desactiverMoteur(0)
nao.desactiverMoteur(1)

#tests reconnaissance vocale en francais
#nao.attribuerVocabulaire("bonjour", "oui", "non");
nao.dire(u"Demarrage de la detection vocale. Dites bonjour, oui ou non.");
#nao.demarrerReconnaissanceVocale();
naoEvenement.demarrerReconnaissanceVocale();

while not naoEvenement.recoVocale:
	time.sleep(0.5)
if naoEvenement.recoVocale:
	nao.dire("J'ai reconnu %s" %(naoEvenement.motReconnu))
	print "Taux : ", naoEvenement.tauxReconnaissance
	naoEvenement.arreterReconnaissanceVocale();
	nao.arreterReconnaissanceVocale();
