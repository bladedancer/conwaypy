import glob
import os
from pygame.locals import *

class Stencils(object):
    def __init__(self):
        self.stencil = {}
        self.loadStencils()

    def loadStencils(self) :
        ''' See http://www.conwaylife.com/wiki/Category:Patterns '''
        for stencil in glob.glob("template/*.lif"):
            name = os.path.basename(stencil)[:-4]
            lines = [line.rstrip('\n') for line in open(stencil)]
            patternLines = []
            for line in lines:
                if not line.startswith('#'):
                    patternLines.append(line)
            self.stencil[name] = patternLines
