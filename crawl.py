__author__ = 's0539720'

from urllib.parse import urlparse
import urllib.request
from bs4 import BeautifulSoup


seed = ["http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d01.html",
        "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d06.html",
        "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d08.html"]
urls = [] #URLs that have to be visited
visited = [] #already visited URLs
linksOnSite = {} #title of site as key, links of the site as values
titleOfSite = {} #url as key, title of the site as value

#crawl every URL in seed list + URLs found on the websites
for url in seed:
    urls.append(url)
    visited.append(url)

    while len(urls) > 0:
        try:
            website = urllib.request.urlopen(urls[0]).read()
        except:
            print("Could not crawl the following website: " + urls[0])

        soup = BeautifulSoup(website)
        title = soup.title.string
        linksOnSite[title] = []
        titleOfSite[urls[0]] = title
        urls.pop(0)

        for tag in soup.findAll('a',href=True):
            tag['href'] = urllib.parse.urljoin(url, tag['href'])
            linksOnSite[title].append(tag['href'])
            if tag['href'] not in visited:
                urls.append(tag['href'])
                visited.append(tag['href'])

#print the link structure
for site, links in linksOnSite.items():
    structure = site + ":"
    first = True
    for link in links:
        if first:
            first = False
            structure = structure + titleOfSite[link]
        else:
            structure = structure + "," + titleOfSite[link]
    print(structure)
