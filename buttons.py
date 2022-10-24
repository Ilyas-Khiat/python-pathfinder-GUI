import pygame
from pygame.locals import *
import pygame.freetype


# suface element that switch between 2 images
class object:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.img = image
        self.state = 0

    def draw(self, screen):
        if self.state == 1:
            screen.blit(self.img[0], (self.x, self.y))
        if self.state == -1:
            screen.blit(self.img[1], (self.x, self.y))


# button displayed as 3 images
class button_i():

    def __init__(self, x, y, w, h, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = img
        self.click = False

    def draw_button(self, screen):

        action = False

        pos = pygame.mouse.get_pos()

        button_rect = Rect(self.x, self.y, self.w, self.h)

        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                screen.blit(self.img[1], (self.x, self.y))
            elif pygame.mouse.get_pressed()[0] == 0 and self.click == True:
                self.click = False
                action = True
            else:
                screen.blit(self.img[2], (self.x, self.y))
        else:
            screen.blit(self.img[0], (self.x, self.y))

        return action


# buttons sustain when clicked
clicks = [[False] * 4, [False] * 8]


class button_s():

    def __init__(self, x, y, w, h, img, n, m):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = img
        self.n = n
        self.m = m

    def draw_button(self, screen):
        global clicks
        action = False

        button_rect = Rect(self.x, self.y, self.w, self.h)

        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1:
            if button_rect.collidepoint(pos):
                for i in range(len(clicks[self.m])):
                    clicks[self.m][i] = False
                clicks[self.m][self.n] = True

        screen.blit(self.img[1], (self.x, self.y)) if clicks[self.m][self.n] else screen.blit(self.img[0],
                                                                                              (self.x, self.y))

        if button_rect.collidepoint(pos) and clicks[self.m][self.n] != True:
            screen.blit(self.img[2], (self.x, self.y))

        return action
