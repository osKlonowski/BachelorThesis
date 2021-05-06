class Player:
    # { ID, Rating, List of Meeting Counts per Player ID }
    def __init__(self, id_num, rating, listMeetingIds):
        self.id = id_num
        self.rating = float(rating)
        self.listMeetingIds = [int(i) for i in listMeetingIds.split(',')]

    def __lt__(self, other):
        return self.rating < other.rating

    def getNumOfEncounters(self):
        # TODO: Remove number of waiting table encounters from the front of the list.
        nonZeroEncounters = sum(x > 0 for x in self.listMeetingIds)
        return int(nonZeroEncounters)

    def getRating(self):
        return float(self.rating)
