import formtact
import gridd
import interface
import player
import tact
import aitact
import pygame
import helper
import movement
import mm_ai
from player import Player

def run_ai_turn(teamb, teama, at1, at2, poss):
    pygame.time.delay(1500)
    poss = mm_ai.play(teamb, teama, poss)
    pygame.time.delay(500)
    aitact.calltact(at1, at2, poss, teamb)
    return poss


def main():
    pygame.init()
    clock = pygame.time.Clock()
    player.scrape() # Scraping fucntion that extracts player stats from FUTWIZ.com
    ClubA, ClubB, formA, formB, ht1, ht2, at1, at2 = formtact.preplay()
    gridd.init_rosters()

    def clubncolor(club):
        if club == "A":
            return "RM", "White"
        elif club == "B":
            return "LIV", "Red"
        else:
            return None, None

    teama, colora = clubncolor(ClubA)
    teamb, colorb = clubncolor(ClubB)

    gridd.setteamA(ClubA)
    gridd.setteamB(ClubB)
    gridd.set_form(formA, ClubA, True)
    gridd.set_form(formB, ClubB, False)
    gridd.kickoff()

    turn = True  # True = Player turn / False = AI turn
    poss = True  # True = Player has possesion / False = AI has possesion

    screen = pygame.display.set_mode((1200, 840))
    pygame.display.set_caption("Football Grid")
    running = True
    selected_cell = None
    menu_open = False
    passing = False
    pass_open = False
    pass_options = []
    pass_origin = ()
    shooting = dribbling = tackling = moving = goal = False
    delay = None
    grid_x = grid_y = 0

    while running:
        bx, by=helper.getball()
        pl=gridd.Field[bx][by]
        if isinstance(pl,Player):
            if pl.Club==teama:
                poss=True
            else:
                poss=False
                

        if turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    grid_x = mouse_pos[1] // 120
                    grid_y = mouse_pos[0] // 100
                    player_obj = gridd.Field[grid_x][grid_y]
                    if isinstance(player_obj, Player) and player_obj.Club == teama:
                        if selected_cell == (grid_x, grid_y) and menu_open:
                            menu_open = False
                            selected_cell = None
                        else:
                            selected_cell = (grid_x, grid_y)
                            menu_open = True
                    else:
                        selected_cell = None
                        menu_open = False

                elif event.type == pygame.KEYDOWN and menu_open:
                    if pygame.K_1 <= event.key <= pygame.K_5:
                        action = event.key
                        if action == pygame.K_1:
                            passing = True
                            pass_origin = (grid_x, grid_y)
                            pass_options = movement.passoptions(grid_x, grid_y, teama)
                            pass_open = True
                            menu_open = False
                            selected_cell = None
                        elif action == pygame.K_2:
                            dribbling = True
                        elif action == pygame.K_3:
                            shooting = True
                        elif action == pygame.K_4:
                            moving = True
                        elif action == pygame.K_5:
                            tackling = True

                elif event.type == pygame.KEYDOWN and pass_open:
                    done, poss = movement.Pass(pass_origin[0], pass_origin[1], pass_options)
                    if done:
                        passing = False
                        pass_open = False
                        pass_options = []
                        pass_origin = ()
                        pygame.time.delay(200)
                        tact.calltact(ht1,ht2,poss,teama)
                        pygame.time.delay(500)
                        aitact.calltact(at1,at2,poss,teamb)
                        turn = False

            if moving:
                done = movement.Move(grid_x, grid_y)
                if done:
                    moving = False
                    pygame.time.delay(200)
                    tact.calltact(ht1,ht2,poss,teama)
                    pygame.time.delay(500)
                    aitact.calltact(at1,at2,poss,teamb)
                    turn = False
            elif shooting:
                done, poss, scored = movement.Shoot(grid_x, grid_y, teama)
                if done:
                    shooting = False
                    pygame.time.delay(200)
                    tact.calltact(ht1,ht2,poss,teama)
                    pygame.time.delay(500)
                    aitact.calltact(at1,at2,poss,teamb)
                    turn = False
                if scored:
                    delay = pygame.time.get_ticks()
                    goal = True
            elif dribbling:
                done, poss = movement.Dribble(grid_x, grid_y, teama)
                if done:
                    dribbling = False
                    pygame.time.delay(200)
                    tact.calltact(ht1,ht2,poss,teama)
                    pygame.time.delay(500)
                    aitact.calltact(at1,at2,poss,teamb)
                    turn = False
            elif tackling:
                done, poss = movement.Tackle(grid_x, grid_y, teama)
                if done:
                    tackling = False
                    pygame.time.delay(200)
                    tact.calltact(ht1,ht2,poss,teama)
                    pygame.time.delay(500)
                    aitact.calltact(at1,at2,poss,teamb)
                    turn = False

        else:
            poss = run_ai_turn(teamb, teama, at1, at2, poss)
            pygame.time.delay(200)
            tact.calltact(ht1, ht2, poss, teama)
            pygame.time.delay(500)
            aitact.calltact(at1, at2, poss, teamb)
            turn = True


        # DRAW
        screen.fill((0, 0, 0))
        interface.startgame(screen, teama, teamb, colora, colorb)
        if menu_open and not dribbling:
            movement.actionmenu(screen, grid_x, grid_y, poss, teama)
        if pass_open:
            movement.passmenu(screen, pass_origin[0], pass_origin[1], pass_options, teama)
        pygame.display.flip()
        clock.tick(60)

        if delay and goal:
            if pygame.time.get_ticks() - delay > 2000:
                gridd.Ball[3][0] = "."
                gridd.Ball[3][11] = "."
                gridd.reset(True)
                delay = None
                goal = False
                turn = True

    pygame.quit()

if __name__ == "__main__":
    main()
