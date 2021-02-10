import time
from threading import Lock

from agent import Agent
from framework import *


class Game:
    def __init__(self):
        self.size = (WIDTH, HEIGHT)
        self.window = None
        self.clock = None
        self.finished = False
        self.agents = []
        self.lock = Lock()
        self.listColors = [WHITE, BLACK, GREEN, RED, BLUE, AQUA, ORANGE, YELLOW, GRAY]

    def pygame_init(self):
        pygame.init()
        self.window = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.clock.tick(60)
        pygame.display.set_caption("Ant Simulation")

    def gameLoop(self):
        self.pygame_init()
        self.generateObjects(NBCOLORS)
        self.initAgents()
        self.runAgents()

        # Display window at the end
        while not self.finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stopAgents()
                    self.finished = True
            self.window.fill(BLACK)
            self.drawGrid()
            refresh()

    def is_finished(self):
        if len(ARRAYAGENTS) == NB_AGENTS:
            return True
        else:
            return False

    def drawGrid(self):
        for row in range(ROWS):
            for column in range(COLUMNS):
                color = getColorFromGrid(row, column)
                pygame.draw.rect(self.window,
                                 color,
                                 [(MARGIN + wCASE) * column + MARGIN,
                                  (MARGIN + hCASE) * row + MARGIN,
                                  wCASE,
                                  hCASE])

    def drawFinalGrid(self):
        for row in range(ROWS):
            for column in range(COLUMNS):
                color = getColorFromGrid(row, column)
                if color == 0:
                    color = 1
                pygame.draw.rect(self.window,
                                 color,
                                 [(MARGIN + wCASE) * column + MARGIN,
                                  (MARGIN + hCASE) * row + MARGIN,
                                  wCASE,
                                  hCASE])

    def generateObjects(self, nbColors):
        count = int(OBJECTS / nbColors)
        index_color = 3
        for x in range(nbColors):
            for y in range(count):
                color = self.listColors[index_color]
                value = getValueColor(color)
                pos_x, pos_y = getRandomPosition()
                grid[pos_x][pos_y] = value
            index_color += 1

    def initAgents(self):
        for i in range(NB_AGENTS):
            pos_x, pos_y = getRandomPosition()
            agent = Agent(pos_x, pos_y, self.lock)
            self.agents.append(agent)

    def runAgents(self):
        for i in self.agents:
            i.start()

    def stopAgents(self):
        for i in self.agents:
            i.stop()


if __name__ == "__main__":
    game = Game()
    game.gameLoop()
