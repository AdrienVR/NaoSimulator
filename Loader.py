# -*- coding: utf-8 -*-

OBJ_REP="objects/"

def cleanup(st):
    return st.strip()

class Material():
    """
    Classe qui permet de charger les matériaux des objets 3D .obj
    présents dans les fichiers .mtl associés
    """
    def __init__(self,fichier,name):
        self.name=name
        self.attributes={"Ns":96.078431,
                "Ka":[.0,.0,.0],
                "Kd":[.5,.5,.5],
                "Ks":[.5,.5,.5],
                "Ni":1.0,
                "d ":1.0,
                "il":2}
        self.texture=False#sinon name of texture
        self.load(fichier,name)

    def load(self,fichier,name="Material"):
        a=open(OBJ_REP+fichier+".mtl")
        i=0
        ls=["Ns","Ka","Kd","Ks","Ni","d ","il"]
        b=a.readlines()
        a.close()
        j=0
        while(b[j][:7+len(name)]!="newmtl "+name):
            j+=1
        while(1):
            if b[j][:2]!=ls[i]:j+=1
            else:
                if i in [0,4]:
                    self.attributes[ls[i]]=float(b[j].replace("\n","").replace(ls[i],""))
                elif i==5:
                    self.attributes[ls[i]]=float(b[j].replace("\n","").replace("d ",""))
                elif i==6:
                    self.attributes[ls[i]]=int(b[j].replace("\n","").replace("illum ",""))
                else:
                    k=b[j].replace("\n","").replace(ls[i]+' ',"")
                    for indice, valeur in enumerate(k.split()):
                        self.attributes[ls[i]][indice]=float(valeur)
                i+=1
                j+=1
            if j<len(b):
                if i==len(ls) and b[j] not in ["","\n"," "," \n"]:
                    self.texture=b[j].replace("\n","")
                    break
                if b[j] in ["","\n"," "," \n"]:
                    break
            else:
                break
    def getColor(self):
        return self.attributes["Kd"]
    def setColor(self,col):
        self.attributes["Kd"]=list(col)
            

class Objet3D():
    """
    Classe utilisée dans le loader pour stocker les informations
    de l'objet, vertices et matériaux.
    """
    materiaux={}
    def __init__(self):
        self.hasTexture=True
        self.name=""
        self.tabCoord=[]
        self.tabText=[]
        self.tabNorm=[]
        
        self.tabCoordInd=[]
        self.tabTextInd=[]
        self.tabNormInd=[]

        #chargement du material
        self.material={}
        #self.loadMaterial(self.name)
        #print Objet3D.materiaux

    def loadMaterial(self,fichier,name,faceNb):
        name = cleanup(name)
        #si le materiau existe deja
        if name in Objet3D.materiaux.keys():
            self.material[faceNb]=Objet3D.materiaux[name]
        #sinn on le stocke dans l'attrib static materiaux
        else :
            Objet3D.materiaux[name]=Material(fichier,name)
            self.material[faceNb]=Objet3D.materiaux[name]

    def multipleColors(self):
        if len(self.material.keys())==1:
            return False
        return True

##    def getFaceNbColors(self):
##        a={}
##        if self.multipleColors():
##            for x in self.material.keys():
##                a[x]=self.material[x].getColor()
##        else:
##            a[0]=self.material[0].getColor()
##        return a
                

class Loader():
    """
    Supporte seulement obj avec vertices normaux, et faces traingulaires.
    """
    def __init__(self):
        pass
    def load(self,name):
        a=open(OBJ_REP+name+".obj")
        b=a.readlines()
        a.close()
        listObj=[]
        i=0
        while(1):
            if b[i][0]!="o":
                i+=1
            else :
                obj=Objet3D()
                i+=1
                #boucle sur les vertices
                while(b[i][1]==" "):
                    li=b[i].split()
                    obj.tabCoord.append(tuple((float(li[1]),float(li[2]),float(li[3]))))
                    i+=1
                #boucle sur les vertices text
                while(b[i][1]=="t"):
                    li=b[i].split()
                    obj.tabText.append(tuple((float(li[1]),float(li[2]))))
                    i+=1
                #boucle sur les vertices normaux
                while(b[i][1]=="n"):
                    li=b[i].split()
                    obj.tabNorm.append(tuple((float(li[1]),float(li[2]),float(li[3]))))
                    i+=1
                while(b[i][0] in ["s","u"]):
                    ##pas de gestion des s
                    if (b[i][:7]=="usemtl "):
                        obj.loadMaterial(name,b[i].split("usemtl ")[1],len(obj.tabCoordInd))
                    i+=1
                while(b[i][0]=="f"):
                    li=b[i].split()
                    for a in range(1,4):
                        obj.tabCoordInd.append(int(li[a].split("/")[0]))
                    if obj.hasTexture:
                        try:
                            for a in range(1,4):
                                obj.tabTextInd.append(int(li[a].split("/")[1]))
                        except:
                            obj.hasTexture=False
                    for a in range(1,4):
                        obj.tabNormInd.append(int(li[a].split("/")[2]))
                    i+=1
                    if i==len(b):break

                    #gestion des interrupteurs de la chaine de faces : s, usemtl
                    while(b[i][0] in ["s","u"]):
                        ##pas de gestion des s
                        if (b[i][:7]=="usemtl "):
                            obj.loadMaterial(name,b[i].split("usemtl ")[1],len(obj.tabCoordInd))
                        i+=1
                        if i==len(b):break
                listObj.append(obj)
                #il est possible de charger plusieurs objets par fichier.
            if i>len(b)-1:break
        return listObj
