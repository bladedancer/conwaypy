import pygame, sys
from pygame.locals import *
from board import BoardSurface
from sidebar import SidebarSurface

MASTER_MARGIN=10
MASTER_COLOR=(127,127,127,0)
SIDEBAR_COLOR=(127,127,127,0)

class Layout(object):
    def __init__(self, board, life):
        self.board = BoardSurface(board)
        self.life = life
        self.sidebar = SidebarSurface(life)
        self.__initSurfaces()

    def getBoardSurface(self) :
        return self.board

    def __initSurfaces(self) :
        boardDim = self.board.getDimension()
        sidebarDim = (300, boardDim[1])
        masterDim = (
            sidebarDim[0] + boardDim[0] + (2 * MASTER_MARGIN),
            max(sidebarDim[1], boardDim[1]) + (2 * MASTER_MARGIN)
            )

        masterRect = pygame.Rect(0, 0, masterDim[0], masterDim[1])
        boardRect = pygame.Rect(
            MASTER_MARGIN, MASTER_MARGIN,
            boardDim[0], boardDim[1]
            )
        sidebarRect = pygame.Rect(
            boardDim[0] + MASTER_MARGIN, MASTER_MARGIN,
            sidebarDim[0], sidebarDim[1])

        pygame.init()
        pygame.display.set_caption('Conways Game of Life')

        # Surfaces
        self.masterSurface = pygame.display.set_mode(masterDim)
        self.masterSurface.fill(MASTER_COLOR)

        boardSurface = self.masterSurface.subsurface(boardRect)
        self.board.setSurface(boardSurface)

        sidebarSurface = self.masterSurface.subsurface(sidebarRect)
        self.sidebar.setSurface(sidebarSurface)

    def update(self, event = None, force = False) :
        self.board.update(event, force)
        self.sidebar.update(event)
        pygame.display.flip()
