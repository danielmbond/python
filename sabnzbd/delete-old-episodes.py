#! python3

# Clean up the orphaned sabnzbd files, delete everything that isn't a mp4 of m4v

import os, sys 


EPISODES_TO_KEEP = 5
SABNZBD_COMPLETE_DIR = r'C:\Users\Daniel\Downloads\complete'
BASE_PATH = r'H:\TV'

shows = ['Saturday Night Live','Conan (2010)','Jimmy Kimmel Live','The Daily Show',
         'Full Frontal With Samantha Bee']

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if sys.platform == 'win32':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

for show in shows:
    directory = os.path.join(BASE_PATH, show)
    print(directory)
    if os.path.isdir(directory) == True:
        for root, dirs, files in os.walk(directory):
            count = 0
            for name in sorted(files, key=lambda name:
                os.path.getmtime(os.path.join(root, name)), reverse=(True)):
                    if count > 4:
                        f = os.path.join(root,name)
                        print(f)
                        os.remove(f)
                    count += 1
                    
##print(f)
##def directoryToFileName(fileFullname):
##    lastDirectory = os.path.basename(os.path.dirname(fileFullname)).strip()
##    fileExtension = os.path.splitext(fileFullname)[1]
##    return(lastDirectory + fileExtension)
##
##for root, dirs, files in os.walk(SABNZBD_COMPLETE_DIR):
##    if(dirs == [] and files == []):
##        os.rmdir(root)
##        continue
##    for name in files:
##        file = os.path.join(root, name)
##        fileSize = os.path.getsize(file)/1024/1024
##        if not "UNPACK" in file:
##            if not file.endswith(".mp4") and not file.endswith(".m4v") or fileSize < 20:
##                print("Deleting", name, fileSize)
##                os.remove(file)
##                continue
##            else:
##                try:
##                    os.rename(file,os.path.join(SABNZBD_COMPLETE_DIR,directoryToFileName(file)))
##                    print("RENAME", file, os.path.join(SABNZBD_COMPLETE_DIR,directoryToFileName(file)))
##                except:
##                    continue
