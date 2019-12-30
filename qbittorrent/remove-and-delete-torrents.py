#! python3
# remove torrents from qbittorrent

import datetime
import os
import requests
import time

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_BASE = r'http://127.0.0.1:7700/api/v2/torrents/'
DAYS_TO_FORCE_PRIVATE_TORRENTS = 30
PAUSE_TORRENTS_LARGER_THAN = 5000000000  # 5GB

DELETE_API = API_BASE + r'delete'
FORCE_START_API = API_BASE + r'setForceStart'
PAUSE_API = API_BASE + r'pause'
QUERY_API = API_BASE + r'info'
TRACKERS_API = API_BASE + r'trackers'


def deleteFiles(files):
    try:
        if len(files) > 0:
            for file in files.split(','):
                os.remove(file)
                os.rmdir(file)
    except Exception as e:
        print('eeep', e)


def forceStartTorrent(tHash, start=True, URL=None):
    if URL is None:
        global FORCE_START_API
        URL = FORCE_START_API
    try:
        param = '?hashes='+tHash+'&value='+str(start)
        requests.get(URL+param)
    except Exception as e:
        print('eeep', e)


def deleteTorrent(tHash, deleteFiles=True, URL=None):
    if URL is None:
        global DELETE_API
        URL = DELETE_API
    try:
        param = '?hashes='+tHash+'&deleteFiles='+str(deleteFiles)
        requests.get(URL+param)
    except Exception as e:
        print('eeep delete torrent', e)


def pauseTorrent(tHash, URL=None):
    if URL is None:
        global PAUSE_API
        URL = PAUSE_API
    try:
        param = '?hashes='+tHash
        requests.get(URL+param)
    except Exception as e:
        print('eeep pause', e)


try:
    SECONDS_IN_A_DAY = 86400
    SECONDS_IN_15_MINUTES = 900

    files = ''
    hashes = ""
    resp = requests.get(QUERY_API, verify=False, timeout=10)

    if str(resp.status_code)[0:2] == '20':
        json = resp.json()
        for torrent in json:
            addedon = torrent['added_on']
            addedonTS = datetime.datetime.fromtimestamp(addedon)
            forceStart = torrent['force_start']
            name = torrent['name']
            now = datetime.datetime.now()
            savePath = torrent['save_path']
            state = torrent['state']
            tHash = torrent['hash']
            timeActiveDays = torrent['time_active']/60/60/24
            timeSinceAdded = (now - addedonTS).total_seconds()
            totalSize = torrent['total_size']

            private = (requests.get(TRACKERS_API+'?hash='+tHash)
                       ).json()[0]['msg']

            if forceStart is False:
                if (private == 'This torrent is private'):
                    forceStartTorrent(tHash)
                if (timeSinceAdded > SECONDS_IN_A_DAY and
                        (state == 'pausedUP' or state == 'stalledUP')):

                    hashes += tHash + '|'
                    files += savePath + name + ','
                if (timeSinceAdded > SECONDS_IN_15_MINUTES and
                        (state == 'missingFiles' or state == 'stalledDL' or
                         state == 'metaDL' or state == 'uploading')):
                    hashes += tHash + '|'
                    files += savePath + name + ','
                if totalSize > PAUSE_TORRENTS_LARGER_THAN:
                    pauseTorrent(tHash)
            if timeActiveDays > DAYS_TO_FORCE_PRIVATE_TORRENTS:
                forceStartTorrent(tHash, False)
    if len(hashes) > 0:
        deleteTorrent(hashes)
        time.sleep(5)
        deleteFiles(files.rstrip(','))
except Exception as e:
    print('eeep gettorrent', e)
