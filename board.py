import pygame, sys, random
from pygame.locals import *
from pen import Pen

class BoardSurface(object):
    def __init__(self, board):
        super().__init__()
        self.boardColor = (255, 255, 255, 0)
        self.fillColor = (0, 0, 0, 0)
        self.scale = 8
        self.board = board
        self.pencil = Pen(self)

    def setSurface(self, surface) :
        self.surface = surface
        self.surface.fill(self.boardColor)

    def getDimension(self) :
        return (self.scale * len(self.board.cells), self.scale * len(self.board.cells[0]))

    def contains(self, point):
        rel = self.sub(point, self.surface.get_abs_offset())
        dim = Rect((0,0), self.getDimension())
        return dim.collidepoint(rel)

    def globalToBoard(self, pos):
        offset = self.surface.get_abs_offset()
        return self.sub(pos, offset)

    def sub(self, u, v):
      return [ u[i]-v[i] for i in range(len(u)) ]

    def fill(self, points) :
        for point in points:
            self.board.fill(int(point[0]/self.scale), int(point[1]/self.scale))
        self.update()

    def update(self, event = None, force = False) :
        if self.pencil :
            self.pencil.update(event)

        if (self.board.dirty or force) :
            self.board.dirty = False
            for x in range(len(self.board.cells)) :
                for y in range(len(self.board.cells[0])) :
                    cell = self.board.cells[x][y]
                    x1 = x * self.scale
                    y1 = y * self.scale
                    width = self.scale
                    height = self.scale
                    if (cell) :
                        pygame.draw.rect(self.surface, self.fillColor, (x1, y1, width, height))
                    else :
                        pygame.draw.rect(self.surface, self.boardColor, (x1, y1, width, height))


class Board(object):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.clear()
        self.dirty = True

    def clear(self) :
        self.cells = [[0 for x in range(self.width)] for y in range(self.height)]
        self.dirty = True

    def randomFill(self, percentage) :
        self.clear()
        for x in range(0, self.width):
            for y in range(0, self.height):
                if (random.randint(1, 100) < percentage):
                    self.fill(x,y)
        self.dirty = True

    def fill(self, x,y) :
        if (x >= 0 and x < self.width and y >=0 and y < self.height):
            self.cells[x][y] = 1
        self.dirty = True
