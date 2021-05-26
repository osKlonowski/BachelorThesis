from preliminaries import getListOfSectionsCompleted
import Formigueiro as Formigueiro
import random


class BRIDGEInstance():
    ##### FOR NOW ----> IT WILL BE ONLY ONE SECTION #####
    def __init__(self, numOfRounds, numOfPairs, listPairIds, prev_meetings_matrix):
        self.numRounds = numOfRounds
        self.numPairs = numOfPairs
        self.pairIds = listPairIds
        self.prev_meetings_matrix = prev_meetings_matrix
        self.fitness_best = self.get_theoretical_best_fitness()
        self.fitness_worst = self.get_theoretical_worst_fitness()

    def getMeetingMatrix(self):
        return self.prev_meetings_matrix

    def compute_meeting_factor(self, meeting_matrix):
        meeting_factor = 0
        for i in range(1, self.numPairs+1):
            for j in range(1, self.numPairs+1):
                cell_value = meeting_matrix.at[i, j] ** 3
                meeting_factor += cell_value
        return meeting_factor

    def compute_theoretical_best_meeting_matrix(self, meeting_history_matrix, numPairs, numRounds):
        theoretical_optimum_matrix = meeting_history_matrix.copy()
        for pair_num in range(1, numPairs+1):
            for i in range(0, numRounds):
                column = theoretical_optimum_matrix[[pair_num]].copy()
                column.drop([pair_num], axis=0, inplace=True)
                pair_id_least_meetings = column.idxmin()
                theoretical_optimum_matrix[pair_num][int(
                    pair_id_least_meetings)] += 4
                theoretical_optimum_matrix[int(
                    pair_id_least_meetings)][pair_num] += 4
        fitness = self.compute_meeting_factor(theoretical_optimum_matrix)
        print(f'\nTheoretical OPTIMUM Matrix: {fitness/fitness}')
        print(theoretical_optimum_matrix)
        return theoretical_optimum_matrix

    def get_theoretical_best_fitness(self):
        fitness = 0
        if(self.numPairs % 2 == 0):
            matrix = self.compute_theoretical_best_meeting_matrix(
                self.prev_meetings_matrix, self.numPairs, self.numRounds)
            fitness = self.compute_meeting_factor(matrix)
        else:
            # TODO: Still need to do
            pass
        return fitness

    def compute_theoretical_worst_meeting_matrix(self, meeting_history_matrix, numPairs, numRounds):
        theoretical_worst_matrix = meeting_history_matrix.copy()
        for pair_num in range(1, numPairs+1):
            for i in range(0, numRounds):
                column = theoretical_worst_matrix[[pair_num]].copy()
                column.drop([pair_num], axis=0, inplace=True)
                pair_id_least_meetings = column.idxmax()
                theoretical_worst_matrix[pair_num][int(
                    pair_id_least_meetings)] += 4
                theoretical_worst_matrix[int(
                    pair_id_least_meetings)][pair_num] += 4
        fitness = self.compute_meeting_factor(theoretical_worst_matrix)
        print(f'\nTheoretical WORST Matrix: {fitness/self.fitness_best}')
        print(theoretical_worst_matrix)
        return theoretical_worst_matrix

    def get_theoretical_worst_fitness(self):
        fitness = 0
        if(self.numPairs % 2 == 0):
            matrix = self.compute_theoretical_worst_meeting_matrix(
                self.prev_meetings_matrix, self.numPairs, self.numRounds)
            fitness = self.compute_meeting_factor(matrix)
        else:
            # TODO: Still need to do
            pass
        return fitness

    def computePairMeetingCost(self, x, y):
        return (self.prev_meetings_matrix.at[x, y] ** 3) + 1

    # Where "x" is a schedule
    # calculate a new meetings_matrix
    # return a fitness value in range(1, 2)
    def compute_fitness(self, x):
        sample_solution_matrix = self.prev_meetings_matrix.copy()
        for pair1, pair2 in x:
            # print(f'Pair1ID: {pair1}, Pair2ID: {pair2}')
            sample_solution_matrix[int(pair1)][int(pair2)] += 4
            sample_solution_matrix[int(pair2)][int(pair1)] += 4
        meeting_factor = self.compute_meeting_factor(sample_solution_matrix)
        # Get overhead
        return meeting_factor / self.fitness_best


