import pygame
from pygame.locals import *
from util import AAfilledRoundedRect
from event import PubSub

class Button(object):
    def __init__(self, operation):
        self.font = pygame.font.SysFont("default", 24)
        self.operation = operation

    def setSurface(self, surface):
        self.surface = surface
        self.paint()

    def onButton(self):
        onButton = False
        mousePos = pygame.mouse.get_pos()
        offset = self.surface.get_abs_offset()
        if self.rect.collidepoint((mousePos[0]-offset[0], mousePos[1]-offset[1])):
            onButton = True
        return onButton

    def paint(self):
        pass

    def update(self, event):
        if event is not None and event.type == pygame.MOUSEBUTTONDOWN:
            if self.onButton():
                self.operation()


class TextButton(Button):
    def __init__(self, value, rect, operation, color = (212,212,212), activeColor = (178, 178, 178), textColor = (0,0,0)):
        super().__init__(operation)
        self.value = value
        self.rect = pygame.Rect(rect)
        self.color = color
        self.activeColor = activeColor
        self.textColor = textColor

    def drawButton(self, color):
        rect = pygame.Rect(0,0,self.rect.width, self.rect.height)
        button = pygame.Surface((rect.width, rect.height), SRCALPHA)
        button.fill((0,0,0,0))
        AAfilledRoundedRect(button, rect, pygame.Color("black"), 0.5)
        butRect = AAfilledRoundedRect(button, rect.inflate(-4, -4), color, 0.5)
        text = self.font.render(self.value, True, self.textColor)
        textrect = text.get_rect(center = (butRect.x + rect.width/2, butRect.y + rect.height/2))
        button.blit(text, textrect)
        return button

    def paint(self):
        self.buttonPassive = self.drawButton(self.color)
        self.buttonActive = self.drawButton(self.activeColor)

    def update(self, event):
        super(TextButton, self).update(event)
        button = self.buttonActive if self.onButton() else self.buttonPassive
        self.surface.blit(button, self.rect)


class TemplateButton(Button):
    def __init__(self, name, template, operation):
        super().__init__(operation)
        self.name = name
        self.template = template
        self.rect = pygame.Rect(0,0,0,0)

    def drawButton(self, fillColor):
        size = 4
        width = 0
        height = (len(self.template) + 2) * size

        for line in self.template:
            width = max((len(line) + 2) * size, width)

        rect = pygame.Rect(0, 0, width, height)
        button = pygame.Surface((rect.width, rect.height))
        button.fill(fillColor)
        self.rect = pygame.Rect(self.rect.topleft, rect.size)

        x = size
        y = 0
        for line in self.template:
            y = y + size
            x = 0
            for c in list(line) :
                x = x + size
                if (c == '1' or c=='*'):
                    pygame.draw.rect(button, pygame.Color('black'), (x, y, size, size))
        return button

    def paint(self):
        self.buttonPassive = self.drawButton(pygame.Color('white'))
        self.buttonSelected = self.drawButton((120,120,255))
        self.current = self.buttonPassive

        PubSub.subscribe('selecttool', lambda name : self.selectTool(name))

    def selectTool(self, name):
        if (name == self.name):
            self.current = self.buttonSelected
        else:
            self.current = self.buttonPassive

    def update(self, event):
        super(TemplateButton, self).update(event)
        self.surface.blit(self.current, self.rect)
