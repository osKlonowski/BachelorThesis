from classes.movement.list_of_rounds import ListOfRounds
from movement import decryptScheduleFile
from preliminaries import getListOfSectionsCompleted
from classes.pair import Pair
from classes.section import Section
import Formigueiro as Formigueiro
import random
import operator
import pandas as pd
import time
# import ray

possibleSchedulePairNums = [8, 10, 12, 14, 16, 18]

schedule_file_registry = {
    8: 'bridge_schedules/schedules/6-rounds-(multiplex)/mpx8-4-6-6.asc',
    10: 'bridge_schedules/schedules/6-rounds-(multiplex)/mpx10-6-6-6.asc',
    12: 'bridge_schedules/schedules/6-rounds-(multiplex)/mpx12-6-6-6.asc',
    14: 'bridge_schedules/schedules/6-rounds-(multiplex)/mpx14-7-6-6.asc',
    16: 'bridge_schedules/schedules/6-rounds-(multiplex)/mpx16-8-6-6.asc',
    18: 'bridge_schedules/schedules/6-rounds-(multiplex)/mpx18-9-6-6.asc',
}

### TAKES IN SCHEDULE_FILE ###
### ASSIGN PAIRS A PAIR ID ###
### TRY SAME SCHEDULE WITH DIFFERENT PAIR NUM-ID Mappings ###

# ray.init()

# @ray.remote
# def f(x):
#     return x * x

# futures = [f.remote(i) for i in range(4)]
# print(ray.get(futures))


def getScheduleFileRounds(numPairs):
    possiblePairNums = [8, 10, 12, 14, 16, 18]
    listRounds = ListOfRounds()
    if numPairs in possiblePairNums:
        file = schedule_file_registry[numPairs]
        listRounds = decryptScheduleFile(file)
    else:
        print(f'Num Pairs: {numPairs} -> trying; {numPairs + 1}')
        num = numPairs + 1
        file = schedule_file_registry[num]
        listRounds = decryptScheduleFile(file)
    return listRounds


