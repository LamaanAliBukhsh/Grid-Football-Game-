import pygame
import gridd
import random
import helper
from player import Player


# def clearball():
#     for i in range(7):
#         for j in range(12):
#             if gridd.Ball[i][j] == "B":
#                 gridd.Ball[i][j] = "."

def passoptions(x, y, teamb):
    player = gridd.Field[x][y]
    options = []
    prange = 2
    if player.PAS>=85:
        prange = 4
    elif player.PAS>=75:
        prange = 3

    for nx in range(max(0, x - prange), min(7, x + prange + 1)):
        for ny in range(max(0, y - prange), min(12, y + prange + 1)):
            dx, dy = nx - x, ny - y
            if (nx == x and ny == y) or not isinstance(gridd.Field[nx][ny], Player):
                continue
            if dx==0 or dy==0 or abs(dx)==abs(dy):
                spot = gridd.Field[nx][ny]
                if spot.Club==teamb:
                    options.append((nx, ny))
    return options

def Pass(x, y, targets):
    player = gridd.Field[x][y]
    if not targets:
        return False, True, True  # Failed, Possession lost

    px, py = targets[0]
    spot = gridd.Field[px][py]
    if not isinstance(player, Player) or not isinstance(spot, Player):
        return False, True, True
    if player.Club != spot.Club:
        return False, True, True

    qx = (px - x) // max(1, abs(px - x)) if x != px else 0
    qy = (py - y) // max(1, abs(py - y)) if y != py else 0

    path = []
    cx, cy = x, y
    while (cx, cy) != (px, py):
        cx += qx
        cy += qy
        path.append((cx, cy))

    for fx, fy in path:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = fx + dx, fy + dy
                if 0 <= nx < 7 and 0 <= ny < 12:
                    obs = gridd.Field[nx][ny]
                    if isinstance(obs, Player) and obs.Club != player.Club:
                        if not resolveINT(player, obs):
                            gridd.move_ball(fx, fy)
                            if gridd.Field[fx][fy] == ".":
                                gridd.Field[fx][fy] = obs
                                gridd.Field[nx][ny] = "."
                            else:
                                gridd.Field[fx][fy], gridd.Field[nx][ny] = obs, player
                            return True, False, True
    gridd.move_ball(px, py)
    return True, True, False



def resolveINT(Attacker, Defender):
    total=Attacker.PAS+Defender.PHY
    wheel=random.randint(1,total)
    return wheel<=Attacker.PAS


def Shoot(x, y, teamb):
    player = gridd.Field[x][y]
    gkx, gky, goaly = (3, 1, 0) if teamb == gridd.Field[3][10].Club else (3, 10, 11)
    dx, dy = gkx - x, gky - y

    if not (dx == 0 or abs(dx) == abs(dy)):
        return False, True, False


    steps = max(abs(dx), abs(dy)) + 1
    qx = dx // abs(dx) if dx != 0 else 0
    qy = dy // abs(dy) if dy != 0 else 0

    path = []
    cx, cy = x, y
    for k in range(steps):
        cx += qx
        cy += qy
        path.append((cx, cy))

    goalcell = (gkx, goaly)
    for px, py in path:
        if not (0 <= px < 7 and 0 <= py < 12):
            continue
        spot = gridd.Field[px][py]
        if isinstance(spot, Player) and spot.Club != teamb:
            if (px, py) == (gkx, gky):
                if not resolveGK(player, spot):
                    gridd.move_ball(px, py)
                    #If GK saves the ball, the ball is thrown to the nearest defender
                    pygame.time.delay(1000)
                    Team = helper.getteam(spot.Club)
                    Def = [(i, j, p) for i, j, p in Team if p.Pos == "D"]
                    if Def:
                        Def.sort(key=lambda d: abs(d[0] - px) + abs(d[1] - py))
                        i, j, pl = Def[0]
                        gridd.move_ball(i, j)
                    return True, False, True
            else:
                if not resolveDEF(player, spot):
                    gridd.move_ball(px, py)
                    return True, False, True

        if (px, py) == goalcell or (px + 1, py) == goalcell or (px - 1, py) == goalcell:
            gridd.move_ball(gkx, goaly)
            return True, False, False
    return True, False, True


def resolveDEF(Attacker, Defender):
    total=Attacker.SHO+Defender.PHY
    return random.randint(1,total)<=Attacker.SHO

def resolveGK(Attacker, Goalie):
    GoalieStat = int((Goalie.POS + Goalie.REF + Goalie.DIV) / 3)
    total=Attacker.SHO+GoalieStat
    return random.randint(1,total)<=Attacker.SHO


def Move(x, y):
    player = gridd.Field[x][y]
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,1), (-1,1), (1,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 7 and 0 <= ny < 12 and gridd.Field[nx][ny] == ".":
            gridd.Field[nx][ny] = player
            gridd.Field[x][y] = "."
            return True
    return False


def resolveDRI(Attacker, Defender):
    total=Attacker.DRI+Defender.DEF
    return random.randint(1,total)<=Attacker.DRI

def Dribble(x, y, teamb):
    player = gridd.Field[x][y]
    for dx, dy in [(-1,0), (1,0), (0,1), (0,-1), (-1,1), (-1,-1), (1,1), (1,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 7 and 0 <= ny < 12:
            spot = gridd.Field[nx][ny]
            if spot == ".":
                gridd.Field[nx][ny] = player
                gridd.move_ball(nx, ny)
                gridd.Field[x][y] = "."
                return True, True, False 
            elif isinstance(spot, Player) and spot.Club != teamb:
                success = resolveDRI(player, spot)
                if success:
                    gridd.Field[nx][ny] = player
                    gridd.move_ball(nx, ny)
                    gridd.Field[x][y] = spot
                    return True, True, False  
                else:
                    gridd.move_ball(nx, ny)
                    return True, False, True  # Lost ball/Possesion
    return False, False, False

def resolveTKL(Defender, Attacker):
    DefStat=random.choice([Defender.PHY, Defender.DEF])
    AttStat=random.choice([Attacker.DRI, Attacker.PHY])
    total=DefStat+AttStat
    return random.randint(1,total)<=DefStat

def Tackle(x, y, teamb):
    player = gridd.Field[x][y]
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 7 and 0 <= ny < 12:
                spot = gridd.Field[nx][ny]
                if isinstance(spot, Player) and spot.Club != teamb:
                    success = resolveTKL(player, spot)
                    if success:
                        gridd.Field[nx][ny] = player
                        gridd.Field[x][y] = spot
                        gridd.move_ball(nx, ny)
                        return True, True
    return False, False
