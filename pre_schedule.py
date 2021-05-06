import numpy as np
import matplotlib.pyplot as plt
from classes.pair import Pair

# bridge_schedules/data2021_pre_balanced/meeting\ history\ april\ 2021
pre_schedule_file = 'bridge_schedules/data2021_pre_balanced/48 pairs_(3 sections,no_waiting_table)'

# Might have to substitute this with a class as well
pairs = []

# Open file
f = open(pre_schedule_file, 'r')

headerline = f.readline()

lines = f.readlines()
for line in lines:
    # print(line)
    lineSplit = line.strip().split(sep=',')
    # print(len(lineSplit))
    # print(lineSplit)
    playerId = lineSplit[0]
    oponentId = lineSplit[1]
    pairs.append(Pair(playerId, oponentId))

print(len(pairs))
