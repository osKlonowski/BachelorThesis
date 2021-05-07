from meeting_history import deconstructMeetingHistoryFile
from classes.list_of_players import ListOfPlayers
from pre_schedule import deconstructRegisteredPairs
from classes.list_of_pairs import ListOfPairs
from classes.pair import Pair
from classes.player import Player
from classes.section import Section
from classes.list_of_sections import ListOfSections
import numpy as np

# Preliminaries:
# For a pair of history and registration files, distribute the registered pairs over the given number of sections, based on their ranking values. For details, see below.
# For each section, compute a matrix of previous meetings among the pairs.
# Meetings are counted per player. So for pairs (A,B) and (C,D), we add up the number of meetings among A-C, A-D, B-C, and B-D to compute the total number of previous meetings among them.
# For each section, record the number of previous waiting tables of each pair, also adding up the waiting tables of both players. This will be a vector of values.

# 1. Distribute (registered) pairs over sections based on combined ranking value.
#       Result: #sections with a list of pairs (evenly distributed)
#   For Each Section:
#       Compute a Matrix of Previous Meetings (Among the Pairs):
#           Meetings are counted per player.
#               Ex. For Pairs (A, B) and (C, D), we add up the number of meetings among A-C, A-D, B-C, B-D
#               Result: Compute total number of previous meetings amongst pair members.
#   For Each Section:
#       Record number of previous waiting tables of each pair (sum of both players). -> (Vector of values for each pair)

# GOAL:
# Matrix of Meetings
# Vector of Waiting Tables

# 1. Compute ranking of a pair.
#       Will need a way to query player rankings from big register.
# 2. Construct a 'Section's with a list of pairs and their rating
# 3. ......

####################################
########## SECTIONS ################
####################################

######## SORT By COMBINED PAIR RATING #########

meeting_history_file = 'bridge_schedules/data2021_pre_balanced/meeting history april 2021'
pre_schedule_file = 'bridge_schedules/data2021_pre_balanced/48 pairs_(3 sections,no_waiting_table)'

listPlayers = deconstructMeetingHistoryFile(meeting_history_file)
listPairs = deconstructRegisteredPairs(pre_schedule_file)

for pair in listPairs.pairs:
    ratingSum = float(0.0)
    for player in pair.players:
        rating = listPlayers.getPlayerRating(player)
        ratingSum += float(rating)
    pair.setPairRating(ratingSum)

for pair in listPairs.pairs:
    total_waiting_tables = int(0)
    for player in pair.players:
        waiting = listPlayers.getPlayerWaitingTables(player)
        total_waiting_tables += waiting
    pair.setPairWaitingTables(total_waiting_tables)

# print(listPairs.sortPairsByRating())
listPairs.sortPairsByRating()

######## SPLIT INTO SECTIONS ##########

listSections = ListOfSections()

result = np.array_split(listPairs.pairs, 3)
for section in result:
    print(len(section))
    listSections.addSection(Section(section))
