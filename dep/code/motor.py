
from time import sleep
from Nao import *

nao=Nao(NaoAPI())

for a in range(0,22):
        nao.activerMoteur(a)
        nao.bougerMoteur(a, 75, 2)
        nao.desactiverMoteur(a)

