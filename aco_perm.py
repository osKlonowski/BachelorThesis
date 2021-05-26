from movement import decryptScheduleFile
from preliminaries import getListOfSectionsCompleted
from classes.pair import Pair
from classes.section import Section
import Formigueiro as Formigueiro
import random
import operator

### TAKES IN SCHEDULE_FILE ###
### ASSIGN PAIRS A PAIR ID ###
### TRY SAME SCHEDULE WITH DIFFERENT PAIR NUM-ID Mappings ###


class BRIDGEInstance():
    ##### FOR NOW ----> IT WILL BE ONLY ONE SECTION #####
    def __init__(self, section, prev_meetings_matrix, listScheduleRounds):
        self.numRounds = len(listScheduleRounds.rounds)
        self.numPairs = len(section.pairs)
        self.pairs = section.pairs,
        self.pairNums = section.listPairNums
        self.listScheduleRounds = listScheduleRounds
        self.prev_meetings_matrix = prev_meetings_matrix
        self.fitness_best = self.get_theoretical_best_fitness()
        self.fitness_worst = self.get_theoretical_worst_fitness()

    def getPairNumbersSet(self):
        V = set([])
        for num in self.pairNums:
            V.add(num)
        return V

    def getPairNumbersList(self):
        list = []
        for pairNum in self.pairNums:
            list.append(int(pairNum))
        return list

    def getIdsToBeAssignedSet(self):
        U = set([])
        for id in range(1, self.numPairs+1):
            U.add(id)
        # for round in self.listScheduleRounds.rounds:
        #     for meeting in round.getTablePairs():
        #         for id in meeting:
        #             if id not in U:
        #                 U.add(int(id))
        return U

    def getIdsToBeAssignedList(self):
        list = []
        for round in self.listScheduleRounds.rounds:
            for meeting in round.getTablePairs():
                for id in meeting:
                    if id not in list:
                        list.append(int(id))
        return list

    def getMeetingMatrix(self):
        return self.prev_meetings_matrix

    def compute_meeting_factor(self, meeting_matrix):
        meeting_factor = 0
        for pair1 in self.pairNums:
            for pair2 in self.pairNums:
                cell_value = meeting_matrix.at[pair1, pair2] ** 3
                meeting_factor += cell_value
        return meeting_factor

    def compute_theoretical_best_meeting_matrix(self, meeting_history_matrix, numRounds):
        theoretical_optimum_matrix = meeting_history_matrix.copy()
        for pair_num in self.pairNums:
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
                self.prev_meetings_matrix, self.numRounds)
            fitness = self.compute_meeting_factor(matrix)
        else:
            # TODO: Still need to do
            pass
        return fitness

    def compute_theoretical_worst_meeting_matrix(self, meeting_history_matrix, numRounds):
        theoretical_worst_matrix = meeting_history_matrix.copy()
        for pair_num in self.pairNums:
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
                self.prev_meetings_matrix, self.numRounds)
            fitness = self.compute_meeting_factor(matrix)
        else:
            # TODO: Still need to do
            pass
        return fitness

    def computePairAssignmentCost(self, id, num):
        # TODO: NEEDS SOMETHING MUCH BETTER
        # ID is in schedule
        # NUM is pair natural number
        # Component is tuple(id, num)
        # return self.prev_meetings_matrix[[num]].max() ** 3 + 1
        # return random.randint(1, 20)
        return id+num

    # return a fitness value in range(1, 2)
    def compute_fitness(self, x):
        # SOLUTION COMPONENTS IS LIST: [(id, num), (id, num)]
        sample_solution_matrix = self.prev_meetings_matrix.copy()
        register = dict(x)
        for round in self.listScheduleRounds.rounds:
            for meeting in round.getTablePairs():
                # single meeting in schedule file
                pair1num = register[int(meeting[0])]
                pair2num = register[int(meeting[1])]
                sample_solution_matrix[pair1num][pair2num] += 4
                sample_solution_matrix[pair2num][pair1num] += 4
        meeting_factor = self.compute_meeting_factor(sample_solution_matrix)
        # Get overhead
        return meeting_factor / self.fitness_best


class BRIDGEAnt(Formigueiro.ACS_Ant):
    # THIS WILL RECEIVE A BRIDGE INSTANCE  --- AN INSTANCE OF THE MEETING MATRIX + WAITING VECTOR (if applicable)
    def __init__(self, instance, **kwargs):
        self.instance = instance

        super().__init__(**kwargs)

    # OVERRIDE with FITNESS VALUE
    # Compute the generated schedule onto a new meeting matrix
    # Compute the FITNESS VALUE in Respect to the Theoretical Best???
    def getSolutionValue(self):
        # SOLUTION COMPONENTS IS LIST: [(id, num), (id, num)]
        return self.instance.compute_fitness(self.getSolutionComponents())

    def getComponentCost(self, component):
        # Component is tuple(id, num)
        return self.instance.computePairAssignmentCost(*component)

    def constructSolution(self):
        # Set of NUMS
        V = self.instance.getPairNumbersSet()
        U = self.instance.getIdsToBeAssignedSet()
        L = set([])
        P = set([])
        while L != V:
            remaining_ids = [id for id in U - P]
            id = random.choice(remaining_ids)
            P.add(id)
            components = [(id, num) for num in V - L]
            _, num = self.makeDecision(components)
            L.add(num)


meeting_history_file = 'bridge_schedules/data2021_pre_balanced/meeting history april 2021'
pre_schedule_file = 'bridge_schedules/data2021_pre_balanced/48 pairs_(3 sections,no_waiting_table)'
path_to_schedule = 'bridge_schedules/schedules/mpx-16-8-6-6-0.asc'

listRounds = decryptScheduleFile(path_to_schedule)

listOfSections = getListOfSectionsCompleted(
    meeting_history_file, pre_schedule_file)
section = listOfSections.sections[0]
prev_meetings_matrix = section.meetings_matrix.copy()

for pair in section.pairs:
    print(f'Pair NUM: {pair.num} -- ID: {pair.id}')

# GENERATE INSTANCE OF THE PROBLEM
instance = BRIDGEInstance(section, prev_meetings_matrix, listRounds)

# ANT-COLONY OPTIMIZATION
# BEST FITNESS IN INTERATION ## GLOBAL BEST FITNESS ## BEST FITNESS FROM ALL ANTS
print('BEST ITER FITNESS -- GLOBAL BEST FITNESS -- BEST ANT FITNESS')
obj, components = Formigueiro.Solve(
    antCls=BRIDGEAnt, instance=instance, numIterations=50, numAnts=5, alpha=1, beta=1)


# def compute_final_meeting_matrix_from_solution(meeting_matrix, schedule):
#     sample_solution_matrix = meeting_matrix.copy()
#     for pair1, pair2 in schedule:
#         # print(f'Pair1ID: {pair1}, Pair2ID: {pair2}')
#         sample_solution_matrix[int(pair1)][int(pair2)] += 4
#         sample_solution_matrix[int(pair2)][int(pair1)] += 4
#     return sample_solution_matrix


print(f'Fitness Overhead: {obj}')

res = components
res.sort(key=operator.itemgetter(0))

print(
    f'\nThe assignments are: {res}\n')

print(
    f'Num of Pair Numbers to Ids Assignments in Solution is: {len(components)}')

# final_matrix = compute_final_meeting_matrix_from_solution(
#     prev_meetings_matrix, components)
# print(f'\nORIGINAL MATRIX\n{prev_meetings_matrix}')
# print(f'\n\nFINAL MATRIX\n{final_matrix}')
