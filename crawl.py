__author__ = 's0539720'

from urllib.parse import urlparse
import urllib.request
from bs4 import BeautifulSoup
import collections


seed = ["http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d01.html",
        "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d06.html",
        "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d08.html"]
urls = [] #URLs that have to be visited
visited = [] #already visited URLs
linksOnSite = {} #title of site as key, links of the site as values
titleOfSite = {} #url as key, title of the site as value
linkStructure = {} #title of sites as key, titles of sites that are linked as values

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

#create link structure and order alphabetically
for site, links in sorted(linksOnSite.items()):
    linkStructure[site] = []
    for link in links:
        linkStructure[site].append(titleOfSite[link])
linkStructure = collections.OrderedDict(sorted(linkStructure.items()))


#print the link structure
for site in linkStructure:
    print(site + ':' + ",".join(linkStructure[site]))
