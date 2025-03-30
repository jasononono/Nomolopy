import random
from data import *
import gui
from tkinter import *

players = []
player_turn = 0
community_chest_spaces = (2, 17, 33)
chance_spaces = (7, 22, 36)
railroads = (5, 15, 25, 35)
utilities = (12, 28)
null_space = (0, 10, 20)

def craneBias(pos):
    gui.omniousMsg('The dice bounce awkwardly on the board...', False)
    for i in range(3, 13):
        if (pos + i) % 40 in [2, 4, 7, 10, 12, 17, 20, 22, 28, 30, 33, 36, 38]:
            d1 = random.randint(1, i - 1)
            d2 = i - d1
            while d1 == d2:
                d1 = random.randint(1, i - 1)
                d2 = i - d1
            return d1, d2
    return random.choice([[1, 2], [2, 1]])

class Player:

    def __init__(self, name, num):
        self.player_name = name
        self.player_num = num
        self.guiPos = None
        self.loop = True
        self.isCrane = 'crane' in self.player_name.lower()

    def rollDice(self, past_roll, double_count):
        gui.dice_screen.deiconify()
        gui.dice_screen.attributes("-topmost", True)
        gui.center(gui.dice_screen, 0, -50)
        if self.isCrane and random.randint(1, 4) <= 3:
            dice1, dice2 = craneBias(players_info[self.player_num][0])
        else:
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
        gui.displayRoll(dice1, dice2)
        if dice1 != dice2 or double_count > 2:
            gui.dice_screen.withdraw()
        print(f"Rolled {dice1} and {dice2}")
        roll = past_roll + dice1 + dice2
        print("The roll is now " + str(roll))
        if dice1 == dice2:
            if players_info[self.player_num][0] == 40:
                players_info[self.player_num][0] = 10
            else:
                double_count += 1
                if double_count >= 3:
                    gui.msg("You rolled 3 doubles in a row. Go to jail.")
                    self.goToJail()
                    return None
                else:
                    return self.rollDice(roll, double_count)
        elif players_info[self.player_num][0] == 40:
            print("Stay in jail")
            return None
        print("Rolled")
        gui.msg(f"{self.player_name} rolled a {roll}.")
        self.move(roll)
        print(players_info[self.player_num][0])
        gui.msg(f"{self.player_name} landed on {property_name[players_info[self.player_num][0]]}.")
        return roll

    def circularTokenMove(self, start, end):
        turn_corner = ((players_info[self.player_num][0] % 10 + end - players_info[self.player_num][0]) > 10 or end < players_info[self.player_num][0]) and end != 40 and players_info[self.player_num][0] != 40
        if turn_corner:
            self.guiPos = gui.moveToken(self.player_num, self.guiPos, (players_info[self.player_num][0] // 10 * 10 + 10) % 40)
            players_info[self.player_num][0] = (players_info[self.player_num][0] // 10 * 10 + 10) % 40
            self.circularTokenMove(players_info[self.player_num][0], end)
        else:
            self.guiPos = gui.moveToken(self.player_num, self.guiPos, end)
            players_info[self.player_num][0] = end
            gui.updateDashboard(self.player_num)
            if players_info[self.player_num][0] == 0:
                players_info[self.player_num][1] += 200
                gui.msg(f"{self.player_name} passed Go and collected $200.")


    def move(self, num):
        self.circularTokenMove(players_info[self.player_num][0], (players_info[self.player_num][0] + num) % 40)

    def goToJail(self):
        self.circularTokenMove(players_info[self.player_num][0], 40)
        gui.updateDashboard(self.player_num)

    def mortgageOrSell(self, amount):
        #UI import
        m_win = gui.mortgagePopup()
        while players_info[self.player_num][2] and players_info[self.player_num][1] < amount:
            gui.updateDashboard(num=self.player_num, can_sell=True)
            previous_money = players_info[self.player_num][1]
            while players_info[self.player_num][1] == previous_money:
                gui.scr.update()
        gui.updateDashboard(num=self.player_num)
        m_win.destroy()
        if players_info[self.player_num][1] >= amount:
            return -1
        else:
            return 1



    def spaceAction(self, space, players):
        if space == 30:
            self.goToJail()
        elif space in community_chest_spaces:
            self.drawCommunityChest()
        elif space in chance_spaces:
            self.drawChance()
        # Taxes
        elif space == 4:
            gui.msg(f"{self.player_name} paid $200.")
            players_info[self.player_num][1] -= 200
        elif space == 38:
            gui.msg(f"{self.player_name} paid $100.")
            players_info[self.player_num][1] -= 100
        elif space in null_space or space in players_info[self.player_num][2]:
            pass
        elif space == 40:
            if players_info[self.player_num][4]:
                query = gui.popup("You have a get out of jail free card. Do you want to use it?", ["YES", "NO"])
            else:
                query = gui.popup("Do you want to pay $50 to get out of jail?", ["YES", "NO"])
            if query == "YES":
                if players_info[self.player_num][4]:
                    players_info[self.player_num][4] = False
                elif players_info[self.player_num][1] >= 50:
                    players_info[self.player_num][1] -= 50
                else:
                    if self.mortgageOrSell(50) == -1:
                        gui.msg(f"{self.player_name} stayed in jail.")
                        return
                self.circularTokenMove(players_info[self.player_num][0], 10)
                gui.updateDashboard(self.player_num)
                return "Out of jail"
            else:
                gui.msg(f"{self.player_name} stayed in jail.")
        elif property_owner[space] != -1:
            if space in railroads:
                railroad_count = 0
                for i in range(4):
                    if (5 + 10 * i) in players[property_owner[space]].owned_properties:
                        railroad_count += 1
                rent = property_rent[space][railroad_count - 1]
            elif space in utilities:
                utility_count = 0
                for space in utilities:
                    if space in players[property_owner[space]].owned_properties:
                        utility_count += 1
                d1, d2 = random.randint(1, 6), random.randint(1, 6)
                gui.dice_screen.deiconify()
                gui.displayRoll(d1, d2)
                if utility_count == 1:
                    rent = 4 * d1 + d2
                else:
                    rent = 10 * d1 + d2
            else:
                rent = property_rent[space][property_state[space]+1]
                players_info[players[property_owner[space]].player_num][1] += rent
                gui.updateDashboard(players[property_owner[space]].player_num)
            if players_info[self.player_num][1] >= rent:
                players_info[self.player_num][1] -= rent
                gui.msg(f"{self.player_name} paid ${str(rent)} to {players[property_owner[space]].player_name}.")
            else:
                if self.mortgageOrSell(rent - players_info[self.player_num][1]) == -1:
                    self.bankrupt()
                else:
                    players_info[self.player_num][1] -= rent
                    gui.msg(f"{self.player_name} paid {str(rent)} to {property_name[property_owner[space]]}.")
        else:
            price = property_purchase_price[space]
            query = gui.popup(f"Would {self.player_name} like to buy {property_name[space]} for ${price}?\n{self.player_name} currently has ${players_info[self.player_num][1]}", ['YES', 'NO'])
            if query == 'YES':
                if players_info[self.player_num][1] >= price:
                    players_info[self.player_num][1] -= price
                else:
                    if self.mortgageOrSell(price) == 1:
                        players_info[self.player_num][1] -= price
                    else:
                        gui.msg("You don't have enough money to buy this property.")
                        return
                gui.msg(f"{self.player_name} has bought {property_name[space]} for ${price}. \n{self.player_name} now has ${players_info[self.player_num][1]}.")
                property_owner[space] = self.player_num
                print(f"Property has been transferred to player {players.index(self)}")
                property_state[space] = 0
                players_info[self.player_num][2].append(space)
                for p in color_sets[color_set_index[space]]:
                    if p not in players_info[self.player_num][2]:
                        return
                players_info[self.player_num][3].append(color_sets[color_set_index[space]])


    def drawChance(self):
        global players
        if self.isCrane and random.randint(1, 4) <= 3:
            gui.omniousMsg('It seems that fortune is \nno longer with this player...', True)
            draw_card = [9, 10, 14, 15, 16][random.randint(0, 4)]
        else:
            draw_card = random.randint(1, 16)

        if draw_card <= 10:
            if draw_card == 1:
                #reading railroad
                gui.msg(f"{self.player_name} advanced to Writing Railroad.")
                self.circularTokenMove(players_info[self.player_num][0], 5)
            elif draw_card == 2:
                #st. charles
                gui.msg(f"{self.player_name} advanced to St. Nicholas Place.")
                self.circularTokenMove(players_info[self.player_num][0], 11)
            elif draw_card == 3:
                #illinois
                gui.msg(f"{self.player_name} advanced to Healthinois Avenue.")
                self.circularTokenMove(players_info[self.player_num][0], 24)
            elif draw_card == 4:
                #boardwalk
                gui.msg(f"{self.player_name} advanced to Plankrun.")
                self.circularTokenMove(players_info[self.player_num][0], 39)
            elif draw_card == 5 or draw_card == 6:
                #nearest railroad
                gui.msg(f"{self.player_name} advanced to the nearest railroad.")
                new_pos = players_info[self.player_num][0]
                if (new_pos - (new_pos % 10) + 5) < (new_pos):
                    new_pos += 5
                new_pos -= new_pos % 10
                new_pos += 5
                new_pos %= 40
                self.circularTokenMove(players_info[self.player_num][0], new_pos)
                if property_owner[players_info[self.player_num][0]] != -1 and property_owner[players_info[self.player_num][0]] != self.player_num:
                    gui.msg(f"{self.player_name} paid double!")
                    self.spaceAction(players_info[self.player_num][0], players=players)
            elif draw_card == 7:
                #nearest utility
                gui.msg(f"{self.player_name} advanced to the nearest utility.")
                if players_info[self.player_num][0] < 12:
                    self.circularTokenMove(players_info[self.player_num][0], 12)
                elif players_info[self.player_num][0] < 28:
                    self.circularTokenMove(players_info[self.player_num][0], 28)
                else:
                    self.circularTokenMove(players_info[self.player_num][0], 12)
                if property_owner[players_info[self.player_num][0]] != -1 and property_owner[players_info[self.player_num][0]] != self.player_num:
                    gui.msg(f"{self.player_name} paid double!")
                    self.spaceAction(players_info[self.player_num][0], players=players)
            elif draw_card == 8:
                #GO
                gui.msg(f"{self.player_name} advanced to Go.")
                self.circularTokenMove(players_info[self.player_num][0], 0)
                gui.msg(f"{self.player_name} passed Go and collected $200.")
                players_info[self.player_num][1] += 200
            elif draw_card == 9:
                #jail
                gui.msg(f"{self.player_name} went to jail.")
                self.goToJail()
            elif draw_card == 10:
                #go back 3 spaces
                gui.msg(f"{self.player_name} went back three spaces.")
                players_info[self.player_num][0] = players_info[self.player_num][0] - 3 % 40
                self.guiPos = gui.moveToken(self.player_num, self.guiPos, players_info[self.player_num][0])
            gui.msg(f"{self.player_name} landed on {property_name[players_info[self.player_num][0]]}.")
            self.spaceAction(players_info[self.player_num][0], players=players)
        elif draw_card == 11:
            #get out of jail free card
            gui.msg(f"{self.player_name} got a get out of jail free card.")
            players_info[self.player_num][4] = True
        elif draw_card == 12:
            #building loan
            gui.msg(f"{self.player_name}'s building loan matured. \n{self.player_name} collected $150.")
            players_info[self.player_num][1] += 150
        elif draw_card == 13:
            #dividends
            gui.msg(f"The bank paid {self.player_name} a dividend of $50.")
            players_info[self.player_num][1] += 50
        elif draw_card == 14:
            gui.msg(f"Speeding fine! {self.player_name} was charged $15.")
            if players_info[self.player_num][1] >= 15:
                players_info[self.player_num][1] -= 15
            else:
                if self.mortgageOrSell(15) == 1:
                    players_info[self.player_num][1] -= 15
                else:
                    self.bankrupt()
                    return
        elif draw_card == 15:
            #chairman
            gui.msg(f"{self.player_name} has been elected chairman of the board. \n{self.player_name} has to pay each player $50.")
            cost = 50*len(players)
            if players_info[self.player_num][1] >= cost:
                players_info[self.player_num][1] -= cost
            else:
                if self.mortgageOrSell(cost) == 1:
                    players_info[self.player_num][1] -= cost
                else:
                    self.bankrupt()
                    return
            for i in range(len(players)):
                if i != self.player_num:
                    players[i].money += 50
        else:
            cost, houses, hotels = self.buildingRepairs(25, 100)
            gui.msg(f"General repairs! {self.player_name} has to pay ${cost} for {houses} houses and {hotels} hotels.")
            if players_info[self.player_num][1] >= cost:
                players_info[self.player_num][1] -= cost
            else:
                if self.mortgageOrSell(cost) == 1:
                    players_info[self.player_num][1] -= cost
                else:
                    self.bankrupt()
                    return
        gui.updateDashboard(num=self.player_num)

    def drawCommunityChest(self):
        global players
        
        if self.isCrane and random.randint(1, 4) <= 3:
            gui.omniousMsg('An omnious red fog engulfed the player...', True)
            draw_card = [2, 11, 12, 13, 16][random.randint(0, 4)]
        else:
            draw_card = random.randint(1, 16)

        if draw_card <= 2:
            if draw_card == 1:
                #GO
                gui.msg(f"{self.player_name} advanced to Go.")
                self.circularTokenMove(players_info[self.player_num][0], 0)
                gui.msg(f"{self.player_name} passed Go and collected $200.")
                players_info[self.player_num][1] += 200
            elif draw_card == 2:
                #jail
                gui.msg(f"{self.player_name} went to jail.")
                self.goToJail()
        elif draw_card == 3:
            gui.msg(f"{self.player_name} won second prize in a beauty contest. \nCollect $10.")
            players_info[self.player_num][1] += 10
        elif draw_card == 4:
            gui.msg(f"{self.player_name} received and income tax refund of $20.")
            players_info[self.player_num][1] += 20
        elif draw_card == 5:
            gui.msg(f"{self.player_name} received a $25 consultancy fee.")
            players_info[self.player_num][1] += 25
        elif draw_card == 6:
            gui.msg(f"{self.player_name} received $50 from stocks.")
            players_info[self.player_num][1] += 50
        elif draw_card == 7:
            gui.msg(f"{self.player_name} inherited $100.")
            players_info[self.player_num][1] += 100
        elif draw_card == 8:
            gui.msg(f"{self.player_name}'s holiday fund matured. \nCollect $100.")
            players_info[self.player_num][1] += 100
        elif draw_card == 9:
            gui.msg(f"{self.player_name}'s life insurance matured. \nCollect $100.")
            players_info[self.player_num][1] += 100
        elif draw_card == 10:
            gui.msg(f"{self.player_name} experienced a favourable bank error. \nCollect $200.")
            players_info[self.player_num][1] += 200
        elif draw_card <= 13:
            if draw_card == 11:
                gui.msg(f"{self.player_name} needs to pay school fees. Pay $50.")
                cost = 50
            elif draw_card == 12:
                gui.msg(f"{self.player_name} needs to pay doctor's fees. Pay $50.")
                cost = 50
            elif draw_card == 13:
                gui.msg(f"{self.player_name} needs to pay hospital fees. Pay $100.")
                cost = 100
            if players_info[self.player_num][1] >= cost:
                players_info[self.player_num][1] -= cost
            else:
                if self.mortgageOrSell(cost) == 1:
                    players_info[self.player_num][1] -= cost
                else:
                    self.bankrupt()
                    return
        elif draw_card == 14:
            gui.msg(f"It's {self.player_name}'s birthday! Every player pays them $10.")
            for player in players:
                if player != self:
                    if player.money >= 10:
                        player.money -= 10
                    else:
                        if player.mortgageOrSell(10) == 1:
                            player.money -= 10
                        else:
                            player.bankrupt()
                            return
            players_info[self.player_num][1] += (len(players)-1)*10
        elif draw_card == 15:
            gui.msg(f"{self.player_name} got a get out of jail free card.")
            if players_info[self.player_num][4]:
                gui.msg(f"{self.player_name} can't have any more cards.")
            else:
                players_info[self.player_num][4] = True
        else:
            cost, houses, hotels = self.buildingRepairs(40, 115)
            gui.msg(f"Street repairs! {self.player_name} has to pay ${cost} for {houses} houses and {hotels} hotels.")
            if players_info[self.player_num][1] >= cost:
                players_info[self.player_num][1] -= cost
            else:
                if self.mortgageOrSell(cost) == 1:
                    players_info[self.player_num][1] -= cost
                else:
                    self.bankrupt()
                    return
        gui.updateDashboard(num=self.player_num)

    def buildingRepairs(self, house_p, hotel_p):
        total_cost = 0
        house_count = 0
        hotel_count = 0
        for property in players_info[self.player_num][2]:
            if property_state[property] == 5:
                total_cost += hotel_p
                hotel_count += 1
            elif property_state[property] > 0:
                total_cost += property_state[property]*house_p
                house_count += property_state[property]
        return total_cost, house_count, hotel_count

    def bankrupt(self):
        global players
        gui.msg(f"{self.player_name} has been bankrupted!")
        players[players.index(self)] = None
        for property in players_info[self.player_num][2]:
            property_state[property] = -2
            property_state[property] = -1
        self.loop = False
