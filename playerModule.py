import random
from data import *
import gui

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
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        print(f"Rolled {dice1} and {dice2}")
        roll = past_roll + dice1 + dice2
        print("The roll is now " + str(roll))
        if dice1 == dice2:
            if self.position == 40:
                self.position = 10
                return roll
            else:
                double_count += 1
                if double_count >= 3:
                    print("You rolled 3 doubles in a row. Go to jail.")
                    self.goToJail()
                    return None
                else:
                    return self.rollDice(roll, double_count)
        elif self.position == 40:
            print("Stay in jail")
            return None
        print("Rolled")
        return roll

    def move(self, num):
        self.position = (self.position + num) % 40
        if self.position - num < 0:
            self.money += 200
            gui.msg("You passed go. Collect $200.")

    def goToJail(self):
        self.position = 40
        gui.moveToken(self.player_num, self.guiPos, 40)

    def mortgageOrSell(self, amount):
        #UI import
        str = ""
        for property in self.owned_properties:
            str += f"{property_name.index(property)}. {property_name[property]} - {property_state[property]} houses\n"
        print(str)
        if input("You don't have enough money to buy this. Would you like to mortgage your properties? (y/n) ").lower() == "n":
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
                print(f"You sold a building and now have ${self.money}.")
            else:
                self.money += property_purchase_price[mortgage]/2
                print(f"You sold {property_name[mortgage]} and now have ${self.money}.")
            print(f"The amount required is ${amount}.")
            property_state[mortgage] -= 1
            if self.money >= amount:
                self.money -= amount
                return 1
            if len(self.owned_properties) < 1:
                return -1
            if input("Do you want to continue selling properties? (y/n) ").lower() == "n":
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
            self.money -= 200
        elif space == 38:
            self.money -= 100
        elif space in null_space or space in self.owned_properties:
            pass
        elif space == 40:
            # UI import
            if input("Do you want to pay $50 to get out of jail? (y/n) ").lower() == "y":  # placeholder
                if self.money >= 50:
                    self.money -= 50
                else:
                    if self.mortgageOrSell(50) == 1:
                        self.position = 10
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
                print(f"You paid {str(rent)} to {players[property_owner[space]].player_name}.")
            else:
                if self.mortgageOrSell(rent - self.money) == -1:
                    self.bankrupt()
                else:
                    self.money -= rent
                    print(f"You paid {str(rent)} to {property_name[property_owner[space]]}.")
        else:
            price = property_purchase_price[space]
            query = gui.popup(f"Would {self.player_name} like to buy {property_name[space]} for ${price}?\n{self.player_name} currently have ${self.money}", ['YES', 'NO'])
            if query == 'YES':
                if self.money >= price:
                    self.money -= price
                else:
                    if self.mortgageOrSell(price) == 1:
                        self.money -= price
                    else:
                        print("You don't have enough money to buy this property.")
                        return
                print(f"You have bought this space for {price}. You now have ${self.money}.")
                property_owner[space] = players.index(self)
                print(f"Property has been transferred to player {players.index(self)}")
                property_state[space] = 0
                self.owned_properties.append(space)

    def drawChance(self):
        global players, property_owner
        print("You landed on chance!")
        draw_card = random.randint(1, 16)
        if draw_card <= 7:
            if draw_card == 1:
                #reading railroad
                self.move((5-self.position)%40)
            elif draw_card == 2:
                #st. charles
                self.move((11-self.position)%40)
            elif draw_card == 3:
                #illinois
                self.move((24-self.position)%40)
            elif draw_card == 4:
                #boardwalk
                self.move((39-self.position)%40)
            elif draw_card == 5 or draw_card == 6:
                #nearest railroad
                self.position -= self.position % 5
                if self.position%10 == self.position%5:
                    self.position += 5
                if property_owner[self.position] != -1 and property_owner[self.position] != self.player_num:
                    gui.msg("You pay double!")
                    self.spaceAction(self.position, players=players)
            elif draw_card == 7:
                #nearest utility
                if self.position < 28:
                    self.move((28-self.position)%40)
                elif self.position < 12:
                    self.move((12-self.position)%40)
                else:
                    self.move((28-self.position)%40)
                if property_owner[self.position] != -1 and property_owner[self.position] != self.player_num:
                    gui.msg("You pay double!")
                    self.spaceAction(self.position, players=players)
            elif draw_card == 8:
                #GO
                self.position = 0
            elif draw_card == 9:
                #jail
                self.goToJail()
            self.guiPos = gui.moveToken(player_turn, self.guiPos, self.position)
            gui.msg(f"{self.player_name} landed on {property_name[self.position]}.")
            self.spaceAction(self.position, players=players)
    def drawCommunityChest(self):
        print("Chest")
        pass

    def purchaseBuildings(self):
        global property_state, color_sets
        if not self.loop:
            return
        if not self.has_set:
            for set in color_sets:
                if set in self.owned_properties:
                    self.has_set = True
                    self.sets.append(set)
        if not self.has_set:
            return
        # UI import
        print("You have the following sets:")
        for set in self.sets:
            print(set)
        purchase_bool = input("Do you want to purchase a building? (y/n) ")  # placeholder
        if purchase_bool.lower == "y":
            # UI import
            purchase_location = int(input("Which property do you want to build on? "))  # placeholder
            if property_state[purchase_location] == 5:
                # UI import - cannot buy more houses
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
            # UI Import
            if input("Do you want to continue purchasing buildings? (y/n)").lower == 'y':  # placeholder
                self.purchaseBuildings()
            else:
                return
        else:
            return

    def bankrupt(self):
        global players, property_state
        players[players.index(self)] = None
        for property in self.owned_properties:
            property_state[property] = -2
            property_state[property] = -1
        self.loop = False
