__author__ = 's0539720'

import collections
import numpy as np
from crawl import Crawler


LINKS = ["http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d01.html",
"http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d06.html",
"http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d08.html"]

myCrawler = Crawler(LINKS)
print("Crawling pages...")

linkStructure = myCrawler.getlinkstructure()



d = 0.95
t = 1 - d
delta = 0.04
N = len(linkStructure) + 0.0
diff = 1.0
diffInStep = [0.0]
step = 1
pageranks = [[1/N for i in range(len(linkStructure))]]

transitionProbabilities = {}
transitions = [[]]

#create transition table
for col in linkStructure:
    for row in linkStructure:
        transitionProbabilities[(col, row)] = 0

#fill transition table and order alphabetically
for site in linkStructure:
    outlinks = len(linkStructure[site])
    if outlinks > 0:
        for link in linkStructure[site]:
            transitionProbabilities[(site, link)] = (1.0 / outlinks) * d + (t/N)
        for link in linkStructure:
                if transitionProbabilities[(site, link)] == 0:
                    transitionProbabilities[(site, link)] = t/N
    else:
        for link in linkStructure:
                transitionProbabilities[(site, link)] = 1.0/N
transitionProbabilities = collections.OrderedDict(sorted(transitionProbabilities.items()))

#transitionProbabilities dict to matrix like array
transitions = []
k = 0
for i in range(len(linkStructure)):
    transitions.append([])
    for j in range(len(linkStructure)):
        transitions[i].append(list(transitionProbabilities.values())[k])
        k += 1

#calculate pageranks
while diff > delta:
    diff = 0.0
    pagerank = list(np.array(np.asarray(np.matrix(pageranks[step - 1]) * np.matrix(transitions))).reshape(-1,)) # matrix to list
    pageranks.append(pagerank)
    for i in range(len(linkStructure)):
        diff += abs(pageranks[step][i] - pageranks[step-1][i])
    diffInStep.append(diff)
    step += 1

#print sites
print("\nCalculating pageranks...")
sites = "            "
for site in sorted(linkStructure.keys()):
    sites = sites + site + "       "
sites = sites + "diff"
print(sites)

#print pageranks
for i in range(step):
    pageranks[i] = [str(format(x, '.4f')) for x in pageranks[i]]
    print("step: " + str(i) + " " + str(pageranks[i]) + " " + str(format(diffInStep[i], '.4f')))
