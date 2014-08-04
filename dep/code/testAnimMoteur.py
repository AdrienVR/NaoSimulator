
from time import sleep
from Nao import *

nao=Nao(NaoAPI())

naoEvenement = AbstractNaoEvenement("naoEvenement", NaoAPI().getMemory(), nao);
naoEvenement.demarrerReconnaissanceVocale();

#tests parole
nao.dire("bonjour")
#tests leds

nao.dire(u"Debut du test des moteurs")

#nao.bloquerTousMoteurs()
#mains fermees
nao.ajouterMouvementAnimationMoteur(7, 0, 1)
nao.ajouterMouvementAnimationMoteur(13, 0, 1)
nao.jouerAnimationMoteur()
nao.effacerAnimationMoteur()

sleep(5)