from data import *
from playerModule import Player, gui, player_turn, players


def setup():
    global players
    num_players, player_names= gui.getPlayers()
    for i in range(num_players):
          players.append(Player(player_names[i], i))
          players[-1].guiPos = gui.moveToken(i, None, None)
          gui.updateDashboard(i, 'GO', players[-1].money, [], False)

def turn(player):
    global property_name
    if not player.loop:
        return
    gui.msg(f"It is {player.player_name}'s turn.")
    if player.position == 40:
        gui.msg("You are in jail.")
    roll = player.rollDice(0, 0)
    if player.spaceAction(player.position, players) == "Out of jail":
        turn(player)
    gui.updateDashboard(player.player_num, money = player.money, properties = player.owned_properties, sets = player.sets)
    player.purchaseBuildings()
    print(player.sets)

gui.updateWindow('menu')
while gui.LOCATION != 'board':
     gui.scr.update()

setup()
while len(players) > 1:
     gui.scr.update()
     turn(players[player_turn])
     player_turn = (player_turn + 1) % len(players)
