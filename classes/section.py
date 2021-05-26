import pandas as pd


class Section:
    def __init__(self, pairs):
        self.pairs = pairs
        self.listPairNums = []

    def setListPairNumbers(self, list):
        self.listPairNums = list

    def assignMeetingsMatrix(self, matrix):
        self.meetings_matrix = matrix

    def assignWaitingVector(self, vector):
        self.waiting_vector = vector
