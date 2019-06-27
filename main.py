import vpk
import dialog
import spawnlist
import re
import collections
import os

CAPTION = "Spawnlist Generator"
UNSORTED_KEY = "Other"
FILE_SEPERATOR_R = re.compile(r"[\/\\]")
SANITISER_R = re.compile(r"[\<\>\:\"\/\\\|\?\*\s\'\`\_\+\=\!\@\#\$\%\^\&\;\,\.\~]")

def main():
    if dialog.ok_cancel_dialog("Select your spawnlist folder (Usually garrysmod/settings/spawnlist).",caption=CAPTION):
        path = dialog.dir_dialog(caption=CAPTION)
        if path:
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            files = sorted(files)

            lastFile = files[-1]
            strid = lastFile[0:3]
            id = int(strid) + 1

            if dialog.ok_cancel_dialog("Select the _dir.vpk file to make a spawnlist from.",caption=CAPTION):
                vpkpath = dialog.open_dialog(caption=CAPTION,wildcard="Valve Pak _dir File (*_dir.vpk)|*_dir.vpk")
                if vpkpath:
                    name = dialog.text_entry_dialog(message="Name your spawnlist.",caption=CAPTION)
                    if name and (not name==""):
                        filename = f"{id:03d}-" + SANITISER_R.sub("-",name) + ".txt"
                        name = name.replace("\"","''")
                        sl = spawnlist.Spawnlist(name,id=id)
                        pak = vpk.open(vpkpath)
                        models = {}
                        unsorted = []
                        for pakfile in pak:
                            if pakfile.endswith(".mdl"):
                                split = FILE_SEPERATOR_R.split(pakfile)
                                if len(split) > 2:
                                    key = split[1]
                                    if not key in models:
                                        models[key] = []
                                    models[key].append(pakfile)
                                else:
                                    unsorted.append(pakfile)

                        od = collections.OrderedDict(sorted(models.items(), key=lambda t: t[0]))

                        od[UNSORTED_KEY] = unsorted

                        for k in od:
                            sl.addHeader(k)
                            for v in od[k]:
                                sl.addModel(v)

                        with open(os.path.join(path,filename),"w") as f:
                            try:
                                f.write(sl.as_string())
                            except IOError:
                                dialog.error_dialog("Failed to save spawnlist to file!",caption=CAPTION)
                            else:
                                dialog.ok_dialog("Successfully saved spawnlist!",caption=CAPTION)


if __name__ == "__main__":
    main()