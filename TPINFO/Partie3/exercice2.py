
## -------------------------
##  ceci est un commentaire
## -------------------------

#Initialisation
from NaoCommunication import *
nao=NaoControle(Nao())

#Pour faire bouger un moteur, on a besoin de son numero:
# 0  :  Tete tournant par rapport a l'axe Z
# 1  :  Tete tournant par rapport a l'axe X
# 2  :  Biceps Gauche tournant par rapport a l'axe X
# 3  :  Biceps Gauche tournant par rapport a l'axe Z
# 4  :  Coude Gauche tournant par rapport a l'axe Y
# 5  :  Coude Gauche tournant par rapport a l'axe Z
# 6  :  Main Gauche Y
# 7  :  Doigt Gauche
# 8  :  Biceps Droit tournant par rapport a l'axe X
# 9  :  Biceps Droit tournant par rapport a l'axe Z
# 10  :  Coude Droit tournant par rapport a l'axe Y
# 11  :  Coude Droit tournant par rapport a l'axe Z
# 12  :  Main Droite Y
# 13  :  Doigt Droit

#Et on utilise ce morceau de code :
nao.bloquerMoteur(A)
nao.bougerMoteur(A, pourcentage, temps)
nao.libererMoteur(A)
# Ce qui provoque :
# Rotation du moteur A jusqu'a sa position pourcentage, en temps secondes.

# 1 - Faire bouger chaque moteur sur le simulateur pour avoir une visualisation
# des mouvements possibles.

# 2 - Ecrire un morceau de code qui fasse bouger la tete de haut en bas
# en 8 secondes.

