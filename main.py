from data import *
from playerModule import Player, gui, player_turn, players


def setup():
    global players
    num_players, player_names= gui.getPlayers()
    for i in range(num_players):
        players.append(Player(player_names[i], i))
        players[-1].guiPos = gui.moveToken(i, None, None)
        gui.updateDashboard(i, pos=0, money=players[-1].money, properties=[], sets=False)

def turn(player):
    if not player.loop:
        return
    gui.msg(f"It is {player.player_name}'s turn.")
    if player.position == 40:
        gui.msg("You are in jail.")
    else:
        player.rollDice(0, 0)
    if player.spaceAction(player.position, players) == "Out of jail":
        turn(player)
    gui.updateDashboard(player.player_num, money = player.money, properties = player.owned_properties, sets = player.sets)
    player.purchaseBuildings()

gui.updateWindow('menu')
while gui.LOCATION != 'board':
     gui.scr.update()

setup()
# player1 = players[0]
# player1.owned_properties.append(1)
# property_state[1] = 0
# player1.owned_properties.append(3)
# property_state[3] = 0
# gui.openDashboard()
# gui.updateDashboard(player1.player_num, money = player1.money, properties = player1.owned_properties, sets = [(1, 3)])
# gui.scr.mainloop()
while len(players) > 1:
     gui.scr.update()
     turn(players[player_turn])
     player_turn = (player_turn + 1) % len(players)

