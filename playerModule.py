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
        self.position = 0
        self.guiPos = None
        self.money = 1500
        self.owned_properties = []
        self.has_set = False
        self.sets = []
        self.jail_free_card = False
        self.loop = True
        self.isCrane = 'crane' in self.player_name.lower()

    def rollDice(self, past_roll, double_count):
        gui.dice_screen.deiconify()
        gui.dice_screen.attributes("-topmost", True)
        gui.center(gui.dice_screen, 0, -50)
        if self.isCrane and random.randint(1, 4) <= 3:
            dice1, dice2 = craneBias(self.position)
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
            if self.position == 40:
                self.position = 10
            else:
                double_count += 1
                if double_count >= 3:
                    gui.msg("You rolled 3 doubles in a row. Go to jail.")
                    self.goToJail()
                    return None
                else:
                    return self.rollDice(roll, double_count)
        elif self.position == 40:
            print("Stay in jail")
            return None
        print("Rolled")
        gui.msg(f"{self.player_name} rolled a {roll}.")
        self.move(roll)
        gui.msg(f"{self.player_name} landed on {property_name[self.position]}.")
        return roll

    def circularTokenMove(self, start, end):
        turn_corner = ((self.position % 10 + end - self.position) > 10 or end < self.position) and end != 40 and self.position != 40
        if turn_corner:
            self.guiPos = gui.moveToken(self.player_num, self.guiPos, (self.position // 10 * 10 + 10) % 40)
            self.position = (self.position // 10 * 10 + 10) % 40
            self.circularTokenMove(self.position, end)
        else:
            self.guiPos = gui.moveToken(self.player_num, self.guiPos, end)
            self.position = end
            gui.updateDashboard(self.player_num, pos=property_name[self.position])
            if self.position == 0:
                self.money += 200
                gui.msg(f"{self.player_name} passed Go and collected $200.")


    def move(self, num):
        self.circularTokenMove(self.position, (self.position + num) % 40)

    def goToJail(self):
        self.circularTokenMove(self.position, 40)
        gui.updateDashboard(self.player_num, pos = property_name[self.position])

    def mortgagePopup(self):
        m_scr = Tk()
        m_scr.config(bg=gui.BLUE1)
        m_scr.geometry("350x100")
        m_scr.title("You can't pay!")
        gui.center(m_scr)
        Label(m_scr, text="You don't have enough to pay!\nSell some properties to continue.", font="optima 20", fg=gui.BLUE2, bg=gui.BLUE1).place(anchor="center", x=175, y=50)
        m_scr.update()
        return m_scr

    def mortgageOrSell(self, amount):
        global property_state, property_name
        #UI import
        m_win = self.mortgagePopup()
        while self.owned_properties and self.money < amount:
            gui.updateDashboard(num=self.player_num, money=self.money, properties=self.owned_properties, can_sell=True)
            while not gui.sell_queue:
                gui.scr.update()
            sell_p = gui.sell_queue.pop(0)
            print(sell_p)
            if property_state[sell_p] == 0:
                self.money += property_purchase_price[sell_p]
                self.owned_properties.remove(sell_p)
                property_state[sell_p] = -2
            else:
                if sell_p < 10:
                    self.money += 25
                elif sell_p < 20:
                    self.money += 50
                elif sell_p < 30:
                    self.money += 100
                else:
                    self.money += 200
                property_state[sell_p] -= 1
        gui.updateDashboard(num=self.player_num, properties=self.owned_properties, money=self.money)
        m_win.destroy()
        if self.money >= amount:
            return -1
        else:
            return 1



    def spaceAction(self, space, players):
        global property_name, property_owner, property_state, property_rent, property_purchase_price
        if space == 30:
            self.goToJail()
        elif space in community_chest_spaces:
            self.drawCommunityChest()
        elif space in chance_spaces:
            self.drawChance()
        # Taxes
        elif space == 4:
            gui.msg(f"{self.player_name} paid $200.")
            self.money -= 200
        elif space == 38:
            gui.msg(f"{self.player_name} paid $100.")
            self.money -= 100
        elif space in null_space or space in self.owned_properties:
            pass
        elif space == 40:
            if self.jail_free_card:
                query = gui.popup("You have a get out of jail free card. Do you want to use it?", ["YES", "NO"])
            else:
                query = gui.popup("Do you want to pay $50 to get out of jail?", ["YES", "NO"])
            if query == "YES":
                if self.jail_free_card:
                    self.jail_free_card = False
                elif self.money >= 50:
                    self.money -= 50
                else:
                    if self.mortgageOrSell(50) == -1:
                        gui.msg(f"{self.player_name} stayed in jail.")
                        return
                self.circularTokenMove(self.position, 10)
                gui.updateDashboard(self.player_num, money=self.money, jailCard=self.jail_free_card)
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
                players[property_owner[space]].money += rent
            if self.money >= rent:
                self.money -= rent
                gui.msg(f"{self.player_name} paid ${str(rent)} to {players[property_owner[space]].player_name}.")
            else:
                if self.mortgageOrSell(rent - self.money) == -1:
                    self.bankrupt()
                else:
                    self.money -= rent
                    gui.msg(f"{self.player_name} paid {str(rent)} to {property_name[property_owner[space]]}.")
        else:
            price = property_purchase_price[space]
            query = gui.popup(f"Would {self.player_name} like to buy {property_name[space]} for ${price}?\n{self.player_name} currently has ${self.money}", ['YES', 'NO'])
            if query == 'YES':
                if self.money >= price:
                    self.money -= price
                else:
                    if self.mortgageOrSell(price) == 1:
                        self.money -= price
                    else:
                        gui.msg("You don't have enough money to buy this property.")
                        return
                gui.msg(f"{self.player_name} has bought {property_name[space]} for ${price}. \n{self.player_name} now has ${self.money}.")
                property_owner[space] = players.index(self)
                print(f"Property has been transferred to player {players.index(self)}")
                property_state[space] = 0
                self.owned_properties.append(space)

    def drawChance(self):
        global players, property_owner
        if self.isCrane and random.randint(1, 4) <= 3:
            gui.omniousMsg('It seems that fortune is \nno longer with this player...', True)
            draw_card = [9, 10, 14, 15, 16][random.randint(0, 4)]
        else:
            draw_card = random.randint(1, 16)

        if draw_card <= 10:
            if draw_card == 1:
                #reading railroad
                gui.msg(f"{self.player_name} advanced to Writing Railroad.")
                self.circularTokenMove(self.position, 5)
            elif draw_card == 2:
                #st. charles
                gui.msg(f"{self.player_name} advanced to St. Nicholas Place.")
                self.circularTokenMove(self.position, 11)
            elif draw_card == 3:
                #illinois
                gui.msg(f"{self.player_name} advanced to Healthinois Avenue.")
                self.circularTokenMove(self.position, 24)
            elif draw_card == 4:
                #boardwalk
                gui.msg(f"{self.player_name} advanced to Plankrun.")
                self.circularTokenMove(self.position, 39)
            elif draw_card == 5 or draw_card == 6:
                #nearest railroad
                gui.msg(f"{self.player_name} advanced to the nearest railroad.")
                new_pos = self.position
                if (new_pos - (new_pos % 10) + 5) < (new_pos):
                    new_pos += 5
                new_pos -= new_pos % 10
                new_pos += 5
                new_pos %= 40
                self.circularTokenMove(self.position, new_pos)
                if property_owner[self.position] != -1 and property_owner[self.position] != self.player_num:
                    gui.msg(f"{self.player_name} paid double!")
                    self.spaceAction(self.position, players=players)
            elif draw_card == 7:
                #nearest utility
                gui.msg(f"{self.player_name} advanced to the nearest utility.")
                if self.position < 12:
                    self.circularTokenMove(self.position, 12)
                elif self.position < 28:
                    self.circularTokenMove(self.position, 28)
                else:
                    self.circularTokenMove(self.position, 12)
                if property_owner[self.position] != -1 and property_owner[self.position] != self.player_num:
                    gui.msg(f"{self.player_name} paid double!")
                    self.spaceAction(self.position, players=players)
            elif draw_card == 8:
                #GO
                gui.msg(f"{self.player_name} advanced to Go.")
                self.circularTokenMove(self.position, 0)
                gui.msg(f"{self.player_name} passed Go and collected $200.")
                self.money += 200
            elif draw_card == 9:
                #jail
                gui.msg(f"{self.player_name} went to jail.")
                self.goToJail()
            elif draw_card == 10:
                #go back 3 spaces
                gui.msg(f"{self.player_name} went back three spaces.")
                self.position = self.position - 3 % 40
                self.guiPos = gui.moveToken(self.player_num, self.guiPos, self.position)
            gui.msg(f"{self.player_name} landed on {property_name[self.position]}.")
            self.spaceAction(self.position, players=players)
        elif draw_card == 11:
            #get out of jail free card
            gui.msg(f"{self.player_name} got a get out of jail free card.")
            self.jail_free_card = True
        elif draw_card == 12:
            #building loan
            gui.msg(f"{self.player_name}'s building loan matured. \n{self.player_name} collected $150.")
            self.money += 150
        elif draw_card == 13:
            #dividends
            gui.msg(f"The bank paid {self.player_name} a dividend of $50.")
            self.money += 50
        elif draw_card == 14:
            gui.msg(f"Speeding fine! {self.player_name} was charged $15.")
            if self.money >= 15:
                self.money -= 15
            else:
                if self.mortgageOrSell(15) == 1:
                    self.money -= 15
                else:
                    self.bankrupt()
                    return
        elif draw_card == 15:
            #chairman
            gui.msg(f"{self.player_name} has been elected chairman of the board. \n{self.player_name} has to pay each player $50.")
            cost = 50*len(players)
            if self.money >= cost:
                self.money -= cost
            else:
                if self.mortgageOrSell(cost) == 1:
                    self.money -= cost
                else:
                    self.bankrupt()
                    return
            for i in range(len(players)):
                if i != self.player_num:
                    players[i].money += 50
        else:
            cost, houses, hotels = self.buildingRepairs(25, 100)
            gui.msg(f"General repairs! {self.player_name} has to pay ${cost} for {houses} houses and {hotels} hotels.")
            if self.money >= cost:
                self.money -= cost
            else:
                if self.mortgageOrSell(cost) == 1:
                    self.money -= cost
                else:
                    self.bankrupt()
                    return
        gui.updateDashboard(num=self.player_num, pos=property_name[self.position], money=self.money, jailCard=self.jail_free_card)

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
                self.circularTokenMove(self.position, 0)
                gui.msg(f"{self.player_name} passed Go and collected $200.")
                self.money += 200
            elif draw_card == 2:
                #jail
                gui.msg(f"{self.player_name} went to jail.")
                self.goToJail()
        elif draw_card == 3:
            gui.msg(f"{self.player_name} won second prize in a beauty contest. \nCollect $10.")
            self.money += 10
        elif draw_card == 4:
            gui.msg(f"{self.player_name} received and income tax refund of $20.")
            self.money += 20
        elif draw_card == 5:
            gui.msg(f"{self.player_name} received a $25 consultancy fee.")
            self.money += 25
        elif draw_card == 6:
            gui.msg(f"{self.player_name} received $50 from stocks.")
            self.money += 50
        elif draw_card == 7:
            gui.msg(f"{self.player_name} inherited $100.")
            self.money += 100
        elif draw_card == 8:
            gui.msg(f"{self.player_name}'s holiday fund matured. \nCollect $100.")
            self.money += 100
        elif draw_card == 9:
            gui.msg(f"{self.player_name}'s life insurance matured. \nCollect $100.")
            self.money += 100
        elif draw_card == 10:
            gui.msg(f"{self.player_name} experienced a favourable bank error. \nCollect $200.")
            self.money += 200
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
            if self.money >= cost:
                self.money -= cost
            else:
                if self.mortgageOrSell(cost) == 1:
                    self.money -= cost
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
            self.money += (len(players)-1)*10
        elif draw_card == 15:
            gui.msg(f"{self.player_name} got a get out of jail free card.")
            if self.jail_free_card:
                gui.msg(f"{self.player_name} can't have any more cards.")
            else:
                self.jail_free_card = True
        else:
            cost, houses, hotels = self.buildingRepairs(40, 115)
            gui.msg(f"Street repairs! {self.player_name} has to pay ${cost} for {houses} houses and {hotels} hotels.")
            if self.money >= cost:
                self.money -= cost
            else:
                if self.mortgageOrSell(cost) == 1:
                    self.money -= cost
                else:
                    self.bankrupt()
                    return
        gui.updateDashboard(num=self.player_num, pos=property_name[self.position], money=self.money, jailCard=self.jail_free_card)

    def buildingRepairs(self, house_p, hotel_p):
        total_cost = 0
        house_count = 0
        hotel_count = 0
        for property in self.owned_properties:
            if property_state[property] == 5:
                total_cost += hotel_p
                hotel_count += 1
            elif property_state[property] > 0:
                total_cost += property_state[property]*house_p
                house_count += property_state[property]
        return total_cost, house_count, hotel_count

    def purchaseBuildings(self):
        global property_state, color_sets
        if not self.loop:
            return
        if not self.has_set:
            for s in color_sets:
                if s in self.owned_properties:
                    self.has_set = True
                    self.sets.append(s)
                    for p in s:
                        if property_state[p] < 1:
                            property_state[p] = 1
        if not self.has_set:
            return
        # UI import
        print("You have the following sets:")
        for s in self.sets:
            print(s)
        purchase_bool = input("Do you want to purchase a building? (y/n) ")  # placeholder
        if purchase_bool.lower == "y":
            # UI import
            purchase_location = int(input("Which property do you want to build on? "))  # placeholder
            if property_state[purchase_location] == 5:
                gui.msg("You cannot buy more houses.")
                return
            elif purchase_location < 10:
                cost = 50
            elif purchase_location < 20:
                cost = 100
            elif purchase_location < 30:
                cost = 150
            else:
                cost = 200
            if self.money >= cost:
                self.money -= cost
                property_state[purchase_location] += 1
            else:
                if self.mortgageOrSell(cost - self.money) == 1:
                    self.money -= cost
                    property_state[purchase_location] += 1
            if gui.popup("Do you want to continue purchasing buildings?", ["YES","NO"]) == "YES":
                self.purchaseBuildings()
            else:
                return
        else:
            return

    def bankrupt(self):
        global players, property_state
        gui.msg(f"{self.player_name} has been bankrupted!")
        players[players.index(self)] = None
        for property in self.owned_properties:
            property_state[property] = -2
            property_state[property] = -1
        self.loop = False
