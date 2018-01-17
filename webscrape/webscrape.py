import re, requests

page = requests.get('https://google.com')

urlRegex = re.compile(r'https://[A-Za-z0-9.]*/')
urls = set(urlRegex.findall(page.text))

def getFQDN(url):
    return(url.replace('https:','').replace('/',''))

for url in urls:
    print(getFQDN(url))

