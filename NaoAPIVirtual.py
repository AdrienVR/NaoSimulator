
#from naoqi import ALProxy, ALBroker;
from naoqiVirtual import ALProxy, ALBroker;

from Animation import Animation
import time, threading, struct;

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
            self.__player = ALProxy();
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
#         self.__voice.setParallelism(value);
#         self.__motors.setParallelism(value);
#         self.__leds.setParallelism(value);
#         self.__sound.setParallelism(value);
#         self.__player.setParallelism(value);

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

    def getPlayer(self):
        return self.__player;

    def getSound(self):
        return self.__player;

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
        self.__parallelism = False;

    def setParallelism(self, value):
        self.__parallelism = value;

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
        self.__parallelism = False;

    def setParallelism(self, value):
        self.__parallelism = value;

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
        self.__proxy.addMotionAnimation(motorNumber, motorAngle, time)

    #test OK
    def resetAnimation(self):
        self.__proxy.resetAnimation();

    #test OK
    #blocking call
    def playAnimation(self):
        self.__proxy.playAnimation();

    def getAnimationData(self):
        return self.__proxy.getAnimationData();

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


"""
LED
"""

class LedsActuator:
    def __init__(self, proxy):
        assert proxy.__class__ is ALProxy;
        self.__proxy = proxy;
        self.__ledsNames, self.__colorsNames = self.__getLedsNames();
        self.__animation = Animation();
        self.__parallelism = False;

    def setParallelism(self, value):
        self.__parallelism = value;

    #test OK
    def getLedsNames(self):
        return self.__ledsNames;

    #test OK
    def __getLedsNames(self):
        names = [];
        colorsNames = {};
        for i in range(1,9):
            name = "RightFaceLed%s" %(i);
            names.append(name);
            degree = (i-1)*45;
            red = "Face/Led/Red/Right/%sDeg/Actuator/Value" %(degree);
            green = "Face/Led/Green/Right/%sDeg/Actuator/Value" %(degree);
            blue = "Face/Led/Blue/Right/%sDeg/Actuator/Value" %(degree);
            tab = [red,green,blue];
            colorsNames[name] = tab;
        for i in range(8,0,-1):
            name = "LeftFaceLed%s" %(i);
            names.append(name);
            degree = (i-1)*45;
            red = "Face/Led/Red/Left/%sDeg/Actuator/Value" %(degree);
            green = "Face/Led/Green/Left/%sDeg/Actuator/Value" %(degree);
            blue = "Face/Led/Blue/Left/%sDeg/Actuator/Value" %(degree);
            tab = [red,green,blue];
            colorsNames[name] = tab;

        return names, colorsNames;

    #test OK
    def getLedName(self, ledsNumber):
        assert ledsNumber < len(self.__ledsNames);
        return self.__ledsNames[ledsNumber];

    #test OK
    def getLedsNumber(self):
        return len(self.__ledsNames);

    #test OK
    def allLedsOn(self):
        name = "FaceLeds";
        self.__proxy.on(name);

    #test OK
    def rightLedsOn(self):
        name = "RightFaceLeds";
        self.__proxy.on(name);

    #test OK
    def leftLedsOn(self):
        name = "LeftFaceLeds";
        self.__proxy.on(name);

    #test OK
    def allLedsOff(self):
        name = "FaceLeds";
        self.__proxy.off(name);

    #test OK
    def rightLedsOff(self):
        name = "RightFaceLeds";
        self.__proxy.off(name);

    #test OK
    def leftLedsOff(self):
        name = "LeftFaceLeds";
        self.__proxy.off(name);

    #test OK
    def getIntensity(self, ledNumber):
        name = self.getLedName(ledNumber);
        return self.__proxy.getIntensity(name);

    #test OK
    #renvoie red, green, blue
    def getColor(self, ledNumber):
        red, green, blue = 0,0,0;

        name = self.getLedName(ledNumber);
        tabColor = self.__colorsNames[name];
        #print self.__colorsNames

        redIntensity = self.__proxy.getIntensity(tabColor[0]);
        greenIntensity = self.__proxy.getIntensity(tabColor[1]);
        blueIntensity = self.__proxy.getIntensity(tabColor[2]);

        red = int(redIntensity*255);
        green = int(greenIntensity*255);
        blue = int(blueIntensity*255);

        return red, green, blue;

    #test OK
    def setIntensity(self, ledNumber, intensity):
        name = self.getLedName(ledNumber);
        self.__proxy.setIntensity(name, intensity);

    #test OK
    def setIntensities(self, ledNumber, redIntensity, greenIntensity, blueIntensity):
        name = self.getLedName(ledNumber);
        tabColor = self.__colorsNames[name];
        self.__proxy.setIntensity(tabColor[0], redIntensity);
        self.__proxy.setIntensity(tabColor[1], greenIntensity);
        self.__proxy.setIntensity(tabColor[2], blueIntensity);

    #test OK
    def fadeIntensity(self, ledsNumber, intensity, duration):
        name = self.getLedName(ledsNumber);
        self.__proxy.fade(name, intensity, duration);

    #test OK
    def setColor(self, ledsNumber, red, green, blue):
        name = self.getLedName(ledsNumber);
        self.__setColor(name, red, green, blue);

    #test OK
    def __setColor(self, ledName, red, green, blue):
        assert type(red) is int;
        assert type(green) is int;
        assert type(blue) is int;
        assert red >= 0 and red <= 255;
        assert green >= 0 and green <= 255;
        assert blue >= 0 and blue <= 255;
        tabColor = self.__colorsNames[ledName];

        redIntensity = 0;
        greenIntensity = 0;
        blueIntensity = 0;

        if red != 0 :
            redIntensity = red/255.0;
        if green != 0 :
            greenIntensity = green/255.0;
        if blue != 0 :
            blueIntensity = blue/255.0;

