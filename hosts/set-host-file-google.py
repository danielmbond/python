#! python3
# use a web service to look up the ip address of domains and add them to your hosts file

import os, re, requests


## url information used to look up addresses
lookup = {}
lookup['url'] = 'http://dig.jsondns.org/IN/'
lookup['hostname'] = 'google.com'
lookup['other'] = '/A'

## (path) sets the location of the file containing the hosts you want to look up
## (osHostsFile) is where to write the completed hosts file 
if 'APPDATA' in os.environ:
    path = os.path.join(os.environ['APPDATA'], 'hosts', 'hosts')
    osHostsFile = r'C:\windows\system32\drivers\etc\hosts'
else:
    path = os.path.join(os.environ['HOME'], 'hosts', 'hosts')
    osHostsFile = r'/etc/hosts'

print('Edit', path, 'to add additional hosts.')

if not os.path.isdir(os.path.dirname(path)):
    os.makedirs(os.path.dirname(os.path.realpath(path)))

## add domains if the path doesn't exist
if not os.path.isfile(path):
    f = open(path, 'a')
    f.write ('facebook.com\n')
    f.write('gmail.com\n')
    f.close()
else:
    with open(path,'r') as f:
        hostsOutput = []
        for line in f:
            hostsOutput.append(line)
        f.close()

def getFQDN(url):
    return(url.replace('https:','').replace('/',''))

## look up domains of other urls contained in the "path" file
def getUrlsFromPage(input):
    domainList = []
    urlRegex = re.compile(r'https://[A-Za-z0-9.]*/')
    for domain in input:
        try:
            print(domain)
            page = requests.get('https://' + domain.strip('\n'), verify=False, timeout=6)
            urls = set(urlRegex.findall(page.text))
            for url in urls:
                print(url)
                domainList.append(getFQDN(url))
        except Exception as e: # catch *all* exceptions
            print( "Error: %s" % e )
    return(set(domainList))

def writeHostsFile(input, writemode='w'):
    hostsDict = {}
    try:
        for host in input:
            host = host.strip()
            lookup['hostname'] = host
            resp = requests.get(lookup['url'] + lookup['hostname'] + lookup['other'], verify=False, timeout=6)
            if str(resp.status_code)[0:2] == '20':
                for item in resp.json()['answer']:
                    if type(item['rdata']) == str:
                        print(item['rdata'])
                        hostsDict[host] = item['rdata']
                    else:
                        print("Did not return a string:", item['rdata'])
                        
        f = open(osHostsFile, mode=writemode, newline='\r\n')
        for k, v in hostsDict.items():
            print(v,k,'\n')
            f.write(v + " " + k + "\n")
    except Exception as e:
        print(e)
    f.close()

writeHostsFile(hostsOutput,'w')
domains = getUrlsFromPage(hostsOutput)
writeHostsFile(domains,'a')

