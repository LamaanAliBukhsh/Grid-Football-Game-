import pygame
import random
import gridd
import helper
from player import Player
import ai_mov

def play(teamb, teama, poss):
    bestact = MinMax(teamb, teama, poss)[1]
    if bestact:
        return doact(bestact, teamb)
    return True

def MinMax(teamb, teama, poss, maximizing=True):
    Team= helper.getteam(teamb if maximizing else teama)
    bestscore = float('-inf') if maximizing else float('inf')
    bestact = None

    all_act = []
    for x, y, p in Team:
        actions = getact(x, y, p, teamb, teama, poss)
        for action in actions:
            score = evalact(action)
            all_act.append((score, action))

    all_act.sort(reverse=maximizing)

    for score, action in all_act[:3]:
        reactscore = 0
        reactions = sim_react(action, teama if maximizing else teamb)
        if reactions:
            reactscore = evalact(reactions[0])

        tscore = score - 0.5 * reactscore if maximizing else score + 0.5 * reactscore

        if maximizing and tscore > bestscore:
            bestscore = tscore
            bestact = action
        elif not maximizing and tscore < bestscore:
            bestscore = tscore
            bestact = action

    return bestscore, bestact

def sim_react(action, oppteam):
    bx, by = helper.getball()
    reactions = []
    if action[0] == "pass" or action[0] == "dribble":
        reactions.append(("shoot", bx, by))
        reactions.append(("dribble", bx, by))
    elif action[0] == "move":
        reactions.append(("move", bx, by, bx + 1, by))
    return reactions

def evalact(action):
    kind = action[0]
    if kind == "shoot":
        x, y = action[1], action[2]
        gx, gy = 3, 1
        dist = abs(x - gx) + abs(y - gy)
        return max(0, 100 - dist * 15)
    elif kind == "pass":
        x1, y1, x2, y2 = action[1], action[2], action[3], action[4]
        dist = abs(x1 - x2) + abs(y1 - y2)
        return 50 - dist * 2
    elif kind == "dribble":
        return 40
    elif kind == "tackle":
        return 45
    elif kind == "move":
        return 25
    return 0

def getact(x, y, player, teamb, teama, poss):
    actions = []
    if not isinstance(gridd.Field[x][y], Player):
        return actions

    has_ball = gridd.Ball[x][y] == "B"
    bx, by = helper.getball()
    team_poss = gridd.Field[bx][by].Club == teamb if isinstance(gridd.Field[bx][by], Player) else False

    if has_ball and team_poss:
        actions.append(("shoot", x, y))
        Team= helper.getteam(teamb)
        for tx, ty, p in Team:
            if (tx, ty) != (x, y):
                actions.append(("pass", x, y, tx, ty))
        actions.append(("dribble", x, y))
    elif not has_ball and team_poss:
        for dx, dy in [(0, 1), (1, 1), (-1, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 7 and 0 <= ny < 12 and gridd.Field[nx][ny] == ".":
                actions.append(("move", x, y, nx, ny))
    elif not has_ball:
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 7 and 0 <= ny < 12 and gridd.Field[nx][ny] == ".":
                actions.append(("move", x, y, nx, ny))
    return actions

def doact(action, teamb):
    pygame.time.delay(200)
    kind = action[0]
    if kind == "shoot":
        _, x, y = action
        done, poss, scored = ai_mov.Shoot(x, y, teamb)
        return poss
    elif kind == "pass":
        _, x, y, tx, ty = action
        done, poss, lost = ai_mov.Pass(x, y, [(tx, ty)])
        return not lost
    elif kind == "dribble":
        _, x, y = action
        done, poss, lost = ai_mov.Dribble(x, y, teamb)
        return not lost
    elif kind == "move":
        _, x, y, nx, ny = action
        ai_mov.Move(x, y)
        return True
    return True