import numpy as np
import matplotlib.pyplot as plt
from classes.player import Player
from classes.list_of_players import ListOfPlayers

# bridge_schedules/data2021_pre_balanced/meeting\ history\ april\ 2021
meeting_history_file = 'bridge_schedules/data2021_pre_balanced/meeting history april 2021'

listPlayers = ListOfPlayers()


def split_user_record(user_record):
    user_record = user_record.strip()
    split_parts = user_record.split(sep='[')
    user_info = split_parts[0]
    user = user_info.split(sep=',')
    id_num = user[0]
    rating = user[1]
    encounters = split_parts[1]
    meeting_history = [int(i) for i in encounters.split(',')]
    num_waiting_tables = meeting_history.pop(0)
    player = Player(id_num, rating, meeting_history, num_waiting_tables)
    listPlayers.addPlayer(player)


def each_chunk(stream, separator):
    buffer = ''
    while True:  # until EOF
        chunk = stream.read(4096)  # CHUNK_SIZE -> I propose 4096 or so
        if not chunk:  # EOF?
            yield buffer
            break
        buffer += chunk
        while True:  # until no separator is found
            try:
                part, buffer = buffer.split(separator, 1)
            except ValueError:
                break
            else:
                yield part


with open(meeting_history_file) as myFile:
    for chunk in each_chunk(myFile, separator=']'):
        if(chunk != ''):
            split_user_record(chunk)

# print(listPlayers.getNumOfPlayers())
# listPlayers.sortPlayers()


def deconstructMeetingHistoryFile(file):
    with open(meeting_history_file) as myFile:
        for chunk in each_chunk(myFile, separator=']'):
            if(chunk != ''):
                split_user_record(chunk)
    return listPlayers
