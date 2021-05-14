import numpy as np
import matplotlib.pyplot as plt
from classes.movement.movement_header import MovementHeader
from classes.movement.pair_movement import PairsMovement
from classes.movement.round import Round
from classes.movement.list_of_rounds import ListOfRounds

# bridge_schedules/schedules/6-rounds-(multiplex)/mpx\ NBB\ _93-8-4-6-6.asc
# path_to_schedule = 'bridge_schedules/schedules/6-rounds-(multiplex)/mpxNBB_93-8-4-6-6.asc'
path_to_schedule = 'bridge_schedules/schedules/mpx-16-8-6-6-0.asc'

# # Open file
# f = open(path_to_schedule, 'r')
# # number-of-contestants(pairs or players), number of tables, number of rounds, number of board groups, Individual
# headerline = f.readline()
# headerline = headerline.strip()
# headerline_columns = headerline.split()
# movement_header = MovementHeader(
#     int(headerline_columns[0]),  # 16
#     int(headerline_columns[1]),  # 8
#     int(headerline_columns[2]),  # 6
#     int(headerline_columns[3]),  # 6
#     int(headerline_columns[4]),  # 0
# )
# # Holds all readlines
# lines = f.readlines()
# lines = lines[:-1]
# print(f'Number of Lines: {len(lines)}')
# # Each line is a round
# for line in lines:
#     line = line.strip()
#     columns = line.split()
#     print(columns)
#     for i in range(0, len(columns), 2):
#         table = PairsMovement(columns[i], columns[i+1])
# f.close()


def readRoundFromLine(columns):
    round = Round()
    for i in range(0, len(columns), 2):
        table = PairsMovement(columns[i], columns[i+1])
        round.addTable(table)
    return round


def decryptScheduleFile(path_to_file):
    # Open file
    file = open(path_to_file, 'r')
    # Read and ignore header lines
    # number-of-contestants(pairs or players), number of tables, number of rounds, number of board groups, Individual
    headerline = file.readline()
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
    listOfRounds = ListOfRounds()
    # Ignoring the footer line
    lines = file.readlines()
    lines = lines[:-1]
    # Each line is a round
    for line in lines:
        line = line.strip()
        columns = line.split()
        round = readRoundFromLine(columns)
        listOfRounds.addRound(round)
    print(f'Number of Rounds: {len(listOfRounds.rounds)}')
    file.close()
    return listOfRounds
