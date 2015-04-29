__author__ = 's0539720'

import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import collections

class Crawler:
    def __init__(self, seed):
        self.seed = seed
        self.urls = [] #URLs that have to be visited
        self.visited = [] #already visited URLs
        self.linksOnSite = {} #title of site as key, links of the site as values
        self.titleOfSite = {} #url as key, title of the site as value
        self.linkStructure = {} #title of sites as key, titles of sites that are linked as values

    #crawl every URL in seed list + URLs found on the websites
    def getlinkstructure(self):
        for url in self.seed:
            self.urls.append(url)
            self.visited.append(url)

            while len(self.urls) > 0:
                try:
                    website = urllib.request.urlopen(self.urls[0]).read()
                except:
                    print("Could not crawl the following website: " + self.urls[0])

                soup = BeautifulSoup(website)
                title = soup.title.string
                self.linksOnSite[title] = []
                self.titleOfSite[self.urls[0]] = title
                self.urls.pop(0)

                for tag in soup.findAll('a',href=True):
                    tag['href'] = urllib.parse.urljoin(url, tag['href'])
                    self.linksOnSite[title].append(tag['href'])
                    if tag['href'] not in self.visited:
                        self.urls.append(tag['href'])
                        self.visited.append(tag['href'])

        #create link structure and order alphabetically
        for site, links in sorted(self.linksOnSite.items()):
            self.linkStructure[site] = []
            for link in links:
                self.linkStructure[site].append(self.titleOfSite[link])
        self.linkStructure = collections.OrderedDict(sorted(self.linkStructure.items()))

        lS = {}
        #print the link structure
        for site in self.linkStructure:
            lS[site] = self.linkStructure[site]
            print(site + ':' + ",".join(self.linkStructure[site]))
        return lS


