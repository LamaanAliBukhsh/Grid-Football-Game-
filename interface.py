import pygame
import gridd
from player import Player
from player import Goalie

clock = pygame.time.Clock()

def startgame(screen, teama, teamb, colora, colorb):
    BALL = (64, 224, 208)
    WHITE = (225, 225, 225)
    WHITE_2 = (33, 41, 48)
    BLACK = (25, 25, 25)
    GREEN = (0, 128, 0)
    RED = (255, 0, 0)
    RED_2 = (225, 50, 150)
    BLUE = (0, 0, 255)
    BLUE_2 = (110, 50, 225)
    
    def kit(colorx):
        if colorx == "White":
            return WHITE, WHITE_2
        elif colorx == "Red":
            return RED, RED_2
        else:
            return None, None
    
    homekit, homegk = kit(colora)
    awaykit, awaygk = kit(colorb)
    
    pygame.display.set_caption("Football gridd")

    def draw_gridd():
        screen.fill(GREEN)
        for x in range(0, 1200, 100):
            for y in range(0, 840, 120):
                rect = pygame.Rect(x, y, 100, 120)
                pygame.draw.rect(screen, BALL, rect, 1)
        draw_players()

    def draw_players():
        font = pygame.font.SysFont('helvetica', 14)
        gfont = pygame.font.SysFont('helvetica', 20)
        for x in range(0,7):
            for y in range(0,12):
                center_x = y * 100 + 50
                center_y = x * 120 + 60
                if gridd.selected_player == (x, y):
                    pygame.draw.circle(screen, (255, 255, 0), (center_x, center_y), 30) 
                if isinstance(gridd.Field[x][y], Player) and (gridd.Field[x][y].Club==teama):
                    pygame.draw.circle(screen, homekit, (center_x, center_y), 25)
                    text = font.render(gridd.Field[x][y].Name, True, (0, 0, 0))
                    text_rect = text.get_rect(center=(center_x, center_y))
                    screen.blit(text, text_rect)
                elif isinstance(gridd.Field[x][y], Player) and (gridd.Field[x][y].Club==teamb):
                    pygame.draw.circle(screen, awaykit, (center_x, center_y), 25)
                    text = font.render(gridd.Field[x][y].Name, True, (0, 0, 0))
                    text_rect = text.get_rect(center=(center_x, center_y))
                    screen.blit(text, text_rect)
                elif isinstance(gridd.Field[x][y], Goalie) and (gridd.Field[x][y].Club==teama):
                    pygame.draw.circle(screen, homegk, (center_x, center_y), 25)
                    text = font.render(gridd.Field[x][y].Name, True, (0, 0, 0))
                    text_rect = text.get_rect(center=(center_x, center_y))
                    screen.blit(text, text_rect)
                elif isinstance(gridd.Field[x][y], Goalie) and (gridd.Field[x][y].Club==teamb):
                    pygame.draw.circle(screen, awaygk, (center_x, center_y), 25)
                    text = font.render(gridd.Field[x][y].Name, True, (0, 0, 0))
                    text_rect = text.get_rect(center=(center_x, center_y))
                    screen.blit(text, text_rect)
                elif gridd.Field[x][y]=="X":
                    rect = pygame.Rect(y * 100, x * 120, 100, 120)
                    pygame.draw.rect(screen, BLACK, rect)
                elif isinstance(gridd.Field[x][y], str) and gridd.Field[x][y].isdigit():
                    text = gfont.render(gridd.Field[x][y], True, BALL)
                    text_rect = text.get_rect(center=(center_x, center_y))
                    screen.blit(text, text_rect)
                if gridd.Ball[x][y]=="B":
                    pygame.draw.circle(screen, BLACK, (center_x, center_y), 14)
                    pygame.draw.circle(screen, BALL, (center_x, center_y), 10)
                
    
    draw_gridd()
