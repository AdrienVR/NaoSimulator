
"""
Extrait originalement de NaoStructure.py
"""

class Animation:
    def __init__(self):
        self.__values = {}
        self.__times = {}

    #test OK
    def addValue(self, name, value, time):
        if name not in self.__values.keys():
            self.__values[name] = [];
            self.__times[name] = [];

        self.__values[name].append(value);
        self.__times[name].append(time);

    #test OK
    def reset(self):
        self.__values.clear();
        self.__times.clear();

    #test OK
    def getNames(self):
        return self.__values.keys();

    #test OK
    #todo vérifier l'ordre des values
    def getValues(self):
        return self.__values.values();

    #test OK
    #todo vérifier l'ordre des values
    def getTimes(self):
        return self.__times.values();
