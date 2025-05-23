#################### IMPORT ####################


from tkinter import *
from tkinter import messagebox
from tkinter import colorchooser
from random import *
from tkinter import filedialog
from PIL import ImageTk, Image
import sys
from data import *

#################### COLOUR PALETTE ####################

TESTING_MODE = False
SAY_YES_TO_EVERYTHING = False
AUTO_SELL = False


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


def tokenSizing(w, h):
    scale = max(w, h) / 40
    return round(w / scale), round(h / scale)

def importFile(p):
    global players_tokenImg
    
    path = filedialog.askopenfilename(title = 'select token', filetypes = [("Png Files", "*.png")])
    if path:
        img = Image.open(rf'{path}')
        img = img.resize(tokenSizing(img.width, img.height))
        img = ImageTk.PhotoImage(img)
        players_tokenImg[p] = img

def changePlayerColor(p):
    global scr, players_color
    new_color = colorchooser.askcolor(title= "Change Player Color")[1]
    players_color[p] = new_color
    players_label[p].config(fg=new_color)
    scr.update()

def retrievePlayers():
    global players_name, players_color
    p = []
    c = []
    for n, i in enumerate(players_name):
        if i.get() != '':
            p.append(i.get())
            c.append(players_color[n])
            
    if len(p) > 1:
        players_color = c
        players_name = p
        return True
    return False

def scatter(principle):
    return principle + randint(-20, 20)

def updateWindow(location):
    global scr, title, subtitle, m_play
    global players_label, players_tokenImg, players_name, players_openfile, players_token, players_dashboard, players_selectcolor
    global tiles_bd, tiles_obj, tiles_frame, tiles_label, mainDialogue, dashboardButton
    global movementSpd, dialogueSpd

    title.place_forget()
    subtitle.place_forget()
    m_play.place_forget()

    topBar.pack_forget()
    setupFrame.pack_forget()
    setupSpacer.pack_forget()
    dialogueSliderTxt.grid_forget()
    movementSliderTxt.grid_forget()
    dialogueSlider.grid_forget()
    movementSlider.grid_forget()
    for i in range(5):
        players_label[i].grid_forget()
        players_openfile[i].grid_forget()
        players_selectcolor[i].grid_forget()

    s_play.place_forget()
    tip.grid_forget()

    for i in range(41):
        tiles_bd[i].place_forget()
        tiles_obj[i].place_forget()
        tiles_frame[i].place_forget()
        tiles_label[i].pack_forget()
    mainDialogue.place_forget()
    openDashboard(False)
    dashboardButton.place_forget()

    if location == 'menu':
        scr.config(bg=BLUE1)

        title.place(anchor=CENTER, x=400, y=300)
        subtitle.place(anchor=CENTER, x=400, y=400)
        m_play.place(anchor=CENTER, x=400, y=500)

    if location == 'setup':
        topBar.pack()
        setupFrame.pack(side = LEFT)
        setupSpacer.pack(side = BOTTOM)
        dialogueSliderTxt.grid(row = 0, column = 0)
        movementSliderTxt.grid(row = 0, column = 1)
        dialogueSlider.grid(row = 1, column = 0)
        movementSlider.grid(row = 1, column = 1)

        for i in range(5):
            players_label[i].grid(row=i, column=0, padx = 10, pady = 5)
            players_openfile[i].grid(row = i, column = 1)
            players_selectcolor[i].grid(row = i, column = 2)

        s_play.place(anchor=CENTER, x=400, y=700)
        tip.grid(row = 5, column = 0)

    if location == 'board':
        scr.config(bg=BLUE0)
        players_token = []
        for i in range(len(players_name)):
            img = defaultToken
            if players_tokenImg[i] != '':
                img = players_tokenImg[i]
            players_token.append(Label(scr, bd = 2, bg = players_color[i], image = img))

        if TESTING_MODE:
            dialogueSpd = 1
            movementSpd = 10000
        else:
            dialogueSpd = (100 - dialogueSlider.get()) * 50 + 1
            movementSpd = movementSlider.get() ** 3 / 5000 + 1

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

        mainDialogue.place(anchor=CENTER, x=400, y=520)
        dashboardButton.place(anchor = CENTER, x = 230, y = 660)

