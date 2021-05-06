import numpy as np
import matplotlib.pyplot as plt

# bridge_schedules/schedules/6-rounds-(multiplex)/mpx\ NBB\ _93-8-4-6-6.asc
path_to_schedule = 'bridge_schedules/schedules/6-rounds-(multiplex)/mpxNBB_93-8-4-6-6.asc'


class MovementHeader:
    # pairs or players, number of tables, number of rounds, number of board groups, Individual
    def __init__(self, n_of_pairs, n_of_tables, n_of_rounds, n_of_board_groups, individual):
        self.n_of_pairs = n_of_pairs
        self.n_of_tables = n_of_tables
        self.n_of_rounds = n_of_rounds
        self.n_of_board_groups = n_of_board_groups
        self.individual = individual


class PairsMovement:
    # { NS-pair, EW-pair, board group }
    def __init__(self, pair, board_group):
        self.pair = pair
        self.ns_pair = pair.split('-')[0]
        self.ew_pair = pair.split('-')[1]
        self.board_group = board_group


# Open file
f = open(path_to_schedule, 'r')
# Read and ignore header lines
# number-of-contestants(pairs or players), number of tables, number of rounds, number of board groups, Individual
headerline = f.readline()
headerline = headerline.strip()
headerline_columns = headerline.split()
movement_header = MovementHeader(
    int(headerline_columns[0]),  # 8
    int(headerline_columns[1]),  # 4
    int(headerline_columns[2]),  # 6
    int(headerline_columns[3]),  # 6
    int(headerline_columns[4]),  # 0
)

# Holds all readlines
listOfRounds = []

# For now ignoring the footer line
lines = f.readlines()
lines = lines[:-1]
# Loop over lines and extract variables of interest
# Each line is a round
for line in lines:
    line = line.strip()
    columns = line.split()
    print(columns)
    for i in range(0, len(columns), 2):
        table = PairsMovement(columns[i], columns[i+1])
        listOfRounds.append(table)

f.close()

# for pair in listOfRounds:
#     print('Pair', pair.board_group)
#     print('NS: ', pair.ns_pair)
#     print('EW: ', pair.ew_pair)
#     print('\n')
