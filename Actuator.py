

from naoqiVirtual import ALProxy
from Animation import Animation

"""
2 classes :

    - VoiceActuator
    - MotorsActuator
"""

#Validated class
class VoiceActuator:
    def __init__(self, proxy):
        #assert type(proxy) is ALProxy;
        # should it be this (following) ?
        assert proxy.__class__ is ALProxy;
        self.__proxy = proxy;
        self.__languages = self.__proxy.getAvailableLanguages();

    #test OK
    def say(self, text):
        self.__proxy.say(text);

    #test OK
    def setVolume(self, value):
        assert value >= 0 and value <= 1;
        self.__proxy.setVolume(value);

    #test OK
    def getVolume(self):
        return self.__proxy.getVolume();

    #test OK
    def getAvailableLanguages(self):
        return self.__languages;

    #test OK
    def getLanguage(self):
        return self.__proxy.getLanguage();

    #test OK
    def setLanguage(self, language):
        assert language in self.__languages;
        self.__proxy.setLanguage(language);
    
class MotorsActuator:
    def __init__(self, proxy):
        #assert type(proxy) is ALProxy;
        assert proxy.__class__ is ALProxy;
        self.__proxy = proxy;
        self.__joints = self.__proxy.getJointNames("Body");
        self.__limits = self.__proxy.getLimits("Body");
        self.__animation = None#Animation();

    #test OK
    def getJointNames(self):
        return self.__joints;

    #test OK
    def getMotorName(self, motorNumber):
        assert motorNumber < len(self.__joints);
        return self.__joints[motorNumber];

    #test OK
    def getMinAngle(self, motorNumber):
        return self.__limits[motorNumber][0];

    #test OK
    def getMaxAngle(self, motorNumber):
        return self.__limits[motorNumber][1];

    #test OK
    def getMaxVelocity(self, motorNumber):
        return self.__limits[motorNumber][2];

    #test OK
    def getStiffnesses(self):
        return self.__proxy.getStiffnesses("Body");

    #test OK
    def setStiffnesses(self, value):
        assert value >= 0 and value <= 1;
        self.__proxy.setStiffnesses("Body", value);

    #test OK
    def getStiffness(self, motorNumber):
        stiffness = -1.0;
        name = self.getMotorName(motorNumber);
        stiffnessTab = self.__proxy.getStiffnesses(name);
        if len(stiffnessTab) > 0 :
            stiffness = stiffnessTab[0];
        return stiffness;

    #test OK
    def setStiffness(self, motorNumber, value):
        name = self.getMotorName(motorNumber);
        self.__proxy.setStiffnesses(name, value);

    #test OK
    def getMotorAngles(self):
        return self.__proxy.getAngles("Body", True);

    #test OK
    def getMotorAngle(self, motorNumber):
        angle = None;
        
        name = self.getMotorName(motorNumber);
        tab = self.__proxy.getAngles(name, True);
        if len(tab)>0:
            angle = tab[0];
        
        return angle;

    #test OK
    #blocking call
    def setMotorAngle(self, motorNumber, motorAngle, time):
        name = self.getMotorName(motorNumber);
        isAbsolute = True;
        self.__proxy.angleInterpolation(name, motorAngle, time, isAbsolute);

    #test OK
    def addMotionAnimation(self, motorNumber, motorAngle, time):
        name = self.getMotorName(motorNumber);
        self.__animation.addValue(name, motorAngle, time);

    #test OK
    def resetAnimation(self):
        self.__animation.reset();

    #test OK
    #blocking call
    def playAnimation(self):
        names = self.__animation.getNames();
        angles = self.__animation.getValues();
        times = self.__animation.getTimes();
        isAbsolute = True;
        self.__proxy.angleInterpolation(names, angles, times, isAbsolute);

    def getAnimationData(self):
        names = self.__animation.getNames();
        angles = self.__animation.getValues();
        times = self.__animation.getTimes();
        return names, angles, times;

    #test OK
    def displayAnimation(self, motorWord, angleWord, timeWord, characterNumbers):
        names = self.__animation.getNames();
        angles = self.__animation.getValues();
        times = self.__animation.getTimes();

        for i in range(len(names)):
            motorNumber = self.__joints.index(names[i]);
            print motorWord,motorNumber," : ";
            for j in range(len(angles[i])):
                string = "    %s : %s" %(angleWord, angles[i][j]);
                string = self.addSpaces(string, characterNumbers); 
                print string,"-",timeWord,":",times[i][j];

    #test OK
    def displayMotorsNumber(self):
        for i in range(len(self.__joints)):
            print i, ":", self.__joints[i];

    #test OK
    def displayMotorAngles(self, motorWord, characterNumbers):
        angles = self.getMotorAngles();
        for i in range(len(self.__joints)):
            joint = "%s %s" %(motorWord, i);
            joint = self.addSpaces(joint, characterNumbers); #take account of the space before ":"
            data = "%s : %s" %(joint, angles[i]);
            print data

    #test OK
    def addSpaces(self, string, characterTotalNumbers):
        characterNumbers = len(string);
        if characterTotalNumbers > characterNumbers:
            spaceNumbers = characterTotalNumbers - characterNumbers;
            string = string+spaceNumbers*' ';
        return string;
