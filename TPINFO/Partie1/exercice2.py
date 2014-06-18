#Initialisation
from time import sleep
from NaoCommunication import *
nao=NaoControle(Nao())

# 1 - Que fait ce code ?
# ...
for nombre in range(0,11,1):
    nao.dire(str(nombre))

# 2 - Que fait cette fonction ?
# ...
sleep(3)

# 3 - Comment faire pour que le robot compte les secondes jusqu'a 10 ?
...

# 4 - Resoudre le probleme de ce morceau de code :
for nombre in range(0,11,1):
nao.dire(str(nombre))

# 5 - Expliquer pourquoi il ne marchait pas.
# ...

# 6 - Resoudre le probleme de ce morceau de code :
for nombre in range(0,11,1):
    nao.dire(str(Nombre))

# 7 - Expliquer pourquoi il ne marchait pas.
# ...
