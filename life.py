
class World(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def getNeighbours(self, point):
        return []

class DonutWorld(World):
    def __init__(self, width, height):
        super().__init__(width, height)

    def getNeighbours(self, point):
        neighbours = []
        xc = point[0]
        yc = point[1]

        neighbours = [
            ((xc-1)%self.width, (yc-1)%self.height), ((xc)%self.width, (yc-1)%self.height), ((xc+1)%self.width, (yc-1)%self.height),
            ((xc-1)%self.width, (yc)%self.height),                                          ((xc+1)%self.width, (yc)%self.height),
            ((xc-1)%self.width, (yc+1)%self.height), ((xc)%self.width, (yc+1)%self.height), ((xc+1)%self.width, (yc+1)%self.height),
        ]
        return neighbours


class FlatWorld(World):
    def __init__(self, width, height):
        super().__init__(width, height)

    def getNeighbours(self, point):
        neighbours = []
        xc = point[0]
        yc = point[1]

        if xc > 1 and xc < self.width - 1 and yc > 1 and yc < self.height -1:
            # Optimised
            neighbours = [
                (xc-1, yc-1), (xc, yc-1), (xc+1, yc-1),
                (xc-1, yc),               (xc+1, yc),
                (xc-1, yc+1), (xc, yc+1), (xc+1, yc+1),
            ]
        else:
            for x in [xc-1, xc, xc+1]:
                for y in [yc-1, yc, yc+1]:
                    if ((x == xc and y == yc) and
                            x >= 0 and x <= self.width and
                            y >= 0 and y <= self.height):
                        neighbours.append((x,y))
        return neighbours


class Life(object):
    def __init__(self, board):
        super().__init__()
        self.board = board
        self.world = DonutWorld(board.width, board.height)
        self.nextCells = [[0 for x in range(board.width)] for y in range(board.height)]
        self.generation = 0
        self.running = False

    def start(self):
         self.running = True

    def stop(self):
         self.running = False

    def clear(self):
        self.board.clear()
        self.generation = 0

    def randomFill(self, percentage):
        self.board.randomFill(percentage)

    def next(self) :
        if not self.running:
            return
        # Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
        # Any live cell with two or three live neighbours lives on to the next generation.
        # Any live cell with more than three live neighbours dies, as if by overpopulation.
        # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

        for x in range(0, self.board.width):
            for y in range(0, self.board.height):
                cellVal = self.board.cells[x][y]
                neighbourCount = 0
                neighbours = self.world.getNeighbours((x,y));
                # print (str((x,y)) + ":" + str(neighbours))
                for neighbour in neighbours:
                    neighbourCount += self.isAlive((neighbour[0], neighbour[1]))

                self.nextCells[x][y] = self.getChildValue(cellVal, neighbourCount)

        tmp = self.board.cells
        self.board.cells = self.nextCells
        self.nextCells = tmp
        self.generation = self.generation + 1

    def isAlive(self, pos):
        return self.board.cells[pos[0]][pos[1]]


class Conway(Life):
    def __init__(self, board):
        super().__init__(board)

    def getChildValue(self, cellVal, neighbourCount) :
        # Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
        # Any live cell with two or three live neighbours lives on to the next generation.
        # Any live cell with more than three live neighbours dies, as if by overpopulation.
        # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        if neighbourCount < 2 :
            return 0
        elif neighbourCount == 2 :
            return cellVal
        elif neighbourCount == 3 :
            return 1
        elif neighbourCount > 3 :
            return 0

class HighLife(Life):
    def __init__(self, board):
        super().__init__(board)

    def getChildValue(self, cellVal, neighbourCount) :
        # Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
        # Any live cell with two or three live neighbours lives on to the next generation.
        # Any live cell with more than three live neighbours dies, as if by overpopulation EXCEPT for 6 neighbours.
        # Any dead cell with exactly three or six live neighbours becomes a live cell, as if by reproduction.
        if neighbourCount == 2:
            return cellVal
        elif neighbourCount == 3 or neighbourCount == 6 :
            return 1

        return 0
