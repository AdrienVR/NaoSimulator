#Initialisation
from time import sleep
from NaoCommunication import *
nao=NaoControle(Nao())

# 1 - Que fait ce morceau de code ?
# ...
for nombre in range(0,11,1):
    if nombre>5:
        nao.dire(str(nombre))

# 2 - Ecrire un code qui fait compter de 10 a 1
...

# 3 - Ecrire un code qui fait compter de 10 a 1, puis 
# fait dire au robot "boum"
...

# 3 - Ecrire un code qui fait compter de 10 a 1, mais 
# qui fait dire au robot "Que se passe-t-il ?" quand il reste
# 5 secondes, puis "boum" à 0 secondes.
...
