
from naoqiVirtual import ALProxy
from Animation import Animation

"""
LED
"""

class LedsActuator:
    def __init__(self, proxy):
        assert proxy.__class__ is ALProxy;
        self.__proxy = proxy;
        self.__ledsNames, self.__colorsNames = self.__getLedsNames();
        self.__animation = Animation();

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

