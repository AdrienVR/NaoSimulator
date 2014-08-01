
import os
from PySide.QtGui import QFileDialog, QUndoCommand, QUndoStack
from PySide.QtCore import QObject

class UndoFormat(QUndoCommand):
    def __init__(self):
        self.target = None
        self.modif = []
        self.originalText = ""
        self.next = ""

    def setOriginal(self, text):
        self.modif.append(text)
        self.originalText = text

    def setNext(self, text):
        self.next = text

    def undo(self):
        self.next = self.target.toPlainText()
        self.target.setPlainText(self.originalText)

    def redo(self):
        self.originalText = self.target.toPlainText()
        if self.next.strip()!="":
            self.target.setPlainText(self.next)

class EditeurPython(QObject):
    def __init__(self, a=None):
        self.undoFormat = UndoFormat()
        self.undoFormat.target = self.textEdit

        self.lastModif = "else"
        self.cancelFormat = False

        #self.undoStack = QUndoStack()
        ###################################### INTERFACE   #####################################################
    def initEditeur(self):
        fenX=self.centralwidget.width()
        sizes=[]
        sizes.append(fenX/2);
        sizes.append(fenX/2);
        self.splitter.setSizes(sizes)
        self.resizeEvent(0)

    def initVue3D(self):
        fenX=self.centralwidget.width()
        fenY=self.centralwidget.height()
        sizes=[]
        sizes.append(fenX/2);
        sizes.append(fenX/2);
        self.splitter.setSizes(sizes)
        sizes=[]
        sizes.append(fenY/2);
        sizes.append(fenY/2);
        self.splitterHB.setSizes(sizes)
        self.resizeEvent(0)
    def initPupitre(self):
        fenX=self.centralwidget.width()
        fenY=self.centralwidget.height()
        sizes=[]
        sizes.append(fenX/2);
        sizes.append(fenX/2);
        self.splitter.setSizes(sizes)
        sizes=[]
        sizes.append(fenY/2);
        sizes.append(fenY/2);
        self.splitterHB.setSizes(sizes)
        self.resizeEvent(0)

    def initTextEdit(self):
        a=open(os.path.join("dep","codeInit.py"))
        b=a.readlines()
        a.close()
        a=""
        for x in b:
            a+=x
        self.textEdit.setText(a)


    ###################################### MENU FORMAT #####################################################

    def uncomment(self):
        fullText=unicode(self.textEdit.toPlainText())#
        text=unicode(self.getHighLightedText(self.textEdit))#
        if text.strip() == "":return
        self.undoFormat.setOriginal(fullText)
        self.lastModif = "format"
        if text=="":return
        a,b=self.getPosInText(fullText,text)
        fullText=fullText[:a]+fullText[a:b].replace("\n##","\n")+fullText[b:]
        self.textEdit.setPlainText(fullText)

    def comment(self):
        fullText=unicode(self.textEdit.toPlainText())#
        text=unicode(self.getHighLightedText(self.textEdit))#
        if text.strip() == "":return
        self.undoFormat.setOriginal(fullText)
        self.lastModif = "format"
        text=self.getHighLightedText(self.textEdit)#
        if text=="":return
        a,b=self.getPosInText(fullText,text)
        fullText=fullText[:a]+fullText[a:b].replace("\n","\n##")+fullText[b:]
        self.textEdit.setPlainText(fullText)

    def unindent(self):
        fullText=unicode(self.textEdit.toPlainText())#
        text=unicode(self.getHighLightedText(self.textEdit))#
        if text.strip() == "":return
        self.undoFormat.setOriginal(fullText)
        self.lastModif = "format"
        text=self.getHighLightedText(self.textEdit)#
        if text=="":return
        a,b=self.getPosInText(fullText,text)
        fullText=fullText[:a]+fullText[a:b].replace("\n\t","\n").replace("\n\ ","\n")+fullText[b:]
        self.textEdit.setPlainText(fullText)
        self.undoFormat.setNext(fullText)

    def indent(self):
        fullText=unicode(self.textEdit.toPlainText())#
        text=unicode(self.getHighLightedText(self.textEdit))#
        if text.strip() == "":return
        self.undoFormat.setOriginal(fullText)
        self.lastModif = "format"
        text=self.getHighLightedText(self.textEdit)#
        if str(text)=="":return
        a,b=self.getPosInText(fullText,text)
        fullText=fullText[:a]+fullText[a:b].replace("\n","\n\t")+fullText[b:]
        self.textEdit.setPlainText(fullText)
        self.undoFormat.setNext(fullText)

    ###################################### MENU EDITION #####################################################
    def paste(self):
        self.textEdit.paste()

    def cut(self):
        self.textEdit.cut()

    def copy(self):
        self.textEdit.copy()

    def delete(self):
        fullText=self.textEdit.toPlainText()#
        text=self.getHighLightedText(self.textEdit)#
        a,b=self.getPosInText(fullText,text)
        fullText=fullText[:a]+fullText[b:]
        self.textEdit.setPlainText(fullText)

    def getHighLightedText(self, container):
        a=container.textCursor()
        if a.anchor()<a.position():
            text=container.toPlainText()[a.anchor():a.position()]
        else:
            text=container.toPlainText()[a.position():a.anchor()]
        return text

    def getPosInText(self, text, piece):
        text=str(text)
        nb=text.index(piece)
        return nb-1,nb+len(piece)

    def redo(self):
        self.lastModif = "undo"
        if self.cancelFormat :
            self.undoFormat.redo()
        else :
            self.textEdit.redo()

    def undo(self):
        self.lastModif = "undo"
        if self.cancelFormat :
            self.undoFormat.undo()
        else :
            self.textEdit.undo()

    ###################################### MENU FICHIER #####################################################
    def setStar(self,modif=True):
        if self.lastModif == "format":
            self.cancelFormat = True
        elif self.lastModif == "else" :
            self.cancelFormat = False
        if modif and not self.modified:
            self.setWindowTitle(self.windowTitle()+" *")
            self.modified = True
        elif not modif:
            self.setWindowTitle(self.windowTitle().replace(" *",""))
            self.modified = False
        self.lastModif = "else"

    def setColors(self):
        #boucle infinie sinon
        return
        self.htmlSet = not self.htmlSet
        if self.htmlSet:return
##        fullText=str(self.textEdit.toPlainText())
##        htmlText=highlight(fullText, PythonLexer(), HtmlFormatter())
##        self.textEdit.setHtml(htmlText)


    def openFile(self):
        fileName = QFileDialog.getOpenFileName(self,
                 "Ouvrir fichier", "/", "Python Files (*.py)")[0]
        if fileName!="":
            self.fileName=fileName
            self.setWindowTitle(self.name+" - "+self.fileName)
        else :
            return
        f=open(fileName)
        self.textEdit.setPlainText(unicode(f.read()))
        f.close()
        self.setStar(False)

    def save(self):
        if self.fileName!="":
            try :
                f=open(self.fileName,"w")
                txt=self.textEdit.toPlainText()
                f.write(txt)
                f.close()
            except Exception,e:
                print "Error :",e;
            self.setStar(False)
            self.setWindowTitle(self.name+" - "+self.fileName)
        else:
            self.saveUnder()

    def saveUnder(self):
        fileName = QFileDialog.getSaveFileName(self,
                 "Enregistrer fichier", "/", "Python Files (*.py)")[0]
        self.fileName=fileName
        if fileName!="":
            self.save()
