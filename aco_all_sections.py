from movement import decryptScheduleFile
from preliminaries import getListOfSectionsCompleted
from classes.pair import Pair
from classes.section import Section
import Formigueiro as Formigueiro
import random
import operator
import pandas as pd
import time

### TAKES IN SCHEDULE_FILE ###
### ASSIGN PAIRS A PAIR ID ###
### TRY SAME SCHEDULE WITH DIFFERENT PAIR NUM-ID Mappings ###


class BRIDGEInstance():
    ##### FOR NOW ----> IT WILL BE ONLY ONE SECTION #####
    def __init__(self, section, prev_meetings_matrix, listScheduleRounds, refMatrix):
        self.numRounds = len(listScheduleRounds.rounds)
        self.numPairs = len(section.pairs)
        self.pairs = section.pairs,
        self.pairNums = section.listPairNums
        self.listScheduleRounds = listScheduleRounds
        self.prev_meetings_matrix = prev_meetings_matrix
        self.refMatrix = refMatrix
        self.fitness_best = self.get_theoretical_best_fitness()
        self.fitness_worst = self.get_theoretical_worst_fitness()

    def getPairNumbersSet(self):
        V = set([])
        for num in self.pairNums:
            V.add(num)
        return V

    def getIdsToBeAssignedSet(self):
        U = set([])
        for id in range(1, self.numPairs+1):
            U.add(id)
        return U

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

    def computePairAssignmentCost(self, id, num, rest):
        # ID is in schedule
        # NUM is pair natural number
        # Component is tuple(id, num)
        register = dict(rest)
        # print(f'Register: {register}')
        # print(f'Next Assignment Attempted: ID: {id} to Pair NUM: {num}')
        if len(register) == 0:
            # This has to be the largest value possible
            # Ideal value is 0.01
            return 64
        else:
            cost = 0.01
            # print(f'Checking against register...')
            for assignment in register.items():
                assID = assignment[0]
                assNum = assignment[1]
                # print(f'Existing Assignment: ID: {assID} - NUM: {assNum}')
                if(self.refMatrix[id][assID] != 0):
                    # print(f'In Schedule ID: {assID} meets {id}')
                    cost += self.prev_meetings_matrix[num][assNum]
                    # print(f'Cost of assignment {id} for Pair Num: {num}')
            # print(f'Total Cost of Assignment: ID: {id} -- NUM: {num}')
            # print(f'Cost of this Pair Assignment is: {cost}')
            return cost

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
        return self.instance.computePairAssignmentCost(*component, self.getSolutionComponents())

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


def computeTheoreticalNumberingMatrix(section, listOfRounds):
    # Compute a reference matrix
    series_rows = pd.Series(range(1, len(section.pairs)+1))
    series_cols = pd.Series(range(1, len(section.pairs)+1))
    # CREATE DATA-FRAME BASED ON COMBINED MEETINGS
    df = pd.DataFrame(series_rows.apply(
        lambda x: series_cols.apply(lambda y: 0)))
    df.index = series_rows
    df.columns = series_cols
    for round in listOfRounds.rounds:
        for meeting in round.getTablePairs():
            # single meeting in schedule file
            pair1id = int(meeting[0])
            pair2id = int(meeting[1])
            df[pair1id][pair2id] += 4
            df[pair2id][pair1id] += 4
    print('Theoretical Assignment Reference Matrix is:')
    print(df)
    return df


def compute_final_meeting_matrix_from_solution(listRounds, meeting_matrix, assignments):
    # SOLUTION COMPONENTS IS LIST: [(id, num), (id, num)]
    sample_solution_matrix = meeting_matrix.copy()
    register = dict(assignments)
    for round in listRounds.rounds:
        for meeting in round.getTablePairs():
            # single meeting in schedule file
            pair1num = register[int(meeting[0])]
            pair2num = register[int(meeting[1])]
            sample_solution_matrix[pair1num][pair2num] += 4
            sample_solution_matrix[pair2num][pair1num] += 4
    # Get overhead
    return sample_solution_matrix


def getPairByNum(section, num):
    for pair in section.pairs:
        if pair.num == num:
            return pair


def getPairsFromNUM(assignments):
    register = dict(assignments)
    defin = {}
    for ass in register.items():
        pair = getPairByNum(ass[1])
        defin[ass[0]] = (pair.player1, pair.player2)
    return defin


def compute_all_sections():
    listRounds = decryptScheduleFile(path_to_schedule)
    listOfSections = getListOfSectionsCompleted(
        meeting_history_file, pre_schedule_file)
    for section in listOfSections.sections:
        prev_meetings_matrix = section.meetings_matrix.copy()
        referenceMatrix = computeTheoreticalNumberingMatrix(
            section, listRounds)
        # GENERATE INSTANCE OF THE PROBLEM
        instance = BRIDGEInstance(
            section, prev_meetings_matrix, listRounds, referenceMatrix)
        obj, components = Formigueiro.Solve(
            antCls=BRIDGEAnt, instance=instance, numIterations=1000, numAnts=22, alpha=1, beta=1)
        section.setBestFitnessReached(obj)
        res = components
        res.sort(key=operator.itemgetter(0))
        section.setAssignments(res)
        print(
            f'THEORETICAL BEST FITNESS: {instance.fitness_best/instance.fitness_best}')
        print(f'Fitness Overhead: {obj}')
        print(
            f'THEORETICAL WORST FITNESS: {instance.fitness_worst/instance.fitness_best}')
        res = components
        res.sort(key=operator.itemgetter(0))
        print(f'\nThe assignments are: {res}\n')
    # Show Results
    for section in listOfSections.sections:
        print(f'Section Fitness: {section.best_fitness}')
        print(f'Assignments: {section.assignments}')
        final_matrix = compute_final_meeting_matrix_from_solution(
            listRounds, section.meetings_matrix.copy(), section.assignments)
        print(f'Final Matrix\n{final_matrix}')


start_time = time.time()
compute_all_sections()
print("--- %s seconds ---" % (time.time() - start_time))

# def getPairByNum(num):
#     for pair in section.pairs:
#         if pair.num == num:
#             return pair


# def getPairsFromNUM(assignments):
#     register = dict(assignments)
#     defin = {}
#     for ass in register.items():
#         pair = getPairByNum(ass[1])
#         defin[ass[0]] = (pair.player1, pair.player2)
#     return defin


# print(
#     f'THEORETICAL BEST FITNESS: {instance.fitness_best/instance.fitness_best}')
# print(f'Fitness Overhead: {obj}')
# print(
#     f'THEORETICAL WORST FITNESS: {instance.fitness_worst/instance.fitness_best}')

# res = components
# res.sort(key=operator.itemgetter(0))

# print(
#     f'\nThe assignments are: {res}\n')
# print(f'PAIRS ARE: {getPairsFromNUM(res)}\n')

# # print(
# #     f'Num of Pair Numbers to Ids Assignments in Solution is: {len(components)}')

# final_matrix = compute_final_meeting_matrix_from_solution(
#     prev_meetings_matrix, components)
# print(f'\nORIGINAL MATRIX\n{prev_meetings_matrix}')
# print(f'\n\nFINAL MATRIX\n{final_matrix}')
