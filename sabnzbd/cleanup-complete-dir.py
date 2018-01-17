#! python3

# Clean up the orphaned sabnzbd files, delete everything that isn't a mp4 of m4v

import os

SABNZBD_COMPLETE_DIR = r'C:\Users\Daniel\Downloads\complete'

os.chdir(SABNZBD_COMPLETE_DIR)

def directoryToFileName(fileFullname):
    lastDirectory = os.path.basename(os.path.dirname(fileFullname)).strip()
    fileExtension = os.path.splitext(fileFullname)[1]
    return(lastDirectory + fileExtension)

for root, dirs, files in os.walk(SABNZBD_COMPLETE_DIR):
    if(dirs == [] and files == []):
        os.rmdir(root)
        continue
    for name in files:
        file = os.path.join(root, name)
        fileSize = os.path.getsize(file)/1024/1024
        if not "UNPACK" in file:
            if not file.endswith(".mp4") and not file.endswith(".m4v") or fileSize < 20:
                print("Deleting", name, fileSize)
                os.remove(file)
                continue
            else:
                try:
                    os.rename(file,os.path.join(SABNZBD_COMPLETE_DIR,directoryToFileName(file)))
                    print("RENAME", file, os.path.join(SABNZBD_COMPLETE_DIR,directoryToFileName(file)))
                except:
                    continue
