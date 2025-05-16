import gridd
from player import Player


def getball():
    for x in range(7):
        for y in range(12):
            if gridd.Ball[x][y] == "B":
                return (x, y)
    return None


def getteam(club):
    return [
        (x, y, p)
        for x, row in enumerate(gridd.Field)
        for y, p in enumerate(row)
        if isinstance(p, Player) and p.Club == club
    ]

