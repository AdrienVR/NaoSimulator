import sys

sys.path.insert(0,'..')
sys.path.insert(0,'/usr/lib/pynaoqi')

from naoqi import ALModule
from nao_training.NaoStructure import Nao;
        
class EventManagerAbstractModule(ALModule):
    
    def __init__(self, name, memory):
        
        ALModule.__init__(self, name)
        self.__name = name;
        self.__memory = memory;
        self.__faceDetectedEvent = "FaceDetected";
        self.__faceDetectedFonction = "onFaceDetected";
        self.__pictureDetectedEvent = "PictureDetected";
        self.__pictureDetectedFonction = "onPictureDetected";
        self.__speechDetectedEvent = "SpeechDetected";
        self.__speechDetectedFonction = "onSpeechDetected";
        self.__wordRecognizedEvent = "WordRecognized";
        self.__onWordRecognizedFonction = "onWordRecognized";
        self.__lastWordRecognizedEvent = "LastWordRecognized";
        self.__onLastWordRecognizedFonction = "onLastWordRecognized";

    ####### BEGIN OF FACE DETECTION #######

    def _faceDetectedEvent(self, face, rate):
        pass;

    def startFaceDetection(self):
        self.__memory.subscribeToEvent(self.__faceDetectedEvent,self.__name,self.__faceDetectedFonction);

    def onFaceDetected(self, *_args):
        self.__memory.unsubscribeToEvent(self.__faceDetectedEvent,self.__name);

        '''
            If a face is recognized, the label is stored in _args[1][1][0][1][2],
            otherwise an empty string is stored.
            The recognition rate is stored at _args[1][1][0][1][1]
        '''
        if _args[0]==self.__faceDetectedEvent:
            faceLabel = _args[1][1][0][1][2];
            recoRate = _args[1][1][0][1][1];
            
            self._faceDetectedEvent(faceLabel, recoRate);

        self.__memory.subscribeToEvent(self.__faceDetectedEvent,self.__name,self.__faceDetectedFonction);

    def stopFaceDetection(self):
        self.__memory.unsubscribeToEvent(self.__faceDetectedEvent,self.__name);
        
    ####### END OF FACE DETECTION #######

    ####### BEGIN OF OBJECT DETECTION #######

    def _pictureDetectedEvent(self, objectName, objectSide, matching, ratio):
        pass;

    def startPictureDetection(self):
        self.__memory.subscribeToEvent(self.__pictureDetectedEvent,self.__name,self.__pictureDetectedFonction);

    def onPictureDetected(self, *_args):
        self.__memory.unsubscribeToEvent(self.__pictureDetectedEvent,self.__name);

        if _args[0]==self.__pictureDetectedEvent :
            if len(_args[1]) > 0:
                objectName = _args[1][1][0][0][1];
                objectSide = _args[1][1][0][0][0];
                matchedKeypointsNumber = _args[1][1][0][1];
                '''
                    The ratio is the number of keypoints retrieved in the current
                    frame for the object divided by the number of keypoints found
                    during the learning stage of the object.
                '''
                ratio = _args[1][1][0][2];
                self._pictureDetectedEvent(objectName, objectSide, matchedKeypointsNumber, ratio);

        self.__memory.subscribeToEvent(self.__pictureDetectedEvent,self.__name,self.__pictureDetectedFonction);

    def stopPictureDetection(self):
        self.__memory.unsubscribeToEvent(self.__pictureDetectedEvent,self.__name);
        
    ####### END OF OBJECT DETECTION #######

    ####### BEGIN OF SPEECH RECOGNITION: SPEECH DETECTED #######

    def _speechDetectedEvent(self):
        pass;

    def startSpeechDetection(self):
        self.__memory.subscribeToEvent(self.__speechDetectedEvent,self.__name,self.__speechDetectedFonction);

    def onSpeechDetected(self, *_args):
        self.__memory.unsubscribeToEvent(self.__speechDetectedEvent,self.__name);

        self._speechDetectedEvent();

        self.__memory.subscribeToEvent(self.__speechDetectedEvent,self.__name,self.__speechDetectedFonction);

    def stopSpeechDetection(self):
        self.__memory.unsubscribeToEvent(self.__speechDetectedEvent,self.__name);
        
    ####### END OF SPEECH RECOGNITION: SPEECH DETECTED #######

    ####### BEGIN OF SPEECH RECOGNITION: WORD RECOGNIZED #######
    
    def _wordRecognizedEvent(self, word, rate):
        pass

    def onWordRecognized(self, *_args):
        word = "";
        rate = 0;
        self.__memory.unsubscribeToEvent(self.__wordRecognizedEvent, self.__name);
        taille = len(_args);
        if taille>2:
            if _args[0] == self.__wordRecognizedEvent :
                if len(_args[1]) > 1 :
                    word = _args[1][0];
                    rate = _args[1][1];
                    self._wordRecognizedEvent(word, rate);
                    
        self.__memory.subscribeToEvent(self.__wordRecognizedEvent, self.__name, self.__onWordRecognizedFonction);

    def startWordRecognition(self):
        #print("Lancement de la reconnaissance de mots");
        self.__memory.subscribeToEvent(self.__wordRecognizedEvent, self.__name, self.__onWordRecognizedFonction);
              
    def stopWordRecognition(self):
        self.__memory.unsubscribeToEvent(self.__wordRecognizedEvent, self.__name);
        #print("Fin de la reconnaissance de mots");

    ####### END OF SPEECH RECOGNITION #######

    ####### BEGIN OF SPEECH RECOGNITION: LAST WORD RECOGNIZED #######
    
    def _lastWordRecognizedEvent(self, word, rate):
        pass

    def onLastWordRecognized(self, *_args):
        word = "";
        rate = 0;
        self.__memory.unsubscribeToEvent(self.__lastWordRecognizedEvent, self.__name);
        taille = len(_args);
        if taille>2:
            if _args[0] == self.__lastWordRecognizedEvent :
                if len(_args[1]) > 1 :
                    word = _args[1][0];
                    rate = _args[1][1];
                    self._lastWordRecognizedEvent(word, rate);
                    
        self.__memory.subscribeToEvent(self.__lastWordRecognizedEvent, self.__name, self.__onLastWordRecognizedFonction);

    def startLastWordRecognition(self):
        #print("Lancement de la reconnaissance de mots");
        self.__memory.subscribeToEvent(self.__lastWordRecognizedEvent, self.__name, self.__onLastWordRecognizedFonction);
              
    def stopLastWordRecognition(self):
        #self.__memory.unsubscribeToEvent(self.__lastWordRecognizedEvent, self.__name);
        print("Fin de la reconnaissance de mots");

    ####### END OF SPEECH RECOGNITION #######
