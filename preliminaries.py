from divide_sections import splitIntoSections
from meeting_history import deconstructMeetingHistoryFile
from classes.list_of_players import ListOfPlayers
from pre_schedule import deconstructRegisteredPairs
from classes.list_of_pairs import ListOfPairs
from classes.pair import Pair
from classes.player import Player
from classes.section import Section
from classes.list_of_sections import ListOfSections
import numpy as np
import pandas as pd

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

# meeting_history_file = 'bridge_schedules/data2021_pre_balanced/meeting history april 2021'
# pre_schedule_file = 'bridge_schedules/data2021_pre_balanced/48 pairs_(3 sections,no_waiting_table)'

# listPlayers = deconstructMeetingHistoryFile(meeting_history_file)
# listPairs = deconstructRegisteredPairs(pre_schedule_file)

# for pair in listPairs.pairs:
#     ratingSum = float(0.0)
#     for player in pair.players:
#         rating = listPlayers.getPlayerRating(player)
#         ratingSum += float(rating)
#     pair.setPairRating(ratingSum)

# for pair in listPairs.pairs:
#     total_waiting_tables = int(0)
#     for player in pair.players:
#         waiting = listPlayers.getPlayerWaitingTables(player)
#         total_waiting_tables += waiting
#     pair.setPairWaitingTables(total_waiting_tables)

# # print(listPairs.sortPairsByRating())
# listPairs.sortPairsByRating()
# listPairs.setPairIds()

# ######## SPLIT INTO SECTIONS ##########

# listSections = ListOfSections()

# result = np.array_split(listPairs.pairs, 3)
# for section in result:
#     # print(len(section))
#     listSections.addSection(Section(section))

# ######### CREATE MEETING MATRIX #########
# #########    FOR EACH SECTION   #########

# #### FUNCTION TO CALCULATE THE NUM OF MEETINGS BETWEEN PAIRS ########
# # for pairs (A,B) and (C,D), we add up the number of meetings among A-C, A-D, B-C, and B-D
# # to compute the total number of previous meetings among them


def getListOfPairNums(pairs):
    list = []
    for pair in pairs:
        list.append(pair.num)
    return list


def pairsMeetingCount(listPairs, listPlayers, pair1num, pair2num):
    # Get pairs by id
    pair1 = listPairs.getPairByNum(pair1num)
    pair2 = listPairs.getPairByNum(pair2num)
    if(pair1num == pair2num):
        return 0
    # pair1 -> (A, B)
    a = listPlayers.getPlayerById(int(pair1.player1))
    b = listPlayers.getPlayerById(int(pair1.player2))
    # pair2 -> (C, D)
    c = listPlayers.getPlayerById(int(pair2.player1))
    d = listPlayers.getPlayerById(int(pair2.player2))
    # SUM BELOW
    total = 0
    # ac = a.meeting_history[c.id]
    ac = a.getNumEncountersWith(c.id)
    ad = a.getNumEncountersWith(d.id)
    bc = b.getNumEncountersWith(c.id)
    bd = b.getNumEncountersWith(d.id)
    total = ac + ad + bc + bd
    return total


def printResults(listSections):
    #### DISPLAYS COMPLETED MEETINGS MATRIX BETWEEN PAIRS + SECTION WAITING VECTOR #####
    for section in listSections.sections:
        print(section.meetings_matrix)
        print(section.waiting_vector)


def createMeetingsMatrix(listSections, listPlayers, listPairs):
    for section in listSections.sections:
        ##### MEETINGS MATRIX ##########
        pairNums = getListOfPairNums(section.pairs)
        section.setListPairNumbers(pairNums)
        # GET List of Pair IDS for pd.DataFrame Construction
        series_rows = pd.Series(section.listPairNums)
        series_cols = pd.Series(section.listPairNums)
        # CREATE DATA-FRAME BASED ON COMBINED MEETINGS
        df = pd.DataFrame(series_rows.apply(
            lambda x: series_cols.apply(lambda y: pairsMeetingCount(listPairs, listPlayers, x, y))))
        df.index = series_rows
        df.columns = series_cols
        ### SET SECTION MATRIX ###
        section.assignMeetingsMatrix(df)
    return listSections


def createWaitingTablesVector(listSections):
    for section in listSections.sections:
        ##### WAITING TABLES VECTOR #######
        vector = np.array([pair.total_waiting for pair in section.pairs])
        section.assignWaitingVector(vector)
        print(f'Vector of Waiting Tables\n {vector}')
    return listSections


# def splitIntoSections(listPairs, numOfSections):
#     listSections = ListOfSections()
#     # TODO: The number of sections here should be determined some other way???
#     result = np.array_split(listPairs.pairs, numOfSections)
#     for section in result:
#         print(f'Num Of Pairs in Section: {len(section)}')
#         listSections.addSection(Section(section))
#     return listSections


def calcualteTotalRaitingsAndWaitingTables(listPairs, listPlayers):
    for pair in listPairs.pairs:
        ratingSum = float(0.0)
        player1 = listPlayers.getPlayerById(int(pair.players[0]))
        player2 = listPlayers.getPlayerById(int(pair.players[1]))
        for player in [player1, player2]:
            rating = listPlayers.getPlayerRating(player.id)
            ratingSum += float(rating)
        pair.setPairRating(ratingSum)
        total_waiting_tables = int(0)
        for player in [player1, player2]:
            waiting = listPlayers.getPlayerWaitingTables(int(player.id))
            total_waiting_tables += waiting
        pair.setPairWaitingTables(total_waiting_tables)
    return listPairs


def getListOfSectionsCompleted(meeting_history_file, pre_schedule_file, hasWaitingTable):
    listPlayers = deconstructMeetingHistoryFile(meeting_history_file)
    listPairs = deconstructRegisteredPairs(pre_schedule_file)
    print(f'Total Num of Pairs: {len(listPairs.pairs)}')
    listPairs.setPairNumbers()
    listPairs = calcualteTotalRaitingsAndWaitingTables(listPairs, listPlayers)
    listPairs.sortPairsByRating()
    listSections = splitIntoSections(listPairs.pairs, 3)
    if hasWaitingTable:
        listSections = createWaitingTablesVector(listSections)
    listSections = createMeetingsMatrix(listSections, listPlayers, listPairs)
    return listSections


# meeting_history_file = 'bridge_schedules/data2021_pre_balanced/meeting history april 2021'
# pre_schedule_file = 'bridge_schedules/data2021_pre_balanced/51pairs_(3_sections,_waiting table)'
# # pre_schedule_file = 'bridge_schedules/data2021_pre_balanced/48 pairs_(3 sections,no_waiting_table)'
# getListOfSectionsCompleted(
#     meeting_history_file, pre_schedule_file, True)
