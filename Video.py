
from naoqiVirtual import ALProxy


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


        
