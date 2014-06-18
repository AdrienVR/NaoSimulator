
from naoqiVirtual import ALProxy

class SpeechRecognitionSensor:
    def __init__(self, proxy):
        #assert type(proxy) is ALProxy;
        assert proxy.__class__ is ALProxy;
        self.__proxy = proxy;
        self.__languages = self.__proxy.getAvailableLanguages();

    #test OK
    def setPreciseVocabulary(self, words):
        self.__proxy.setWordListAsVocabulary(words);

    #Pas fait de test
    def setApproximativeVocabulary(self, words):
        self.__proxy.setVocabulary(words, true);

    #test OK
    #doublon avec Voice
    def getAvailableLanguages(self):
        return self.__languages;

    #test OK
    #doublon avec Voice
    def getLanguage(self):
        return self.__proxy.getLanguage();

    #test OK
    #doublon avec Voice
    def setLanguage(self, language):
        assert language in self.__languages;
        self.__proxy.setLanguage(language);

    #test OK
    def startSpeechRecognition(self):
        print "START SPEECH RECOGNITION 1";
        self.__proxy.subscribe("naoEnib");
        print "START SPEECH RECOGNITION 2";

    #test OK
    def stopSpeechRecognition(self):
        print "STOP SPEECH RECOGNITION 1";
        self.__proxy.unsubscribe("naoEnib");
        print "STOP SPEECH RECOGNITION 2";
        return

        
