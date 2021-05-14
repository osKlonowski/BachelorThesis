class ListOfRounds:
    def __init__(self):
        self.rounds = []

    def addRound(self, round):
        self.rounds.append(round)

    def printAll(self):
        for round in self.rounds:
            print(round.getTablePairs())

    def getListOfPairMeetings(self):
        list = []
        for round in self.rounds:
            list.append(round.getTablePairs())
        return list
