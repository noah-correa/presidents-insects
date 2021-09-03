import pygame

from src.card import Card, CARD_W, CARD_H

BG_COLOUR = (0, 71, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 204, 0)

H1 = 'resources/fonts/casino.3d-filled-marquee-italic.ttf'
H2 = 'resources/fonts/casino.3d-lines-regular.ttf'
N = 'resources/fonts/casino.3d-regular.ttf'


# Finds rectangle alignment
def get_rect_align(s: pygame.Surface, position: tuple[int,int], align: str):
    if align == 'tl':
        return s.get_rect(topleft=position)
    elif align == 'tl':
        return s.get_rect(topleft=position)
    elif align == 'c':
        return s.get_rect(center=position)
    elif align == 'br':
        return s.get_rect(bottomright=position)
    elif align == 'bl':
        return s.get_rect(bottomleft=position)



# Plain Text class
class PlainText():
    def __init__(self, text, size, position, align=False, font='N'):
        self.string = text
        self.font = pygame.font.Font(eval(font), size)
        self.text = self.font.render(self.string, 1, BLACK)
        self.rect = get_rect_align(self.text, position, align)

    def draw(self, window):
        window.blit(self.text, self.rect)


# Text Button class
class TextButton():
    def __init__(self, text, size, position, callback, params=None, align='tl', font='N'):
        self.string = text
        self.font = pygame.font.Font(eval(font), size)
        self.text = self.font.render(self.string, 1, BLACK)
        self.rect = get_rect_align(self.text, position, align)
        self.callback = callback
        self.params = params

    def draw(self, window, pos=None):
        if pos is not None and self.rect.collidepoint(pos):
            text = self.font.render(self.string, 1, WHITE)
            window.blit(text, self.rect)
        else:
            text = self.font.render(self.string, 1, BLACK)
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


# Card Button class
class CardButton():
    def __init__(self, card: Card, position, callback=None, params=None, align='tl'):
        self.card = card
        self.rect = get_rect_align(card.img, position, align)
        self.callback = callback
        self.params = params

    def getCard(self):
        return self.card

    def draw(self, window, pos=None):
        #Call this method to draw the button on the screen
        if pos is not None and self.rect.collidepoint(pos):
            window.blit(self.card.img, (self.rect[0], self.rect[1] - CARD_H//8))
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


# Image Button class
class ImageButton():
    def __init__(self, image, size, position, callback, params=None, hover=None, align='tl'):
        self.image = pygame.transform.scale(pygame.image.load(image), size)
        self.hover = pygame.transform.scale(pygame.image.load(hover), size)
        self.size = size
        self.rect = get_rect_align(self.image, position, align)
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
