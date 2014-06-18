
from time import sleep
from NaoCommunication import *

nao=NaoControle(Nao())

for a in range(0,22):
        nao.bloquerMoteur(a)
        nao.bougerMoteur(a, 75, 2)
        nao.libererMoteur(a)
