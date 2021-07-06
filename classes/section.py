import pandas as pd


class Section:
    def __init__(self, pairs):
        self.pairs = pairs
        self.listPairNums = []
        self.best_fitness = 0
        self.assignments = []

    def setListPairNumbers(self, list):
        self.listPairNums = list

    def assignMeetingsMatrix(self, matrix):
        self.meetings_matrix = matrix

    def assignWaitingVector(self, vector):
        self.waiting_vector = vector

    def setBestFitnessReached(self, best_fitness):
        self.best_fitness = best_fitness

    def getBestFitness(self):
        return self.best_fitness

    def setAssignments(self, assignments):
        self.assignments = assignments

    def getTotalWaitingValue(self):
        total_waiting = 0
        for pair in self.pairs:
            total_waiting += pair.total_waiting
        return total_waiting