def updateAnimation(location, direction):
    global LOCATION, transition, scr

    if location == 'setup' or (location == 'board' and retrievePlayers()):
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

        if end == 40:
            pos = [scatter(600), scatter(200)]
        else:
            pos = [scatter(pos[rem + 1]), scatter(pos[rem])]
        
        dist = ((pos[0] - start[0]) ** 2 + (pos[1] - start[1]) ** 2) ** 0.5
        calc = movementSpd / dist
        spd = [calc * (pos[0] - start[0]), calc * (pos[1] - start[1])]
        currentPos = start.copy()
        
        for i in range(int(dist / movementSpd)):
            players_token[token].place(anchor = CENTER, x = currentPos[0] + spd[0], y = currentPos[1] + spd[1])
            currentPos = [currentPos[0] + spd[0], currentPos[1] + spd[1]]
            scr.update()
        players_token[token].place(anchor = CENTER, x = pos[0], y = pos[1])

    return pos

def getPlayers():
    return len(players_name), players_name

def msg(m):
    global mainDialogue
    if TESTING_MODE:
        print(m)
        return
    mainDialogue.config(fg = BLUE2)
    mainDialogue.config(text = m)
    scr.update()
    # for i in range(20000):
    #     scr.update()
    scr.after(dialogueSpd)

def omniousMsg(m, pause):
    global mainDialogue
    mainDialogue.config(text = m)
    mainDialogue.config(fg = RED)
    scr.update()
    if pause:
        scr.after(dialogueSpd)

def alterAns(ans):
    global queryAns
    queryAns = ans

def center(win, x_offset = 0, y_offset = 0): #center a window
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2 + x_offset
    y = win.winfo_screenheight() // 2 - win_height // 2 + y_offset
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

def popup(msg, options = ['OK']):
    global scr, queryAns

    if SAY_YES_TO_EVERYTHING or TESTING_MODE:
        if 'OK' in options:
            return 'OK'
        if 'YES' in options:
            return 'YES'
    
    queryAns = None
    window = Tk()
    window.title('Query')
    # window.geometry('{}x{}+{}+{}'.format(600, 200, 0, 0))
    window.geometry('600x200')
    center(window)
    window.config(bg=BLUE1)
    Label(window, text = msg, font = 'optima 20', fg=BLUE2, bg=BLUE1).place(anchor = CENTER, x = 300, y = 50)
    f = Frame(window)
    f.pack(side = BOTTOM, pady = 20)
    for i in options:
        Button(f, text = i, height = 2, highlightbackground=BLUE1, command = lambda x = i: alterAns(x)).pack(side = RIGHT)
    while queryAns is None:
        scr.update()
        window.update()
    window.destroy()
    return queryAns

def openDashboard(fixedState = None):
    global players_dashboard, dashboardState
    state = False
    dashboardState = False
    if fixedState or (fixedState is not False and len(players_dashboard) == 0):
        state = True
        dashboardState = True
        
    for i in players_dashboard:
        i.destroy()
    players_dashboard = []
    if state:
        for i, j in enumerate(players_name):
            players_dashboard.append(Tk())
            players_dashboard[-1].geometry('300x400')
            players_dashboard[-1].title(f'Player {i + 1} - {j}')
            players_dashboard[-1].config(bg = BLUE1, padx = 2, pady = 2)
            players_dashboard[-1].resizable(False, False)
    for i in range(len(players_dashboard)):
        packDashboard(i, False)

def exitProgram():
    query = messagebox.askyesno('Caution!', 'Are you sure you want to exit the program?\nYour game\'s progress will be lost.')
    if query:
        scr.destroy()
        exit()

def updateDashboard(num, can_sell = False):
    global players_dashboard
    if len(players_dashboard) > 0:
        packDashboard(num, can_sell)

