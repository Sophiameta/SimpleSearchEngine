__author__ = 's0539720'

import urllib.request
from bs4 import BeautifulSoup
import re
import collections
from crawl import Crawler
from PageRank import PageRank

def normalize(text):
    text = text.lower()
    words = re.compile('\w+').findall(text)
    return words

stopwords = [
    'd01', 'd02', 'd03', 'd04', 'd05', 'd06', 'd07', 'd08',
    'a', 'also', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'do',
    'for', 'have', 'is', 'in', 'it', 'of', 'or', 'see', 'so',
    'that', 'the', 'this', 'to', 'we'
]

LINKS = ["http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d01.html",
"http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d06.html",
"http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d08.html"]

myCrawler = Crawler(LINKS)
myPageRank = PageRank(myCrawler.getLinkStructure())

urls = myCrawler.getVisited()

print("Crawling pages...")
myCrawler.printLinkStructure()

print("Calculating pageranks...")
myPageRank.printPageRank()

index = {}


for url in urls:
    website = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(website)
    text = soup.get_text()
    words = normalize(text)
    title = soup.title.string

    for word in words:
        if word not in stopwords:
            if word not in index:
                index[word] = {}
                index[word][title] = 1
            elif title not in index[word]:
                index[word][title] = 1
            else:
                index[word][title] += 1
index = collections.OrderedDict(sorted(index.items()))

#print index
print("\nBuilding index...")

for word in index:
    print("("+ word + ", df:" + str(len(index[word])) + ")" + " -> " + str(list(index[word].items())))
