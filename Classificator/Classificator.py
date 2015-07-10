__author__ = 's0539720'

import glob
import os
import math
import re

class Classificator:

    TRAININGDATA = {
        "politik" : "./data/politik/train",
        "sport" : "./data/sport/train",
        "wirtschaft" : "./data/wirtschaft/train"
    }

    TESTINGDATA = {
        "politik" : "./data/politik/test",
        "sport" : "./data/sport/test",
        "wirtschaft" : "./data/wirtschaft/test"
    }

    __N = 0     #number of documents
    __Nc = {}   #numberof documents in class
    __classWordCount = {}   #number of words in all documents of the class
    __Tct = {}    #V = Tct.keys()
    __Vc = {}     #V of Class c
    __prior = {}
    __condprob = {}

    __translation_table = {
        "ß": "ss",
        "ä": "ae",
        "ö": "oe",
        "ü": "ue"
    }

    def __normalize(self, text):
        text = text.lower()
        text = text.translate(str.maketrans(self.__translation_table))
        words = re.compile('\w+').findall(text)
        return words

    def __countTokens(self):
        for topic in self.TRAININGDATA:
            self.__Nc[topic] = 0
            self.__classWordCount[topic] = 0
            self.__Vc[topic] = []

            for document in glob.glob(os.path.join(self.TRAININGDATA[topic], '*.txt')):
                self.__N += 1
                self.__Nc[topic] += 1
                f = open(document, encoding="utf8")
                text = self.__normalize(f.read())

                for word in text:
                    self.__classWordCount[topic] += 1
                    if word not in self.__Tct.keys():
                        self.__Tct[word] = {}
                        for topik in self.TRAININGDATA:
                            self.__Tct[word][topik] = 0
                    self.__Tct[word][topic] += 1
                    if self.__Tct[word][topic] == 1:
                        self.__Vc[topic].append(word)

    def __calculateCondprob(self):
        for topic in self.__Vc:
            for term in self.__Tct.keys():
                if term not in self.__condprob:
                    self.__condprob[term] = {}
                self.__condprob[term][topic] = (self.__Tct[term][topic] + 1.0) / (self.__classWordCount[topic] + len(self.__Tct.keys()))

    def doTraining(self):
        self.__countTokens()
        self.__calculateCondprob()

        for topic in self.__Nc:
            self.__prior[topic] = self.__Nc[topic] / self.__N

    def __extractTokensFromDoc(self, document):
        f = open(document, encoding="utf8")
        W = []
        text = self.__normalize(f.read())

        for word in text:
            if word in self.__Tct.keys() and word not in W:
                W.append(word)
        return W

    def doTesting(self):
        score = {}
        for clazz in self.TESTINGDATA:
            print(clazz + "/test")

            for document in glob.glob(os.path.join(self.TESTINGDATA[clazz], '*.txt')):
                W = self.__extractTokensFromDoc(document)
                for topic in self.__Vc:
                    score[topic] = math.log10(self.__prior[topic])

                    for term in W:
                        score[topic] += math.log10(self.__condprob[term][topic])
                print(max(score.keys(), key=(lambda k: score[k])))
            print("")

    def __init__(self):
        self.doTraining()
        self.doTesting()

Classificator()