class BRIDGEAnt(Formigueiro.ACS_Ant):
    # THIS WILL RECEIVE A BRIDGE INSTANCE  --- AN INSTANCE OF THE MEETING MATRIX + WAITING VECTOR (if applicable)
    def __init__(self, instance, **kwargs):
        self.instance = instance

        super().__init__(**kwargs)

    def getSolutionComponents(self):
        return (c for c in self.components)

    def addSolutionComponent(self, component):
        # print(
        #     f'Component to be added: {component}: length: {len(list(self.components))}')
        return super().addSolutionComponent(component)

    # OVERRIDE with FITNESS VALUE
    # Compute the generated schedule onto a new meeting matrix
    # Compute the FITNESS VALUE in Respect to the Theoretical Best???
    def getSolutionValue(self):
        return self.instance.compute_fitness(self.getSolutionComponents())

    def getComponentCost(self, component):
        # Component is a tuple, pair of players
        return self.instance.computePairMeetingCost(*component)

    # THIS WILL GENERATE A SINGLE MEETING SCHEDULE
    def constructSolution(self):
        # A set of the form: [1, 2, 3, 4, 5...14, 15, 16]
        V = set(range(1, self.instance.numPairs+1))
        for i in range(0, self.instance.numRounds):
            S = set([])
            while S != V:
                remaining_pairIds = [pairId for pairId in V - S]
                pair1 = random.choice(remaining_pairIds)
                S.add(pair1)
                components = [(pair1, pair2) for pair2 in V - S]
                pair1, pair2 = self.makeDecision(components)
                S.add(pair2)


meeting_history_file = 'bridge_schedules/data2021_pre_balanced/meeting history april 2021'
pre_schedule_file = 'bridge_schedules/data2021_pre_balanced/48 pairs_(3 sections,no_waiting_table)'

listOfSections = getListOfSectionsCompleted(
    meeting_history_file, pre_schedule_file)
section = listOfSections.sections[0]
numOfPairs = len(section.listPairIds)
listPairIds = section.listPairIds
prev_meetings_matrix = section.meetings_matrix.copy()

# GENERATE INSTANCE OF THE PROBLEM
instance = BRIDGEInstance(6, numOfPairs, listPairIds,
                          prev_meetings_matrix)

# ANT-COLONY OPTIMIZATION
# BEST FITNESS IN INTERATION ## GLOBAL BEST FITNESS ## BEST FITNESS FROM ALL ANTS
print('BEST ITER FITNESS -- GLOBAL BEST FITNESS -- BEST ANT FITNESS')
obj, components = Formigueiro.Solve(
    antCls=BRIDGEAnt, instance=instance, numIterations=200, numAnts=25, alpha=1, beta=1)


def compute_final_meeting_matrix_from_solution(meeting_matrix, schedule):
    sample_solution_matrix = meeting_matrix.copy()
    for pair1, pair2 in schedule:
        # print(f'Pair1ID: {pair1}, Pair2ID: {pair2}')
        sample_solution_matrix[int(pair1)][int(pair2)] += 4
        sample_solution_matrix[int(pair2)][int(pair1)] += 4
    return sample_solution_matrix


print(f'Fitness Overhead: {obj}')

print(f'\nThe solution components are: {components}\n')

print(f'Num of Pair Meetings in Solution Schedule is: {len(components)}')

final_matrix = compute_final_meeting_matrix_from_solution(
    prev_meetings_matrix, components)
print(f'\nORIGINAL MATRIX\n{prev_meetings_matrix}')
print(f'\n\nFINAL MATRIX\n{final_matrix}')
