from movement import decryptScheduleFile
from classes.movement.list_of_rounds import ListOfRounds
from preliminaries import getListOfSectionsCompleted
from math import *

# Compute a matrix of meetings and a vector of waiting tables:

# Start from a copy of the “previous meetings matrix”,
# use the schedule file for the respective number of pairs (and rounds)
# such that for all meetings that happen in the new tournament
# the number of meetings among two pairs will be incremented by 4.
# (two players each meeting two other players)

# Start with a copy of the vector of “previous waiting tables”.
# For each pair having a waiting table increment their value by 2.
# (both players have a waiting table)

####
####

# Get Previous Meetings Matrix and Waiting Tables Vector
meeting_history_file = 'bridge_schedules/data2021_pre_balanced/meeting history april 2021'
pre_schedule_file = 'bridge_schedules/data2021_pre_balanced/48 pairs_(3 sections,no_waiting_table)'


# listOfSections = getListOfSectionsCompleted(
#     meeting_history_file, pre_schedule_file)

##### START WITH ONE SECTION OF 16 PLAYERS #######
# section = listOfSections.sections[0]
# numOfPairs = len(section.listPairIds)

# print(section.meetings_matrix)
# print(section.waiting_vector)

#### COPYING PREVIOUS MEETING MATRIX #####
# prev_meeting_matrix = section.meetings_matrix.copy()

# print(prev_meeting_matrix)

#### COPYING WAITING VECTOR #######
# prev_waiting_vector = section.waiting_vector.copy()

# Example -- Basic Schedule File Header
# number of pairs    number of tables    number of rounds    number of board groups    Individual=0
# path_to_schedule = 'bridge_schedules/schedules/mpx-16-8-6-6-0.asc'

# listRounds = decryptScheduleFile(path_to_schedule)

# listOfPairMeetings = listRounds.getListOfPairMeetings()

# new_meetings_matrix = prev_meeting_matrix.copy()
# for round in listOfPairMeetings:
#     for pairMeeting in round:
#         i = int(pairMeeting[0])
#         j = int(pairMeeting[1])
#         # print(f'Pair I: {i}, Pair J: {j}')
#         prev_meeting_count = prev_meeting_matrix.at[i, j]
#         new_meetings_matrix.at[i, j] = int(prev_meeting_count+4)

# print('\nOriginal Meeting Matrix Before Anything')
# print(prev_meeting_matrix)
# # print(prev_waiting_vector)
# print('\nNEW Meeting Matrix After GENERATED Schedule is Applied')
# print(new_meetings_matrix)

######### FITNESS FUNCTION #########
# The fitness is the sum of the meeting factor and the waiting factor.
# The meeting factor is the sum over all entries in the matrix, where each entry is taken to the third power.
# The waiting factor is the sum over all entries in the vector, where each entry is taken to the sixth power.
# the waiting factor only applies when a section has an odd number of pairs


def compute_meeting_factor(numPairs, meeting_matrix):
    meeting_factor = 0
    for i in range(1, numPairs+1):
        for j in range(1, numPairs+1):
            cell_value = meeting_matrix.at[i, j] ** 3
            meeting_factor += cell_value
    return meeting_factor


def compute_waiting_factor(waiting_vector):
    waiting_factor = 0
    for item in waiting_vector:
        val = item ** 6
        waiting_factor += val
    return waiting_factor


def compute_fitness_even(meeting_matrix):
    meeting_factor = compute_meeting_factor(16, meeting_matrix)
    return meeting_factor


def compute_fitness_odd(meeting_matrix, waiting_vector):
    meeting_factor = compute_meeting_factor(16, meeting_matrix)
    waiting_factor = compute_waiting_factor(waiting_vector)
    return meeting_factor + waiting_factor


# fitness_value_new = compute_fitness_even(new_meetings_matrix)

# print(
#     f'Fitness: {fitness_value_new}')

##### GENERATE THE THEORETICAL BEST CASE ###########
# the theoretical minimum fitness value is: given a meeting history matrix for a section, and a waiting table vector for the same section (if applicable).
# If the section has a waiting table, let those pairs have a waiting table who had the least ones in the past.
# For all pairs, assign a meeting with those other pairs with whom they had the fewest meetings so far.
# (Those pairs who are assigned a waiting table, get one meeting less than those who are not.) In total, each pair has as many entries in the meeting matrix as there are rounds.
# In practice, you need to sort the waiting table vector, and for each pair, the number of past meetings with the other pairs in the section.
# Then you can create a new meeting matrix with the values that represent such a theoretically optimal tournament schedule.

