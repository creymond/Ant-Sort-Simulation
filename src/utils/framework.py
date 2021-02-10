import random

import pygame

from constantes import *


# True if the given position is out of bound, false otherwise
def outOfBound(x, y):
    if (x < 0 or x >= ROWS) and (y >= COLUMNS or y < 0):
        return True
    else:
        return False


# Update the screen display
def refresh():
    pygame.display.flip()


# End the execution of pygame instance
def quitApp():
    pygame.quit()


# Initialize grid
def createGrid():
    for row in range(ROWS):
        grid.append([])
        for column in range(COLUMNS):
            grid[row].append(1)


def getValueColor(color):
    if color == WHITE:
        return 0
    elif color == BLACK:
        return 1
    elif color == GREEN:
        return 2
    elif color == RED:
        return 3
    elif color == BLUE:
        return 4
    elif color == AQUA:
        return 5
    elif color == ORANGE:
        return 6
    elif color == YELLOW:
        return 7
    elif color == GRAY:
        return 8

def getColorFromGrid(row, column):
    color = None
    if grid[row][column] == 1:
        color = BLACK
    elif grid[row][column] == 0:
        color = WHITE
    elif grid[row][column] == 2:
        color = GREEN
    elif grid[row][column] == 3:
        color = RED
    elif grid[row][column] == 4:
        color = BLUE
    elif grid[row][column] == 5:
        color = AQUA
    elif grid[row][column] == 6:
        color = ORANGE
    elif grid[row][column] == 7:
        color = YELLOW
    elif grid[row][column] == 8:
        color = GRAY
    return color


# Modify the object displayed at given position
def setColor(x, y, color):
    grid[x][y] = color

def clearAgents():
    for x in range(ROWS):
        for y in range(COLUMNS):
            v = grid[x][y]
            if v == 0:
                grid[x][y] = 1

# Generate random position from grid where there is no object
def getRandomPosition():
    x = random.randint(0, ROWS - 1)
    y = random.randint(0, COLUMNS - 1)
    while grid[x][y] != 1:
        x = random.randint(0, ROWS - 1)
        y = random.randint(0, COLUMNS - 1)
    return x, y


def hasObject(x, y):
    if grid[x][y] >= 2:
        return True
    else:
        return False
