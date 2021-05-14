from movement import decryptScheduleFile
from classes.movement.list_of_rounds import ListOfRounds
from preliminaries import getListOfSectionsCompleted

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


listOfSections = getListOfSectionsCompleted(
    meeting_history_file, pre_schedule_file)

##### START WITH ONE SECTION OF 16 PLAYERS #######
section = listOfSections.sections[0]

# print(section.meetings_matrix)
# print(section.waiting_vector)

#### COPYING PREVIOUS MEETING MATRIX #####
prev_meeting_matrix = section.meetings_matrix.copy()

# print(prev_meeting_matrix)

# Example -- Basic Schedule File Header
# number of pairs    number of tables    number of rounds    number of board groups    Individual=0
path_to_schedule = 'bridge_schedules/schedules/mpx-16-8-6-6-0.asc'

listRounds = decryptScheduleFile(path_to_schedule)

listOfPairMeetings = listRounds.getListOfPairMeetings()

new_meetings_matrix = prev_meeting_matrix.copy()
for round in listOfPairMeetings:
    for pairMeeting in round:
        i = int(pairMeeting[0])
        j = int(pairMeeting[1])
        # print(f'Pair I: {i}, Pair J: {j}')
        prev_meeting_count = prev_meeting_matrix.at[i, j]
        # print(f'Previous Meeting Count: {prev_meeting_count}')
        new_meetings_matrix.at[i, j] = int(prev_meeting_count+4)
        # print(f'New Meeting Count: {new_meetings_matrix[j][i]}')

print(prev_meeting_matrix)
print(new_meetings_matrix)
