class ListOfPairs:
    def __init__(self):
        self.pairs = []

    def addPair(self, pair):
        self.pairs.append(pair)

    def sortPairsByRating(self):
        self.pairs.sort()
        # return self.pairs
