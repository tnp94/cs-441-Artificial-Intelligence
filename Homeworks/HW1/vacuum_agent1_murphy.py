import numpy as np
import math
import random

startingDirt = 1
runs = 100000

grid = np.zeros((3,3))

vacuumX = 0
vacuumY = 0
dirtCount = 0

def initializeGrid():
  global dirtCount
  dirtCount = startingDirt
  global vacuumX
  vacuumX = random.randint(0,2)
  global vacuumY
  vacuumY = random.randint(0,2)
  global grid
  grid = np.zeros((3,3))

  for i in range(dirtCount):
    newdirtX = random.randint(0,2)
    newdirtY = random.randint(0,2)
    while grid[newdirtY][newdirtX] == 1:
      newdirtX = random.randint(0,2)
      newdirtY = random.randint(0,2)
    grid[newdirtY][newdirtX] = 1
    
  grid[vacuumY][vacuumX] = grid[vacuumY][vacuumX] + 2
  return

def moveRight():
  global vacuumX
  global vacuumY
  #print("I am at (" + str(vacuumX) + ", " + str(vacuumY) + "). Moving right...")
  grid[vacuumY][vacuumX] = grid[vacuumY][vacuumX] - 2
  vacuumX += 1
  grid[vacuumY][vacuumX] = grid[vacuumY][vacuumX] + 2
def moveLeft():
  global vacuumX
  global vacuumY
  #print("I am at (" + str(vacuumX) + ", " + str(vacuumY) + "). Moving left...")
  grid[vacuumY][vacuumX] = grid[vacuumY][vacuumX] - 2
  vacuumX -= 1
  grid[vacuumY][vacuumX] = grid[vacuumY][vacuumX] + 2
def moveUp():
  global vacuumX
  global vacuumY
  #print("I am at (" + str(vacuumX) + ", " + str(vacuumY) + "). Moving up...")
  grid[vacuumY][vacuumX] = grid[vacuumY][vacuumX] - 2
  vacuumY -= 1
  grid[vacuumY][vacuumX] = grid[vacuumY][vacuumX] + 2
def moveDown():
  global vacuumX
  global vacuumY
  #print("I am at (" + str(vacuumX) + ", " + str(vacuumY) + "). Moving down...")
  grid[vacuumY][vacuumX] = grid[vacuumY][vacuumX] - 2
  vacuumY += 1
  grid[vacuumY][vacuumX] = grid[vacuumY][vacuumX] + 2

def pickMove():
  global vacuumX
  global vacuumY
  if vacuumY == 0:
    if vacuumX < 2:
      moveRight()
    else:
      moveDown()
  elif vacuumY == 2:
    if vacuumX > 0:
      moveLeft()
    else:
      moveUp()
  else:
    if vacuumX == 0:
      upChance = random.randint(0,1)
      if upChance == 1:
        moveUp()
      else:
        moveRight()
    elif vacuumX == 1:
      moveLeft()
    else:
      moveDown()


#print(grid)


cumulativeTotal = 0
for r in range(runs):
  actionCount = 0
  initializeGrid()
  #print("Starting grid:\n", grid)
  for i in range(300):
    if dirtCount == 0:
      break
    if random.randint(1, 10) == 1:
      if grid[vacuumY][vacuumX] % 2 == 0:
        '''Sensor thought it was dirty, suck a clean floor'''
        #print("Sensor failed... sucking a clean floor")
      elif grid[vacuumY][vacuumX] % 2 == 1:
        #print("Sensor failed... moving past...")
        pickMove()

    else:
      if grid[vacuumY][vacuumX] % 2 == 1:
        if random.random() <= 0.25:
          #print("Sucking mechanism failed at (" + str(vacuumX) + ", " + str(vacuumY) + "). Dumping...")
          if grid[vacuumY][vacuumX] == 0:
            grid[vacuumY][vacuumX] += 1
            dirtCount += 1
        else:
          #print("Dirt found at (" + str(vacuumX) + ", " + str(vacuumY) + "). Sucking...")
          grid[vacuumY][vacuumX] = grid[vacuumY][vacuumX] - 1
          dirtCount = dirtCount - 1
      else:
        pickMove()
    actionCount += 1
    #print(str(dirtCount) + " dirty squares remain")
    #print(grid)

  #print("I finished in " + str(actionCount) + " moves")
  cumulativeTotal += actionCount

print("The average actions per run after " + str(runs) + " for this agent cleaning " + str(startingDirt) + " dirt piles was " + str(cumulativeTotal/runs))
  
    

    
