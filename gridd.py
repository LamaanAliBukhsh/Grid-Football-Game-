import random
import copy
from player import roster
from player import Player
from player import Goalie

scoreA=0
scoreB=0
selected_player = None
null = ["X","X","X","X","X","X","X","X","X","X","X","X"]
play = ["X","k",".",".",".",".",".",".",".",".","k","X"]
gk = [str(scoreA),"M",".",".",".",".",".",".",".",".","N",str(scoreB)]
ball = ["GH",".",".",".",".",".",".",".",".",".",".","GA"]


Field = [
        copy.deepcopy(null),
        copy.deepcopy(play),
        copy.deepcopy(play),
        copy.deepcopy(gk),
        copy.deepcopy(play),
        copy.deepcopy(play),
        copy.deepcopy(null)
    ]

Ball = [
        copy.deepcopy(null),
        copy.deepcopy(play),
        copy.deepcopy(play),
        copy.deepcopy(ball),
        copy.deepcopy(play),
        copy.deepcopy(play),
        copy.deepcopy(null)
    ]

RM = {}
RMD = []
RMM = []
RMA = []
LIV = {}
LIVD = []
LIVM = []
LIVA = []
initial={}

def init_rosters():
    global RM, RMD, RMM, RMA, LIV, LIVD, LIVM, LIVA
    for i in range(0, 12):
        roster[i].Club="RM"
    
    for i in range(12, 24):
        roster[i].Club="LIV"

    for i in range(0, 12):
        RM[roster[i].Name] = roster[i]
    RMD = list(roster[1:5])
    random.shuffle(RMD)
    RMM = list(roster[5:9])
    random.shuffle(RMM)
    RMA = list(roster[9:12])
    random.shuffle(RMA)

    for i in range(12, 24):
        LIV[roster[i].Name] = roster[i]
    LIVD = list(roster[13:17])
    random.shuffle(LIVD)
    LIVM = list(roster[17:20])
    random.shuffle(LIVM)
    LIVA = list(roster[20:24])
    random.shuffle(LIVA)


def displayfield():
    for x in range(0,7):
        for y in range(0,12):
            if isinstance(Field[x][y],Player) or isinstance(Field[x][y],Goalie):
                print(Field[x][y].Name[:3], end=" ")
            else:
                print(Field[x][y], end="          ")
        print(" ")

def displayball():
    for x in range(0,7):
        for y in range(0,12):
            print(Ball[x][y], end=" ")
        print(" ")


def setteamA(team):
    global homeD,homeM,homeA
    if team=="A":
        homeD = set(copy.deepcopy(RMD))
        homeM = set(copy.deepcopy(RMM))
        homeA = set(copy.deepcopy(RMA))
    elif team=="B":
        homeD = set(copy.deepcopy(LIVD))
        homeM = set(copy.deepcopy(LIVM))
        homeA = set(copy.deepcopy(LIVA))

    
def setteamB(team):
    global awayD,awayM,awayA
    if team=="A":
        awayD = set(copy.deepcopy(RMD))
        awayM = set(copy.deepcopy(RMM))
        awayA = set(copy.deepcopy(RMA))
    elif team=="B":
        awayD = set(copy.deepcopy(LIVD))
        awayM = set(copy.deepcopy(LIVM))
        awayA = set(copy.deepcopy(LIVA))
        
def set_form(form, team, bool):
    set_gk(3,1,bool,team)
    if form == "A":
        set_player(1,2,bool,"D")     
        set_player(3,2,bool,"D")  
        set_player(5,2,bool,"D")
 
        set_player(2,5,bool,"M")  
        set_player(4,5,bool,"M")  

        set_player(3,8,bool,"A")
    elif form == "B":
        set_player(2,2,bool,"D")
        set_player(4,2,bool,"D")

        set_player(1,5,bool,"M")
        set_player(5,5,bool,"M")

        set_player(2,8,bool,"A")
        set_player(4,8,bool,"A")
    elif form == "C":
        set_player(1,2,bool,"D")
        set_player(5,2,bool,"D")

        set_player(2,5,bool,"M")
        set_player(3,5,bool,"M")
        set_player(4,5,bool,"M")

        set_player(3,8,bool,"A")


def set_gk(x, y, bool, team):
    if bool:
        X=x
        Y=y
    else:
        X=6-x
        Y=11-y
    if team=="A":
        Field[X][Y] = roster[0]
    initial[Field[X][Y]]=(X,Y)
    if team=="B":
        Field[X][Y] = roster[12]
    initial[Field[X][Y]]=(X,Y)
def set_player(x, y, bool, pos):
    if bool:
        X, Y = x, y
        pool = {"D": homeD, "M": homeM, "A": homeA}[pos]
    else:
        X, Y = 6 - x, 11 - y
        pool = {"D": awayD, "M": awayM, "A": awayA}[pos]
    
    pl=pool.pop()
    Field[X][Y]=pl
    initial[Field[X][Y]]=(X,Y)



# def resolvecol(x, y, newy, teama, teamb):
#     mover = Field[x][y]
#     target = Field[x][newy]

#     if mover.Club == teama:
#         offsety = 1
#     else:
#         offsety = -1

#     if isinstance(target, Player):
#         decider = random.randint(0, 1)
#         if decider == 1:
#             future_y = newy + offsety

#             Field[x][future_y] = target
#             Field[x][newy] = mover
#             Field[x][y] = "."
#         else:
#             alt_y = newy + random.choice([-1, 1]) 
#             if 0 <= alt_y < 12 and Field[x][alt_y] == ".":
#                 Field[x][alt_y] = mover
#                 Field[x][y] = "."
#             else:
#                 pass
#     else:
#         Field[x][newy] = mover
#         Field[x][y] = "."



# def kickoff(teama,teamb):
#         for x in range(1,6,-1):
#             for y in range(2,7,-1):
#                 newy=0
#                 if isinstance(Field[x][y], Player):
#                     newy=(y+2)                   
#                     Field[x][newy] = Field[x][y]
#                     Field[x][y] = "."
#         for x in range(1,6):
#             for y in range(7,13):
#                 newy=0
#                 if isinstance(Field[x][y], Player):
#                     newy=(y-2)                   
#                     Field[x][newy] = Field[x][y]
#                     Field[x][y] = "."


    

        

      

def kickoff():
        while True:
            midx=random.randint(1,5)
            if isinstance(Field[midx][5],Player):
                Ball[midx][5]="B"
                break

def reset(goal):
    global scoreA, scoreB
    for i in range(1,6):
        for j in range(1,11):
            Field[i][j] = "."

    for player, (x, y) in initial.items():
        Field[x][y] = player
        
    if not goal:
        while True:
            midx=random.randint(1,5)
            if isinstance(Field[midx][5],Player):
                Ball[midx][5]="B"
                scoreB+=1
                Field[3][11]=str(scoreB)
                break
    else:
        while True:
            midx=random.randint(1,5)
            if isinstance(Field[midx][6],Player):
                Ball[midx][6]="B"
                scoreA+=1
                Field[3][0]=str(scoreA)
                break

          

def move_ball(newx, newy):
    for x in range(7):
        for y in range(12):
            if Ball[x][y] == "B":
                Ball[x][y] = "."
    Ball[newx][newy] = "B"