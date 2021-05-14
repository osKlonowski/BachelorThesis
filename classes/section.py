import pandas as pd


class Section:
    def __init__(self, pairs):
        self.pairs = pairs
        self.listPairIds = []
        # self.df = pd.DataFrame

    def setListPairIds(self, list):
        self.listPairIds = list

    def assignMeetingsMatrix(self, matrix):
        self.meetings_matrix = matrix

    def assignWaitingVector(self, vector):
        self.waiting_vector = vector
