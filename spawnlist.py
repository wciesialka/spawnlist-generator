import valvedict

class Spawnlist:

    ID = 0

    def __init__(self,name,parentid=0,icon="icon16/page.png"):
        self.id = Spawnlist.ID
        Spawnlist.ID += 1

        self.name = name
        self.parentid = parentid
        self.icon = icon

        self.contentCounter = 1
        self.contents = {}

        self.children = []
        self.parent = None

    def addChild(self,child):
        child.parent = self
        self.children.append(child)

    def createChild(self,name,icon="icon16/page.png"):
        child = Spawnlist(name,parentid=self.id,icon=icon)

        self.addChild(child)

        return child

    def __finishAddingContent(self):
        self.contentCounter += 1

    def addHeader(self,text):
        self.contents[f"{self.contentCounter}"] = {
            "type": "header",
            "text": text
            }
        self.__finishAddingContent()

    def addModel(self,modelpath):
        self.contents[f"{self.contentCounter}"] = {
            "type": "model",
            "model": modelpath
            }
        self.__finishAddingContent()

    def as_dict(self):
        return {
            "parentid": f"{self.parentid}",
            "icon": self.icon,
            "id": f"{self.id}",
            "contents": self.contents,
            "name": self.name,
            "version": "3"
        }
    
    def as_valve_dict(self):
        return valvedict.DictToKeyValues(self.as_dict())

    def __str__(self):
        return self.as_valve_dict()

    def __len__(self):
        length = 1
        for child in self.children:
            length += len(child) 
        return length