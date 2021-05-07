class Player:
    # { ID, Rating, List of Meeting Counts per Player ID }
    def __init__(self, id_num, rating, meeting_history, waiting_tables):
        self.id = id_num
        self.rating = float(rating)
        self.meeting_history = meeting_history
        self.num_waiting_tables = waiting_tables

    def __lt__(self, other):
        return self.rating < other.rating

    def getNumOfEncounters(self):
        nonZeroEncounters = sum(x > 0 for x in self.meeting_history)
        return int(nonZeroEncounters)

    def getRating(self):
        return float(self.rating)
