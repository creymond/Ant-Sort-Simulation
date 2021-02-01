from agent import Agent
from framework import *
from threading import Lock
import time


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
        self.generateObjects(NBCOLORS)
        self.initAgents()
        self.runAgents()

        # Wait for timer to finish
        start_time = time.time()
        while True:
            if time.time() > start_time + TIME:
                self.stopAgents()
                break
        print("--- %s seconds ---" % (time.time() - start_time))

        # Display window at the end
        self.pygame_init()
        clearAgents()
        count = 0
        while not self.finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stopAgents()
                    self.finished = True
            self.window.fill(BLACK)
            self.drawGrid()
            refresh()
            if count == 0:
                pygame.image.save(self.window, "../screenshot/"
                                  + str(NB_AGENTS) + "A_" + str(TIME)
                                  + "s_" + str(FRAME) + "F_" + str(SIZE_MEMORY) + "M_" + str(MOVEMENT) + "MO.png")
                count += 1

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
