__author__ = 's0539720'

import collections
import numpy as np


class PageRank:
    def __init__(self, linkStructure):
        self.__linkStructure = linkStructure
        self.__d = 0.95
        self.__t = 1 - self.__d
        self.__delta = 0.04
        self.__diffInStep = [0.0]
        self.__N = len(self.__linkStructure) + 0.0
        self.__pageRanks = [[1/self.__N for i in range(len(self.__linkStructure))]]
        __transitions = self.__getTransitionProbabilities()
        self.__calculatePageRank(__transitions)

    def __getTransitionProbabilities(self):
        transitionProbabilities = {}

        #create transition table
        for col in self.__linkStructure:
            for row in self.__linkStructure:
                transitionProbabilities[(col, row)] = 0

        #fill transition table and order alphabetically
        for site in self.__linkStructure:
            outlinks = len(self.__linkStructure[site])
            if outlinks > 0:
                for link in self.__linkStructure[site]:
                    transitionProbabilities[(site, link)] = (1.0 / outlinks) * self.__d + (self.__t/self.__N)
                for link in self.__linkStructure:
                    if transitionProbabilities[(site, link)] == 0:
                        transitionProbabilities[(site, link)] = self.__t/self.__N
            else:
                for link in self.__linkStructure:
                    transitionProbabilities[(site, link)] = 1.0/self.__N
        transitionProbabilities = collections.OrderedDict(sorted(transitionProbabilities.items()))

        #transform transitionProbabilities dictionary into a matrixlike array
        transitions = []
        k = 0
        for i in range(len(self.__linkStructure)):
            transitions.append([])
            for j in range(len(self.__linkStructure)):
                transitions[i].append(list(transitionProbabilities.values())[k])
                k += 1
        return transitions

    #calculate pageranks
    def __calculatePageRank(self, transitions):
        diff = 1.0
        step = 0

        while diff > self.__delta:
            step += 1
            diff = 0.0
            pageRank = list(np.array(np.asarray(np.matrix(self.__pageRanks[step - 1]) * np.matrix(transitions))).reshape(-1,)) # matrix to list
            self.__pageRanks.append(pageRank)
            for i in range(len(self.__linkStructure)):
                diff += abs(self.__pageRanks[step][i] - self.__pageRanks[step-1][i])
            self.__diffInStep.append(diff)

    def getPageRank(self):
        #create dictionary with sites as keys and pagerank as values
        pageRank = {}
        lastStep = len(self.__pageRanks) - 1
        i = 0
        for site in self.__linkStructure:
            pageRank[site] = self.__pageRanks[lastStep][i]
            i += 1
        return pageRank

    def printPageRank(self):
        #print name of sites
        sites = "            "
        for site in sorted(self.__linkStructure.keys()):
            sites = sites + site + "       "
        sites = sites + "diff"
        print(sites)

        #print pageranks of sites
        for i in range(len(self.__pageRanks)):
            self.__pageRanks[i] = [str(format(x, '.4f')) for x in self.__pageRanks[i]]
            print("step: " + str(i) + " " + str(self.__pageRanks[i]) + " " + str(format(self.__diffInStep[i], '.4f')))
