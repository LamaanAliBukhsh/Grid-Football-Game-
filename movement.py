import pygame
import gridd
import random
import interface
from player import Player

MENU1 = ["Pass", "Dribble"]
MENU4 = ["Pass", "Dribble", "SHOOT"]
MENU2 = ["Move"]
MENU3 = ["Move","Tackle"]



def actionmenu(screen, x, y, poss, teama):
    menu_rect = pygame.Rect(0, 0, 1200, 100) # Render Menu
    pygame.draw.rect(screen, (25, 25, 25), menu_rect)
    pygame.draw.line(screen, (255, 255, 255), (0, 100), (1200, 100), 2)

    stats_rect = pygame.Rect(0, 740, 1200, 100) # Render Stats
    pygame.draw.rect(screen, (25, 25, 25), stats_rect)
    pygame.draw.line(screen, (255, 255, 255), (0, 740), (1200, 740), 2)

    player = gridd.Field[x][y]
    

    font1 = pygame.font.SysFont('helvetica', 22) 
    font2 = pygame.font.SysFont('helvetica', 16)
    
    dx,dy=0,0

    if isinstance(player, (Player)):
        if player.Club == teama:
            gkx, gky = 3, 10
        else:
            gkx, gky = 3, 1

        dx, dy = gkx - x, gky - y

        stats = [
        f"Name: {player.Name}",
        f"Pos: {player.Pos}",
        f"OVR: {player.OVR}",
        f"PAC: {player.PAC}",
        f"SHO: {player.SHO}",
        f"PAS: {player.PAS}",
        f"DRI: {player.DRI}",
        f"DEF: {player.DEF}",
        f"PHY: {player.PHY}"
        ]
        

        for i, stat in enumerate(stats):
            text = font2.render(stat, True, (255, 255, 255))
            screen.blit(text, (20 + i * 120, 750))

    if poss and (dx == 0 or abs(dx) == abs(dy)) and gridd.Ball[x][y] == "B":
        for i, option in enumerate(MENU4):
            text = font1.render(f"{i+1}. {option}", True, (255, 255, 255))
            screen.blit(text, (20 + i*220, 30))
    elif poss and gridd.Ball[x][y] != "B":
        for i, option in enumerate(MENU2):
            text = font1.render(f"{i+4}. {option}", True, (255, 255, 255))
            screen.blit(text, (20 + i*220, 30))
    elif not poss:
        for i, option in enumerate(MENU3):
            text = font1.render(f"{i+4}. {option}", True, (255, 255, 255))
            screen.blit(text, (20 + i*220, 30))
    elif poss and gridd.Ball[x][y] == "B":
        for i, option in enumerate(MENU1):
            text = font1.render(f"{i+1}. {option}", True, (255, 255, 255))
            screen.blit(text, (20 + i*220, 30))

def passmenu(screen, x, y, options, teama):
    menu_rect = pygame.Rect(0, 0, 1200, 100)
    pygame.draw.rect(screen, (25, 25, 25), menu_rect)
    pygame.draw.line(screen, (255, 255, 255), (0, 100), (1200, 100), 2)


    player = gridd.Field[x][y]
    

    font1 = pygame.font.SysFont('helvetica', 22)
    for i, (ox, oy) in enumerate(options[:5]):
        spot = gridd.Field[ox][oy].Name
        text = font1.render(f"{i+1}. Pass to {spot}", True, (255, 255, 255))
        screen.blit(text, (20 + i*220, 30))


def passoptions(x, y, teama):
    player=gridd.Field[x][y]

    options=[]
    prange=2
    if player.PAS>=85:
        prange=4
    elif player.PAS>=75:
        prange=3
    
    for nx in range(max(0, x-prange), min(7, x+prange+1)):
        for ny in range(max(0, y-prange), min(12, y+prange+1)):
            dx, dy=nx-x, ny-y
            # Skip self and non-players
            if (nx == x and ny == y) or not isinstance(gridd.Field[nx][ny], Player):
                continue
            if dx == 0 or dy == 0 or abs(dx) == abs(dy):
                spot = gridd.Field[nx][ny]
                if spot.Club == teama:
                        options.append((nx, ny))
    
    return options

def drawoptions(screen, options):
    surface = pygame.Surface((1200, 840), pygame.SRCALPHA)
    for x, y in options:
        center_x = y * 100 + 50
        center_y = x * 120 + 60
        pygame.draw.circle(surface, (0, 255, 100, 150), (center_x, center_y), 35)
    screen.blit(surface, (0, 0))
    
    


