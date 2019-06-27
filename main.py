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

def populateSpawnlist(sl,modelList,i=1):

    n = i + 2

    unsorted = []
    models = {}
    childrenToCreate = []

    for mdl in modelList:
        split = FILE_SEPERATOR_R.split(mdl)
        key = split[i]

        if len(split) > n:
            if not key in childrenToCreate:
                childrenToCreate.append(key)
        elif len(split) == n:
            if not key in models:
                models[key] = []
            models[key].append(mdl)
            modelList.remove(mdl)
        elif len(split) == n-1:
            unsorted.append(mdl)
            modelList.remove(mdl)
    
    for childToCreate in childrenToCreate:
        child = sl.createChild(childToCreate)
        populateSpawnlist(child,modelList,i=i+1)

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

def saveSpawnlist(sl,path):
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
            dialog.error_dialog("Failed to save spawnlist to file!",caption=CAPTION)
        else:
            dialog.ok_dialog("Successfully saved spawnlist!",caption=CAPTION)
    for child in sl.children:
        saveSpawnlist(child,path)

def main():
    if dialog.ok_cancel_dialog("Select your spawnlist folder (Usually garrysmod/settings/spawnlist).",caption=CAPTION):
        path = dialog.dir_dialog(caption=CAPTION,defaultPath=config.get("DEFAULT","PreviousSpawnlistDirectory",fallback=""))
        if path:
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

                        populateSpawnlist(sl,models)

                        saveSpawnlist(sl,path)

    with open("PreviousDirectories.cfg","w") as f:
        config.write(f)


if __name__ == "__main__":
    main()