##        print tabColor
##        print "ok"
##        print self.__colorsNames
        self.__proxy.setIntensity(tabColor[0], redIntensity);
        self.__proxy.setIntensity(tabColor[1], greenIntensity);
        self.__proxy.setIntensity(tabColor[2], blueIntensity);


    #test OK
    def fadeColor(self, ledNumber, red, green, blue, duration):
        name = self.getLedName(ledNumber);
        color = self.__RGBToInt(red, green, blue);

        self.__proxy.fadeRGB (name, color, duration);

    #test OK
    def addLedAnimation(self, ledNumber, red, green, blue, time):
        name = self.getLedName(ledNumber);
        rgb = self.__RGBToInt(red, green, blue);
        self.__animation.addValue(name, rgb, time);

    #test OK
    def resetAnimation(self):
        self.__animation.reset();

    #test OK
    def playAnimation(self):
        names = self.__animation.getNames();
        values = self.__animation.getValues();
        times = self.__animation.getTimes();
        threads = [];

        i = 0;
        for name in names :
            valuesTab = values[i];
            timesTab = times[i];
            thread = threading.Thread(None, self.__playLedAnimation, None, (name, valuesTab, timesTab), {});
            threads.append(thread);
            i=i+1;

        for thread in threads:
            thread.start();

    #test OK
    def __playLedAnimation(self, name, values, times):
        assert len(values) == len(times);
        durations = self.__getDurations(times);
        for i in range(len(times)):
            duration = durations[i];
            color = values[i];
            time.sleep(duration);
            red,green,blue = self.__intToRGB(color);
            self.__setColor(name, red, green, blue);

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

    #test OK
    def displayLedsNumber(self, ledsWord):
        for i in range(len(self.__ledsNames)):
            print ledsWord,i, ":", self.__ledsNames[i];

    #test OK
    def displayAnimation(self, ledWord, valueWord, timeWord, characterNumbers):
        names = self.__animation.getNames();
        values = self.__animation.getValues();
        times = self.__animation.getTimes();

        for i in range(len(names)):
            ledNumber = self.__ledsNames.index(names[i]);
            print ledWord,ledNumber," : ";
            for j in range(len(values[i])):
                string = "    %s : %s" %(valueWord, hex(values[i][j]));
                string = self.addSpaces(string, characterNumbers);
                print string,"-",timeWord,":",times[i][j];

    #test OK
    #doublon !!!!
    def addSpaces(self, string, characterTotalNumbers):
        characterNumbers = len(string);
        if characterTotalNumbers > characterNumbers:
            spaceNumbers = characterTotalNumbers - characterNumbers;
            string = string+spaceNumbers*' ';
        return string;

    #test OK
    def __displayColorsNames(self):

        for name in self.__ledsNames:
            print name,' :';
            tab = self.__colorsNames[name];
            print "   ",tab[0];
            print "   ",tab[1];
            print "   ",tab[2];


    #test OK
    def __RGBToInt(self, red, green, blue):
        assert type(red) is int;
        assert type(green) is int;
        assert type(blue) is int;
        assert red >= 0 and red <= 255;
        assert green >= 0 and green <= 255;
        assert blue >= 0 and blue <= 255;

        color = int('%02x%02x%02x' %(red, green, blue), 16);

        #to check
        #print hex(color);

        return color;

    #test OK
    def __intToRGB(self, rgb):
        blue, green, red = [(rgb >> (8*i)) & 255 for i in range(3)];
        return red,green,blue;

    def test(self):
        rgb = self.__RGBToInt(85,127,12);
        print self.__intToRGB(rgb);

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
        print "START SPEECH RECOGNITION 2";

    #test OK
    def stopSpeechRecognition(self):
        print "STOP SPEECH RECOGNITION 1";
        print "STOP SPEECH RECOGNITION 2";
        return

