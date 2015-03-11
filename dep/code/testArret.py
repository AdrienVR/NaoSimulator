
from time import sleep
from Nao import *

nao=Nao(NaoAPI())

naoEvenement = AbstractNaoEvenement("naoEvenement", NaoAPI().getMemory(), nao);
naoEvenement.demarrerReconnaissanceVocale();

#DEBUT DE LA ZONE DE CODE DES ETUDIANTS
#A executer en saisissant dans une console :
#python nao.py

#tests parole
nao.dire("bonjour")

nao.arreterReconnaissanceVocale();
