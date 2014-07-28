
from time import sleep
from NaoCommunication import *

nao=NaoControle(Nao())

naoEvenement = AbstractNaoEvenement("naoEvenement", Nao().getMemory(), nao);
naoEvenement.demarrerReconnaissanceVocale();

#tests parole
nao.dire("bonjour")
