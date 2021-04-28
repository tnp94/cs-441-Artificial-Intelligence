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
  



#print(grid)


cumulativeTotal = 0
for r in range(runs):
  actionCount = 0
  initializeGrid()
  #print("Starting grid:\n", grid)
  for i in range(300):
    if dirtCount == 0:
      break


    acted = False
    while acted == False:
      decision = random.randint(0,4)
      # 0 = left, 1 = up, 2 = right, 3 = down, 4 = suck
      if decision == 4:
        if grid[vacuumY][vacuumX] % 2 == 1:
          #print("Dirt found at (" + str(vacuumX) + ", " + str(vacuumY) + "). Sucking...")
          grid[vacuumY][vacuumX] = grid[vacuumY][vacuumX] - 1
          dirtCount = dirtCount - 1
        acted = True
      elif decision == 0 and vacuumX > 0:
        moveLeft()
        acted = True
      elif decision == 1 and vacuumY > 0:
        moveUp()
        acted = True
      elif decision == 2 and vacuumX < 2:
        moveRight()
        acted = True
      elif decision == 3 and vacuumY < 2:
        moveDown()
        acted = True
    actionCount += 1
    #print(str(dirtCount) + " dirty squares remain")
    #print(grid)

  #print("I finished in " + str(actionCount) + " moves")
  cumulativeTotal += actionCount

print("The average actions per run after " + str(runs) + " for this agent cleaning " + str(startingDirt) + " dirt piles was " + str(cumulativeTotal/runs))
  
    

    
