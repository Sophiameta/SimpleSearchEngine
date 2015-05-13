__author__ = 's0539720'

import collections
import numpy as np
from crawl import Crawler


class PageRank:
    def __init__(self, lS):
        self.linkStructure = lS
        self.d = 0.95
        self.t = 1 - self.d
        self.delta = 0.04
        self.N = len(lS) + 0.0
        self.diff = 1.0
        self.diffInStep = [0.0]
        self.step = 1
        self.pageranks = [[1/self.N for i in range(len(lS))]]

    def getTransitionProbabilities(self):
        transitionProbabilities = {}

        #create transition table
        for col in self.linkStructure:
            for row in self.linkStructure:
                transitionProbabilities[(col, row)] = 0

        #fill transition table and order alphabetically
        for site in self.linkStructure:
            outlinks = len(self.linkStructure[site])
            if outlinks > 0:
                for link in self.linkStructure[site]:
                    transitionProbabilities[(site, link)] = (1.0 / outlinks) * self.d + (self.t/self.N)
                for link in self.linkStructure:
                    if transitionProbabilities[(site, link)] == 0:
                        transitionProbabilities[(site, link)] = self.t/self.N
            else:
                for link in self.linkStructure:
                    transitionProbabilities[(site, link)] = 1.0/self.N
        transitionProbabilities = collections.OrderedDict(sorted(transitionProbabilities.items()))
        return transitionProbabilities

    def getTransitions(self):
        #transitionProbabilities dict to matrix like array
        transitions = []
        k = 0
        for i in range(len(self.linkStructure)):
            transitions.append([])
            for j in range(len(self.linkStructure)):
                transitions[i].append(list(self.getTransitionProbabilities().values())[k])
                k += 1
        return transitions

    #calculate pageranks
    def getPageRank(self):
        while self.diff > self.delta:
            self.diff = 0.0
            pagerank = list(np.array(np.asarray(np.matrix(self.pageranks[self.step - 1]) * np.matrix(self.getTransitions()))).reshape(-1,)) # matrix to list
            self.pageranks.append(pagerank)
            for i in range(len(self.linkStructure)):
                self.diff += abs(self.pageranks[self.step][i] - self.pageranks[self.step-1][i])
            self.diffInStep.append(self.diff)
            self.step += 1
        return self.pageranks

    #print sites
    def printPageRank(self):
        pageranks = self.getPageRank()
        sites = "            "
        for site in sorted(self.linkStructure.keys()):
            sites = sites + site + "       "
        sites = sites + "diff"
        print(sites)

        #print pageranks
        for i in range(self.step):
            pageranks[i] = [str(format(x, '.4f')) for x in pageranks[i]]
            print("step: " + str(i) + " " + str(pageranks[i]) + " " + str(format(self.diffInStep[i], '.4f')))

