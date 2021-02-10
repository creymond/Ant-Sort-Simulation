from threading import Thread

from framework import *


class Agent(Thread):
    def __init__(self, x, y, lock):
        super().__init__()
        self.finished = False
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.object_holding = None
        self.memory = []
        self.lock = lock
        self.movement = 0
        self.iteration = ITERATION

    # def run(self):
    #     self.randomize_movement()
    #     while not self.finished:
    #         positions = self.generateListPosition2()
    #         self.move(positions)

    def run(self):
        self.randomize_movement()
        while self.iteration > 0:
            positions = self.generateListPosition2()
            self.move(positions)
            self.iteration -= 1
        self.lock.acquire()
        ARRAYAGENTS.append(1)
        self.lock.release()

    def stop(self):
        self.finished = True

    def move(self, positions):
        rand = random.randint(0, len(positions) - 1)
        pos = positions[rand]
        self.x = pos[0]
        self.y = pos[1]

        self.lock.acquire()
        value = grid[self.x][self.y]
        self.vision()

        if self.object_holding:
            if value == 1:
                self.dropObject()
        else:
            if value >= 2:
                self.getObject(value)
            elif value == 1:
                grid[self.prev_x][self.prev_y] = 1
                grid[self.x][self.y] = 0
                self.prev_x = self.x
                self.prev_y = self.y
            # elif value == 1:
            #     self.x = self.prev_x
            #     self.y = self.prev_y
        self.lock.release()

        self.randomize_movement()

    def generateListPosition(self):
        res = []
        if 0 <= self.x - 1 < ROWS:
            res.append((self.x - 1, self.y))

        if 0 <= self.x + 1 < ROWS:
            res.append((self.x + 1, self.y))

        if 0 <= self.y - 1 < COLUMNS:
            res.append((self.x, self.y - 1))

        if 0 <= self.y + 1 < COLUMNS:
            res.append((self.x, self.y + 1))
        return res

    def generateListPosition2(self):
        res = []
        x_up = self.x - self.movement
        x_down = self.x + self.movement
        y_left = self.y - self.movement
        y_right = self.y + self.movement
        if 0 <= x_up < ROWS:
            res.append((x_up, self.y))

        if 0 <= x_down < ROWS:
            res.append((x_down, self.y))

        if 0 <= y_left < COLUMNS:
            res.append((self.x, y_left))

        if 0 <= y_right < COLUMNS:
            res.append((self.x, y_right))
        return res

    def updateMemory(self, obj):
        if len(self.memory) == SIZE_MEMORY:
            # remove first object
            self.memory.pop(0)
        self.memory.append(obj)

    def getProportion(self, obj):
        count = 0
        for i in self.memory:
            if i == obj:
                count = count + 1
        return count / len(self.memory)

    def getObject(self, value):
        rand = random.random()
        f = self.getProportion(value)
        frac = KP / (KP + f)
        prise = pow(frac, 2)
        if rand <= prise:
            self.object_holding = value
            grid[self.x][self.y] = 1

    # Drop object if holding one and at current position, if conditions are satisfied
    def dropObject(self):
        rand = random.random()
        f = self.getProportion(self.object_holding)
        frac = f / (KD + f)
        drop = pow(frac, 2)
        if rand <= drop:
            grid[self.x][self.y] = self.object_holding
            self.object_holding = None

    def randomize_movement(self):
        rand = random.randint(1, MOVEMENT)
        self.movement = rand

    def modify_memory(self, arr):
        self.memory = []
        for x in arr:
            self.memory.append(x)

    def vision(self):
        x_min = self.x - FRAME
        x_max = self.x + FRAME
        y_min = self.y - FRAME
        y_max = self.y + FRAME
        l = []

        for x in range(x_min, x_max + 1):
            if 0 <= x < ROWS:
                for y in range(y_min, y_max + 1):
                    if 0 <= y < COLUMNS:
                        value = grid[x][y]
                        if value >= 1:
                            l.append(value)
        if len(l) == 0:
            l.append(-1)
        self.modify_memory(l)
        #print(self.memory)

