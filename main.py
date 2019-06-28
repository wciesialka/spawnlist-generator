import vpk
import dialog
import spawnlist
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

def populateSpawnlist(sl,modelList,i=1,strictTo=None):

    n = i + 2

    unsorted = []
    models = {}
    childrenToCreate = []
    toRemove = []

    for j,mdl in enumerate(modelList):
        split = FILE_SEPERATOR_R.split(mdl)
        length = len(split)

        if i >= length:
            continue
        elif strictTo:
            if (not strictTo == split[i-1]):
                continue

        if length == i+1:
            unsorted.append(mdl)
            toRemove.append(j)
        elif length == n:
            if not split[i] in models:
                models[split[i]] = []
            models[split[i]].append(mdl)
            toRemove.append(j)
        elif length > n:
            if not split[i] in childrenToCreate:
                childrenToCreate.append(split[i])

    toRemove = sorted(toRemove,reverse=True)

    for j in toRemove:
        modelList.pop(j)

    for childToCreate in childrenToCreate:
        child = sl.createChild(childToCreate)
        populateSpawnlist(child,modelList,i+1,childToCreate)

    od = collections.OrderedDict(sorted(models.items(), key=lambda t: t[0]))

    if len(unsorted) > 0:
        od[UNSORTED_KEY] = unsorted

    for k in od:
        sl.addHeader(k)
        v = od[k]
        if not type(v) is str:
            for m in od[k]:
                sl.addModel(m)
        else:
            sl.addModel(v)

def sanitiseName(name):
    return SANITISER_R.sub("-",name)

def saveSpawnlist(sl,path,isChildProcess=False):
    names = [sanitiseName(sl.name)]
    slp = sl.parent
    while not slp == None:
        names.append(sanitiseName(slp.name))
        slp = slp.parent 
    cleanName = ""
    for name in names[::-1]:
        cleanName += name + "-"
    filename = f"{sl.id:03d}-" + cleanName[:-1] + ".txt"
    with open(os.path.join(path,filename),"w") as f:
        try:
            f.write(sl.as_string())
        except IOError:
            if isChildProcess:
                dialog.error_dialog("Failed to save child spawnlist to file!",caption=CAPTION)
            else:
                dialog.error_dialog("Failed to save main spawnlist to file!",caption=CAPTION)
        else:
            if not isChildProcess:
                dialog.ok_dialog("Successfully saved spawnlist!",caption=CAPTION)
    for child in sl.children:
        saveSpawnlist(child,path,isChildProcess=True)

def workItHarderDoItBetter(path):
    config["DEFAULT"]["PreviousSpawnlistDirectory"] = os.path.dirname(path)

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    files = sorted(files)

    lastFile = files[-1]
    strid = lastFile[0:3]
    id = int(strid) + 1

    if dialog.ok_cancel_dialog("Select the _dir.vpk file to make a spawnlist from.",caption=CAPTION):
        vpkpath = dialog.open_dialog(caption=CAPTION,wildcard="Valve Pak _dir File (*_dir.vpk)|*_dir.vpk",defaultDir=config.get("DEFAULT","PreviousVPKDirectory",fallback=""))
        if vpkpath:
            config["DEFAULT"]["PreviousVPKDirectory"] = os.path.dirname(vpkpath)
            name = dialog.text_entry_dialog(message="Name your spawnlist.",caption=CAPTION)
            if name and (not name==""):
                name = name.replace("\"","''")
            
                pak = vpk.open(vpkpath)

                sl = spawnlist.Spawnlist(name,id=id)

                models = []
                for pakfile in pak:
                    if pakfile.endswith(".mdl"):
                        models.append(pakfile)

                models = sorted(models,key=lambda model: len(FILE_SEPERATOR_R.findall(model)))
                populateSpawnlist(sl,models)

                saveSpawnlist(sl,path)

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