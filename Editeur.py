
import os
from PySide.QtGui import QFileDialog

##from pygments import highlight
##from pygments.lexers import PythonLexer
##from pygments.formatters import HtmlFormatter

class EditeurPython(object):
    def __init__(a=None):
        pass
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
        fullText=self.textEdit.toPlainText()#
        text=self.getHighLightedText(self.textEdit)#
        if text=="":return
        a,b=self.getPosInText(fullText,text)
        fullText=fullText[:a]+fullText[a:b].replace("\n##","\n")+fullText[b:]
        self.textEdit.setPlainText(fullText)

    def comment(self):
        fullText=self.textEdit.toPlainText()#
        text=self.getHighLightedText(self.textEdit)#
        if text=="":return
        a,b=self.getPosInText(fullText,text)
        fullText=fullText[:a]+fullText[a:b].replace("\n","\n##")+fullText[b:]
        self.textEdit.setPlainText(fullText)

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
        self.textEdit.redo()

    def undo(self):
        self.textEdit.undo()

    ###################################### MENU FICHIER #####################################################
    def setStar(self,modif=True):
        if modif and not self.modified:
            self.setWindowTitle(self.windowTitle()+" *")
            self.modified = True
        elif not modif:
            self.setWindowTitle(self.windowTitle().replace(" *",""))
            self.modified = False

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
                 "Ouvrir fichier", "/", "Python Files (*.py)")
        if fileName!="":
            self.fileName=fileName
            self.setWindowTitle(self.name+" - "+self.fileName)
        else :
            return
        try :
            f=open(fileName)
            self.textEdit.setPlainText(f.read())
            f.close()
            self.setStar(False)
        except Exception,e:
            print "Error :",e;

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
                 "Enregistrer fichier", "/", "Python Files (*.py)")
        self.fileName=fileName
        if fileName!="":
            self.save()
