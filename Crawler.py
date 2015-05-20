__author__ = 's0539720'

from urllib.parse import urlparse
import urllib.request
from bs4 import BeautifulSoup
import collections

class Crawler:

    def __init__(self, seed):
        self.__seed = seed
        self.__urls = [] #URLs that have to be visited
        self.__visited = [] #already visited URLs
        self.__linksOnSite = {} #title of site as key, links of the site as values
        self.__titleOfSite = {} #url as key, title of the site as value
        self.__linkStructure = {} #title of sites as key, titles of sites that are linked as values
        self.__crawl()

    #crawl every URL in seed list + URLs found on the websites
    def __crawl(self):
        for url in self.__seed:
            self.__urls.append(url)
            self.__visited.append(url)

            while len(self.__urls) > 0:
                try:
                    website = urllib.request.urlopen(self.__urls[0]).read()
                except:
                    print("Could not crawl the following website: " + self.__urls[0])

                soup = BeautifulSoup(website)
                title = soup.title.string
                self.__linksOnSite[title] = []
                self.__titleOfSite[self.__urls[0]] = title
                self.__urls.pop(0)
                for tag in soup.findAll('a',href=True):
                    tag['href'] = urllib.parse.urljoin(url, tag['href'])
                    self.__linksOnSite[title].append(tag['href'])
                    if tag['href'] not in self.__visited:
                        self.__urls.append(tag['href'])
                        self.__visited.append(tag['href'])

        #create link structure and order alphabetically
        for site, links in sorted(self.__linksOnSite.items()):
            self.__linkStructure[site] = []
            for link in links:
                self.__linkStructure[site].append(self.__titleOfSite[link])
        self.__linkStructure = collections.OrderedDict(sorted(self.__linkStructure.items()))

    def getVisited(self):
        return self.__visited

    def getLinkStructure(self):
        return self.__linkStructure

    #print the link structure
    def printLinkStructure(self):
            for site in self.__linkStructure:
                print(site + ':' + ",".join(self.__linkStructure[site]))
