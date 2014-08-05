
#from naoqi import ALProxy, ALBroker;
from naoqiVirtual import ALProxy, ALBroker;

from Actuator import *
from LedActuator import *
from Sensor import *
from Animation import Animation
from Video import *

import sys

#FakeALProxy

class NaoAPI():
    """
    Permet d'utiliser les fonctions qui programment le robot réel
    sur le robot virtuel
    """
    def __init__(self, naoAddress=0, naoPort=0):
            self.__address = naoAddress;
            self.__port = naoPort;
            #self.__xml = XML("files/nao.xml");
            #self.__xml.parse();
            self.__parallelism = False;
            self.setParallelism(False)

        #try :
            ttsProxy = ALProxy("ALTextToSpeech", self.__address, self.__port);
            motorsProxy = ALProxy("ALMotion",self.__address, self.__port);
            ledsProxy = ALProxy("ALLeds",self.__address, self.__port);
            memoryProxy = ALProxy("ALMemory",self.__address, self.__port);
            speechRecoProxy = ALProxy("ALSpeechRecognition",self.__address, self.__port);
            faceRecoProxy = ALProxy("ALFaceDetection",self.__address, self.__port);
            videoProxy = ALProxy("ALVideoDevice",self.__address, self.__port);

            self.__voice = VoiceActuator(ttsProxy);
            self.__motors = MotorsActuator(motorsProxy);
            self.__leds = LedsActuator(ledsProxy);
            self.__memory = memoryProxy;
            self.__speechReco = SpeechRecognitionSensor(speechRecoProxy);
            self.__videoDisplayer = VideoDisplayer(videoProxy);
            #self.__visualReco = VisualRecognition(faceRecoProxy, self.__xml);
            self.__createBroker();

##        except Exception,e:
##            print "Could not communicate with the robot";
##            print "Error was :",e;
##            sys.exit(1);

    def __createBroker(self):
        #self.__broker = ALBroker("ENIB_EventBroker","0.0.0.0", 0, self.__address,self.__port)
        pass

    def setParallelism(self, value):
        ALProxy.setParallelism(value)
        # self.__voice.setParallelism(value);
        # self.__motors.setParallelism(value);
        # self.__leds.setParallelism(value);
        # self.__sound.setParallelism(value);
        # self.__player.setParallelism(value);

    def stop(self):
        self.__broker.shutdown();

    def getVoice(self):
        return self.__voice;

    def getMotors(self):
        return self.__motors;

    def getLeds(self):
        return self.__leds;

    def getMemory(self):
        return self.__memory;

    def getSpeechReco(self):
        return self.__speechReco;

    def getFaceReco(self):
        return self.__faceReco;

    def getVideo(self):
        return self.__videoDisplayer;

    def getVisualReco(self):
        return self.__visualReco;
