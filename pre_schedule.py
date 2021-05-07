import numpy as np
import matplotlib.pyplot as plt
from classes.pair import Pair
from classes.list_of_pairs import ListOfPairs

# bridge_schedules/data2021_pre_balanced/meeting\ history\ april\ 2021
pre_schedule_file = 'bridge_schedules/data2021_pre_balanced/48 pairs_(3 sections,no_waiting_table)'

# Might have to substitute this with a class as well
pairs = ListOfPairs()


def deconstructRegisteredPairs(pre_schedule_file):
    # Open file
    f = open(pre_schedule_file, 'r')
    headerline = f.readline()
    lines = f.readlines()
    for line in lines:
        lineSplit = line.strip().split(sep=',')
        playerId = lineSplit[0]
        oponentId = lineSplit[1]
        pairs.addPair(Pair(playerId, oponentId))
    return pairs
