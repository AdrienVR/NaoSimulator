
from NaoMembre import Membre

## Calcul du gris des yeux
FORMAT_COLORS = 255.0
EYES_GREY = 175.0
R_COLOR = EYES_GREY / FORMAT_COLORS

# aka virtualNao

class Nao3D():
    def __init__(self):
        self.loaded=False

        self.eyesColoring=[EYES_GREY,EYES_GREY,EYES_GREY]

        Membre("torseS","torseSG")
        Membre("torseS","torseSD")

        ##Création de l'architecture
        Membre("torse","torseG")
        Membre("torse","torseD")

        arbre=[{"torse":["hanche","tete","biceps","epaule","epauleBiceps"]},
               {"biceps":["coude"],"hanche":["cuisse"],
                "tete":["eye1","eye2","eye3","eye4","eye5",
                        "eye6","eye7","eye8"]},
               {"coude":["main"],"cuisse":["mollet"]},
               {"main":["doigt1","doigt2","doigt3"],"mollet":["pied"]}]

        mother={"pied":"mollet","mollet":"cuisse","cuisse":"hanche",
                "hanche":"torse","tete":"torse",
                "biceps":"torse","coude":"biceps",
                "main":"coude",
                "doigt1":"main","doigt2":"main","doigt3":"main",
                "eye1":"tete","eye2":"tete","eye3":"tete","eye4":"tete",
                "eye5":"tete","eye6":"tete","eye7":"tete","eye8":"tete"}

        cote="GD"

        ##exceptionSymetrie=["tete"]
        for coteM in cote:
            for brancheN in range(len(arbre)):
                for mere in arbre[brancheN].keys():
                    for partieJ in arbre[brancheN][mere]:
                        #Creation de chaque sous-membre : Membre(partieJ,partieJ+coteM)
                        Membre.membresRecup[mere+coteM].addUnder(partieJ,partieJ+coteM)
        #copie du dictionnaire statique de la classe Membre.
        self.membres=Membre.membresRecup.copy()

        # les firsts nécessitent un roll back des Rotations si divers membres
        # se succèdent.
        for a in cote:
            self.membres["torse"+a].isFirst=True
            self.membres["biceps"+a].isFirst=True
            self.membres["tete"+a].isFirst=True
            self.membres["epaule"+a].isFirst=True
            self.membres["coude"+a].isFirst=True
            self.membres["main"+a].isFirst=True
            self.membres["doigt1"+a].isFirst=True
            self.membres["doigt2"+a].isFirst=True
            self.membres["doigt3"+a].isFirst=True
            self.membres["hanche"+a].isFirst=True
            self.membres["epauleBiceps"+a].isFirst=True

        #Positionnement des Membres de gauche
        Membres=["pied","mollet","cuisse",
                  "hanche","torse","tete",
                  "epaule","biceps","coude",
                  "epauleBiceps",
                  "main",
                 "doigt1","doigt2","doigt3",
                 "eye1","eye2","eye3","eye4",
                 "eye5","eye6","eye7","eye8"]

        #positions initiales des origines de chaque objet dans Blender
        #han:0,0,0
        depG=[[0.49986,0.0288,-2.42088],[0.49925,0.02880,-1.41198],[0.49831,0.02797,-0.36973],
              [0.0,.0,.0],[.0,.0,.0],[0,0,1.76],
              [0.95093,0,1.5],[0.95093,0,1.5],[0.96,-1.049,1.5],
              [0.72208,0,1.48455],
              [0.96194,-1.62163,1.49876],
              [0.97679,-2.10791,1.35952],[1.08727,-2.27286,1.46021],[0.87248,-2.25619,1.46523],
              [0,0,1.76],[0,0,1.76],[0,0,1.76],[0,0,1.76],
              [0,0,1.76],[0,0,1.76],[0,0,1.76],[0,0,1.76]      ]

        for m in cote:
            i=0
            for a in Membres:
                self.membres[a+m].pos=depG[i][:]
                #inversion de l'axe y
                self.membres[a+m].pos[1]=-self.membres[a+m].pos[1]
