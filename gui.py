#################### IMPORT ####################


from tkinter import *
from random import *
from tkinter import filedialog
from PIL import ImageTk, Image
import sys

#################### COLOUR PALETTE ####################


BLUE0 = '#ceddf5'
BLUE1 = '#99baf0'
BLUE2 = '#4e8ef5'
WHITE = '#ffffff'

# tile colours
BROWN = '#733a14'
BLUE = '#11cfff'
PINK = '#dd00ff'
ORANGE = '#ff9100'
RED = '#ff3c00'
YELLOW = '#ffd500'
GREEN = '#00ba35'
RICH = '#003eba'
BAD = '#660103'

tiles_colour = [WHITE, BROWN, WHITE, BROWN, BAD, WHITE, BLUE, WHITE, BLUE, BLUE, WHITE,
                PINK, WHITE, PINK, PINK, WHITE, ORANGE, WHITE, ORANGE, ORANGE, WHITE,
                RED, WHITE, RED, RED, WHITE, YELLOW, YELLOW, WHITE, YELLOW, BAD,
                GREEN, GREEN, WHITE, GREEN, WHITE, WHITE, RICH, BAD, RICH, BAD]
tiles_name = ["GO\n->", "Arctic\nAvenue", "Commu\n-nity\nChest", "North\nSea\nAvenue", "Income\nTax",
              "Writing\nRail\n-road", "Disori\n-ented\nAvenue", "Chance", "Ventnor\nAvenue", "Connect\nFour\nAvenue",
              "Just\nVisiting", "St. Nicholas\nPlace", "Electric\nCompany", "Provinces\nAvenue", "Washington\nAvenue",
              "Pencil\nRailroad", "Crane's\nPlace", "Community\nChest", "Tessinee\nAvenue", "Old York\nAvenue",
              "Free\nParking", "Chic\n-ken\nAvenue", "Chance", "India\nAvenue", "Healthi\n-nois\nAvenue",
              "M&M\nRail\n-road", "Pacific\nAvenue", "Ver\n-mont\nAvenue", "Water\nWorks", "Martin\nGar\n-dens",
              "Go To\nJail", "Atlantic\nAvenue", "South Caro\n-lina Avenue", "Community\nChest", "Pencil\nAvenue",
              "Long Line", "Chance", "Drive Place", "Luxury Tax", "Plankrun", "Jail"]
LOCATION = 'menu'

#################### FUNCTIONS ####################


def importFile(p):
    global players_tokenImg
    path = filedialog.askopenfilename(title = 'select token', filetypes = [("Png Files", "*.png")])
    if path:
        img = Image.open(rf'{path}')
        img = img.resize([10, 10])
        img = ImageTk.PhotoImage(img)

def retrievePlayers():
    global players_name
    p = []
    for i in players_name:
        if i.get() != '':
            p.append(i.get())
    if len(p) > 1:
        players_name = p
        return True
    return False

def scatter(principle):
    return principle + randint(-20, 20)

def updateWindow(location):
    global scr, title, subtitle, m_play
    global players_label, players_tokenImg, players_name, players_openfile, players_token
    global tiles_bd, tiles_obj, tiles_frame, tiles_label, mainDisplay

    title.place_forget()
    subtitle.place_forget()
    m_play.place_forget()

    for i in range(5):
        players_label[i].grid_forget()
        players_openfile[i].grid_forget()

    s_play.place_forget()

    for i in range(41):
        tiles_bd[i].place_forget()
        tiles_obj[i].place_forget()
        tiles_frame[i].place_forget()
        tiles_label[i].pack_forget()
    mainDisplay.place_forget()

    if location == 'menu':
        scr.config(bg=BLUE1)

        title.place(anchor=CENTER, x=400, y=300)
        subtitle.place(anchor=CENTER, x=400, y=400)
        m_play.place(anchor=CENTER, x=400, y=500)

    if location == 'setup':
        for i in range(5):
            players_label[i].grid(row=i, column=0)
            players_openfile[i].grid(row = i, column = 1)

        s_play.place(anchor=CENTER, x=400, y=500)

    if location == 'board':
        scr.config(bg=BLUE0)
        players_token = []
        for i in range(len(players_name)):
            img = defaultToken
            if players_tokenImg[i] != '':
                img = players_tokenImg[i]
            players_token.append(Label(scr, bd = 0, image = img))
        title.place(anchor=CENTER, x=400, y=380)
        subtitle.place(anchor=CENTER, x=400, y=450)
        for i in range(40):
            mod, rem = i % 10, i // 10
            if mod == 0:
                pos = [52, 52, 748, 748, 52]
            else:
                pos = [52, 66 * mod + 70, 748, 730 - 66 * mod, 52]
            pos = [pos[rem + 1], pos[rem]]

            tiles_bd[i].place(anchor=CENTER, x=pos[0], y=pos[1])
            tiles_obj[i].place(anchor=CENTER, x=pos[0], y=pos[1])
            tiles_frame[i].place(anchor=CENTER, x=pos[0], y=pos[1])
            tiles_label[i].pack()
        tiles_bd[-1].place(anchor=CENTER, x=600, y=200)
        tiles_obj[-1].place(anchor=CENTER, x=600, y=200)
        tiles_frame[-1].place(anchor=CENTER, x=600, y=200)
        tiles_label[-1].pack()

        mainDisplay.place(anchor=CENTER, x=400, y=520)

