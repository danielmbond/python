import datetime
import os
import requests
import time
import logging

# Configuration
API_BASE = r'http://127.0.0.1:7700/api/v2/torrents/'
DAYS_TO_FORCE_PRIVATE_TORRENTS = 30
PAUSE_TORRENTS_LARGER_THAN = 5000000000  # 5GB

DELETE_API = API_BASE + r'delete'
FORCE_START_API = API_BASE + r'setForceStart'
PAUSE_API = API_BASE + r'pause'
QUERY_API = API_BASE + r'info'
TRACKERS_API = API_BASE + r'trackers'

SECONDS_IN_A_DAY = 86400
SECONDS_IN_15_MINUTES = 900

# Logging configuration
logging.basicConfig(level=logging.INFO, filename='qbthang.log')

def delete_files(files):
    """Delete specified files."""
    for file in files.split(','):
        try:
            os.remove(file)
            os.rmdir(file)
        except Exception as e:
            print("e",e)
            logging.error('Error deleting file: %s', e)

def send_request(session, url, params):
    """Send a GET request with the specified parameters."""
    try:
        session.get(url, data=params)
        
    except Exception as e:
        logging.error('Request error: %s', e)

def send_post(session, url, params):
    """Send a POST request with the specified parameters."""
    try:
        session.post(url, data=params)
        
    except Exception as e:
        logging.error('Request error: %s', e)

def force_start_torrent(session, t_hash, start=True):
    """Force start or stop a torrent."""
    send_post(session, FORCE_START_API, {"hashes": t_hash, "value": start})

def delete_torrent(session, t_hash, delete_files=True):
    """Delete a torrent."""
    send_request(session, DELETE_API, {'hashes': t_hash, 'deleteFiles': str(delete_files)})

def pause_torrent(session, t_hash):
    """Pause a torrent."""
    send_request(session, PAUSE_API, {'hashes': t_hash})

def process_torrents():
        """Process torrents based on specified criteria."""
        files = ''
        hashes = ''

        with requests.Session() as session:

            try:
                resp = session.get(QUERY_API, verify=False, timeout=10)
                resp.raise_for_status()
            except Exception as e:
                logging.error('Error fetching torrents: %s', e)
                return

            torrents = resp.json()
            now = datetime.datetime.now()

            for torrent in torrents:
                added_on = datetime.datetime.fromtimestamp(torrent['added_on'])
                time_since_added = (now - added_on).total_seconds()
                time_active_days = torrent['time_active'] / SECONDS_IN_A_DAY
                t_hash = torrent['hash']
                save_path = torrent['save_path']
                name = torrent['name']
                state = torrent['state']
                total_size = torrent['total_size']

                try:
                    private = session.get(TRACKERS_API, params={'hash': t_hash}).json()[0]['msg']
                except Exception as e:
                    logging.error('Error fetching tracker info: %s', e)
                    continue

                if not torrent['force_start']:
                    if private == 'This torrent is private':
                        force_start_torrent(session, t_hash, True)
                    if time_since_added > SECONDS_IN_A_DAY and state in ['pausedUP', 'stalledUP']:
                        hashes += t_hash + '|'
                        files += save_path + name + ','
                    if time_since_added > SECONDS_IN_15_MINUTES and state in ['missingFiles', 'stalledDL', 'metaDL', 'uploading']:
                        hashes += t_hash + '|'
                        files += save_path + name + ','
                    if total_size > PAUSE_TORRENTS_LARGER_THAN:
                        pause_torrent(session, t_hash)
                if time_active_days > DAYS_TO_FORCE_PRIVATE_TORRENTS:
                    force_start_torrent(session, t_hash, False)

            if hashes:
                delete_torrent(session, hashes.rstrip('|'))
                time.sleep(5)
                delete_files(files.rstrip(','))

if __name__ == '__main__':
    process_torrents()

