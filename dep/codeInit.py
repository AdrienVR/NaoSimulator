
from time import sleep
from Nao import *

nao=Nao(NaoAPI())

naoEvenement = AbstractNaoEvenement("naoEvenement", NaoAPI().getMemory(), nao);
naoEvenement.demarrerReconnaissanceVocale();

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

nao.dire("Tests des moteurs. Regardez ma tete.")
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

#tests reconnaissance vocale en francais
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
