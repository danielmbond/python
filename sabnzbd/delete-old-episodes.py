# Delete old episodes 

import os
import sys

TV_PATH = r'D:\TV'
KIDS_TV_PATH = r'D:\KidsTV'

# Show Name : Episodes to Keep
SHOWS = {
    '60 Minutes': 5,
    '8 Out of 10 Cats': 1,
    'America\'s Top Dog': 1,
    'American Idol': 20,
    'Big Brother': 40,
    'Comedians in Cars Getting Coffee': 13,
    'Conan (2010)': 1,
    'Cops': 200,
    'Doctor Who (2005)': 20,
    'Full Frontal With Samantha Bee': 1,
    'Gogglebox': 10,
    'Jersey Shore Family Vacation': 34,
    'Jimmy Kimmel Live': 1,
    'Judy Justice': 108,
    'Judge Judy': 48,
    'Last Week Tonight with John Oliver': 1,
    'Law & Order- Special Victims Unit': 122,
    'Law & Order- True Crime': 122,
    'Lip Sync Battle': 1,
    'Live Pd': 10,
    'Live PD- Police Patrol': 5,
    'Live PD - Wanted': 5,
    'Live PD- Women on Patrol': 5,
    'Live Rescue': 1,
    'Love After Lockup': 70,
    'Married at First Sight': 20,
    'On Patrol - Live': 10,
    'Paw Patrol': 40,
    'PD Cam': 10,
    'Pokemon': 80,
    'Real Time with Bill Maher': 1,
    'RuPaul\'s Drag Race': 12,
    'Saturday Night Live': 12,
    'Sesame Street': 70,
    'Taskmaster': 20,
    'The Daily Show': 1,
    'The Masked Singer': 1,
    'The People\'s Court (1997)': 4,
    'The Repair Shop': 15,
    'Top Chef': 15,
    'Vice': 5
}

def delete_old_episodes(TV_PATH, shows):
    """
    Delete old episodes of shows, keeping only the specified number of recent episodes.
    """
    for show, episodes_to_keep in shows.items():
        directory = os.path.join(TV_PATH, show)
        if os.path.isdir(directory):
            for root, _, files in os.walk(directory):
                files.sort(key=lambda name: os.path.getmtime(os.path.join(root, name)), reverse=True)
                for count, name in enumerate(files):
                    if count >= episodes_to_keep:
                        print(root, name)
                        os.remove(os.path.join(root, name))

delete_old_episodes(TV_PATH, SHOWS)
delete_old_episodes(KIDS_TV_PATH, SHOWS)

