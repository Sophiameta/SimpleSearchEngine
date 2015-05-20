__author__ = 's0539720'

import math
import collections
import operator
from Index import Index
from PageRank import PageRank

class Scorer:

    def __init__(self, pageRanks, index, linkStructure):
        self.__index = index
        self.__pageRanks = pageRanks
        self.__linkStructure = linkStructure
        self.__documentLengths = {}
        self.__N = len(self.__linkStructure)
        self.__calculateDocumentLengths()
        self.__pageRankIsOn = False

    def __calculateDocumentLengths(self):
        for site in self.__linkStructure:
            self.__documentLengths[site] = []

        for word in self.__index:
            for site in self.__index[word]:
                tf = self.__index[word][site]
                df = len(self.__index[word]) + 0.0
                tfidf = (1 + math.log10(tf)) * math.log10(self.__N/df)
                self.__documentLengths[site].append(tfidf)

        for site in self.__documentLengths:
            self.__documentLengths[site] = math.sqrt(sum(i**2 for i in self.__documentLengths[site]))

        self.__documentLengths = collections.OrderedDict(sorted(self.__documentLengths.items()))

    #configuration to decide whether to use the page rank to calculate the score
    def usePageRank(self, usePageRank):
        self.__pageRankIsOn = usePageRank

    def printDocumentLengths(self):
        for site in self.__documentLengths:
            print(site + ':    ' + str(format(self.__documentLengths[site], '.6f')))

    def __calculateQueryLength(self, query):
        queryLength = []
        for term in query:
            df = len(self.__index[term]) + 0.0
            wtq = math.log10(self.__N/df)
            queryLength.append(wtq)
        queryLength = math.sqrt(sum(i**2 for i in queryLength))
        return queryLength


    def calculateScores(self, query):
        scores = {}

        for term in query:
            term = Index.normalize(term)

        queryLength = self.__calculateQueryLength(query)
        for term in query:
            if term in self.__index:
                postingList = self.__index[term]
                df = len(postingList) + 0.0
                wtq = math.log10(self.__N/df)

                for site in postingList:
                    if site not in scores:
                        scores[site] = 0
                    tf = postingList[site]
                    wtd = (1 + math.log10(tf)) * wtq
                    scores[site] += wtd * wtq
        for site in scores:
            scores[site] /= self.__documentLengths[site] * queryLength

        if self.__pageRankIsOn:
            for site in scores:
                scores[site] *= self.__pageRanks[site]

        scores = (sorted(scores.items(), key = operator.itemgetter(1)))
        scores.reverse()
        scores = collections.OrderedDict(scores)

        #print scores
        print(query)
        for site in scores:
            print(site + ':    ' + str(format(scores[site], '.6F')))
