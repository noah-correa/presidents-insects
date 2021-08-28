"""
main.py for Presidents and Insects Python Card Game
Noah Correa
"""
import sys
import pygame

from game import Game
from buttons import *





pygame.init()

window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
window.fill(BG_COLOUR)
pygame.display.set_caption("Presidents and Insects")
pygame.display.set_icon(pygame.image.load('images/cockroach.png'))
pygame.display.update()


# Main menu screen
def game_intro():

    b_play = button(BG_COLOUR, WINDOW_W//2-300, 2*WINDOW_H//3, 200, 100, 'Play')
    b_rules = button(BG_COLOUR, WINDOW_W//2+100, 2*WINDOW_H//3, 200, 100, 'Rules')

    run = True
    while run:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_play.isOver(pos):
                    singleplayer_number()
                    run = False
                if b_rules.isOver(pos):
                    rules()
                    run = False
            if event.type == pygame.MOUSEMOTION:
                b_play.hover(pos)
                b_rules.hover(pos)


        window.fill(BG_COLOUR)
        text = load_text(100)
        title, title_rect = text_objects("Presidents and Insects", text, BLACK)
        title_rect.center = ((WINDOW_W // 2), (WINDOW_H // 2))
        window.blit(title, title_rect)

        main_image = pygame.transform.scale(pygame.image.load("images/cockroach.png"), (151*2, 191*2))
        window.blit(main_image, (WINDOW_W // 2 - 151, WINDOW_H // 3 - 275))

        b_play.draw(window)
        b_rules.draw(window)

        pygame.display.update()
        pygame.time.delay(15)

    quit_game()

# Choose total number of players screen
def singleplayer_number():

    b_back = button(BG_COLOUR, 0, WINDOW_H - 100, 200, 100, 'Back')
    b_5 = button(BG_COLOUR, WINDOW_W // 2 - 200, WINDOW_H // 2, 100, 100, '5')
    b_6 = button(BG_COLOUR, WINDOW_W // 2 - 50, WINDOW_H // 2, 100, 100, '6')
    b_7 = button(BG_COLOUR, WINDOW_W // 2 + 100, WINDOW_H // 2, 100, 100, '7')

    run = True
    while run:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_back.isOver(pos):
                    game_intro()
                    run = False
                if b_5.isOver(pos):
                    loading_screen(5)
                    run = False
                if b_6.isOver(pos):
                    loading_screen(6)
                    run = False
                if b_7.isOver(pos):
                    loading_screen(7)
                    run = False
            if event.type == pygame.MOUSEMOTION:
                b_back.hover(pos)
                b_5.hover(pos)
                b_6.hover(pos)
                b_7.hover(pos)

        window.fill(BG_COLOUR)

        text = load_text(50)
        title, title_rect = text_objects("Choose total number of players", text, BLACK)
        title_rect.center = ((WINDOW_W // 2), (WINDOW_H // 3))
        window.blit(title, title_rect)

        b_back.draw(window)
        b_5.draw(window)
        b_6.draw(window)
        b_7.draw(window)

        pygame.display.update()
        pygame.time.delay(15)

    quit_game()

# Rules screen
def rules():

    b_back = button(BG_COLOUR, 0, WINDOW_H - 100, 200, 100, 'Back')

    run = True
    while run:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_back.isOver(pos):
                    game_intro()
                    run = False

            if event.type == pygame.MOUSEMOTION:
                b_back.hover(pos)

        window.fill(BG_COLOUR)
        b_back.draw(window)

        pygame.display.update()
        pygame.time.delay(15)

    quit_game()


def loading_screen(total):
    window.fill(BG_COLOUR)
    text = load_text(50)
    title, title_rect = text_objects("LOADING", text, BLACK)
    title_rect.center = ((WINDOW_W // 2), (WINDOW_H // 3))
    window.blit(title, title_rect)
    pygame.display.update()
    pygame.time.delay(500)
    game = Game(1, total)
    pygame.time.delay(500)
    game_loop(game)

# Game screen
def game_loop(game):
    b_back = button(BG_COLOUR, 0, WINDOW_H - 100, 200, 100, 'Back')
    game.newGame()
    run = True
    while run:
        window.fill(BG_COLOUR)
        pos = pygame.mouse.get_pos()
        b_back.draw(window)
        player = game.players[game.getPlayerId("Player 1")]
        p_hand = draw_player_hand(window, pos, player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_back.isOver(pos):
                    run = False
                    game_intro()
                for i, card in enumerate(p_hand):
                    if card.isOver(pos):
                        player.addCardMove(i)
                        draw_player_move(window, pos, player)
                        # draw_player_hand(window, pos, player)

            if event.type == pygame.MOUSEMOTION:
                b_back.hover(pos)
                for i, card in enumerate(p_hand):
                    if card.isOver(pos):
                        draw_player_hand(window, pos, player)

        pygame.display.update()
        pygame.time.delay(15)

    quit_game()




def draw_player_hand(win, pos, player):
    ret = []
    start = WINDOW_W//2 - 115 * len(player.hand)//2
    for i, card in enumerate(player.hand):
        card = card_button(player.hand[i])
        card.draw(win, pos, start + 115 * i, WINDOW_H - 176//2)
        ret.append(card)
            
    return ret

def draw_player_move(win, pos, player):
    card = card_button(player.move[0])
    card.draw(win, pos, WINDOW_W//2 - 115//2, WINDOW_H - 176 - 25)

# Quit game
def quit_game():
    pygame.quit()
    sys.exit()
    # quit()


game_intro()
quit_game()
