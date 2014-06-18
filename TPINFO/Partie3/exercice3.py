#Initialisation
from time import sleep
from NaoCommunication import *
nao=NaoControle(Nao())

# 1 - Que fait ce code ?
# ...
def compter(jusqua):
    for nombre in range(0,jusqua,1):
        nao.dire(str(nombre))
compter(4)

# 2 - Ecrire une       fonction
# qui reutilise votre code sur l'exercice Incendie
# (Partie 1 : exercice 4)
# en rajoutant a la fin les mouvements pour que
# le robot leve les bras en 2 secondes lors de l'explosion
...

# 3 - executer cette fonction.
