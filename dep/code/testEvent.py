
from time import sleep
from Nao import *

class EventManagerModule(AbstractNaoEvenement):

    def __init__(self):
        self.naoN=Nao(NaoAPI())
        AbstractNaoEvenement.__init__(self, "naoEvenement", NaoAPI().getMemory(), self.naoN);
        self.nao = NaoAPI();

    def _faceDetectedEvent(self, visage, tauxReco):
        print("visage :",visage);
        print("tauxReco :", tauxReco);
        if visage!='' and tauxReco > 0.5 :
            phrase = "Je vois %s" %(visage);
            print(phrase);
            self.nao.getVoice().say(phrase);
        else:
            self.nao.getVoice().say("Je vois quelqu'un que je ne connais pas.");

    def _pictureDetectedEvent(self, objectName, objectSide, matching, ratio):
        phrase = u"J'ai detecte %s" %(objectName);
        self.nao.getVoice().say(phrase);
        print("Ratio :",ratio);

    def _speechDetectedEvent(self):
        print("Speech detected.");

    def _wordRecognizedEvent(self, mot, tauxReco):
        self.naoN.effacerAnimationLed()
        for i in range(16):
        	self.naoN.ajouterAnimationLed(i,255,0,0,1)
        	self.naoN.ajouterAnimationLed(i,125,125,0,3)
        self.naoN.jouerAnimationLed()
        print("MOT PROBABLE :",mot);
        print("Taux de reconnaissance :", tauxReco);
        if mot=="bonjour" and tauxReco > 0.4 :
            self.nao.getVoice().say("Bonjour toi !");
        elif mot=="hello" and tauxReco > 0.4:
            nao.getVoice().setLanguage("English");
            self.nao.getVoice().say("Hello you!");
            nao.getVoice().setLanguage("French");
        else :
            self.nao.getVoice().say("J'ai reconnu : "+mot);

    #Quelle difference avec wordRecognizedEvent ?
    def _lastWordRecognizedEvent(self, mot, tauxReco):
        print("DERNIER MOT PROBABLE :",mot);
        print("Taux de reconnaissance :", tauxReco);
        
    def _tactileEvent(self, location, state):
        print("detect machin")
        self.nao.getVoice().say("On me touche : "+str(location));


a = EventManagerModule()
print("test")

time.sleep(50)


