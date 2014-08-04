
from time import sleep
from Nao import *

nao=Nao(NaoAPI())

naoEvenement = AbstractNaoEvenement("naoEvenement", NaoAPI().getMemory(), nao);
naoEvenement.demarrerReconnaissanceVocale();

#tests parole
nao.dire("bonjour")
#tests leds

nao.dire(u"Debut du test des moteurs")

nao.bloquerTousMoteurs()
#mains fermees
nao.ajouterMouvementAnimationMoteur(0, 0, 1)
nao.ajouterMouvementAnimationMoteur(1, 0, 1)
nao.ajouterMouvementAnimationMoteur(0, 50, 2)
nao.ajouterMouvementAnimationMoteur(1, 50, 2)
nao.jouerAnimationMoteur()
nao.effacerAnimationMoteur()

sleep(4)