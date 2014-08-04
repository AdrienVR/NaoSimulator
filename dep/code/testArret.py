
from time import sleep
from NaoCommunication import *

address = "169.254.16.208"; #A VERIFIER
port = 9559;

naoRobot = Nao(address, port);
nao = NaoControle(naoRobot);
naoEvenement = AbstractNaoEvenement("naoEvenement", naoRobot.getMemory(), nao);

#DEBUT DE LA ZONE DE CODE DES ETUDIANTS
#A executer en saisissant dans une console :
#python nao.py

#tests parole
nao.dire("bonjour")

nao.arreterReconnaissanceVocale();