"""
2 classes définies dans ce fichier

Affichage du robot : VideoDisplayer
Reconaissance visuelle : VisualRecognition
"""

class VideoDisplayer:
    def __init__(self, proxy):
        #assert type(proxy) is ALProxy;
        assert proxy.__class__ is ALProxy;
        self.__proxy = proxy;
        self.__frame = None;
        self.__resolution=2;
        self.__colorSpace=11;
        self.__fps=15;
        self.__name = "test";
        self.__isRunning = False;

    #test OK
    def displayVideo(self, title):
        thread = threading.Thread(None, self.__displayVideo, None, (title,), {});
        thread.start();
        time.sleep(5);
        return self.__frame;

    #test OK
    def isRunning(self):
        return self.__isRunning;

    #test OK
    def close(self):
        self.__frame.quit();
        self.__unsubscribeVideo();
        self.__isRunning = False;

    #test OK
    def __subscribeVideo(self):
        self.__name = self.__proxy.subscribe(self.__name, self.__resolution, self.__colorSpace, self.__fps);
        self.__isRunning = True;

    #test OK
    def __unsubscribeVideo(self):
        self.__proxy.unsubscribe(self.__name);
        self.__isRunning = False;

    #test OK
    def __getPicture(self):
        image = self.__proxy.getImageRemote(self.__name);
        width = image[0];
        height = image[1];
        data =  image[6];

        picture = Image.fromstring("RGB", (width, height), data);
        self.__proxy.releaseImage(self.__name);

        return picture;

    #test OK
    def __frameClosing(self):
        self.__frame.destroy();
        self.__unsubscribeVideo();
        self.__isRunning = False;
        self.__frame = None;

    #test OK
    def __displayVideo(self, title):

        self.__frame = Tk();
        self.__frame.title(title);

        canvas = Canvas(self.__frame)
        canvas.configure(width=640, height=480)
        canvas.configure(bg="white", bd =2, relief=SUNKEN)
        canvas.pack(fill=X, side=TOP, expand=YES)

        self.__subscribeVideo()
        self.__tick(canvas)
        self.__frame.protocol("WM_DELETE_WINDOW", self.__frameClosing);
        self.__frame.mainloop()

    #test OK
    def __tick(self, canvas):
        self.photo = ImageTk.PhotoImage(self.__getPicture());
        self.item = canvas.create_image(320,240,image=self.photo);
        self.__frame.after(1, lambda : self.__tick(canvas));


