import pygame

WINDOW_W = 1600
WINDOW_H = 900
BG_COLOUR = (0, 71, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 204, 0)

# Returns text surface and rectangle
def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

# Returns default text with varying size
def load_text(size) -> pygame.font:
    return pygame.font.Font('freesansbold.ttf', size)

class Button():
    def __init__(self, win, x, y, size, text=''):
        self.window = win
        self.over = False
        self.x = x
        self.y = y
        self.text = text
        self.size = int(size * 0.8)
        font = load_text(self.size)
        txt = font.render(self.text, 1, (0, 0, 0))
        self.width = txt.get_width()
        self.height = txt.get_height()

    def draw(self, pos=None):

        if self.text != '':
            font = load_text(self.size)
            if pos is not None:
                self.isOver(pos)
            if self.over:
                # font = load_text(int(self.size * 1.2))
                text = font.render(self.text, 1, WHITE)
                # win.blit(text, (self.x + self.width//2 - text.get_width()//2, self.y + self.height//2 - text.get_height()//2))
                # win.blit(text, (self.x, self.y))
            else:
                text = font.render(self.text, 1, BLACK)
            self.window.blit(text, (self.x, self.y))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                self.over = True
                return True
        self.over = False
        return False


class CardButton():
    def __init__(self, win, card, x, y):
        self.window = win
        self.card = card
        self.x = x
        self.y = y
        self.w = 115
        self.h = 176
        self.over = 0

    def getCard(self):
        return self.card

    def draw(self, pos=None):
        #Call this method to draw the button on the screen
        if pos is not None:
            self.isOver(pos)
        if self.over:
            # pygame.draw.rect(win, YELLOW, (self.x - 2, self.y - 2, self.w + 4, self.h + 4), 0)
            self.window.blit(self.card.img, (self.x, self.y - 176//8))
        else:
            self.window.blit(self.card.img, (self.x, self.y))


    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                self.over = True
                return True
        self.over = False
        return False
