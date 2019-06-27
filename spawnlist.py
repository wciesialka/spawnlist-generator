import valvedict

class Spawnlist:

    def __init__(self,name,id=1,parentid=0,icon="icon16/page.png"):
        self.id = id

        self.name = name
        self.parentid = parentid
        self.icon = icon

        self.contentCounter = 1
        self.contents = {}

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
        return {"TableToKeyValues": {
            "parentid": f"{self.parentid}",
            "icon": self.icon,
            "id": f"{self.id}",
            "contents": self.contents,
            "name": self.name,
            "version": "3"
        }}
    
    def as_valve_dict(self):
        return valvedict.dict_as_valve_dict(self.as_dict())

    def as_string(self):
        s = ""
        lines = self.as_valve_dict()
        for line in lines:
            s += line + "\n"
        return s

    def __str__(self):
        return self.as_string()