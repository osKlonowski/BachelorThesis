class Pair:
    def __init__(self, player1, player2):
        self.id = 0
        self.player1 = player1
        self.player2 = player2
        self.players = [player1, player2]
        self.combinedRating = float(0.0)
        self.total_waiting = int(0)

    def __lt__(self, other):
        return self.combinedRating < other.combinedRating

    def setPairRating(self, rate):
        self.combinedRating = float(rate)

    def setPairWaitingTables(self, waiting):
        self.total_waiting = int(waiting)

    def setPairId(self, id):
        self.id = id
