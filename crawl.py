__author__ = 's0540017'

from urllib.parse import urlparse
import urllib
from bs4 import BeautifulSoup

url = "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d01.html"

urls = [url]
visited = [url]

htmltext = ""

while len(urls) > 0:
    try:
        htmltext = urllib.urlopen(urls[0]).read()
    except:
        print(urls[0])
    soup = BeautifulSoup(htmltext)

    urls.pop(0)
    print(len(urls))

    for tag in soup.findAll('a',href=True):
        tag['href'] = urlparse.urljoin(url, tag['href'])
        if url in tag['href'] and tag['href'] not in visited:
            urls.append(tag['href'])
            visited.append(tag['href'])

print(visited)