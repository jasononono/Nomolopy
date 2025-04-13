from data import *
from playerModule import Player, gui, player_turn, players



def setup():
    num_players, player_names= gui.getPlayers()
    for i in range(num_players):
        players.append(Player(player_names[i], i))
        players[-1].guiPos = gui.moveToken(i, None, None)
        players_info[i][0] = 0
        players_info[i][1] = 1500
        players_info[i][2] = []
        players_info[i][3] = []
        players_info[i][4] = False

def turn(player):
    if not player.loop:
        return
    gui.msg(f"It is {player.player_name}'s turn.")
    if players_info[player.player_num][0] == 40:
        gui.msg("You are in jail.")
    else:
        player.rollDice(0, 0)
    if player.spaceAction(players_info[player.player_num][0], players) == "Out of jail":
        turn(player)
    gui.updateDashboard(player.player_num)
    # player.purchaseBuildings()


gui.updateWindow('menu')
while gui.LOCATION != 'board':
    gui.scr.update()

setup()
winner = None
while len(players) > 1:
    gui.scr.update()
    turn(players[player_turn])
    player_turn = (player_turn + 1) % len(players)
    if len(players) == 1:
        winner = players[player_turn].player_name
        break
gui.popup(f"{winner} won!")
