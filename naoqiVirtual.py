
"""
La classe ALProxy doit bouger le Nao Virtuel
Attribut statique référence le nao virtuel.

Peut etre qu'il faudrait faire hériter la classe
du virtualNao de ALProxy et surcharger les méthodes
mais ca serait pas bien pour les fonctions non surchargées
"""
import time as TimerT
from Animation import Animation
import time, threading, struct;

class ALProxy():
    # staticNao = NaoCommunicationVirtual.AbstractNaoEvenement
    # (remplace les fonctions du robot réel pour les events)
    staticNao=None
    # virtualNao = Nao3D
    # (remplace les membres du robot réel)
    virtualNao=None

    vocabList = []
    typeRobot="T14"

    membres={0:"HeadYaw",1:"HeadPitch",
                    2:"LShoulderPitch",3:"LShoulderRoll",4:"LElbowYaw",5:"LElbowRoll",6:"LWristYaw",7:"LHand",
                    8:"RShoulderPitch",9:"RShoulderRoll",10:"RElbowYaw",11:"RElbowRoll",12:"RWristYaw",13:"RHand"}

    membresVirtual={0:"teteG2", 1:"teteG0",#ok
                            2:"bicepsG0",3:"bicepsG2",4:"coudeG1",5:"coudeG2",6:"mainG1",7:"doigt1G0",#ok
                            8:"bicepsD0",9:"bicepsD2",10:"coudeD1",11:"coudeD2",12:"mainD1",13:"doigt1D0"#ok
                            }

    jointsAll={"T14":["HeadYaw", "HeadPitch",
                       "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand",
                       "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"],

               "H21":['HeadYaw', 'HeadPitch',
                       'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll',
                       'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll',
                       'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll',
                       'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll'],
               #not tested, may not work :
               "H25":['HeadYaw', 'HeadPitch',
                       'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', "LWristYaw", "LHand",
                       'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll',
                       'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll',
                       'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll',"RWristYaw", "RHand"]
                }

    def __init__(self,name=0,adress=0,port=0):
        self.name=name
        self.membre=None

        # Différence par rapport à naoqi :
        # Dans l'interface OpenGL, les rotations des membres droits sont inversé par la symétrie
        # Donc en fait les angles pour la partie gauche et la partie droite sont les memes
        # alors que dans naoqi, les parties droite et gauche sont gérées indépendemment
        # Solution :
        # Après copie de la liste renvoyée par le naoqi réel,
        # on copie tous les éléments de la partie gauche pour les coller et remplacer ceux de
        # la partie droite.
        # Données : [angleMin, angleMax, vitesseMin, vitesseMax]
        self.limitsAll={"T14":[[-2.08566856384 , 2.08566856384 , 8.26797389984 , 1.20000004768 ], [-0.671951770782 , 0.514872133732 , 7.19407272339 , 1.20000004768 ],
                               [-2.08566856384 , 2.08566856384 , 8.26797389984 , 1.20000004768 ], [-0.314159274101 , 1.32645022869 , 7.19407272339 , 1.20000004768 ], [-2.08566856384 , 2.08566856384 , 8.26797389984 , 1.20000004768 ], [-1.54461634159 , -0.0349065847695 , 7.19407272339 , 1.20000004768 ], [-1.82386910915 , 1.82386910915 , 24.6229305267 , 0.759999990463 ], [0.0 , 1.0 , 8.32999992371 , 0.550000011921 ],
                               [-2.08566856384 , 2.08566856384 , 8.26797389984 , 1.20000004768 ], [-0.314159274101 , 1.32645022869 , 7.19407272339 , 1.20000004768 ], [-2.08566856384 , 2.08566856384 , 8.26797389984 , 1.20000004768 ], [-1.54461634159 , -0.0349065847695 , 7.19407272339 , 1.20000004768 ], [-1.82386910915 , 1.82386910915 , 24.6229305267 , 0.759999990463 ], [0.0 , 1.0 , 8.32999992371 , 0.550000011921 ]],

                        "H21":[[-2.0856685638427734, 2.0856685638427734, 8.267973899841309, 1.2000000476837158], [-0.6719517707824707, 0.514872133731842, 7.194072723388672, 1.2000000476837158],
                               [-2.0856685638427734, 2.0856685638427734, 8.267973899841309, 1.2000000476837158], [-0.3141592741012573, 1.326450228691101, 7.194072723388672, 1.2000000476837158], [-2.0856685638427734, 2.0856685638427734, 8.267973899841309, 1.2000000476837158], [-1.5446163415908813, -0.03490658476948738, 7.194072723388672, 1.2000000476837158],
                               [-1.1452850103378296, 0.7407177090644836, 4.161737442016602, 3.200000047683716], [-0.37943458557128906, 0.7904596328735352, 4.161737442016602, 3.200000047683716], [-1.535889744758606, 0.4839797914028168, 6.40239143371582, 3.200000047683716], [-0.09232791513204575, 2.112546443939209, 6.40239143371582, 3.200000047683716], [-1.1894419193267822, 0.9225810170173645, 6.40239143371582, 3.200000047683716], [-0.3977605402469635, 0.7689920663833618, 4.161737442016602, 3.200000047683716],
                               [-1.1452850103378296, 0.7407177090644836, 4.161737442016602, 3.200000047683716], [-0.37943458557128906, 0.7904596328735352, 4.161737442016602, 3.200000047683716], [-1.535889744758606, 0.4839797914028168, 6.40239143371582, 3.200000047683716], [-0.09232791513204575, 2.112546443939209, 6.40239143371582, 3.200000047683716], [-1.1894419193267822, 0.9225810170173645, 6.40239143371582, 3.200000047683716], [-0.3977605402469635, 0.7689920663833618, 4.161737442016602, 3.200000047683716],
                               [-2.0856685638427734, 2.0856685638427734, 8.267973899841309, 1.2000000476837158], [-0.3141592741012573, 1.326450228691101, 7.194072723388672, 1.2000000476837158], [-2.0856685638427734, 2.0856685638427734, 8.267973899841309, 1.2000000476837158], [-1.5446163415908813, -0.03490658476948738, 7.194072723388672, 1.2000000476837158]],
                        #not tested
                        "H25":[[-2.08566856384 , 2.08566856384 , 8.26797389984 , 1.20000004768 ], [-0.671951770782 , 0.514872133732 , 7.19407272339 , 1.20000004768 ],
                               [-2.08566856384 , 2.08566856384 , 8.26797389984 , 1.20000004768 ], [-0.314159274101 , 1.32645022869 , 7.19407272339 , 1.20000004768 ], [-2.08566856384 , 2.08566856384 , 8.26797389984 , 1.20000004768 ], [-1.54461634159 , -0.0349065847695 , 7.19407272339 , 1.20000004768 ], [-1.82386910915 , 1.82386910915 , 24.6229305267 , 0.759999990463 ], [0.0 , 1.0 , 8.32999992371 , 0.550000011921 ],
                               [-1.1452850103378296, 0.7407177090644836, 4.161737442016602, 3.200000047683716], [-0.37943458557128906, 0.7904596328735352, 4.161737442016602, 3.200000047683716], [-1.535889744758606, 0.4839797914028168, 6.40239143371582, 3.200000047683716], [-0.09232791513204575, 2.112546443939209, 6.40239143371582, 3.200000047683716], [-1.1894419193267822, 0.9225810170173645, 6.40239143371582, 3.200000047683716], [-0.3977605402469635, 0.7689920663833618, 4.161737442016602, 3.200000047683716],
                               [-1.1452850103378296, 0.7407177090644836, 4.161737442016602, 3.200000047683716], [-0.37943458557128906, 0.7904596328735352, 4.161737442016602, 3.200000047683716], [-1.535889744758606, 0.4839797914028168, 6.40239143371582, 3.200000047683716], [-0.09232791513204575, 2.112546443939209, 6.40239143371582, 3.200000047683716], [-1.1894419193267822, 0.9225810170173645, 6.40239143371582, 3.200000047683716], [-0.3977605402469635, 0.7689920663833618, 4.161737442016602, 3.200000047683716],
                               [-2.08566856384 , 2.08566856384 , 8.26797389984 , 1.20000004768 ], [-0.314159274101 , 1.32645022869 , 7.19407272339 , 1.20000004768 ], [-2.08566856384 , 2.08566856384 , 8.26797389984 , 1.20000004768 ], [-1.54461634159 , -0.0349065847695 , 7.19407272339 , 1.20000004768 ], [-1.82386910915 , 1.82386910915 , 24.6229305267 , 0.759999990463 ], [0.0 , 1.0 , 8.32999992371 , 0.550000011921 ]]
                        }

        self.ledMnM={'RightFaceLed8':"eye1D", 'RightFaceLed7':"eye2D",
                     'RightFaceLed6':"eye3D", 'RightFaceLed5':"eye4D",
                     'RightFaceLed4':"eye5D", 'RightFaceLed3':"eye6D",
                     'RightFaceLed2':"eye7D", 'RightFaceLed1':"eye8D",

                     'LeftFaceLed8':"eye8G", 'LeftFaceLed7':"eye7G",
                     'LeftFaceLed6':"eye6G", 'LeftFaceLed5':"eye5G",
                     'LeftFaceLed4':"eye4G", 'LeftFaceLed3':"eye3G",
                     'LeftFaceLed2':"eye2G", 'LeftFaceLed1':"eye1G"
                     }

        self.ledIntensities={'RightFaceLed1':[.0,.0,.0],
                             'RightFaceLed2':[.0,.0,.0],
                             'RightFaceLed3':[.0,.0,.0],
                             'RightFaceLed4':[.0,.0,.0],
                             'RightFaceLed5':[.0,.0,.0],
                             'RightFaceLed6':[.0,.0,.0],
                             'RightFaceLed7':[.0,.0,.0],
                             'RightFaceLed8':[.0,.0,.0],
                             'LeftFaceLed8':[.0,.0,.0],
                             'LeftFaceLed7':[.0,.0,.0],
                             'LeftFaceLed6':[.0,.0,.0],
                             'LeftFaceLed5':[.0,.0,.0],
                             'LeftFaceLed4':[.0,.0,.0],
                             'LeftFaceLed3':[.0,.0,.0],
                             'LeftFaceLed2':[.0,.0,.0],
                             'LeftFaceLed1':[.0,.0,.0]}

        self.ledColors={'RightFaceLed1': ['Face/Led/Red/Right/0Deg/Actuator/Value', 'Face/Led/Green/Right/0Deg/Actuator/Value', 'Face/Led/Blue/Right/0Deg/Actuator/Value'], 'RightFaceLed3': ['Face/Led/Red/Right/90Deg/Actuator/Value', 'Face/Led/Green/Right/90Deg/Actuator/Value', 'Face/Led/Blue/Right/90Deg/Actuator/Value'], 'RightFaceLed2': ['Face/Led/Red/Right/45Deg/Actuator/Value', 'Face/Led/Green/Right/45Deg/Actuator/Value', 'Face/Led/Blue/Right/45Deg/Actuator/Value'], 'RightFaceLed5': ['Face/Led/Red/Right/180Deg/Actuator/Value', 'Face/Led/Green/Right/180Deg/Actuator/Value', 'Face/Led/Blue/Right/180Deg/Actuator/Value'], 'RightFaceLed4': ['Face/Led/Red/Right/135Deg/Actuator/Value', 'Face/Led/Green/Right/135Deg/Actuator/Value', 'Face/Led/Blue/Right/135Deg/Actuator/Value'], 'RightFaceLed7': ['Face/Led/Red/Right/270Deg/Actuator/Value', 'Face/Led/Green/Right/270Deg/Actuator/Value', 'Face/Led/Blue/Right/270Deg/Actuator/Value'], 'RightFaceLed6': ['Face/Led/Red/Right/225Deg/Actuator/Value', 'Face/Led/Green/Right/225Deg/Actuator/Value', 'Face/Led/Blue/Right/225Deg/Actuator/Value'], 'RightFaceLed8': ['Face/Led/Red/Right/315Deg/Actuator/Value', 'Face/Led/Green/Right/315Deg/Actuator/Value', 'Face/Led/Blue/Right/315Deg/Actuator/Value'], 'LeftFaceLed1': ['Face/Led/Red/Left/0Deg/Actuator/Value', 'Face/Led/Green/Left/0Deg/Actuator/Value', 'Face/Led/Blue/Left/0Deg/Actuator/Value'], 'LeftFaceLed3': ['Face/Led/Red/Left/90Deg/Actuator/Value', 'Face/Led/Green/Left/90Deg/Actuator/Value', 'Face/Led/Blue/Left/90Deg/Actuator/Value'], 'LeftFaceLed2': ['Face/Led/Red/Left/45Deg/Actuator/Value', 'Face/Led/Green/Left/45Deg/Actuator/Value', 'Face/Led/Blue/Left/45Deg/Actuator/Value'], 'LeftFaceLed5': ['Face/Led/Red/Left/180Deg/Actuator/Value', 'Face/Led/Green/Left/180Deg/Actuator/Value', 'Face/Led/Blue/Left/180Deg/Actuator/Value'], 'LeftFaceLed4': ['Face/Led/Red/Left/135Deg/Actuator/Value', 'Face/Led/Green/Left/135Deg/Actuator/Value', 'Face/Led/Blue/Left/135Deg/Actuator/Value'], 'LeftFaceLed7': ['Face/Led/Red/Left/270Deg/Actuator/Value', 'Face/Led/Green/Left/270Deg/Actuator/Value', 'Face/Led/Blue/Left/270Deg/Actuator/Value'], 'LeftFaceLed6': ['Face/Led/Red/Left/225Deg/Actuator/Value', 'Face/Led/Green/Left/225Deg/Actuator/Value', 'Face/Led/Blue/Left/225Deg/Actuator/Value'], 'LeftFaceLed8': ['Face/Led/Red/Left/315Deg/Actuator/Value', 'Face/Led/Green/Left/315Deg/Actuator/Value', 'Face/Led/Blue/Left/315Deg/Actuator/Value']}

        self.language="french"
        self.volume=0
        self.listLimits={"Body":[]}

        self.animation = Animation()

    #test ok
    @staticmethod
    def associateVirtualRobot(nao):
        ALProxy.virtualNao=nao

    @staticmethod
    def associateStaticNao(nao):
        ALProxy.staticNao=nao

    @staticmethod
    def getFunction(functionName):
        functionsByName={
            "onWordRecognized":ALProxy.staticNao._wordRecognizedEvent,
            "onPictureDetected":ALProxy.staticNao._pictureDetectedEvent,
            "onFaceDetected":ALProxy.staticNao._faceDetectedEvent,
            "onTactileDetected":ALProxy.staticNao._tactileEvent,
            "onWordDetected":ALProxy.staticNao._speechDetectedEvent}
        return functionsByName[functionName]

    @staticmethod
    def eventCall(function, args):
        ##try:
        if function != "onWordDetected":
            ALProxy.getFunction(function)(*args)
            return 1
        else :
            for mot in args[0].split():
                if mot.strip() in ALProxy.vocabList :
                    ALProxy.getFunction(function)()
                    return 1
                else :
                    print mot.strip()+"is not in Vocabulary list"
        ##except:
        ##    print "Pas de AbstractNaoEvenement instancié"
        return 0

    @staticmethod
    def setType(robot="T14"):
        ALProxy.typeRobot=robot
        #reconstruction des membres
        ALProxy.membres={}
        for a in range(len(ALProxy.jointsAll[robot])):
            ALProxy.membres[a]=ALProxy.jointsAll[robot][a]

        if robot=="T14":
            ALProxy.membresVirtual={0:"teteG2", 1:"teteG0",#ok
                                2:"bicepsG0", 3:"bicepsG2", 4:"coudeG1", 5:"coudeG2", 6:"mainG1", 7:"doigt1G0",#ok
                                8:"bicepsD0", 9:"bicepsD2", 10:"coudeD1", 11:"coudeD2", 12:"mainD1", 13:"doigt1D0"#ok
                                }
        elif robot=="H21":
            ALProxy.membresVirtual={0:"teteG2", 1:"teteG0",#ok
                                2:"bicepsG0", 3:"bicepsG2", 4:"coudeG1", 5:"coudeG2",#ok
                                6:'hancheG1', 7:'cuisseG1', 8:'cuisseG0', 9:'molletG0', 10:'piedG0', 11:'piedG1',
                                12:'hancheD1', 13:'cuisseD1', 14:'cuisseD0', 15:'molletD0', 16:'piedD0', 17:'piedD1',
                                18:"bicepsD0", 19:"bicepsD2",20:"coudeD1",21:"coudeD2"
                                }
        elif robot=="H25":
            ALProxy.membresVirtual={0:"teteG2", 1:"teteG0",#ok
                                2:"bicepsG0", 3:"bicepsG2", 4:"coudeG1", 5:"coudeG2", 6:"mainG1", 7:"doigt1G0",
                                8:'hancheG1', 9:'cuisseG1', 10:'cuisseG0', 11:'molletG0', 12:'piedG0', 13:'piedG1',
                                14:'hancheD1', 15:'cuisseD1', 16:'cuisseD0', 17:'molletD0', 18:'piedD0', 19:'piedD1',
                                20:"bicepsD0", 21:"bicepsD2", 22:"coudeD1", 23:"coudeD2", 24:"mainD1", 25:"doigt1D0"
                                }

    #test ok
    def setLanguage(self, language):
        self.language=language

    #test ok
    def getLanguage(self):
        return self.language

    #test ok
    def say(self, text):
        #print "NAO dit : "+str(text)
        self.virtualNao.addSpeaking(text)

    def setVolume(self, value):
        self.volume=value

    def getVolume(self):
        return self.volume

    #test ok
    def getJointNames(self, part="Body"):
        return self.jointsAll[self.typeRobot]

    #test ok
    def getLimits(self, part="Body"):
        return self.limitsAll[self.typeRobot]

    #test ok
    def getStiffnesses(self, part="Body"):
        r=[]
        for a in self.membres.keys():
            num=self.getNumberFromName(a)
            nom=self.membresVirtual[num][:-1]
            r.append(self.virtualNao.getMembre(nom).stiffness)
        return r

    def getStiffness(self, numeroMoteur):
            print "not implemented"

    def setStiffnesses(self, part="Body", value=1):
        names=self.getNamesFromPart(part)
        for a in names:
            self.virtualNao.getMembre(a[:-1]).stiffness=value

    def setStiffness(self, numeroMoteur, taux):
            print "not implemented"

    def getAngles(self, part="Body", isStg=True):
        return [0,0,0,0]

    #a verifier
    def getMinAngle(self, numero):
        return self.limitsAll[self.typeRobot][0]

    #a verifier
    def getMaxAngle(self, numero):
        return self.limitsAll[self.typeRobot][1]

    def angleInterpolation(self, name, motorAngle, time, isAbsolute):
        num=self.getNumberFromName(name)
        nom=self.membresVirtual[num][:-1]
        n=int(self.membresVirtual[num][-1])
        self.virtualNao.getMembre(nom).setAngle(n,motorAngle/3.14*180,time)        #print self.virtualNao.getMembre(nom).rotate, nom
        #print self.virtualNao.getMembre(nom).angle,self.virtualNao.getMembre(nom).timeMove
        TimerT.sleep(time)

    def getAnimationData(self):
        names = self.animation.getNames()
        values = self.animation.getValues()
        times = self.animation.getTimes()
        return names, angles, times

    def addMotionAnimation(self, numeroMoteur, position, temps):
        self.animation.addValue(self.getNameFromNumber(numeroMoteur), position, temps);

    def resetAnimation(self):
        self.animation.reset();

    #test OK
    def playAnimation(self):
        names = self.animation.getNames();
        values = self.animation.getValues();
        times = self.animation.getTimes();
        threads = [];

        i = 0;
        for name in names :
            valuesTab = values[i];
            timesTab = times[i];
            thread = threading.Thread(None, self.__playMotorAnimation, None, (name, valuesTab, timesTab), {});
            threads.append(thread);
            i=i+1;

        for thread in threads:
            thread.start();

    #test OK
    def __playMotorAnimation(self, name, values, times):
        assert len(values) == len(times);
        durations = self.__getDurations(times);
        for i in range(len(times)):
            duration = durations[i];
            motorAngle = values[i];
            time.sleep(duration);
            self.angleInterpolation(name, motorAngle, duration, True);

    #test OK
    def __getDurations(self, timesTab):
        durationTab = [];
        previousTime = -1;

        if len(timesTab)>0:
            previousTime = timesTab[0];
            durationTab.append(previousTime);
            for i in range(1, len(timesTab)):
                currentTime = timesTab[i];
                if currentTime <= previousTime :
                    string = "Times must be inscreasing at index %s : %s" %(i, timesTab[i])
                    raise Exception("TimeError", string);
                else:
                    duration = currentTime - previousTime;
                    previousTime = currentTime;
                    durationTab.append(duration);

        return durationTab;

    def getNumberFromName(self, name):
        num=0
        for x in self.membres:
            if name==self.membres[x]:
                return x
        print "error numberName"
        return num

    def getNameFromNumber(self, number):
        return self.membres[number]

    def getNamesFromPart(self, part):
        if part.lower()=="body":
            return self.membresVirtual.values()
        for x in self.membres.keys():
            if self.membres[x]==part:
                return [self.membresVirtual[x]]
        print "error Names part", part
        return []


    def getAvailableLanguages(self):
        return ["fr"]

    ###############" LED

    def getListFromName(self, name):
        result=[]
        if name in self.ledMnM.keys():
            return [self.ledMnM[name]]
        elif "Right" in name:
            for x in self.ledMnM.keys():
                if "Right" in x: result.append(self.ledMnM[x])
        elif "Left" in name:
            for x in self.ledMnM.keys():
                if "Left" in x: result.append(self.ledMnM[x])
        else:result=self.ledMnM.values()
        return result

    def getListNamesFromName(self, name):
        result=[]
        if name in self.ledMnM.keys():
            return [name]
        elif "Right" in name:
            for x in self.ledMnM.keys():
                if "Right" in x: result.append(x)
        elif "Left" in name:
            for x in self.ledMnM.keys():
                if "Left" in x: result.append(x)
        else:result=self.ledMnM.values()
        return result

    def setIntensity(self, name, intensity):
        #print intensity
        if name in self.ledMnM.keys():
            a=self.ledMnM[name]
            color=[intensity,intensity,intensity]
            self.ledIntensities[name]=color
        else:
            for b in self.ledColors.keys():
                if name in self.ledColors[b]:
                    #detection de la composante de couleur
                    pos=self.ledColors[b].index(name)
                    name=b
                    a=self.ledMnM[b]
                    self.ledIntensities[name][pos]=intensity
                    break
        self.virtualNao.setEye(self.ledIntensities[name],a)

    def getIntensity(self,name):
        return self.ledIntensities[name]

    def on(self,name):
        a=self.getListFromName(name)
        self.virtualNao.setEyes(1,a)

    def off(self,name):
        a=self.getListFromName(name)
        self.virtualNao.setEyes(0,a)

    def fade(self,name, intensity, duration):
        pass

    def fadeRGB (self, name, color, duration):
        pass

    def setWordListAsVocabulary(self, vocabList):
        ALProxy.vocabList = vocabList

    def startSpeechRecognition(self):
        pass

class ALBroker():
    def __init__(self,name,adress,port,adressRec,portRec):
        self.name=name

    def shutdown(self):
        pass