##                if m=="D":
##                    self.membres[a+m].pos[0]*=-1
##                    if self.membres[a+m].isFirst:
##                        self.membres[a+m].size[0]=-1
                i+=1

        #travaille sur une copie
        copie={}
        for m in cote:
            for x in mother.keys():
                j=[]
                for i in range(3):
                        j.append(self.membres[x+m].pos[i]-self.membres[mother[x]+m].pos[i])
                copie[x+m]=j[:]

        for x in self.membres.keys():
            if x in copie.keys():
                self.membres[x].pos=copie[x][:]

        self.imageText=None
        self.ImageLoad("naoText.png")

        #T14, H21 ou H25
        self.type="H21"

        #private
        self.timePerCharacter=0.1
        self.timeSpeaking=.0
        self.speakingList=[]
        self.speaking=""

        self.finishedSpeaking=True

        #self.membres["eye1G"].replaceColor=[1.0,.0,.0]
        self.legG=self.membres["torseSG"]
        self.legG.underObjects=self.membres["torseG"].underObjects.copy()
        self.legD=self.membres["torseSD"]
        self.legD.underObjects=self.membres["torseD"].underObjects.copy()
        self.loaded=True

    def updateSpeaking(self, dt):
        if self.timeSpeaking>.0:
            self.timeSpeaking-=dt

        elif self.timeSpeaking<=.0 and self.speakingList!=[]:
            self.speaking=self.speakingList[0]
            self.speakingList=self.speakingList[1:]
            self.timeSpeaking+=len(self.speaking)*self.timePerCharacter
            if len(self.speaking)==1:self.timeSpeaking+=0.5

        else:
            self.speaking=""
            self.finishedSpeaking=True

    def addSpeaking(self,texte):
        self.finishedSpeaking=False
        if self.speaking=="":
            self.speaking=texte
            self.timeSpeaking+=len(self.speaking)*self.timePerCharacter
        else:
            self.speakingList.append(texte)

    def resetSpeaking(self):
        self.timeSpeaking=.0
        self.speakingList=[]
        self.speaking=""
        self.finishedSpeaking=True

    def ImageLoad(self,filename):
        #self.imageText=Gui.QImage(filename,"RGB")
        #print "texture chargee"
        return

    def changeLegs(self):
        a=self.legD
        b=self.legG
        self.legD=self.membres["torseD"]
        self.legG=self.membres["torseG"]
        self.membres["torseD"]=a
        self.membres["torseG"]=b

    def getMembreKeys(self):
        return self.membres.keys()

    def getMembre(self, name):
        return self.membres[name]

    def setEye(self, color, eye):
        self.membres[eye].replaceColor=self.getGLColoringFloat(color)

    def setEyes(self, onOff, eyesList):
        if onOff:
            for a in eyesList:
                self.membres[a].replaceColor=self.getGLColoring([255.0,255.0,255.0])
        else :
            for a in eyesList:
                self.membres[a].replaceColor=self.getGLColoring([.0,.0,.0])

    def setEyesColoring(self, R, G, B):
        self.eyesColoring=[R,G,B]

    def getGLColoring(self, color=[]):
        if color==[]:color=self.eyesColoring
        return [color[0]/FORMAT_COLORS*(1.0-R_COLOR)+R_COLOR,
                color[1]/FORMAT_COLORS*(1.0-R_COLOR)+R_COLOR,
                color[2]/FORMAT_COLORS*(1.0-R_COLOR)+R_COLOR]

    def getGLColoringFloat(self, color=[]):
        if color==[]:color=self.eyesColoring
        return [color[0]*(1.0-R_COLOR)+R_COLOR,
                color[1]*(1.0-R_COLOR)+R_COLOR,
                color[2]*(1.0-R_COLOR)+R_COLOR]

    def colorEyes(self, eyesList):
        for a in eyesList:
            self.membres[a].replaceColor=self.getGLColoring()
