#! python3
# use a web service to look up the ip address
# of domains and add them to your hosts file

import os
import re
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# (path) sets the location of the file containing the hosts you want to look up
# (osHostsFile) is where to write the completed hosts file
if 'APPDATA' in os.environ:
    path = os.path.join(os.environ['APPDATA'], 'hosts', 'hosts')
    osHostsFile = r'C:\windows\system32\drivers\etc\hosts'
else:
    path = os.path.join(os.environ['HOME'], 'hosts', 'hosts')
    osHostsFile = r'/etc/hosts'

print('Edit', path, 'to add additional hosts.')

if not os.path.isdir(os.path.dirname(path)):
    os.makedirs(os.path.dirname(os.path.realpath(path)))

# add domains if the path doesn't exist
if not os.path.isfile(path):
    f = open(path, 'a')
    f.write('facebook.com\n')
    f.write('gmail.com\n')
    f.close()
else:
    with open(path, 'r') as f:
        hostsOutput = []
        for line in f:
            hostsOutput.append(line)
        f.close()


def getFQDN(url):
    return(url.replace('https:', '').replace('/', ''))


# look up domains of other urls contained in the "path" file
def getUrlsFromPage(input):
    domainList = []
    urlRegex = re.compile(r'https://[A-Za-z0-9.]*/')
    for domain in input:
        try:
            print(domain)
            page = requests.get('https://' +
                                domain.strip('\n'), verify=False, timeout=6)
            urls = set(urlRegex.findall(page.text))
            for url in urls:
                print('+', url)
                domainList.append(getFQDN(url))
        except Exception as e:  # catch *all* exceptions
            print("Error: %s" % e)
    return(set(domainList))


def writeHostsFile(hostList, writemode='w'):
    try:
        f = open(osHostsFile, mode=writemode, newline='\r\n')
        for host in hostList:
            host = host.strip()
            ip = lookupDNS(host)
            print(ip, host, '\n')
            f.write(ip + " " + host + "\n")
    except Exception as e:
        print('oh no', e)
    f.close()


def convertHostToURL(dnsName):
    try:
        return('https://dns.google.com/resolve?name='+dnsName)
    except Exception as e:
        print(e)


def lookupDNS(dnsName):
    try:
        ip = ""
        resp = requests.get(convertHostToURL(dnsName), verify=False, timeout=6)
        if str(resp.status_code)[0:2] == '20':
            ip = resp.json()['Answer'][(len(resp.json()['Answer'])-1)]['data']
            dnsName = ip.strip()
            return(ip)
    except Exception as e:
        print('eeep', e)


def appendGoSkope():
    f = open(osHostsFile, mode='a', newline='\r\n')
    f.write("127.0.0.1 goskope.com\n")
    f.close()


writeHostsFile(hostsOutput, 'w')
domains = getUrlsFromPage(hostsOutput)
writeHostsFile(domains, 'a')
appendGoSkope()
