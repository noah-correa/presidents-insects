from math import sqrt
import pygame

from src.card import Card, CARD_W, CARD_H

BG_COLOUR = (0, 71, 0)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 204, 0)

H1 = 'resources/fonts/casino.3d-filled-marquee-italic.ttf'
H2 = 'resources/fonts/casino.3d-lines-regular.ttf'
N = 'resources/fonts/casino.3d-regular.ttf'

T = 500/15
VELO = (1, 1)

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
    def __init__(self, text, size, position, align=False, font=N):
        self.string = text
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(self.string, 1, BLACK)
        self.rect = get_rect_align(self.text, position, align)

    def draw(self, window, colour=BLACK):
        self.text = self.font.render(self.string, 1, colour)
        window.blit(self.text, self.rect)


# Text Button class
class TextButton():
    def __init__(self, text, size, position, callback, params=None, align='tl', font=N):
        self.string = text
        self.font = pygame.font.Font(font, size)
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

# Image Class
class PlainImage():
    def __init__(self, imgpath, size, position, align='tl'):
        self.img = pygame.transform.scale(pygame.image.load(imgpath), size)
        self.rect = get_rect_align(self.img, position, align)

    def draw(self, window):
        window.blit(self.img, self.rect)


# Image Button class
class ImageButton():
    def __init__(self, image, size, position, callback, params=None, hover=None, align='tl'):
        self.image = pygame.transform.scale(pygame.image.load(image), size)
        if hover is not None:
            self.hover = pygame.transform.scale(pygame.image.load(hover), size)
        self.size = size
        self.rect = get_rect_align(self.image, position, align)
        self.callback = callback
        self.params = params

    def setHover(self, hover):
        self.hover = pygame.transform.scale(pygame.image.load(hover), self.size)

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


# Card Button class
class CardButton():
    def __init__(self, card: Card, position, callback=None, params=None, align='tl'):
        self.card = card
        self.rect = get_rect_align(card.img, position, align)
        self.callback = callback
        self.params = params
        self.startpos = position
        self.curr = position

    def getCard(self):
        return self.card

    def draw(self, window, pos=None):
        #Call this method to draw the button on the screen
        if pos is not None and self.rect.collidepoint(pos):
            window.blit(self.card.img, (self.rect[0], self.rect[1] - CARD_H//8))
        else:
            window.blit(self.card.img, self.rect)
        
    def animate(self, window, position, angle):
        card = pygame.transform.rotate(self.card.img, angle)
        pos = (self.currpos[0] + VELO[0], self.currpos[1] + VELO[1])

        # Draw

        self.currpos = pos


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


class ImageAnimation():
    def __init__(self, img: pygame.Surface, start, target, angle=0):
        self.img = img
        self.target = target
        self.currpos = start
        self.angle = angle
        self.d = int(sqrt((target[0]-start[0])**2 + (target[1]-start[1])**2) * 500/15)
        self.dx = int((target[0]-start[0])/T)
        self.dy = int((target[1]-start[1])/T)

    def update(self, window):
        self.currpos[0] += self.dx
        self.currpos[1] += self.dy
        rect = self.img.get_rect(center=self.currpos)
        surf = pygame.transform.rotate(self.img, self.angle)
        window.blit(surf, rect)
        if self.endpos == self.currpos:
            return True
        return False

