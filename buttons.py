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
def load_text(size):
    return pygame.font.Font('freesansbold.ttf', size)

class Button():
    def __init__(self, colour, x, y, width, height, text=''):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = load_text(60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width // 2 - text.get_width() // 2), self.y + (self.height // 2 - text.get_height() // 2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

    def hover(self, pos):
        if self.isOver(pos):
            self.colour = WHITE
        else:
            self.colour = BG_COLOUR

class CardButton():
    def __init__(self, card):
        self.card = card
        self.x = None
        self.y = None
        self.w = 115
        self.h = 176
        self.outline = 0


    def getCard(self):
        return self.card

    def draw(self, win, pos, x, y):
        #Call this method to draw the button on the screen
        self.x = x
        self.y = y
        self.hover(pos)
        if self.outline:
            pygame.draw.rect(win, YELLOW, (self.x - 2, self.y - 2, self.w + 4, self.h + 4), 0)
        win.blit(self.card.img, (self.x, self.y))


    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
        return False

    def hover(self, pos):
        self.outline = 1 if self.isOver(pos) else 0