class VisualRecognition():
    def __init__(self, faceRecoProxy, naoXML):
        #assert type(faceRecoProxy) is ALProxy;
        assert faceRecoProxy.__class__ is ALProxy
        self.__recoProxy = faceRecoProxy;
        self.__xml = naoXML;

    #test OK
    def learnFace(self, title, label, boutonTitle):
        self.__display(title, label, boutonTitle);

    #test PAS OK
    def removeFace(self, name):
        isRemoved = False;
        if self.__recoProxy.forgetPerson(name) :
            self.__xml.removeFace(name);
            isRemoved = True;
        return isRemoved;

    #test OK
    def removeAllFaces(self):
        isRemoved = False;
        if self.__recoProxy.clearDatabase() :
            self.__xml.removeAllFaces();
            isRemoved = True;
        return isRemoved;

    #test OK
    def getFaces(self):
        return self.__xml.getFaces();

    #test OK
    def displayFaces(self):
        faces = self.__xml.getFaces();
        for face in faces:
            print face;

    #test OK
    def learnObject(self, name, side):
        if not self.__xml.objectExists(name, side) :
            self.__xml.addObject(name, side);

    #test OK
    def removeObject(self, name, side):
        self.__xml.removeObject(name, side);

    #test OK
    def removeAllObjects(self):
        self.__xml.removeAllObjects();

    #test OK
    def getObjects(self):
        return self.__xml.getObjects();

    #test OK
    def displayObjects(self):
        objects = self.__xml.getObjects();
        for tabObject in objects:
            print "Name :",tabObject[0];
            print "Side :",tabObject[1];

    #test OK
    def __display(self, title, label, boutonTitle):

        self.__frame = Tk();
        #self.__win = TopLevel(self.__frame);
        self.__frame.title(title);
        #self.__win.title(title);

        labelInfo = Label(self.__frame, text=label, fg='black');
        #labelInfo = Label(self.__win, text=label, fg='black');
        labelInfo.pack();

        visageNameStringVar = StringVar();
        visageNameStringVar.set("OK");
        textArea = Entry(self.__frame, textvariable=visageNameStringVar);
        #textArea = Entry(self.__win, textvariable=visageNameStringVar);
        textArea.focus_set();
        textArea.pack();

        button=Button(self.__frame, text=boutonTitle, command=lambda:self.__onButtonClicked(visageNameStringVar));
        #button=Button(self.__win, text=boutonTitle, command=lambda:self.__onButtonClicked(visageNameStringVar));
        button.pack()

        self.__frame.protocol("WM_DELETE_WINDOW", self.__frameClosing);
        #self.__win.protocol("WM_DELETE_WINDOW", self.__frameClosing);
        self.__frame.mainloop();
        #self.__win.mainloop();

    #test OK
    def __learnFace(self, name):
        isLearned = False;
        if name in self.__xml.getFaces() :
            isLearned = self.__recoProxy.reLearnFace(name);
        else:
            if self.__recoProxy.learnFace(name) :
                self.__xml.addFace(name);
                isLearned = True;
        return isLearned;

    #test OK
    def __onButtonClicked(self, visageNameStringVar):
        print type(visageNameStringVar);
        nomVisage = visageNameStringVar.get();
        print "enregistrer ",nomVisage;
        #TODO : externaliser cette information.
        print "Enregistrement OK :",self.__learnFace(nomVisage);
        visageNameStringVar.set("");

    #test OK
    def __frameClosing(self):
        self.__frame.destroy();




