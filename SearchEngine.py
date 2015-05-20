__author__ = 's0539720'

from Crawler import Crawler
from PageRank import PageRank
from Index import Index
from Scorer import Scorer

class SearchEngine:

    LINKS = [
        "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d01.html",
        "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d06.html",
        "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d08.html"
    ]

    STOPWORDS = [
        'd01', 'd02', 'd03', 'd04', 'd05', 'd06', 'd07', 'd08',
        'a', 'also', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'do',
        'for', 'have', 'is', 'in', 'it', 'of', 'or', 'see', 'so',
        'that', 'the', 'this', 'to', 'we'
    ]

    def __init__(self):
        myCrawler = Crawler(self.LINKS)
        crawledURLs = myCrawler.getVisited()
        linkStructure = myCrawler.getLinkStructure()
        print("Link-Struktur:\n")
        myCrawler.printLinkStructure()

        myPageRank = PageRank(linkStructure)
        pageRanks = myPageRank.getPageRank()
        print("\n\nPageRanks:\n")
        myPageRank.printPageRank()

        myIndex = Index(self.STOPWORDS, crawledURLs)
        index = myIndex.getIndex()
        print("\n\nIndex:\n")
        myIndex.printIndex()

        myScorer = Scorer(pageRanks, index,linkStructure)
        #myScorer.usePageRank(True)
        print("\n\nDokumentenlängen:\n")
        myScorer.printDocumentLengths()
        print("\n\nSuchergebnisse:\n")
        myScorer.calculateScores(["tokens"])
        myScorer.calculateScores(["index"])
        myScorer.calculateScores(["classification"])
        myScorer.calculateScores(["tokens", "classification"])

SearchEngine()