class BRIDGEInstance():
    ##### FOR NOW ----> IT WILL BE ONLY ONE SECTION #####
    def __init__(self, section, prev_meetings_matrix, prev_waiting_vector, listRounds, refMatrix):
        self.possibleSchedulePairs = possibleSchedulePairNums
        self.solutionsTried = 0
        self.section = section
        self.numRounds = len(listRounds.rounds)
        self.numPairs = len(section.pairs)
        self.pairs = section.pairs,
        self.pairNums = section.listPairNums
        self.listScheduleRounds = listRounds
        self.prev_meetings_matrix = prev_meetings_matrix
        self.prev_waiting_vector = prev_waiting_vector
        self.refMatrix = refMatrix
        self.fitness_best = self.compute_theoretical_best_fitness(
            len(section.pairs) % 2 != 0, prev_meetings_matrix, prev_waiting_vector, len(listRounds.rounds))
        self.fitness_worst = self.compute_theoretical_worst_fitness(
            len(section.pairs) % 2 != 0, prev_meetings_matrix, prev_waiting_vector, len(listRounds.rounds))
        self.hasWaitingTable = len(section.pairs) % 2 != 0

    def getPairNumbersSet(self):
        V = set([])
        for num in self.pairNums:
            V.add(num)
        if self.hasWaitingTable:
            V.add(0)
        return V

    def getIdsToBeAssignedSet(self):
        U = set([])
        if self.hasWaitingTable:
            for id in range(1, self.numPairs+2):
                U.add(id)
        else:
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

    def compute_waiting_factor(self, waiting_vector):
        waiting_factor = 0
        for val in waiting_vector:
            waiting_factor += val ** 6
        return waiting_factor

    def compute_theoretical_best_fitness(self, hasWaitingTable, meeting_history_matrix, waiting_vector, numRounds):
        meeting_factor = 0
        waiting_factor = 0
        if hasWaitingTable:
            theoretical_waiting_vector = waiting_vector.copy()
            for _ in range(0, numRounds):
                minVal = theoretical_waiting_vector.min()
                index = list(theoretical_waiting_vector).index(minVal)
                theoretical_waiting_vector[index] += 2
            waiting_factor = self.compute_waiting_factor(
                theoretical_waiting_vector)
        theoretical_optimum_matrix = meeting_history_matrix.copy()
        for pair_num in self.pairNums:
            for _ in range(0, numRounds):
                column = theoretical_optimum_matrix[[pair_num]].copy()
                column.drop([pair_num], axis=0, inplace=True)
                pair_id_least_meetings = column.idxmin()
                theoretical_optimum_matrix[pair_num][int(
                    pair_id_least_meetings)] += 4
                theoretical_optimum_matrix[int(
                    pair_id_least_meetings)][pair_num] += 4
        meeting_factor = self.compute_meeting_factor(
            theoretical_optimum_matrix)
        fitness = meeting_factor + waiting_factor
        print(
            f'\nTheoretical OPTIMUM Fitness: {fitness} RATIO: {fitness/fitness}')
        return fitness

    def compute_theoretical_worst_fitness(self, hasWaitingTable, meeting_history_matrix, waiting_vector, numRounds):
        meeting_factor = 0
        waiting_factor = 0
        if hasWaitingTable:
            theoretical_waiting_vector = waiting_vector.copy()
            for _ in range(0, numRounds):
                maxVal = theoretical_waiting_vector.max()
                index = list(theoretical_waiting_vector).index(maxVal)
                theoretical_waiting_vector[index] += 2
            waiting_factor = self.compute_waiting_factor(
                theoretical_waiting_vector)
        theoretical_worst_matrix = meeting_history_matrix.copy()
        for pair_num in self.pairNums:
            for _ in range(0, numRounds):
                column = theoretical_worst_matrix[[pair_num]].copy()
                column.drop([pair_num], axis=0, inplace=True)
                pair_id_least_meetings = column.idxmax()
                theoretical_worst_matrix[pair_num][int(
                    pair_id_least_meetings)] += 4
                theoretical_worst_matrix[int(
                    pair_id_least_meetings)][pair_num] += 4
        meeting_factor = self.compute_meeting_factor(theoretical_worst_matrix)
        fitness = meeting_factor + waiting_factor
        print(
            f'Theoretical WORST Fitness: {fitness} RATIO: {fitness/self.fitness_best}\n')
        return fitness

    def getWaitingTablePenalty(self, id, num):
        # TODO: Find a way to evaluate the pair waiting table assignment - maybe just try different value for this??? huh?
        return 0.01 ** 6

    def computePairAssignmentCost(self, id, num, rest):
        # ID is in schedule
        # NUM is pair natural number
        # Component is tuple(id, num)
        register = dict(rest)
        # Ideal value is 0.01
        if len(register) == 0:
            # This has to be the largest value possible or it doesn't matter
            return self.numPairs ** 3
        elif num == 0:
            return self.getWaitingTablePenalty(id, num)
        else:
            cost = 0.01
            # print(f'Checking against register...')
            rec = {key: val for key, val in register.items() if val != 0}
            for assignment in rec.items():
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

    def compute_fitness(self, x):
        # SOLUTION COMPONENTS IS LIST: [(id, num), (id, num)]
        sample_solution_matrix = self.prev_meetings_matrix.copy()
        sample_waiting_vector = self.prev_waiting_vector.copy()
        register = dict(x)
        for round in self.listScheduleRounds.rounds:
            for meeting in round.getTablePairs():
                if register[int(meeting[0])] == 0 or register[int(meeting[1])] == 0:
                    # This is a waiting table assignment
                    if register[int(meeting[0])] == 0:
                        # register[int(meeting[1])] has a waiting table
                        waitingTablePairNum = register[int(meeting[1])]
                        indexOfWaitingTableVictim = self.pairNums.index(
                            waitingTablePairNum)
                        sample_waiting_vector[indexOfWaitingTableVictim] += 2
                        pass
                    else:
                        # register[int(meeting[0])] has a waiting table
                        waitingTablePairNum = register[int(meeting[0])]
                        indexOfWaitingTableVictim = self.pairNums.index(
                            waitingTablePairNum)
                        sample_waiting_vector[indexOfWaitingTableVictim] += 2
                        pass
                    pass
                else:
                    pair1num = register[int(meeting[0])]
                    pair2num = register[int(meeting[1])]
                    sample_solution_matrix[pair1num][pair2num] += 4
                    sample_solution_matrix[pair2num][pair1num] += 4
        meeting_factor = self.compute_meeting_factor(sample_solution_matrix)
        if self.hasWaitingTable:
            # Get the index of the Pair Num that was assigned the waiting table
            # indexOfWaitingTableVictim = self.pairNums.index(register[0])
            # sample_waiting_vector[indexOfWaitingTableVictim] += 2
            waiting_factor = self.compute_waiting_factor(sample_waiting_vector)
            return (meeting_factor + waiting_factor) / self.fitness_best
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
        self.instance.solutionsTried += 1


