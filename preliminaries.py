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


def getListOfPairIDs(pairs):
    list = []
    for pair in pairs:
        list.append(pair.id)
    return list


def pairsMeetingCount(listPairs, listPlayers, pair1id, pair2id):
    # Get pairs by id
    pair1 = listPairs.getPairById(pair1id)
    pair2 = listPairs.getPairById(pair2id)
    if(pair1 == pair2):
        return 0
    # pair1 -> (A, B)
    a = listPlayers.getPlayerById(pair1.player1)
    b = listPlayers.getPlayerById(pair1.player2)
    # pair2 -> (C, D)
    c = listPlayers.getPlayerById(pair2.player1)
    d = listPlayers.getPlayerById(pair2.player2)
    # SUM BELOW
    total = 0
    ac = a.meeting_history[int(c.id)]
    ad = a.meeting_history[int(d.id)]
    bc = b.meeting_history[int(c.id)]
    bd = b.meeting_history[int(d.id)]
    total = ac + ad + bc + bd
    return total


#### FOR EACH SECTION ####
# for section in listSections.sections:
#     ##### MEETINGS MATRIX ##########
#     pairIds = getListOfPairIDs(section.pairs)
#     section.setListPairIds(pairIds)
#     # GET List of Pair IDS for pd.DataFrame Construction
#     series_rows = pd.Series(section.listPairIds)
#     series_cols = pd.Series(section.listPairIds)
#     # CREATE DATA-FRAME BASED ON COMBINED MEETINGS
#     df = pd.DataFrame(series_rows.apply(
#         lambda x: series_cols.apply(lambda y: pairsMeetingCount(x, y))))
#     df.index = series_rows
#     df.columns = series_cols
#     ### SET SECTION MATRIX ###
#     section.assignMeetingsMatrix(df)
#     ##### WAITING TABLES VECTOR #######
#     vector = np.array([pair.total_waiting for pair in section.pairs])
#     section.assignWaitingVector(vector)


def printResults(listSections):
    #### DISPLAYS COMPLETED MEETINGS MATRIX BETWEEN PAIRS + SECTION WAITING VECTOR #####
    for section in listSections.sections:
        print(section.meetings_matrix)
        print(section.waiting_vector)


def createMeetingsMatrix(listSections, listPlayers, listPairs):
    for section in listSections.sections:
        ##### MEETINGS MATRIX ##########
        pairIds = getListOfPairIDs(section.pairs)
        section.setListPairIds(pairIds)
        # GET List of Pair IDS for pd.DataFrame Construction
        series_rows = pd.Series(section.listPairIds)
        series_cols = pd.Series(section.listPairIds)
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
    return listSections


def splitIntoSections(listPairs, numOfSections):
    listSections = ListOfSections()
    # TODO: The number of sections here should be determined some other way???
    result = np.array_split(listPairs.pairs, numOfSections)
    for section in result:
        print(f'Num Of Pairs in Section: {len(section)}')
        listSections.addSection(Section(section))
    return listSections


def calcualteTotalRaitingsAndWaitingTables(listPairs, listPlayers):
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
    return listPairs


def getListOfSectionsCompleted(meeting_history_file, pre_schedule_file):
    listPlayers = deconstructMeetingHistoryFile(meeting_history_file)
    listPairs = deconstructRegisteredPairs(pre_schedule_file)
    print(f'Total Num of Pairs: {len(listPairs.pairs)}')
    listPairs = calcualteTotalRaitingsAndWaitingTables(listPairs, listPlayers)
    listPairs.sortPairsByRating()
    listPairs.setPairIds()
    listSections = splitIntoSections(listPairs, 3)
    listSections = createMeetingsMatrix(listSections, listPlayers, listPairs)
    listSections = createWaitingTablesVector(listSections)
    # printResults(listSections)
    return listSections
