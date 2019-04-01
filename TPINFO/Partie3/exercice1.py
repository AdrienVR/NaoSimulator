#Initialisation
from time import sleep
from NaoCommunication import *
nao=NaoControle(Nao())

# 1 - Decrire le resultat de ce morceau de code
# ...
for a in range(16):
	if a%2==0:
		nao.reglerCouleur(a,a*15,50,50)                  
	else :
		nao.reglerCouleur(a,255,0,0)
	sleep(0.1)
for a in range(15,-1,-1):
	nao.eteindreLed(a)
	sleep(0.1)

# 2 - Decrire le resultat de ce deuxieme morceau de code
# ...
for a in range(15,-1,-1):
	nao.allumerLed(a)
	sleep(0.1)
for a in range(0,16,1):
	nao.eteindreLed(a)
	sleep(0.1)

# 3 - A partir des exemples precedents, ecrire un code qui
# allume alternativement les deux leds 1 seconde chacune
# pendant 10 secondes.