meeting_history_file = 'bridge_schedules/data2021_pre_balanced/meeting history april 2021'
pre_schedule_waiting_table = 'bridge_schedules/data2021_pre_balanced/51pairs_(3_sections,_waiting table)'
path_to_schedule = 'bridge_schedules/schedules/mpx-16-8-6-6-0.asc'


def computeTheoreticalNumberingMatrix(section, listOfRounds):
    matrix_size = len(section.pairs)
    if matrix_size not in possibleSchedulePairNums:
        matrix_size += 1
    # Compute a reference matrix
    series_rows = pd.Series(range(1, matrix_size+1))
    series_cols = pd.Series(range(1, matrix_size+1))
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


def compute_final_meeting_matrix_from_solution(pairNums, listRounds, meeting_matrix, prev_waiting_vector, assignments):
    # SOLUTION COMPONENTS IS LIST: [(id, num), (id, num)]
    sample_solution_matrix = meeting_matrix.copy()
    sample_waiting_vector = prev_waiting_vector.copy()
    register = dict(assignments)
    for round in listRounds.rounds:
        for meeting in round.getTablePairs():
            # single meeting in schedule file
            if register[int(meeting[0])] == 0 or register[int(meeting[1])] == 0:
                # waiting table assigned to either of the pairs here.
                if register[int(meeting[0])] == 0:
                    index = pairNums.index(register[int(meeting[1])])
                    sample_waiting_vector[index] += 2
                else:
                    index = pairNums.index(register[int(meeting[0])])
                    sample_waiting_vector[index] += 2
            else:
                pair1num = register[int(meeting[0])]
                pair2num = register[int(meeting[1])]
                sample_solution_matrix[pair1num][pair2num] += 4
                sample_solution_matrix[pair2num][pair1num] += 4
    # Get overhead
    return [sample_solution_matrix, sample_waiting_vector]


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
    # listRounds = decryptScheduleFile(path_to_schedule)
    listOfSections = getListOfSectionsCompleted(
        meeting_history_file, pre_schedule_waiting_table, True)
    for section in listOfSections.sections:
        prev_meetings_matrix = section.meetings_matrix.copy()
        prev_waiting_vector = section.waiting_vector.copy()
        listRounds = getScheduleFileRounds(len(section.pairs))
        referenceMatrix = computeTheoreticalNumberingMatrix(
            section, listRounds)
        # GENERATE INSTANCE OF THE PROBLEM
        instance = BRIDGEInstance(
            section, prev_meetings_matrix, prev_waiting_vector, listRounds, referenceMatrix)
        obj, components = Formigueiro.Solve(
            antCls=BRIDGEAnt, instance=instance, numIterations=5000, numAnts=50, alpha=3, beta=0.8, Q=2)
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
        # The num of solutions tried is obviously num of iterations * num of ants
        print(f'\nNum of Solutions Constructed: {instance.solutionsTried}\n')
        print(f'\nThe assignments are: {res}\n')
    # Show Results
    for section in listOfSections.sections:
        print('\n\n')
        print(f'Section Fitness: {section.best_fitness}')
        print(f'Assignments: {section.assignments}')
        final_matrix_vector = compute_final_meeting_matrix_from_solution(
            section.listPairNums, listRounds, section.meetings_matrix.copy(), section.waiting_vector.copy(), section.assignments)
        print(f'Final Matrix\n{final_matrix_vector[0]}')
        if len(section.pairs) % 2 != 0:
            # print(f'Prev Waiting Vector\n{section.waiting_vector}')
            print(f'Waiting Vector\n{final_matrix_vector[1]}')


start_time = time.time()
compute_all_sections()
print("--- %s seconds ---" % (time.time() - start_time))