def packDashboard(num, can_sell):
    global players_dashboard
    for widget in players_dashboard[num].winfo_children():
        widget.destroy()
    Label(players_dashboard[num], font = 'optima 30', fg = BLUE1, bg = BLUE0, text = f'                    💵 {players_info[num][1]}                    ').pack(padx = 2, pady = 2)
    Label(players_dashboard[num], font = 'optima 20', fg = BLUE1, bg = BLUE0, text = f'                         📍{property_name[players_info[num][0]]}                         ').pack(padx = 2, pady = 2)
    f = Frame(players_dashboard[num], bg = BLUE0)
    f.pack(padx = 2, pady = 2)
    Label(f, font = 'aharoni 15', fg = BLUE1, bg = BLUE0, text = '                              PROPERTIES                              ').pack(padx = 2, pady = 2)
    for i in sorted(players_info[num][2]):
        b = Canvas(f, bg = tiles_colour[i], width=280, height=26, highlightthickness=0)
        b.pack(padx = 4)
        b.create_rectangle(1, 1, 279, 25, fill=BLUE1, outline=tiles_colour[i], width=2)
        inSet = False
        for s in players_info[num][3]:
            if i in s:
                inSet = True
                break
        if inSet:
            if property_state[i] == 6:
                buildings = "🔴"
            elif property_state[i] > 1:
                buildings = f"🟢x{property_state[i] - 1}"
            else:
                buildings = ""
            b.create_text(140.5, 13, font='optima 15 bold', text=f'{buildings}  {property_name[i]}', fill='#fad852')
            buy_button = Button(b, height=1, font='optima 10', width=3, text="Upgrade", highlightthickness=0, highlightbackground=BLUE1, command=lambda x=i: upgradeProperty(x))
            buy_button.place(x=2, y=2)
        else:
            b.create_text(140.5, 13, font = 'optima 15', fill = WHITE, text = f'{property_name[i]}')
        if can_sell:
            sell_button = Button(b, height=1, font = 'optima 10', text="Sell", highlightthickness=0, highlightbackground=BLUE1, command=lambda x = i: sellProperty(x))
            sell_button.place(x=223, y=2)

def mortgagePopup(amount):
    m_scr = Tk()
    m_scr.config(bg=BLUE1)
    m_scr.geometry("350x100")
    m_scr.title("You can't pay!")
    center(m_scr)
    Label(m_scr, text=f"You don't have enough to pay!\nYou need: ${amount}\nSell some properties to continue.", font="optima 20", fg=BLUE2, bg=BLUE1).place(anchor="center", x=175, y=50)
    m_scr.update()
    return m_scr

def sellProperty(property):
    if property_state[property] == 0:
        players_info[property_owner[property]][1] += property_purchase_price[property]
        players_info[property_owner[property]][2].remove(property)
        property_state[property] = -1
        property_owner[property] = -1
    else:
        if property < 10:
            players_info[property_owner[property]][1] += 25
        elif property < 20:
            players_info[property_owner[property]][1] += 50
        elif property < 30:
            players_info[property_owner[property]][1] += 100
        else:
            players_info[property_owner[property]][1] += 200
        property_state[property] -= 1

def upgradeProperty(property):
    for i in color_sets[color_set_index[property]]:
        if property_state[i] < property_state[property]:
            popup("You must build evenly.")
            return
    if property_state[property] == 6:
        popup("This property has already been fully upgraded.")
        return
    if property < 10:
        price = 25
    elif property < 20:
        price = 50
    elif property < 30:
        price = 100
    else:
        price = 200
    if players_info[property_owner[property]][1] < price:
        popup(f"You don't have enough to pay for this upgrade (${price}).")
    else:
        players_info[property_owner[property]][1] -= price
        property_state[property] += 1
        updateDashboard(property_owner[property])

#################### TK ####################


scr = Tk()
scr.geometry('800x800')
center(scr)
scr.title(' NOMOLOPY ')
scr.resizable(False, False)
scr.protocol('WM_DELETE_WINDOW', exitProgram)
#################### MAIN MENU ####################


### title & subtitle ###

title = Label(scr, bg=BLUE0, fg=BLUE1, text='NOMOLOPY', font='arial 80 bold')
subtitle = Label(scr, bg=BLUE0, fg=BLUE1, text='~ Very Original, est. 2024 ~', font='optima 40 italic')

### buttons ###

m_play = Button(scr, bg=BLUE1, fg=BLUE2, text='PLAY', font='aharoni 60', command=lambda: updateAnimation('setup', 1), highlightbackground=BLUE1)

#################### SETUP MENU ####################

topBar = Label(scr, bg = BLUE0, fg = BLUE1, width = 30, font = 'arial 50 bold', text = 'GAME SETUP')
setupFrame = Frame(scr, bg = BLUE1)
setupSpacer = Frame(scr, bg = BLUE1)

dialogueSliderTxt = Label(setupSpacer, text = 'Dialogue Speed')
movementSliderTxt = Label(setupSpacer, text = 'Movement Speed')
dialogueSlider = Scale(setupSpacer, from_ = 0, to = 100, orient = HORIZONTAL)
movementSlider = Scale(setupSpacer, from_ = 0, to = 100, orient = HORIZONTAL)

