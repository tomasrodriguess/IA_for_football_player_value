import utils
from webscraping import loadLeague
import pandas
from webscraping import loadPlayers
from Objects.Team import Team
from Objects.League import League
from Objects.Player import Player
from utils import *
import csv


links = ["https://www.transfermarkt.pt/liga-nos/startseite/wettbewerb/PO1",
         "https://www.transfermarkt.pt/primera-division/startseite/wettbewerb/ES1",
         "https://www.transfermarkt.pt/premier-league/startseite/wettbewerb/GB1",
         "https://www.transfermarkt.pt/1-bundesliga/startseite/wettbewerb/L1",
         "https://www.transfermarkt.pt/serie-a/startseite/wettbewerb/IT1",
         "https://www.transfermarkt.pt/ligue-1/startseite/wettbewerb/FR1"
         ]
"""
links = [
"https://www.transfermarkt.pt/fc-porto/startseite/verein/720"
]
"""

header = ["ID", "Name", "Age", "Height", "Nationality", "Position", "Agent", "N_internacional_games",
          "N_internacional_goals", "years_left_in_contrat", "Preferred_foot", "Team", "League", "Value"]
dataset = open("players.csv")
reader = csv.reader(dataset)
if next(reader) != header:
    with open('players.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        id = 1


def remove_repetions_of_league(league):
    df = pandas.read_csv('players.csv')
    df = df[df.league != league]
    df.to_csv('players.csv', index=False)

id=1
with open('players.csv', 'a+', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for link in links:
        data,league = loadLeague(link)
        #remove_repetions_of_league(league)
        for player in data:
            player.insert(0,id)
            writer.writerow(player)
            id += 1
            print(player)
f.close()