def Pass(x, y, options):
    player = gridd.Field[x][y]

    keys = pygame.key.get_pressed()
    px = py = None

    if keys[pygame.K_1] and len(options) > 0:
        px, py = options[0]
    elif keys[pygame.K_2] and len(options) > 1:
        px, py = options[1]
    elif keys[pygame.K_3] and len(options) > 2:
        px, py = options[2]
    elif keys[pygame.K_4] and len(options) > 3:
        px, py = options[3]
    elif keys[pygame.K_5] and len(options) > 4:
        px, py = options[4]
    elif keys[pygame.K_6]:
        return True, True

    if px is None or py is None:
        return False, True
    
    spot = gridd.Field[px][py]
    if not isinstance(player, Player) or not isinstance(spot, Player):
        return False, True
    if player.Club != spot.Club:
        return False, True

    qx = (px - x) // max(1, abs(px - x)) if x != px else 0
    qy = (py - y) // max(1, abs(py - y)) if y != py else 0
    
    gridd.Ball[x][y] = "." 

    path = []
    cx, cy = x, y
    while (cx, cy) != (px, py):
        cx += qx
        cy += qy
        path.append((cx, cy))

    for (fx, fy) in path:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = fx + dx, fy + dy
                if 0 <= nx < 7 and 0 <= ny < 12:
                    obs = gridd.Field[nx][ny]
                    if isinstance(obs, Player) and obs.Club != player.Club:
                        if not resolveINT(player, obs):
                            gridd.Ball[fx][fy] = "B"
                            player=gridd.Field[fx][fy]
                            if player == ".":
                                gridd.Field[fx][fy] = obs
                                gridd.Field[nx][ny] = "."
                            elif isinstance(player, Player) and player.Club != obs.Club:
                                gridd.Field[fx][fy] = obs
                                gridd.Field[nx][ny] = player
                            return True, False 
    gridd.Ball[px][py] = "B"
    return True, True


def resolveINT(Attacker, Defender):
    total=Attacker.PAS+Defender.PHY
    wheel=random.randint(1,total)
    if wheel<=Attacker.PAS:
            return True
    else:
        return False


def Shoot(x, y, teama):
    player = gridd.Field[x][y]

    if teama == gridd.Field[3][1].Club:
        gkx, gky, goaly = 3, 10, 11
    else:
        gkx, gky, goaly = 3, 1, 0

    dx, dy = gkx - x, gky - y

    if not (dx == 0 or abs(dx) == abs(dy)):
        return False, True, False

    steps = max(abs(dx), abs(dy)) + 1
    qx = dx // abs(dx) if dx != 0 else 0
    qy = dy // abs(dy) if dy != 0 else 0


    gridd.Ball[x][y] = "."

    path = []
    cx, cy = x, y
    for _ in range(steps):
        cx += qx
        cy += qy
        path.append((cx, cy))

    goalcell = (gkx, goaly)


    for px, py in path:
        if not (0 <= px < 7 and 0 <= py < 12):
            continue

        spot = gridd.Field[px][py]

        if isinstance(spot, Player) and spot.Club != teama:
            if (px, py) == (gkx, gky):
                if not resolveGK(player, spot):

                    gridd.Ball[px][py]="B"
                    return True, False, False
            else:
                if not resolveDEF(player, spot):
                    gridd.Ball[px][py]="B"
                    return True, False, False

        if (px, py) == goalcell or (px+1, py) == goalcell or (px-1, py) == goalcell:
            gridd.Ball[gkx][goaly] = "B"
            return True, False, True

    # Ball reached end, place at last path cell
    # fx, fy = path[-1]
    # if 0 <= fx < 7 and 0 <= fy < 12:
    #     gridd.Ball[fx][fy] = "B"
    # return False, True, False


# def resolveSTOP(Defender, x, y):
#     cells = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
#     random.shuffle(cells)

#     # Decide likelihood of dropping at feet vs deflecting
#     if Defender.Pos=="G":
#         total = abs(Defender.HAN - Defender.SPD)
#     else:
#         total = abs(Defender.DEF - Defender.PHY)

#     # Prevent divide-by-zero or invalid wheel
#     total = max(1, total)
#     wheel = random.randint(1, total)

#     # 50% chance to keep at feet

#     # Try to deflect to nearest available cell
#     for dx, dy in cells:
#         nx, ny = x + dx, y + dy
#         if 0 <= nx < 7 and 0 <= ny < 12 and gridd.Field[nx][ny].Club==gridd.Field[x][y].Club:
#             gridd.Ball[x][y] = "."  # Clear original
#             gridd.Ball[nx][ny] = "B"
#             return
    
    
#     # Fallback: drop on blocker
#     gridd.Ball[x][y] = "B"


    

def resolveDEF(Attacker, Defender):
    total=Attacker.SHO+Defender.PHY
    wheel=random.randint(1,total)
    if wheel<=Attacker.SHO:
            return True
    else:
        return False

def resolveGK(Attacker, Goalie):
    GoalieStat = int((Goalie.POS + Goalie.REF + Goalie.DIV) / 3)
    total=Attacker.SHO+GoalieStat
    wheel=random.randint(1,total)
    if wheel<=Attacker.SHO:
            return True
    else:
        return False

