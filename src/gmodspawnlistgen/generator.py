from gmodspawnlistgen.config import SpawnlistGeneratorConfig
from gmodspawnlistgen.spawnlist import Spawnlist
from gmodspawnlistgen.modelpath import ModelPath
from gmodspawnlistgen.valvetable import ValveTableFile
import os
import vpk

class SpawnlistGenerator:

    def __init__(self, config: SpawnlistGeneratorConfig):
        self.__config = config

    @property
    def gmod_path(self):
        return self.__config.gmod_path
    
    @property
    def spawnlist_dir(self):
        return self.gmod_path / "garrysmod" / "settings" / "spawnlist"
    
    def get_latest_spawnlist_id(self):
        path = self.spawnlist_dir
        files = sorted([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
        last_file = files[-1]
        last_id = last_file[:3]
        return int(last_id)
    
    def get_new_spawnlist_id(self):
        return self.get_latest_spawnlist_id() + 1

    def populate_spawnlist(self, spawnlist: Spawnlist, structure: ModelPath):
        models = sorted(structure.models)
        subpaths = structure.subpaths

        for subpath_key in sorted(subpaths.keys()):
            subpath = subpaths[subpath_key]

            if len(subpath.models) > 0:
                spawnlist.add_header(subpath_key)
                to_pop = []
                for i, model in enumerate(subpath.models):
                    spawnlist.add_model(model)
                    to_pop.append(i)
                for i in sorted(to_pop, reverse=True):
                    subpath.pop_model(i)
            if len(subpath.subpaths) > 0:
                child_spawnlist = spawnlist.create_child(subpath_key)
                self.populate_spawnlist(child_spawnlist, subpath)
        
        if len(models) > 0:
            spawnlist.add_header(structure.key)
            for model in models:
                spawnlist.add_model(model)
    
    def spawnlist_from_vpk(self, name: str, pak: vpk.VPKFile) -> Spawnlist:
        Spawnlist.ID = self.get_new_spawnlist_id()
        spawnlist = Spawnlist(name)
        structure = ModelPath("root")

        for pakfile in pak:
            if pakfile.endswith(ModelPath.MODEL_EXTENSION):
                structure.add_model(pakfile)
        
        self.populate_spawnlist(spawnlist, structure.get_subpath("models"))

        return spawnlist
    
    def save_spawnlist(self, spawnlist: Spawnlist):
        filename = f"{spawnlist.id:03d}-" + spawnlist.name + ".txt"
        filepath = self.spawnlist_dir / filename

        with ValveTableFile(filepath, "w") as vtf:
            vtf.write("TableToKeyValues", spawnlist.as_dict())
        
        for child in spawnlist.children:
            self.save_spawnlist(child)