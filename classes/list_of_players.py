
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

    def getPlayerRating(self, playerId):
        return next((float(player.rating)
                     for player in self.players if player.id == playerId), None)

    def getPlayerWaitingTables(self, playerId):
        return next((int(player.num_waiting_tables)
                     for player in self.players if player.id == playerId), None)