def Move(x, y):

    player = gridd.Field[x][y]
    # if player.Club != teama or gridd.Ball[x][y] == "B":
    #     return False

    keys = pygame.key.get_pressed()
    qx, qy = x, y

    if keys[pygame.K_UP] and x > 0 and gridd.Field[x-1][y] == ".":
        qx -= 1
    elif keys[pygame.K_DOWN] and x < 6 and gridd.Field[x+1][y] == ".":
        qx += 1
    elif keys[pygame.K_LEFT] and y > 0 and gridd.Field[x][y-1] == ".":
        qy -= 1
    elif keys[pygame.K_RIGHT] and y < 11 and gridd.Field[x][y+1] == ".":
        qy += 1
    elif keys[pygame.K_e] and x > 0 and y < 11 and gridd.Field[x-1][y+1] == ".":
        qx -= 1
        qy += 1
    elif keys[pygame.K_c] and x < 6 and y < 11 and gridd.Field[x+1][y+1] == ".":
        qx += 1
        qy += 1
    elif keys[pygame.K_q] and x > 0 and y > 0 and gridd.Field[x-1][y-1] == ".":
        qx -= 1
        qy -= 1
    elif keys[pygame.K_z] and x < 6 and y > 0 and gridd.Field[x+1][y-1] == ".":
        qx += 1
        qy -= 1

    if (qx, qy) != (x, y):
        gridd.Field[qx][qy] = player
        gridd.Field[x][y] = "."
        return True

    return False



def resolveDRI(Attacker, Defender):
    total=Attacker.DRI+Defender.DEF
    wheel=random.randint(1,total)
    if wheel<=Attacker.DRI:
        return True
    else:
        return False


def Dribble(x, y, teama):

    # if not isinstance(gridd.Field[x][y], Player):
    #     return False

    player = gridd.Field[x][y]
    # if player.Club != teama or gridd.Ball[x][y] != "B":
    #     return False

    # PAC = player.PAC
    # moves = 1
    # if PAC >= 90:
    #     moves = 3
    # elif PAC >= 80:
    #     moves = 2

    keys = pygame.key.get_pressed()
    qx, qy = x, y

    if keys[pygame.K_UP]: qx -= 1
    elif keys[pygame.K_DOWN]: qx += 1
    elif keys[pygame.K_LEFT]: qy -= 1
    elif keys[pygame.K_RIGHT]: qy += 1
    elif keys[pygame.K_e]: qx -= 1; qy += 1
    elif keys[pygame.K_c]: qx += 1; qy += 1
    elif keys[pygame.K_q]: qx -= 1; qy -= 1
    elif keys[pygame.K_z]: qx += 1; qy -= 1


    if (0 <= qx < 7 and 0 <= qy < 12):
        spot = gridd.Field[qx][qy]
        if spot == ".":
            gridd.Field[qx][qy] = player
            gridd.Ball[qx][qy] = "B"
            gridd.Field[x][y] = "."
            gridd.Ball[x][y] = "."
            x, y = qx, qy
            return True, True

        elif isinstance(spot, Player) and spot.Club != teama:
            success =  resolveDRI(player,spot)
            if success:
                gridd.Field[qx][qy] = player
                gridd.Ball[qx][qy] = "B"
                gridd.Field[x][y] = spot
                gridd.Ball[x][y] = "."
                return True, True
            else:
                gridd.Ball[x][y] = "."
                gridd.Ball[qx][qy] = "B"
                return True, False
        elif isinstance(spot, Player) and spot.Club == teama:
            return False, True

    return False, False

def Tackle(x, y, teama):
    player = gridd.Field[x][y]
 
    keys = pygame.key.get_pressed()
    qx, qy = x, y
    if keys[pygame.K_UP]: qx -= 1
    elif keys[pygame.K_DOWN]: qx += 1
    elif keys[pygame.K_LEFT]: qy -= 1
    elif keys[pygame.K_RIGHT]: qy += 1
    elif keys[pygame.K_e]: qx -= 1; qy += 1
    elif keys[pygame.K_c]: qx += 1; qy += 1
    elif keys[pygame.K_q]: qx -= 1; qy -= 1
    elif keys[pygame.K_z]: qx += 1; qy -= 1


    if (0 <= qx < 7 and 0 <= qy < 12):
        spot = gridd.Field[qx][qy]
        if spot == ".":
            gridd.Field[qx][qy] = player
            gridd.Field[x][y] = "."
            x, y = qx, qy
            return True, False


        elif isinstance(spot, Player) and spot.Club != teama:
            attacker = gridd.Field[qx][qy]
            success =  resolveTKL(player,attacker)
            if success:
                gridd.Field[qx][qy] = player
                gridd.Field[x][y] = attacker
                return True, True
            else:
                gridd.Field[qx][qy] = player
                gridd.Field[x][y] = attacker
                gridd.Ball[qx][qy] = "."
                gridd.Ball[x][y] = "B"
                return True, False

    return False, False

def resolveTKL(Defender,Attacker):
    DefStat=random.choice([Defender.PHY,Defender.DEF])
    AttStat=random.choice([Attacker.DRI,Attacker.PHY])
    total=DefStat+AttStat
    wheel=random.randint(1,total)
    if wheel<=DefStat:
        return True
    else:
        return False