from data import *
from playerModule import Player
import gui
#This is a test to determine the push
players = []

def setup():
    global players
    num_players, player_names= gui.getPlayers()
    for i in range(num_players):
          players.append(Player(player_names[i]))

def turn(player):
    global property_name
    if not player.loop:
        return
    print(f"It is {player.player_name}'s turn.")
    if player.position == 40:
        print("You are in jail.")
    roll = player.rollDice(0, 0)
    print(roll)
    if roll != None:
        print(f"You rolled a {roll}.")
        player.move(roll)
        print(f"You landed on {property_name[player.position]}.")
        player.spaceAction(player.position, players)
    player.purchaseBuildings()

gui.updateWindow('menu')
while gui.LOCATION != 'board':
     gui.scr.update()

setup()
player_turn = 0
while len(players) > 1:
     gui.scr.update()
     turn(players[player_turn])
     player_turn = (player_turn + 1) % len(players)
