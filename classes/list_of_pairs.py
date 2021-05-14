class ListOfPairs:
    def __init__(self):
        self.pairs = []

    def addPair(self, pair):
        self.pairs.append(pair)

    def sortPairsByRating(self):
        self.pairs.sort()
        # return self.pairs

    def setPairIds(self):
        i = 1
        for pair in self.pairs:
            pair.setPairId(i)
            i += 1

    def getIDList(self):
        list = []
        for pair in self.pairs:
            list.append(pair.id)
        return list

    def getPairById(self, idd):
        for pair in self.pairs:
            if(pair.id == idd):
                return pair
