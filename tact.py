import gridd
import helper
import random


def calltact(t1,t2,bool,teama):
    if bool:
        if t2=="A":
            HL(teama)
        elif t2=="B":
            SWB(teama)
        elif t2=="c":
            SS(teama)
        elif t2=="D":
            HTL(teama)
    else:
        if t1=="A":
            BT(teama)
        elif t1=="B":
            LB(teama)
        elif t1=="c":
            SW(teama)
        elif t1=="D":
            HM(teama)

def HL(teama):
    bx, by = helper.getball()

    Y, E = 4, 10

    Team = helper.getteam(teama)
    midmin = [j for i, j, p in Team if p.Pos == "M" and (Y < j < E)]

    if not midmin:
        return

    my = min(midmin) - 1

    for i, j, p in Team:
        if p.Pos == "D":
            if j < my and j < by:
                newj = j + 1

            else:
                continue

            if 0 <= newj < 12 and gridd.Field[i][newj] == ".":
                gridd.Field[i][newj] = p
                gridd.Field[i][j] = "."

def SWB(teama):

    Team=helper.getteam(teama)

    for i, j, p in Team:
        if p.Pos=="D" and (i==1 or i==5):
            step = 1 
            newj = j + step
            if 2 <= newj < 10 and gridd.Field[i][newj] == ".":
                gridd.Field[i][newj] = p
                gridd.Field[i][j] = "."

def SS(teama):
    Team = helper.getteam(teama)
    Att = [(i, j, p) for i, j, p in Team if p.Pos == "A"]

    if len(Att) != 2:
        return

    random.shuffle(Att)
    Att1, Att2 = Att


    M1 = [(-1, 1), (0, 1), (1, 1)]
    M2 = [(-1, -1), (0, -1), (1, -1)]


    try_move(*Att1[:2], Att1[2], M1)
    try_move(*Att2[:2], Att2[2], M2)


def try_move(x, y, p, dirs):
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 7 and 0 <= ny < 12 and gridd.Field[nx][ny] == ".":
            gridd.Field[nx][ny] = p
            gridd.Field[x][y] = "."
            break


def HTL(teama):
    Team = helper.getteam(teama)
    Mid = [(i, j, p) for i, j, p in Team if p.Pos == "M"]

    if len(Mid) != 3:
        return

    random.shuffle(Mid)
    target = [1, 3, 5]

    for (targetx, (i, j, p)) in zip(target, Mid):
        dx = targetx - i
        qx = (1 if dx > 0 else -1) if dx != 0 else 0

        newx = i + qx
        newy = j

        if 0 <= newx < 7 and gridd.Field[newx][newy] == ".":
            gridd.Field[newx][newy] = p
            gridd.Field[i][j] = "."

def BT(teama):
    Team = helper.getteam(teama)


    for i, j, p in Team:
        if p.Pos=="A":
            step = -1 
            newj = j + step
            if 3 <= newj < 9 and gridd.Field[i][newj] == ".":
                    gridd.Field[i][newj] = p
                    gridd.Field[i][j] = "."
        
def LB(teama):
    Team = helper.getteam(teama)
   
    
    for i, j, p in Team:
        if p.Pos=="D":
            step = -1
            newj = j + step
            if 2 <= newj < 10 and gridd.Field[i][newj] == ".":
                    gridd.Field[i][newj] = p
                    gridd.Field[i][j] = "."
        elif p.Pos=="M":
            step = -1
            newj = j + step
            if 3 <= newj < 10 and gridd.Field[i][newj] == ".":
                    gridd.Field[i][newj] = p
                    gridd.Field[i][j] = "."

def SW(teama):
    Team = helper.getteam(teama)

    for i, j, p in Team:
        if p.Pos == "A":
            newi = i + 1
        elif p.Pos == "M":
            newi = i - 1
        else:
            continue

        if 0 <= newi < 7 and gridd.Field[newi][j] == ".":
            gridd.Field[newi][j] = p
            gridd.Field[i][j] = "."


def HM(teama):
    Team = helper.getteam(teama)

    for i, j, p in Team:
        if p.Pos == "M" and i in (2, 4):
            step = -1 if i == 4 else 1
            newi = i + step
            if 1 <= newi < 6 and gridd.Field[newi][j] == ".":
                gridd.Field[newi][j] = p
                gridd.Field[i][j] = "."

