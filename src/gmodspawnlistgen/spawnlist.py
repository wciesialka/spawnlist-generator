from gmodspawnlistgen.valvetable import ValveTableFile

class Spawnlist:

    ID = 0

    def __init__(self, name: str, parent_id: int = 0, icon: str = "icon16/page.png"):
        self.id = Spawnlist.ID
        Spawnlist.ID += 1

        self.name = name
        self.parent_id = parent_id
        self.icon = icon

        self.n_contents = 0
        self.contents = {}

        self.children = []
        self.parent = None

    def add_child(self, child: Spawnlist):
        self.children.append(child)
        child.set_parent(self)
    
    def set_parent(self, parent: Spawnlist):
        self.parent = parent
    
    def create_child(self, name: str, icon: str = "icon16/page.png") -> Spawnlist:
        child = Spawnlist(name, self.id, icon)
        self.add_child(child)
        return child

    def add_header(self, text: str):
        self.contents[f"{self.n_contents}"] = {
            "type": "header",
            "text": text
        }
        self.n_contents += 1
    
    def add_model(self, path: str):
        self.contents[f"{self.n_contents}"] = {
            "type": "model",
            "model": path
        }
        self.n_contents += 1
    
    def as_dict(self):
        return {
            "parentid": str(self.parent_id),
            "icon": self.icon,
            "id": str(self.id),
            "contents": self.contents,
            "name": self.name,
            "version": "3"
        }
    
    def as_valve_table(self):
        return ValveTableFile.dict_to_table("TableToKeyValues", self.as_dict())
    
    def __str__(self):
        return self.as_valve_table()
    
    def __len__(self):
        return 1 + len(self.children)