__author__ = 's0539720'

import urllib.request
from bs4 import BeautifulSoup
import re
import collections

class Index:

    def __init__(self, stopwords, urls):
        self.__stopwords = stopwords
        self.__urls = urls
        self.__index = {}
        self.__calculateIndex()

    @staticmethod
    def normalize(text):
        text = text.lower()
        words = re.compile('\w+').findall(text)
        return words

    def __calculateIndex(self):
        for url in self.__urls:
            website = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(website)
            text = soup.get_text()
            words = self.normalize(text)
            title = soup.title.string

            for word in words:
                if word not in self.__stopwords:
                    if word not in self.__index:
                        self.__index[word] = {}
                        self.__index[word][title] = 1
                    elif title not in self.__index[word]:
                        self.__index[word][title] = 1
                    else:
                        self.__index[word][title] += 1
        self.__index = collections.OrderedDict(sorted(self.__index.items()))

    def getIndex(self):
        return self.__index

    #print index
    def printIndex(self):
        for word in self.__index:
            print(word + ", df:" + str(len(self.__index[word])) + " -> " + str(self.__index[word]))
