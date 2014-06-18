
from time import sleep
from NaoCommunication import *

nao=NaoControle(Nao())

naoEvenement = AbstractNaoEvenement("naoEvenement", Nao().getMemory(), nao);
naoEvenement.demarrerReconnaissanceVocale();

while not naoEvenement.recoVocale:
	time.sleep(0.5)
nao.dire("j'ai reconnu : "+naoEvenement.motReconnu)
print naoEvenement.motReconnu

for a in range(16):
	if a%2==0:
		nao.reglerCouleur(a,a*15,50,50)                  
	else :
		nao.reglerCouleur(a,255,0,0)
	sleep(0.1)
for a in range(15,-1,-1):
	nao.eteindreLed(a)
	sleep(0.1)
