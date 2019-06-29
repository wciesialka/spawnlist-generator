import vpk
import dialog
import spawnlist
import modelpath
import re
import collections
import os
import configparser

config = configparser.ConfigParser()
config['DEFAULT'] = {"PreviousSpawnlistDirectory": "",
                     "PreviousVPKDirectory": ""}
config.read("PreviousDirectories.cfg")

CAPTION = "Spawnlist Generator"
UNSORTED_KEY = "Other"
FILE_SEPERATOR_R = re.compile(r"[\/\\]")
SANITISER_R = re.compile(r"[\<\>\:\"\/\\\|\?\*\s\'\`\_\+\=\!\@\#\$\%\^\&\;\,\.\~]")

def populateSpawnlist(sl,structure):
    models = structure.models
    subpaths = structure.subpaths
    for subpath_key in subpaths:
        subpath = subpaths[subpath_key]
        
        if len(subpath.models) > 0:
            sl.addHeader(subpath_key)
            toPop = []
            for i,model in enumerate(subpath.models):
                sl.addModel(model)
                toPop.append(i)
            for i in sorted(toPop,reverse=True):
                subpath.popModel(i)
        if len(subpath.subpaths) > 0:
            child = sl.createChild(subpath_key)
            populateSpawnlist(child,subpath)

    if(len(models) > 0):
        sl.addHeader(structure.key)

        for model in models:
            sl.addModel(model)

def sanitiseName(name):
    return SANITISER_R.sub("-",name)


def createStructure(modelList):
    inorder = sorted(modelList,key=lambda model: (len(FILE_SEPERATOR_R.findall(model)), str.lower))
    structure = modelpath.ModelPath("root")
    for model in inorder:
        structure.addModel(model)
    return structure

TaskSuccessful = True

def saveSpawnlist(sl,path,isChildProcess=False):
    global TaskSuccessful
    filename = f"{sl.id:03d}-" + sanitiseName(sl.name) + ".txt"
    with open(os.path.join(path,filename),"w") as f:
        try:
            f.write(str(sl))
        except IOError:
            if TaskSuccessful:
                TaskSuccessful = False
            if isChildProcess:
                dialog.error_dialog("Failed to save child spawnlist to file!",caption=CAPTION)
            else:
                dialog.error_dialog("Failed to save main spawnlist to file!",caption=CAPTION)

    for child in sl.children:
        saveSpawnlist(child,path,isChildProcess=True)

def workItHarderDoItBetter(path):
    global TaskSuccessful
    config["DEFAULT"]["PreviousSpawnlistDirectory"] = os.path.dirname(path)

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    files = sorted(files)

    lastFile = files[-1]
    strid = lastFile[0:3]
    id = int(strid) + 1
    spawnlist.Spawnlist.ID = id

    if dialog.ok_cancel_dialog("Select the _dir.vpk file to make a spawnlist from.",caption=CAPTION):
        vpkpath = dialog.open_dialog(caption=CAPTION,wildcard="Valve Pak _dir File (*_dir.vpk)|*_dir.vpk",defaultDir=config.get("DEFAULT","PreviousVPKDirectory",fallback=""))
        if vpkpath:
            config["DEFAULT"]["PreviousVPKDirectory"] = os.path.dirname(vpkpath)
            name = dialog.text_entry_dialog(message="Name your spawnlist.",caption=CAPTION)
            if name and (not name==""):
                name = name.replace("\"","''")
            
                pak = vpk.open(vpkpath)

                sl = spawnlist.Spawnlist(name)

                models = []
                for pakfile in pak:
                    if pakfile.endswith(".mdl"):
                        models.append(pakfile)

                structure = createStructure(models)

                with open("structure_" + name + ".txt","w") as f:
                    f.write(str(structure))

                populateSpawnlist(sl,structure.getSubPath("models"))

                saveSpawnlist(sl,path)

                if TaskSuccessful:
                    dialog.ok_dialog("Successfully saved spawnlist!",caption=CAPTION)
                else:
                    dialog.ok_dialog("Could not successfully save spawnlist!",caption=CAPTION)

def main():
    if dialog.ok_cancel_dialog("Select your spawnlist folder (Usually garrysmod/settings/spawnlist).",caption=CAPTION):
        path = dialog.dir_dialog(caption=CAPTION,defaultPath=config.get("DEFAULT","PreviousSpawnlistDirectory",fallback=""))
        if path:
            shouldRun = True
            while shouldRun:
                workItHarderDoItBetter(path)

                with open("PreviousDirectories.cfg","w") as f:
                    config.write(f)
                
                shouldRun = dialog.yes_no_dialog("Generate another spawnlist?",caption=CAPTION)


if __name__ == "__main__":
    main()