from functools import reduce
import re

class ModelPath:
    R = re.compile(r"[\/\\]")
    EXTENSION = ".mdl"

    def __init__(self, key):
        self.key = key
        self.models = []
        self.subpaths = {}
    
    def addSubPath(self,subdir):
        self.subpaths[subdir.key] = subdir

    def addModel(self,path,split=None):
        if split is None:
            split = ModelPath.R.split(path)
        if len(split) == 1:
            if not path in self.models:
                self.models.append(path)
        else:
            if not split[0] in self:
                childPath = ModelPath(split[0])
                self.addSubPath(childPath)
            else:
                childPath = self.getSubPath(split[0])
            childPath.addModel(path,split=split[1:])
        
    def getSubPath(self,key):
        return self.subpaths[key]

    def removeModel(self,model):
        self.models.remove(model)

    def popModel(self,index):
        return self.models.pop(index)

    def __len__(self):
        length = len(self.models)
        for path in self.subpaths:
            length += len(path)
        return length

    def __as_string(self,tabs = 0):        
        newtabs = tabs + 1
        s = "".join(["\t" for i in range(tabs)])
        s += "\"" + self.key + "\" {"
        if len(self.models) > 0:
            s += "\n"
            s += "".join(["\t" for i in range(newtabs)])
            s += str(self.models) + "\n"
        if len(self.subpaths) > 0:
            s += "\n"
            s += "".join(["\t" for i in range(newtabs)])
            for key in self.subpaths:
                sub = self.subpaths[key]
                s += sub.__as_string(newtabs)
        s += "".join(["\t" for i in range(tabs)])
        s += "}\n"
        return s

    def __str__(self):
        return self.__as_string()

    def __contains__(self,key):
        if key.endswith(ModelPath.EXTENSION):
            return key in self.models 
        else:
            return key in self.subpaths