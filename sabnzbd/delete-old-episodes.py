#! python3

# Clean up the orphaned sabnzbd files, delete
# everything that isn't a mp4 of m4v

import os
import sys

BASE_PATH = r'D:\TV'

# Show Name : Episodes to Keep
shows = {'60 Minutes': 5,
         'American Idol': 20,
         'Anthony Bourdain- Parts Unknown': 25,
         'Conan (2010)': 5,
         'Cops': 25,
         'Court Cam': 10,
         'Full Frontal With Samantha Bee': 5,
         'Jimmy Kimmel Live': 5,
         'Judge Judy': 5,
         'Last Week Tonight with John Oliver': 5,
         'Law & Order- Special Victims Unit': 15,
         'Law & Order- True Crime': 15,
         'Lip Sync Battle': 5,
         'Live Pd': 10,
         'Live PD- Police Patrol': 5,
         'Live PD - Wanted': 5,
         'Live PD- Women on Patrol': 5,
         'Live Rescue': 1,
         'PD Cam': 5,
         'Saturday Night Live': 15,
         'The Daily Show': 5,
         'The Masked Singer': 5,
         'Top Chef': 15,
         'Tosh 0': 25,
         'Vice': 5
         }


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


def deleteShows(BASE_PATH=BASE_PATH, shows=shows):
    for show in shows:
        directory = os.path.join(BASE_PATH, show)
        print(directory)
        if os.path.isdir(directory) is True:
            for root, dirs, files in os.walk(directory):
                count = 0
                for name in sorted(files, key=lambda name:
                                   os.path.getmtime(os.path.join(root, name)),
                                   reverse=(True)):
                    if count > shows[show]-1:
                        f = os.path.join(root, name)
                        print(f)
                        os.remove(f)
                    count += 1


deleteShows()
deleteShows(r'H:\TV')
