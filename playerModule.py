import random
from data import *
import gui

players = []
player_turn = 0
community_chest_spaces = (2, 17, 33)
chance_spaces = (7, 22, 36)
railroads = (5, 15, 25, 35)
utilities = (12, 28)
null_space = (0, 10, 20)


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

    def rollDice(self, past_roll, double_count):
        gui.dice_screen.deiconify()
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        gui.displayRoll(dice1, dice2)
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
        gui.dice_screen.withdraw()
        gui.msg(f"{self.player_name} rolled a {roll}.")
        self.move(roll)
        gui.msg(f"{self.player_name} landed on {property_name[self.position]}.")
        return roll

    def circularTokenMove(self, place):
        turn_corner = ((self.position % 10 + place - self.position) > 10 or place < self.position) and place != 40 and self.position != 40
        if turn_corner:
            self.guiPos = gui.moveToken(self.player_num, self.guiPos, (self.position // 10 * 10 + 10) % 40)
            self.position = (self.position // 10 * 10 + 10) % 40
            self.circularTokenMove(place)
        else:
            self.guiPos = gui.moveToken(self.player_num, self.guiPos, place)
            self.position = place


    def move(self, num):
        self.circularTokenMove((self.position + num) % 40)
        gui.updateDashboard(self.player_num, pos = property_name[self.position])
        if num < 0:
            return
        if self.position - num < 0:
            self.money += 200
            gui.msg(f"{self.player_name} passed Go and collected $200.")

    def goToJail(self):
        self.circularTokenMove(40)
        gui.updateDashboard(self.player_num, pos = property_name[self.position])

    def mortgageOrSell(self, amount):
        global property_state, property_name
        #UI import
        str = ""
        for property in self.owned_properties:
            str += f"{property_name.index(property)}. {property_name[property]} - {property_state[property]} houses\n"
        print(str)
        if gui.popup(f"{self.player_name}, you don't have enough money to pay for this. \nWould you like to mortgage your properties?", ["YES", "NO"]) == "NO":
            return -1
        while True:
            mortgage = self.owned_properties[int(input("Which properties would you like to mortgage?")) - 1]
            if property_state[mortgage] > 0:
                if mortgage < 10:
                    self.money += 25
                elif mortgage < 20:
                    self.money += 50
                elif mortgage < 30:
                    self.money += 75
                else:
                    self.money += 100
                gui.msg(f"{self.player_name} sold a building on {property_name[mortgage]} and now have ${self.money}.")
            else:
                self.money += property_purchase_price[mortgage]/2
                gui.msg(f"{self.player_name} sold {property_name[mortgage]} and now have ${self.money}.")
            gui.msg(f"The amount required is ${amount}.")
            property_state[mortgage] -= 1
            if self.money >= amount:
                self.money -= amount
                return 1
            if len(self.owned_properties) < 1:
                return -1
            if gui.popup("Do you want to continue selling properties?", ["YES", "NO"]) == "NO":
                return -1




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
                self.circularTokenMove(10)
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
                if utility_count == 1:
                    rent = 4 * (random.randint(1, 6) + random.randint(1, 6))
                else:
                    rent = 10 * (random.randint(1, 6) + random.randint(1, 6))
            else:
                rent = property_rent[space][property_state[space]]
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
        draw_card = random.randint(1, 16)
        if draw_card <= 10:
            if draw_card == 1:
                #reading railroad
                gui.msg(f"{self.player_name} advanced to Writing Railroad.")
                self.circularTokenMove(5)
            elif draw_card == 2:
                #st. charles
                gui.msg(f"{self.player_name} advanced to St. Nicholas Place.")
                self.circularTokenMove(11)
            elif draw_card == 3:
                #illinois
                gui.msg(f"{self.player_name} advanced to Healthinois Avenue.")
                self.circularTokenMove(24)
            elif draw_card == 4:
                #boardwalk
                gui.msg(f"{self.player_name} advanced to Plankrun.")
                self.circularTokenMove(39)
            elif draw_card == 5 or draw_card == 6:
                #nearest railroad
                gui.msg(f"{self.player_name} advanced to the nearest railroad.")
                new_pos = self.position
                if (new_pos - (new_pos % 10) + 5) < (new_pos):
                    new_pos += 5
                new_pos -= new_pos % 10
                new_pos += 5
                new_pos %= 40
                self.circularTokenMove(new_pos)
                if property_owner[self.position] != -1 and property_owner[self.position] != self.player_num:
                    gui.msg(f"{self.player_name} paid double!")
                    self.spaceAction(self.position, players=players)
            elif draw_card == 7:
                #nearest utility
                gui.msg(f"{self.player_name} advanced to the nearest utility.")
                if self.position < 12:
                    self.circularTokenMove(12)
                elif self.position < 28:
                    self.circularTokenMove(28)
                else:
                    self.circularTokenMove(12)
                if property_owner[self.position] != -1 and property_owner[self.position] != self.player_num:
                    gui.msg(f"{self.player_name} paid double!")
                    self.spaceAction(self.position, players=players)
            elif draw_card == 8:
                #GO
                gui.msg(f"{self.player_name} advanced to Go.")
                self.circularTokenMove(0)
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

    def drawCommunityChest(self):
        global players
        draw_card = random.randint(1, 16)
        if draw_card <= 2:
            if draw_card == 1:
                #GO
                gui.msg(f"{self.player_name} advanced to Go.")
                self.circularTokenMove(0)
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
