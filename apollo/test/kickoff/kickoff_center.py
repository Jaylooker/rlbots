from rlbot.utils.game_state_util import GameState
import csv

#Extract kickoff.csv file
with open('center_kickoff.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ')
    for row in spamreader:
        #add reading of data into Gamestate