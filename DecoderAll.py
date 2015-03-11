# -*- coding: utf-8 -*-
#Adrien
#07/11/2013

class Decoder():
    
    def __init__(self):
        self.codecs=["utf-8","ISO-8859-15","utf-16",""]
        
    def decode(self,text):
        for codec in self.codecs:
                try:
                    text=text.decode(codec)
                    return text
                except:
                  pass
                
    def encode(self,text):
        for codec in self.codecs:
                try:
                    text=text.encode(codec)
                    return text
                except:
                  pass
