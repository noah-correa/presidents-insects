import pygame
import os.path

import pygame
import pygame.locals as pl

from src.card import Card, CARD_W, CARD_H

pygame.font.init()


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
        self.img = pygame.transform.scale(pygame.image.load(imgpath).convert_alpha(), size)
        self.rect = get_rect_align(self.img, position, align)

    def draw(self, window):
        window.blit(self.img, self.rect)


# Image Button class
class ImageButton():
    def __init__(self, image, size, position, callback, params=None, hover=None, align='tl'):
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), size)
        if hover is not None:
            self.hover = pygame.transform.scale(pygame.image.load(hover).convert_alpha(), size)
        self.size = size
        self.rect = get_rect_align(self.image, position, align)
        self.callback = callback
        self.params = params

    def setHover(self, hover):
        self.hover = pygame.transform.scale(pygame.image.load(hover).convert_alpha(), self.size)

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

# Textbox Class
class TextInput:
    def __init__(
            self,
            size,
            position,
            initial_string="",
            font_family=N,
            antialias=True,
            colour=BLACK,
            max_string_length=-1):
        """
        :param position: Postiion of the text box on the screen
        :param initial_string: Initial text to be displayed
        :param font_size:  Size of font in pixels
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :param text_color: Color of text
        :param max_string_length: Allowed length of text
        """

        # Text related vars:
        self.position = position
        self.antialias = antialias
        self.text_color = colour
        self.font_size = size[1] - 5
        self.length = size[0]
        self.max_string_length = max_string_length
        self.input_string = initial_string  # Inputted text
        self.rect = pygame.Rect(self.position[0]-self.length//2, self.position[1]-(self.font_size+5)//2, self.length, self.font_size+5)

        self.font_object = pygame.font.Font(font_family, self.font_size)

        # Text-surface will be created during the first update call:
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = 400
        self.keyrepeat_interval_ms = 35

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size / 20 + 1), self.font_size))
        self.cursor_surface.fill((0, 0, 1))
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  # /|\
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def draw(self, window):
        pygame.draw.rect(window, WHITE, self.rect, width=0)
        pygame.draw.rect(window, BLACK, self.rect, width=3)
        rect = self.surface.get_rect(center=self.position)
        if self.input_string != "":
            self.surface = self.font_object.render(self.input_string, self.antialias, self.text_color)

        window.blit(self.surface, rect)

    def onClick(self, event):
        return event.button == 1 and self.rect.collidepoint(event.pos)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if event.key not in self.keyrepeat_counters:
                    if not event.key == pl.K_RETURN: # Filters out return key, others can be added as necessary
                        self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pl.K_BACKSPACE:
                    self.input_string = (
                        self.input_string[:max(self.cursor_position - 1, 0)]
                        + self.input_string[self.cursor_position:]
                    )

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == pl.K_DELETE:
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + self.input_string[self.cursor_position + 1:]
                    )

                elif event.key == pl.K_RETURN:
                    return True

                elif event.key == pl.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                elif event.key == pl.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pl.K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == pl.K_HOME:
                    self.cursor_position = 0

                elif len(self.input_string) < self.max_string_length or self.max_string_length == -1:
                    if event.unicode.isalpha() or event.unicode.isdigit() or event.unicode == ':' or event.unicode == '.':
                        # If no special key is pressed, add unicode of key to input_string
                        # print(type(event.unicode), event.unicode)
                        self.input_string = (
                            self.input_string[:self.cursor_position]
                            + event.unicode
                            + self.input_string[self.cursor_position:]
                        )
                        self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

            elif event.type == pl.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

        # Update key counters:
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = (
                    self.keyrepeat_intial_interval_ms
                    - self.keyrepeat_interval_ms
                )

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(pygame.event.Event(pl.KEYDOWN, key=event_key, unicode=event_unicode))

        self.surface = self.font_object.render(self.input_string, self.antialias, self.text_color)

        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.cursor_position > 0:
                cursor_y_pos -= self.cursor_surface.get_width()
            self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))

        self.clock.tick()
        return False

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string = ""
        self.cursor_position = 0

