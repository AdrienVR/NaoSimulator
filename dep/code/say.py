
from time import sleep
from Nao import *

nao=Nao(NaoAPI())

naoEvenement = AbstractNaoEvenement("naoEvenement", NaoAPI().getMemory(), nao);
naoEvenement.demarrerReconnaissanceVocale();

#tests parole
nao.dire("bonjour")
