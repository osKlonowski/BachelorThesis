
class ListOfPlayers:
    def __init__(self):
        self.players = []

    def addPlayer(self, player):
        self.players.append(player)

    def getNumOfPlayers(self):
        return len(self.players)

    def sortPlayers(self):
        self.players.sort()
        return self.players
