# -*- coding: utf8 -*
import sys, os
import re

sys.path.insert(0,'..')
from xml.dom import minidom
from xml.parsers.expat import ExpatError;

class XML():
  def __init__(self, directory, fileName):
    self.__fileName = directory+"/"+fileName;
    self.__doc = None;
    if not os.path.exists(directory):
      os.mkdir(directory)
        
  #test OK
  def exists(self):
    exists = False;
    try:
      with open(self.__fileName): exists = True;
    except IOError:
      exists = False;
    return exists;
  
  #test OK
  def parse(self):
    try :
      self.__doc = minidom.parse(self.__fileName);
    except IOError :
      self.__createDefaultFile();
    except ExpatError :
      self.__createDefaultFile();
    
  #test OK
  def getFaces(self):
    faces = [];
    if self.__doc.hasChildNodes():
      node = self.findNode(u'faces');
      if node.nodeName==u'faces':
        faceList = node.getElementsByTagName(u'face');
        for face in faceList:
          chaine = face.firstChild.nodeValue;
          chaine = chaine.encode('utf8');
          faces.append(chaine);
    return faces;
    
  #test OK
  def objectExists(self, name, side):
    exists = False;
    name = name.decode('utf8');
    side = side.decode('utf8');
    
    objects = self.getObjects();
    for tab in objects:
      if tab[0]==name and tab[1]==side:
        exists = True;
        break;
    
    return exists;
  
  #test OK
  def getObjects(self):
    objects = [];
    if self.__doc.hasChildNodes():
      node = self.findNode(u'objects');
      if node.nodeName==u'objects':
        objectList = node.getElementsByTagName(u'object');
        for object in objectList:
          name = "";
          side = "";
          for child in object.childNodes:
            if child.nodeName == u'name':
              name = child.firstChild.nodeValue;
            elif child.nodeName == u'side':
              side = child.firstChild.nodeValue;
          if name!="" and side!="":
            name = name.encode('utf8');
            side = side.encode('utf8');
            objects.append([name,side]);
    return objects;
    
  #test OK sauf avec accents
  def addFace(self, face):
    face = face.decode('utf8');
    faceElt = self.__doc.createElement(u'face');
    text = self.__doc.createTextNode(face);
    faceElt.appendChild(text);
    if self.__doc.hasChildNodes():
      node = self.findNode(u'faces');
      node.appendChild(faceElt);
      self.__save();
      self.__removeEmptyLines();
  
  #test OK sauf avec accents
  def addObject(self, name, side):
    name = name.decode('utf8');
    side = side.decode('utf8');
    objectElt = self.__doc.createElement(u'object');
    nameElt = self.__doc.createElement(u'name');
    sideElt = self.__doc.createElement(u'side');
    nameText = self.__doc.createTextNode(name);
    sideText = self.__doc.createTextNode(side);
    sideElt.appendChild(sideText);
    nameElt.appendChild(nameText);
    objectElt.appendChild(nameElt);
    objectElt.appendChild(sideElt);
    if self.__doc.hasChildNodes():
      node = self.findNode(u'objects');
      node.appendChild(objectElt);
      self.__save();
      self.__removeEmptyLines();    
    
  #test OK
  def removeFace(self, face):
    face = face.decode('utf8');
    if self.__doc.hasChildNodes():
      facesElt = self.findNode(u'faces');
      if facesElt.nodeName==u'faces':
        faceList = facesElt.getElementsByTagName(u'face');
        for faceElt in faceList:
          if faceElt.firstChild.nodeValue == face:
            sup = facesElt.removeChild(faceElt);
            sup.unlink();
            self.__save();
            self.__removeEmptyLines();
            break;
  #test OK    
  def removeObject(self, name, side):
    name = name.decode('utf8');
    side = side.decode('utf8');
    if self.__doc.hasChildNodes():
      node = self.findNode(u'objects');
      if node.nodeName==u'objects':
        objectList = node.getElementsByTagName(u'object');
        for object in objectList:
          nameValue = "";
          sideValue = "";
          for child in object.childNodes:
            if child.nodeName == u'name':
              nameValue = child.firstChild.nodeValue;
            elif child.nodeName == u'side':
              sideValue = child.firstChild.nodeValue;
            if name==nameValue and side==sideValue:
              sup = node.removeChild(object);
              sup.unlink();
              self.__save();
              self.__removeEmptyLines();
              break;
  
  #test OK  
  def removeAllFaces(self) :
    self.__removeAllNodes(u'faces');
  
  #test OK
  def removeAllObjects(self) :
    self.__removeAllNodes(u'objects');
    
  #test OK
  def findNode(self, nodeName):
    node = None;
    root = self.__doc.documentElement;
    nodeList = root.getElementsByTagName(nodeName);
    if nodeList.length == 1:
      node = nodeList[0];
      
    return node;
    
  #test OK
  def __removeAllNodes(self, nodeName):
    if self.__doc.hasChildNodes():
      oldElt = self.findNode(nodeName);
      newElt = self.__doc.createElement(nodeName);
      root = self.__doc.documentElement;
      root.insertBefore(newElt, oldElt);
      sup = root.removeChild(oldElt);
      sup.unlink();
      self.__save();
      self.__removeEmptyLines();
    
  #test OK
  def __removeEmptyLines(self):
    regx = re.compile("[\s\t]*\n");
    content = "";
    file = open(self.__fileName,"U");
    for line in file.readlines():
      if regx.match(line) is None:
        content+=line;
    file.close();

    file = open(self.__fileName, "w");
    file.write(content);
    file.close();
    
  #test OK
  def __createDefaultFile(self):
    self.__doc = minidom.Document();
    root = self.__doc.createElement(u'nao_database');
    facesEl = self.__doc.createElement(u'faces');
    objectsEl = self.__doc.createElement(u'objects');
    self.__doc.appendChild(root);
    root.appendChild(facesEl);
    root.appendChild(objectsEl);
    self.__save();
    
  #test OK
  def __save(self):
    xml = self.__doc.toprettyxml(encoding="UTF-8");
    file = open(self.__fileName, "w");
    file.write(xml);
    file.close();

if __name__=="__main__" :
  print(sys.getdefaultencoding());
  xml = XML("files/test.xml");
  xml.parse();
  #xml.addFace("Celine");
  #xml.addObject("pingouin", "face");
  #xml.addFace('Céline');
  #xml.addObject("pingouin", "féce");
  #xml.removeFace('Céline');
  print("Faces  :",xml.getFaces());
  print("Objets :",xml.getObjects());
