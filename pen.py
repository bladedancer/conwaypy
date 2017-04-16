import pygame, sys
import glob
import os
from pygame.locals import *
from stencil import Stencils
from event import PubSub

class Pen(object):
    def __init__(self, boardSurface):
        self.boardSurface = boardSurface
        self.penDown = False

        self.tools = {
            'line': {'func': 'line'}
        }

        stencils = Stencils().stencil
        for name in stencils:
            self.tools[name] = {
                'func': 'stencil',
                'template': stencils[name]
            }
        self.selectedTool = 'line'
        PubSub.subscribe('selecttool', lambda name : self.selectTool(name))

    def selectTool(self, name):
        self.selectedTool = name

    def stencil(self, e, tool):
        if e.type == pygame.MOUSEBUTTONDOWN:
            pos = self.boardSurface.globalToBoard(e.pos)
            xstart = pos[0]
            pos = (xstart, pos[1])
            points = []
            template = tool['template']
            for line in template:
                for c in list(line) :
                    if (c == '1' or c=='*'):
                        points.append(pos);
                    pos = (pos[0] + self.boardSurface.scale, pos[1])
                pos = (xstart, pos[1] + self.boardSurface.scale)
            self.boardSurface.fill(points)

    def line(self, e, tool):
        if e.type == pygame.MOUSEBUTTONDOWN:
            pos = self.boardSurface.globalToBoard(e.pos)
            self.lastPos = pos
            self.penDown = True
        elif e.type == pygame.MOUSEBUTTONUP:
            pos = self.boardSurface.globalToBoard(e.pos)
            self.boardSurface.fill([pos])
            self.penDown = False
        elif e.type == pygame.MOUSEMOTION:
            if self.penDown:
                pos = self.boardSurface.globalToBoard(e.pos)
                self.boardSurface.fill(self.getPoints(self.lastPos, pos))
                self.lastPos = pos

    def update(self, e):
        if e is None or not hasattr(e, 'pos') or not self.boardSurface.contains(e.pos):
            return
        # Handle draw event
        tool = self.tools[self.selectedTool]
        toolFn = getattr(self, tool['func'])
        toolFn(e, tool)

    def getPoints(self, posA, posB) :
        points = []

        if (posB[0] - posA[0]) != 0 :
            m = (posB[1] - posA[1]) / (posB[0] - posA[0])
            fy = lambda x: (m * (x-posA[0])) + posA[1]
            fx = lambda y: ((y-posA[1])/m) + posA[0]
            for x in range(posA[0], posB[0], 1 if posA[0] < posB[0] else -1):
                points.append((x, int(fy(x))))

            if (m !=0):
                for y in range(posA[1], posB[1], 1 if posA[1] < posB[1] else -1):
                    points.append((int(fx(y)), y))
        else:
            for y in range(posA[1], posB[1], 1 if posA[1] < posB[1] else -1):
                points.append((posA[0], y))

        return points