def updateAnimation(location, direction):
    global LOCATION, transition, scr

    if location != 'board' or retrievePlayers():
        transition.place(x=800 * direction, y=0)
        for i in range(15):
            current = int(transition.place_info().get('x'))
            spd = (15 - (255 - i ** 2) ** 0.5) * direction
            transition.place(x=current - 20 * spd, y=0)
            scr.update()
        updateWindow(location)
        for i in range(15, 30):
            current = int(transition.place_info().get('x'))
            spd = (15 - (i * 60 - i ** 2 - 675) ** 0.5) * direction
            transition.place(x=current - 20 * spd, y=0)
            scr.update()
        transition.place_forget()
        LOCATION = location

def moveToken(token, start, end):
    global players_token, scr
    
    if start is None:
        pos = [scatter(52) for _ in range(2)]
        players_token[token].place(anchor = CENTER, x = pos[0], y = pos[1])
        scr.update()
    else:
        mod, rem = end % 10, end // 10
        if mod == 0:
            pos = [52, 52, 748, 748, 52]
        else:
            pos = [52, 66 * mod + 70, 748, 730 - 66 * mod, 52]
        pos = [scatter(pos[rem + 1]), scatter(pos[rem])]
        
        SPEED = 100
        spd = [(pos[0] - start[0]) / SPEED, (pos[1] - start[1]) / SPEED]
        currentPos = start.copy()
        for i in range(SPEED):
            players_token[token].place(anchor = CENTER, x = currentPos[0] + spd[0], y = currentPos[1] + spd[1])
            currentPos = [currentPos[0] + spd[0], currentPos[1] + spd[1]]
            scr.update()
    return pos

def getPlayers():
    return len(players_name), players_name


#################### TK ####################


scr = Tk()
scr.geometry('800x800')
scr.title(' NOMOLOPY ')
#################### MAIN MENU ####################


### title & subtitle ###

title = Label(scr, bg=BLUE0, fg=BLUE1, text='NOMOLOPY', font='arial 80 bold')
subtitle = Label(scr, bg=BLUE0, fg=BLUE1, text='~ Very Original, est. 2024 ~', font='optima 40 italic')

### buttons ###

m_play = Button(scr, bg=BLUE1, fg=BLUE2, text='PLAY', font='aharoni 60', command=lambda: updateAnimation('setup', 1))

#################### SETUP MENU ####################


players_name = [StringVar(scr, '') for i in range(5)]
players_label = []
players_openfile = []
players_tokenImg = [''] * 5
players_token = []
for i in range(5):
    players_label.append(Entry(scr, width=10, textvariable=players_name[i], font='optima 50 italic bold'))
    players_openfile.append(Button(scr, text = 'Token', command = lambda x = i: importFile(x)))

s_play = Button(scr, bg=BLUE1, fg=BLUE2, text='PLAY', font='aharoni 60', command=lambda: updateAnimation('board', 1))

#################### GAME BOARD ####################


### tiles ###

tiles_bd = []
tiles_obj = []
tiles_frame = []
tiles_label = []
for i in range(40):
    size = [100] * 2
    if i % 10:
        if (i // 10) % 2:
            size[1] = 64
        else:
            size[0] = 64
    tiles_bd.append(Frame(scr, bg=tiles_colour[i], width=size[0], height=size[1]))
    tiles_obj.append(Frame(scr, bg=BLUE1, width=size[0] - 4, height=size[1] - 4))
    tiles_frame.append(Frame(scr, bg=BLUE1, width=size[0] - 4, height=size[1] - 4))
    tiles_label.append(Label(tiles_frame[-1], bg=BLUE1, fg=tiles_colour[i], text=tiles_name[i], font='aharoni 25 bold'))
    if i % 10:
        tiles_label[-1].config(font='aharoni 15')

tiles_bd.append(Frame(scr, bg=BAD, width=150, height=150))
tiles_obj.append(Frame(scr, bg=BLUE1, width=146, height=146))
tiles_frame.append(Frame(scr, bg=BLUE1, width=146, height=146))
tiles_label.append(Label(tiles_frame[-1], bg=BLUE1, fg=tiles_colour[-1], text=tiles_name[-1], font='aharoni 30 bold'))

### dialogue ###

mainDisplay = Label(scr, bg=BLUE0, fg=BLUE2, text='Crane has been fined $9127436802!!!!\noops', font='optima 30')

#################### OTHER STUFF ####################


transitionImg = Image.open('transition.png')
transitionImg = transitionImg.resize([800, 800])
transitionImg = ImageTk.PhotoImage(transitionImg)
transition = Label(scr, image=transitionImg, bd=0)

defaultToken = Image.open('token1.png')
defaultToken = defaultToken.resize([35, 35])
defaultToken = ImageTk.PhotoImage(defaultToken)


#################### MAINLOOP ####################
