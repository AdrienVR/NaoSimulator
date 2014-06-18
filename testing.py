from NaoCommunicationVirtual import *

nao=NaoControle(Nao())

from Nao3D import *

virtualNao=Nao3D()
from naoqiVirtual import *
ALProxy.associateVirtualRobot(virtualNao)

nao.bloquerMoteur(0)
nao.bougerMoteur(0, 80, 2)
