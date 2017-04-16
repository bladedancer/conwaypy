import pygame
from button import TextButton, TemplateButton
from stencil import Stencils
from event import PubSub

class SidebarSurface(object):
    def __init__(self, life):
        super().__init__()
        self.font = pygame.font.SysFont("default", 24)
        self.textColor = (255,0,0)
        self.backgroundColor = (69,69,69)
        self.life = life

        self.startButton = TextButton('Start', (10, 10, 150, 50), self.onStart)
        self.stopButton = TextButton('Stop', (10, 10, 150, 50), self.onStop)
        self.clearButton = TextButton('Clear', (10, 80, 150, 25), self.onClear)
        self.randomButton = TextButton('Random', (10, 110, 150, 25), self.onRandomFill)

        self.stencils = [
            TemplateButton('line', ['001','010','100'], lambda: self.selectTool('line'))
        ]

        stencilsDefs = Stencils().stencil
        for name in stencilsDefs:
            but = TemplateButton(name, stencilsDefs[name], lambda name=name: self.selectTool(name))
            self.stencils.append(but)

    def selectTool(self, name):
        PubSub.publish('selecttool', name=name)

    def onStart(self):
        self.life.start()

    def onStop(self):
        self.life.stop()

    def onClear(self):
        self.life.clear()

    def onRandomFill(self):
        self.life.randomFill(20) # TODO INPUT

    def setSurface(self, surface) :
        self.surface = surface
        self.surface.fill(self.backgroundColor)
        self.startButton.setSurface(self.surface)
        self.stopButton.setSurface(self.surface)
        self.clearButton.setSurface(self.surface)
        self.randomButton.setSurface(self.surface)

        top = 180
        left = 0
        prevSize = (0,0)
        sidebarWidth = self.surface.get_rect().width

        for stencil in self.stencils:
            stencil.setSurface(self.surface)

        # Sort stenzils by height and name
        self.stencils.sort(key=lambda stencil: (stencil.rect.height, stencil.name))
        for stencil in self.stencils:
            left = left + prevSize[0] + 10
            if (left + stencil.rect.width > sidebarWidth):
                left = 10
                top = top + prevSize[1] + 10

            stencil.rect.left = left
            stencil.rect.top = top
            prevSize = stencil.rect.size

        self.selectTool('line')

    def update(self, event) :
        self.surface.fill(self.backgroundColor)
        buttons = list()

        for stencil in self.stencils:
            buttons.append(stencil)

        if (self.life.running):
            buttons.append(self.stopButton)
        else:
            buttons.append(self.startButton)
            buttons.append(self.clearButton)
            buttons.append(self.randomButton)

        [but.update(event) for but in buttons]

        text = self.font.render("Generation: " + str(self.life.generation), 1, self.textColor)
        textrect = text.get_rect()
        textrect.left = 10
        textrect.top = self.surface.get_rect().height - 20
        pygame.draw.rect(self.surface, self.backgroundColor, textrect)
        self.surface.blit(text, textrect)