# numOfRounds = len(listRounds.rounds)


def create_theoretical_best_waiting_vector(waiting_table_vector):
    # TODO: Still need to finish, and pair with assigned table, gets one less meeting
    minimum = min(waiting_table_vector)
    return minimum


def compute_theoretical_best_meeting_matrix(meeting_history_matrix, numPairs, numRounds):
    theoretical_optimum_matrix = meeting_history_matrix.copy()
    for pair_num in range(1, numPairs+1):
        # Get the id of pair with which pair 'i' has had the least amount of meetings.
        pair_id_least_meetings = 0
        for round_num in range(0, numRounds):
            pair_id_least_meetings = theoretical_optimum_matrix[[
                pair_num]].idxmin()
            prev_count = theoretical_optimum_matrix[pair_num][pair_id_least_meetings]
            theoretical_optimum_matrix[pair_num][pair_id_least_meetings] = prev_count+4
    print('\nTheoretical OPTIMUM Matrix')
    print(theoretical_optimum_matrix)
    return theoretical_optimum_matrix


# TODO: GONNA have to add waiting vector to arguments later
def get_theoretical_best_fitness(numPairs, numRounds, meeting_matrix):
    fitness = 0
    if(numPairs % 2 == 0):
        matrix = compute_theoretical_best_meeting_matrix(
            meeting_matrix, numPairs, numRounds)
        fitness = compute_fitness_even(matrix)
    else:
        # TODO: Still need to do
        pass
    return fitness


# theoretical_best_fitness = get_theoretical_best_fitness(
#     numOfPairs, numOfRounds, prev_meeting_matrix)
# # prev_waiting_vector

# print(f'Fitness of Theoretical Optimum is: {theoretical_best_fitness}')

##### GENERATE THE THEORETICAL WORST CASE ###########
# the fitness of the worst permutation should be obvious now:
# assign waiting tables to those pairs who had the most waiting tables so far,
# and let all pairs play against those pairs they had met before the most frequently.


def create_theoretical_worst_waiting_vector(waiting_table_vector):
    # TODO: Still need to finish, and pair with assigned table, gets one less meeting
    minimum = min(waiting_table_vector)
    return minimum


def compute_theoretical_worst_meeting_matrix(meeting_history_matrix, numPairs, numRounds):
    theoretical_worst_matrix = meeting_history_matrix.copy()
    for pair_num in range(1, numPairs+1):
        # Get the id of pair with which pair 'i' has had the least amount of meetings.
        pair_id_most_meetings = 0
        for round_num in range(1, numRounds+1):
            pair_id_most_meetings = theoretical_worst_matrix[[
                pair_num]].idxmax()
            prev_count = theoretical_worst_matrix[pair_num][pair_id_most_meetings]
            theoretical_worst_matrix[pair_num][pair_id_most_meetings] = prev_count+4
    print('\nTheoretical WORST Matrix')
    print(theoretical_worst_matrix)
    return theoretical_worst_matrix

# TODO: GONNA have to add waiting vector to arguments later


def get_theoretical_worst_fitness(numPairs, numRounds, meeting_matrix):
    fitness = 0
    if(numPairs % 2 == 0):
        matrix = compute_theoretical_worst_meeting_matrix(
            meeting_matrix, numPairs, numRounds)
        fitness = compute_fitness_even(matrix)
    else:
        # TODO: Still need to do
        pass
    return fitness


# theoretical_worst_fitness = get_theoretical_worst_fitness(
#     numOfPairs, numOfRounds, prev_meeting_matrix)
# # prev_waiting_vector

# print(f'Fitness of Theoretical Worst Case is: {theoretical_worst_fitness}')

#### RANGE OF FITNESS VALUES #######


def compute_range_fitness_values(fitness_best, fitness_worst):
    best = fitness_best / fitness_best
    worst = fitness_worst / fitness_best
    print(f'Range of Fitness Values is: {best} -- {worst}')
    return [best, worst]


def compute_fitness_overhead(fitness, best):
    return fitness/best


# compute_range_fitness_values(
#     theoretical_best_fitness, theoretical_worst_fitness)
# print(
#     f'Fitness of This Permutation is: {compute_fitness_overhead(fitness_value_new, theoretical_best_fitness)}')

#### OVERHEAD ACROSS MUULTIPLE SECTIONS #####
# As a side effect, we can compare the normalized overheads across all sections, and hence also add them up.
