property_name = ["GO", "Arctic Avenue", "Community Chest", "North Sea Avenue", "Income Tax", "Writing Railroad", "Disoriented Avenue", "Chance", "Ventnor Avenue", "Connect Four Avenue", "Just Visiting", "St. Nicholas Place", "Electric Company", "Provinces Avenue", "Washington Avenue", "Pencil Railroad", "Crane's Place", "Community Chest", "Tessinee Avenue", "Old York Avenue", "Free Parking", "Chicken Avenue", "Chance", "India Avenue", "Healthinois Avenue", "M. & M. Railroad", "Pacific Avenue", "Vermont Avenue", "Water Works", "Martin Gardens", "Go To Jail", "Atlantic Avenue", "South Carolina Avenue", "Community Chest", "Pencil Avenue", "Long Line", "Chance", "Drive Place", "Luxury Tax", "Plankrun", "Jail"]
property_rent = [0, [2, 4, 10, 30, 90, 160, 250], 0, [4, 8, 20, 60, 180, 320, 450], 0, [25, 50, 100, 200], [6, 12, 30, 90, 270, 400, 550], 0, [6, 12, 30, 90, 270, 400, 550], [8, 16, 40, 100, 300, 450, 600], 0, [10, 20, 50, 150, 450, 625, 750], 0, [10, 20, 50, 150, 450, 625, 750], [12, 24, 60, 180, 500, 700, 900], [25, 50, 100, 200], [14, 28, 70, 200, 550, 750, 950], 0, [14, 28, 70, 200, 550, 750, 950], [16, 32, 80, 220, 600, 800, 1000], 0, [18, 36, 90, 250, 700, 875, 1050], 0, [18, 36, 90, 250, 700, 875, 1050], [20, 40, 100, 300, 750, 925, 1100], [25, 50, 100, 200], [22, 44, 110, 330, 800, 975, 1150], [22, 44, 110, 330, 800, 975, 1150], 0, [24, 48, 120, 360, 850, 1025, 1200], 0, [26, 52, 130, 390, 900, 1100, 1275], [26, 52, 130, 390, 900, 1100, 1275], 0, [28, 56, 150, 450, 1000, 1200, 1400], [25, 50, 100, 200], 0, [35, 70, 175, 500, 1100, 1300, 1500], 0, [50, 100, 200, 600, 1400, 1700, 2000]]
color_sets = ((1, 3), (6, 8, 9), (11, 13, 14), (16, 18, 19), (21, 23, 24), (26, 27, 29), (31, 32, 34), (37, 39))
property_purchase_price = (0, 60, 0, 60, 0, 200, 100, 0, 100, 120, 0, 140, 150, 140, 160, 200, 180, 0, 180, 200, 0, 220, 0, 220, 240, 200, 260, 260, 150, 280, 0, 300, 300, 0, 320, 200, 0, 350, 0, 400)
#-2 = not owned, -1 = mortgaged, 0 = owned, 1 = color set, >1 = has houses
property_state = [-2]*40
# -1 = unowned, otherwise player index
property_owner = [-1]*40

players_info = [[None] * 5 for i in range(5)]