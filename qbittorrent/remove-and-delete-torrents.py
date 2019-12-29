#! python3
# remove torrents from qbittorrent

import os, requests, time, datetime
##urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_BASE = r'http://127.0.0.1:7700/api/v2/torrents/'
DAYS_TO_FORCE_PRIVATE_TORRENTS = 30
PAUSE_TORRENTS_LARGER_THAN = 5000000000 #5GB

DELETE_API      = API_BASE + r'delete'
FORCE_START_API = API_BASE + r'setForceStart'
PAUSE_API       = API_BASE + r'pause'
QUERY_API       = API_BASE + r'info'
TRACKERS_API    = API_BASE + r'trackers'

files = ''

def deleteFiles(files):
    try:
        if len(files) > 0:
            for file in files.split(','):
                os.remove(file)
                os.rmdir(file)
    except Exception as e:
        print('eeep',e)

def forceStartTorrent(tHash, start=True, URL=None):
    if URL is None:
        global FORCE_START_API
        URL = FORCE_START_API
    try:
        param = '?hashes='+tHash+'&value='+str(start)
        resp = requests.get(URL+param)
    except Exception as e:
        print('eeep',e)

def deleteTorrent(tHash, deleteFiles=True, URL=None):
    if URL is None:
        global DELETE_API
        URL = DELETE_API
    try:
        param = '?hashes='+tHash+'&deleteFiles='+str(deleteFiles)
        resp = requests.get(URL+param)
    except Exception as e:
        print('eeep delete torrent',e)

def pauseTorrent(tHash, URL=None):
    if URL is None:
        global PAUSE_API
        URL = PAUSE_API
    try:
        param = '?hashes='+tHash
        resp = requests.get(URL+param)
    except Exception as e:
        print('eeep pause',e)

def getTorrents(URL=None):
    if URL is None:
        global QUERY_API
        URL = QUERY_API
    try:
        global DAYS_TO_FORCE_PRIVATE_TORRENTS
        global DELETE_API
        global files
        global FORCE_START_API
        global PAUSE_API
        global PAUSE_TORRENTS_LARGER_THAN
        global TRACKERS_API
        
        SECONDS_IN_A_DAY      = 86400
        SECONDS_IN_15_MINUTES = 900

        hashes = ""
        resp   = requests.get(URL, verify=False, timeout=10)

        if str(resp.status_code)[0:2] == '20':
            json = resp.json()
            for torrent in json:
                addedon    = torrent['added_on']
                forceStart = torrent['force_start']
                name       = torrent['name']
                savePath   = torrent['save_path']
                state      = torrent['state']
                tHash      = torrent['hash']
                timeActiveDays = torrent['time_active']/60/60/24
                timeSinceAdded = (datetime.datetime.now() - datetime.datetime.fromtimestamp(addedon)).total_seconds()
                totalSize  = torrent['total_size']

                private    = (requests.get(TRACKERS_API+'?hash='+tHash)).json()[0]['msg']

                if forceStart == False:
                    if (private=='This torrent is private'):
                        forceStartTorrent(tHash)
                    if (timeSinceAdded > SECONDS_IN_A_DAY and (state == 'pausedUP' or state == 'stalledUP')):
                        hashes += tHash + '|'
                        files += savePath + name + ','
                    if (timeSinceAdded > SECONDS_IN_15_MINUTES and (state == 'missingFiles' or state == 'stalledDL' or state == 'metaDL' or state == 'uploading')):
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
        print('eeep gettorrent',e)

getTorrents(QUERY_API)
