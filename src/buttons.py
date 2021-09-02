import pygame

from src.card import Card

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

class TextButton():
    def __init__(self, text, size, position, callback, params=None, center=False):
        self.text = text
        self.size = size
        font = load_text(self.size)
        txt = font.render(self.text, 1, BLACK)
        self.rect = txt.get_rect(topleft=position)
        if center:
            self.rect = txt.get_rect(center=position)
        self.callback = callback
        self.params = params

    def draw(self, window, pos=None):
        font = load_text(self.size)
        if pos is not None and self.rect.collidepoint(pos):
            text = font.render(self.text, 1, WHITE)
            window.blit(text, self.rect)
        else:
            text = font.render(self.text, 1, BLACK)
            window.blit(text, self.rect)

    def onClick(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback is None:
                    return True
                if self.params is None:
                    self.callback()
                    return False
                else:
                    self.callback(self.params)
                    return False


class CardButton():
    def __init__(self, card: Card, position, callback=None, params=None):
        self.card = card
        self.rect = card.img.get_rect(topleft=position)
        self.callback = callback
        self.params = params

    def getCard(self):
        return self.card

    def draw(self, window, pos=None):
        #Call this method to draw the button on the screen
        if pos is not None and self.rect.collidepoint(pos):
            window.blit(self.card.img, (self.rect[0], self.rect[1] - 176//8))
        else:
            window.blit(self.card.img, self.rect)

    def onClick(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback is None:
                    return True
                if self.params is None:
                    self.callback()
                    return False
                else:
                    self.callback(self.params)
                    return False


class ImageButton():
    def __init__(self, image, size, position, callback, params=None, hover=None):
        self.image = pygame.transform.scale(pygame.image.load(image), size)
        self.hover = pygame.transform.scale(pygame.image.load(hover), size)
        self.size = size
        self.rect = self.image.get_rect(topleft=position)
        self.callback = callback
        self.params = params

    def draw(self, window, pos=None):
        if pos is not None and self.rect.collidepoint(pos) and self.hover is not None:
            window.blit(self.hover, self.rect)
        else:
            window.blit(self.image, self.rect)

    def onClick(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback is None:
                    return True
                if self.params is None:
                    self.callback()
                    return False
                else:
                    self.callback(self.params)
                    return False


class PlainText():
    def __init__(self, text, size, position, center=False):
        self.text = text
        self.size = size
        font = load_text(self.size)
        txt = font.render(self.text, 1, BLACK)
        self.rect = txt.get_rect(topleft=position)
        if center:
            self.rect = txt.get_rect(center=position)

    def draw(self, window):
        font = load_text(self.size)
        text = font.render(self.text, 1, BLACK)
        window.blit(text, self.rect)
