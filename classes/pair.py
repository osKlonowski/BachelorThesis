# def combineMeetingHistories(meeting_history_one, meeting_history_two):
#     list = []
#     for i in range(0, len(meeting_history_one)):
#         list.append(meeting_history_one[i]+meeting_history_two[i])
#     return list


# , player1_meeting_history, player2_meeting_history
class Pair:
    def __init__(self, player1, player2):
        self.id = 0
        self.num = 0
        self.player1 = player1
        self.player2 = player2
        self.players = [player1, player2]
        self.combinedRating = float(0.0)
        self.total_waiting = int(0)
        # self.combined_meeting_history = combineMeetingHistories(
        #     player1_meeting_history, player2_meeting_history)

    def __lt__(self, other):
        return self.combinedRating < other.combinedRating

    def setPairRating(self, rate):
        self.combinedRating = float(rate)

    def setPairWaitingTables(self, waiting):
        self.total_waiting = int(waiting)

    def setPairId(self, id):
        self.id = id

    def setPairNum(self, num):
        self.num = num
