#! python3
# remove torrents from qbittorrent

import os, requests, time, datetime
##urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

queryApi = r'http://127.0.0.1:7700/query/torrents'
deleteApi = r'http://127.0.0.1:7700/command/deletePerm'

files = ''

def deleteFiles(files):
    try:
        if len(files) > 0:
            for file in files.split(','):
            ##print(file)
                os.remove(file)
                os.rmdir(file)
    except Exception as e:
        print('eeep',e)

def deleteTorrent(URL, hashes):
    try:
        resp = requests.post(URL, data={'hashes': hashes}, verify=False, timeout=10)
##        print(resp.status_code, URL)
    except Exception as e:
        print('eeep',e)

def getTorrents(URL):
    try:
        resp = requests.get(URL, verify=False, timeout=10)
        global deleteApi
        global files
        hashes = ""
        secondsInADay = 86400
        secondsInAnHour = 3600

        if str(resp.status_code)[0:2] == '20':
            json = resp.json()
            for torrent in json:
                state = torrent['state']
                timeActive = torrent['time_active']/60/60
                addedon = torrent['added_on']
                timeSinceAdded = (datetime.datetime.now() - datetime.datetime.fromtimestamp(addedon)).total_seconds()
                name = torrent['name']
                tHash = torrent['hash']
                savePath = torrent['save_path']
                if (timeSinceAdded > secondsInADay and (state == 'missingFiles' or state == 'pausedUP')):
                        hashes += tHash + '|'
                        files += savePath + name + ','
                if timeSinceAdded > secondsInAnHour and (state == 'stalledDL' or state == 'metaDL':
                        hashes += tHash + '|'
                        files += savePath + name + ','
        if len(hashes) > 0:
            dt = datetime.datetime.now()
            
##            print(datetime.datetime.utcfromtimestamp(addedon), datetime.datetime.utcnow(), datetime.datetime.utcfromtimestamp(datetime.datetime.utcnow().timestamp() - addedon), datetime.datetime.utcnow().timestamp() - addedon)
##            print(datetime.datetime.fromtimestamp(addedon))
##            print(timeSinceAdded)
            deleteTorrent(deleteApi, hashes.rstrip('|'))
            time.sleep(5)
            deleteFiles(files.rstrip(','))
    except Exception as e:
        print('eeep',e)

getTorrents(queryApi)