dialogueSpd = 1000
movementSpd = 100
dialogueSlider.set(75)
movementSlider.set(25)

players_name = [StringVar(scr, '') for i in range(5)]
players_label = []
players_openfile = []
players_selectcolor = []
players_tokenImg = [''] * 5
players_color = [RED, GREEN, BLUE, YELLOW, PINK]
players_token = []
for i in range(5):
    players_label.append(Entry(setupFrame, width=10, fg = players_color[i], bg=BLUE0, textvariable=players_name[i], font='optima 50 italic bold', highlightbackground=BLUE1))
    players_openfile.append(Button(setupFrame, text = 'Import token', command = lambda x = i: importFile(x), highlightbackground=BLUE1))
    players_selectcolor.append(Button(setupFrame, text = 'Change color', command = lambda x = i: changePlayerColor(x), highlightbackground=BLUE1))

s_play = Button(scr, bg=BLUE1, fg=BLUE2, text='PLAY', font='aharoni 60', command=lambda: updateAnimation('board', 1), highlightbackground=BLUE1)

tip = Label(setupFrame, bg = BLUE1, fg = RED, text = 'Press ~ for testing mode\nPress \\ for "say-yes-to-everything" mode', font = 'optima 10 italic')

def pressedT(a):
    global TESTING_MODE
    TESTING_MODE = True

def pressedY(a):
    global SAY_YES_TO_EVERYTHING
    SAY_YES_TO_EVERYTHING = True

def pressedA(a):
    global AUTO_SELL
    AUTO_SELL = True

scr.bind('<Control-t>', pressedT)
scr.bind('<Control-y>', pressedY)
scr.bind('<Control-a>', pressedA)

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

### dialogue & query ###

mainDialogue = Label(scr, bg=BLUE0, fg=BLUE2, text='', font='optima 30')
queryAns = None

### dashboards ###

players_dashboard = []
dashboardState = False
dashboardButton = Button(scr, text = 'Dashboards', font = 'optima 30', command = openDashboard, highlightbackground=BLUE0)

#################### OTHER STUFF ####################

transitionImg = Image.open('transition.png')
transitionImg = transitionImg.resize([800, 800])
transitionImg = ImageTk.PhotoImage(transitionImg)
transition = Label(scr, image=transitionImg, bd=0)
defaultToken = Image.open('token1.png')
defaultToken = defaultToken.resize(tokenSizing(defaultToken.width, defaultToken.height))
defaultToken = ImageTk.PhotoImage(defaultToken)

def displayDice(c, num):
    c.delete("all")
    if num in [1, 3, 5]:
        c.create_oval(42.5, 42.5, 62.5, 62.5, fill="black")
    if num in [2, 3, 4, 5, 6]:
        c.create_oval(20, 20, 40, 40, fill="black")
        c.create_oval(65, 65, 85, 85, fill="black")
    if num in [4, 5, 6]:
        c.create_oval(65, 20, 85, 40, fill="black")
        c.create_oval(20, 65, 40, 85, fill="black")
    if num == 6:
        c.create_oval(20, 42.5, 40, 62.5, fill="black")
        c.create_oval(65, 42.5, 85, 62.5, fill="black")

def displayRoll(d1, d2):
    global dice_screen, dice1, dice2
    if TESTING_MODE:
        return

    dice_screen.deiconify()
    dice_screen.lift()
    center(dice_screen, 0, -50)

    speed = 25
    while speed > 1:
        dice_screen.after(int(500 / speed))
        displayDice(dice1, randint(1, 6))
        displayDice(dice2, randint(1, 6))
        dice_screen.update()
        speed -= 0.5 * dialogueSpd / (dialogueSpd - 0.996)
    dice_screen.after(500)
    displayDice(dice1, d1)
    displayDice(dice2, d2)
    dice_screen.update()
    dice_screen.after(dialogueSpd)

dice_screen = Tk()
dice_screen.title("Roll the Dice")
dice_screen.config(background=BLUE1)
dice_screen.geometry("500x250")
dice_screen.resizable(False, False)
dice1 = Canvas(dice_screen, height=100, width=100, bg="white", highlightbackground=BLUE1)
dice1.place(x=100, y=75)
dice2 = Canvas(dice_screen, height=100, width=100, bg="white", highlightbackground=BLUE1)
dice2.place(x=300, y=75)
dice_screen.withdraw()
