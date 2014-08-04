import sys

sys.path.insert(0,'..')
sys.path.insert(0,'/usr/lib/pynaoqi')

from naoqi import ALModule
from nao_api.NaoAPI import NaoAPI;
        
class EventManagerAbstractModule(ALModule):
    
    def __init__(self, name, memory):
        
        ALModule.__init__(self, name)
        self.__name = name;
        self.__memory = memory;
        self.__faceDetectedEvent = "FaceDetected";
        self.__faceDetectedFunction = "onFaceDetected";
        self.__pictureDetectedEvent = "PictureDetected";
        self.__pictureDetectedFunction = "onPictureDetected";
        self.__speechDetectedEvent = "SpeechDetected";
        self.__speechDetectedFunction = "onSpeechDetected";
        self.__wordRecognizedEvent = "WordRecognized";
        self.__onWordRecognizedFunction = "onWordRecognized";
        self.__lastWordRecognizedEvent = "LastWordRecognized";
        self.__onLastWordRecognizedFunction = "onLastWordRecognized";
        self.__handRightBackTouched = "HandRightBackTouched";
        self.__handRightLeftTouched = "HandRightLeftTouched";
        self.__handRightRightTouched = "HandRightRightTouched";
        self.__handLeftBackTouched = "HandLeftBackTouched";
        self.__handLeftLeftTouched = "HandLeftLeftTouched";
        self.__handLeftRightTouched = "HandLeftRightTouched";
        self.__frontTactilTouched = "FrontTactilTouched";
        self.__middleTactilTouched = "MiddleTactilTouched";
        self.__rearTactilTouched = "RearTactilTouched";
        self.__onTactileEventFunction = "onTactileEvent";

    ####### BEGIN OF FACE DETECTION #######

    def unsubscribeToEvent(self, event, name):
        try :
            self.__memory.unsubscribeToEvent(event, name);
        except RuntimeError:
            pass        

    def _faceDetectedEvent(self, face, rate):
        pass;

    def startFaceDetection(self):
        self.__memory.subscribeToEvent(self.__faceDetectedEvent,self.__name,self.__faceDetectedFunction);

    def onFaceDetected(self, *_args):
        self.unsubscribeToEvent(self.__faceDetectedEvent,self.__name);

        '''
            If a face is recognized, the label is stored in _args[1][1][0][1][2],
            otherwise an empty string is stored.
            The recognition rate is stored at _args[1][1][0][1][1]
        '''
        if _args[0]==self.__faceDetectedEvent:
            faceLabel = _args[1][1][0][1][2];
            recoRate = _args[1][1][0][1][1];
            
            self._faceDetectedEvent(faceLabel, recoRate);

        self.__memory.subscribeToEvent(self.__faceDetectedEvent,self.__name,self.__faceDetectedFunction);

    def stopFaceDetection(self):
        self.unsubscribeToEvent(self.__faceDetectedEvent,self.__name);
        
    ####### END OF FACE DETECTION #######

    ####### BEGIN OF OBJECT DETECTION #######

    def _pictureDetectedEvent(self, objectName, objectSide, matching, ratio):
        pass;

    def startPictureDetection(self):
        self.__memory.subscribeToEvent(self.__pictureDetectedEvent,self.__name,self.__pictureDetectedFunction);

    def onPictureDetected(self, *_args):
        self.unsubscribeToEvent(self.__pictureDetectedEvent,self.__name);

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

        self.__memory.subscribeToEvent(self.__pictureDetectedEvent,self.__name,self.__pictureDetectedFunction);

    def stopPictureDetection(self):
        self.unsubscribeToEvent(self.__pictureDetectedEvent,self.__name);
        
    ####### END OF OBJECT DETECTION #######

    ####### BEGIN OF SPEECH RECOGNITION: SPEECH DETECTED #######

    def _speechDetectedEvent(self):
        pass;

    def startSpeechDetection(self):
        self.__memory.subscribeToEvent(self.__speechDetectedEvent,self.__name,self.__speechDetectedFunction);

    def onSpeechDetected(self, *_args):
        self.unsubscribeToEvent(self.__speechDetectedEvent,self.__name);

        self._speechDetectedEvent();

        self.__memory.subscribeToEvent(self.__speechDetectedEvent,self.__name,self.__speechDetectedFunction);

    def stopSpeechDetection(self):
        self.unsubscribeToEvent(self.__speechDetectedEvent,self.__name);
        
    ####### END OF SPEECH RECOGNITION: SPEECH DETECTED #######

    ####### BEGIN OF SPEECH RECOGNITION: WORD RECOGNIZED #######
    
    def _wordRecognizedEvent(self, word, rate):
        pass

    def onWordRecognized(self, *_args):
        word = "";
        rate = 0;
        self.unsubscribeToEvent(self.__wordRecognizedEvent, self.__name);
        taille = len(_args);
        if taille>2:
            if _args[0] == self.__wordRecognizedEvent :
                if len(_args[1]) > 1 :
                    word = _args[1][0];
                    rate = _args[1][1];
                    self._wordRecognizedEvent(word, rate);
                    
        self.__memory.subscribeToEvent(self.__wordRecognizedEvent, self.__name, self.__onWordRecognizedFunction);

    def startWordRecognition(self):
        #print("Lancement de la reconnaissance de mots");
        self.__memory.subscribeToEvent(self.__wordRecognizedEvent, self.__name, self.__onWordRecognizedFunction);
              
    def stopWordRecognition(self):
        self.unsubscribeToEvent(self.__wordRecognizedEvent, self.__name);
        #print("Fin de la reconnaissance de mots");

    ####### END OF SPEECH RECOGNITION #######

    ####### BEGIN OF SPEECH RECOGNITION: LAST WORD RECOGNIZED #######
    
    def _lastWordRecognizedEvent(self, word, rate):
        pass

    def onLastWordRecognized(self, *_args):
        word = "";
        rate = 0;
        self.unsubscribeToEvent(self.__lastWordRecognizedEvent, self.__name);
        taille = len(_args);
        if taille>2:
            if _args[0] == self.__lastWordRecognizedEvent :
                if len(_args[1]) > 1 :
                    word = _args[1][0];
                    rate = _args[1][1];
                    self._lastWordRecognizedEvent(word, rate);
                    
        self.__memory.subscribeToEvent(self.__lastWordRecognizedEvent, self.__name, self.__onLastWordRecognizedFunction);

    def startLastWordRecognition(self):
        #print("Lancement de la reconnaissance de mots");
        self.__memory.subscribeToEvent(self.__lastWordRecognizedEvent, self.__name, self.__onLastWordRecognizedFunction);
              
    def stopLastWordRecognition(self):
        self.unsubscribeToEvent(self.__lastWordRecognizedEvent, self.__name);
        #print("Fin de la reconnaissance de mots");

    ####### END OF SPEECH RECOGNITION #######

    ####### BEGIN OF TACTILE EVENT RECOGNITION #######

    def _tactileEvent(self, location, state):
        pass

    def onTactileEvent(self, *_args):
        self.unsubscribeToEvent(self.__handRightBackTouched, self.__name);
        self.unsubscribeToEvent(self.__handRightLeftTouched, self.__name);
        self.unsubscribeToEvent(self.__handRightRightTouched, self.__name);
        self.unsubscribeToEvent(self.__handLeftBackTouched, self.__name);
        self.unsubscribeToEvent(self.__handLeftLeftTouched, self.__name);
        self.unsubscribeToEvent(self.__handLeftRightTouched, self.__name);
        self.unsubscribeToEvent(self.__frontTactilTouched, self.__name);
        self.unsubscribeToEvent(self.__middleTactilTouched, self.__name);
        self.unsubscribeToEvent(self.__rearTactilTouched, self.__name);
        
        print _args
        print len(_args)
        if len(_args)==3:
            location = _args[0]
            state = _args[1]
            self._tactileEvent(location, state)
                    
        self.__memory.subscribeToEvent(self.__handRightBackTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__handRightLeftTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__handRightRightTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__handLeftBackTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__handLeftLeftTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__handLeftRightTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__frontTactilTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__middleTactilTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__rearTactilTouched, self.__name, self.__onTactileEventFunction);

    def startTactileEventRecognition(self):
        #print("Lancement de la reconnaissance de mots");
        self.__memory.subscribeToEvent(self.__handRightBackTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__handRightLeftTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__handRightRightTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__handLeftBackTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__handLeftLeftTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__handLeftRightTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__frontTactilTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__middleTactilTouched, self.__name, self.__onTactileEventFunction);
        self.__memory.subscribeToEvent(self.__rearTactilTouched, self.__name, self.__onTactileEventFunction);
              
    def stopTactileEventRecognition(self):
        self.unsubscribeToEvent(self.__handRightBackTouched, self.__name);
        self.unsubscribeToEvent(self.__handRightLeftTouched, self.__name);
        self.unsubscribeToEvent(self.__handRightRightTouched, self.__name);
        self.unsubscribeToEvent(self.__handLeftBackTouched, self.__name);
        self.unsubscribeToEvent(self.__handLeftLeftTouched, self.__name);
        self.unsubscribeToEvent(self.__handLeftRightTouched, self.__name);
        self.unsubscribeToEvent(self.__frontTactilTouched, self.__name);
        self.unsubscribeToEvent(self.__middleTactilTouched, self.__name);
        self.unsubscribeToEvent(self.__rearTactilTouched, self.__name);
        print("Fin de la reconnaissance tactiles");

    ####### END OF TACTILE EVENT RECOGNITION #######

