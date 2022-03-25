# Thomas Pollard
# Programming 3
# CS441 Artificial Intelligence
# Winter 2021

import numpy as np
import math
import random
import watchrobby

# Number of episodes
N = 5000

# Number of actions
M = 200

# Grid size
GRIDSIZE = (10,10)

# Can placement chance
canProcChance = 0.5

ETA = 0.2
DISCOUNT_RATE = 0.9
EPSILON = 0.1





def initGrid():
  # Initialized a grid with random can placement
  grid = np.zeros((GRIDSIZE[1], GRIDSIZE[0]))
  for row in grid:
    for i in range(len(row)):
      if random.random() <= canProcChance:
        row[i] += 1
  return grid

class Robby():
  def __init__(self):    
    self.QMatrix = np.zeros(((3*3*3*3*3*3*3*3*3),(len(self.actions))))
    self.Learn = True

  def reset(self, grid):
    self.grid = grid[:]
    self.y = random.randint(0,GRIDSIZE[0]-1)
    self.x = random.randint(0,GRIDSIZE[1]-1)
    self.grid[GRIDSIZE[1]-self.y-1][self.x] += 2
    self.reward = 0

    #TEST TO GET THE LAST Q INDEX STATE
##    self.x = 1
##    self.y = 1
##    self.grid[GRIDSIZE[1]-self.y-1][self.x] = 3
##    self.grid[GRIDSIZE[1]-self.y-2][self.x] = 1
##    self.grid[GRIDSIZE[1]-self.y][self.x] = 1
##    self.grid[GRIDSIZE[1]-self.y-1][self.x+1] = 1
##    self.grid[GRIDSIZE[1]-self.y-1][self.x-1] = 1


  def doStep(self):
    lastState = self.stateQIndex()
    action = self.chooseAction()
    reward = self.actions[action](self)
    reward -= 0.5
    self.reward += reward
    newState = self.stateQIndex()
    if self.Learn:
      self.updateQMatrix(lastState, action, reward)
    

  def getState(self):
    # Returns a list [north, northNorth, east, eastEast, south, southSouth, west, westWest, current]
    # 1 if can, -1 if wall, 0 if empty
    state = [self.northStatus(), self.northNorthStatus(), self.eastStatus(), self.eastEastStatus(),
             self.southStatus(), self.southSouthStatus(), self.westStatus(), self.westWestStatus(), self.currentStatus()]

    # This was used for adding corner sensors.
##    state = [self.northStatus(), self.northEastStatus(), self.eastStatus(), self.southEastStatus(),
##             self.southStatus(), self.southWestStatus(), self.westStatus(), self.northWestStatus(), self.currentStatus()]
    return state

  # SENSORS - Return 1 if a can, 0 if empty, -1 if wall
  def northStatus(self):
    if self.y == 9:
      return -1
    else:
      return 1 if self.grid[GRIDSIZE[1]-self.y-2][self.x] % 2 == 1 else 0

  def eastStatus(self):
    if self.x == 9:
      return -1
    else:
      return 1 if self.grid[GRIDSIZE[1]-self.y-1][self.x+1] % 2 == 1 else 0

  def southStatus(self):
    if self.y == 0:
      return -1
    else:
      return 1 if self.grid[GRIDSIZE[1]-self.y][self.x] % 2 == 1 else 0

  def westStatus(self):
    if self.x == 0:
      return -1
    else:
      return 1 if self.grid[GRIDSIZE[1]-self.y-1][self.x-1] % 2 == 1 else 0

  # ADDING CORNER SENSORS
  def northEastStatus(self):
    if self.eastStatus() == -1 or self.northStatus() == -1:
      return -1
    else:
      return 1 if self.grid[GRIDSIZE[1]-self.y-2][self.x+1] % 2 == 1 else 0
    
  def southEastStatus(self):
    if self.eastStatus() == -1 or self.southStatus() == -1:
      return -1
    else:
      return 1 if self.grid[GRIDSIZE[1]-self.y][self.x+1] % 2 == 1 else 0
    
  def southWestStatus(self):
    if self.westStatus() == -1 or self.southStatus() == -1:
      return -1
    else:
      return 1 if self.grid[GRIDSIZE[1]-self.y][self.x-1] % 2 == 1 else 0

  def northWestStatus(self):
    if self.westStatus() == -1 or self.northStatus() == -1:
      return -1
    else:
      return 1 if self.grid[GRIDSIZE[1]-self.y-2][self.x-1] % 2 == 1 else 0

  # ADDING DOUBLE DISTANCE SENSORS
  def northNorthStatus(self):
    if self.y >= 8:
      return -1
    else:
      return 1 if self.grid[GRIDSIZE[1]-self.y-3][self.x] % 2 == 1 else 0
    
  def eastEastStatus(self):
    if self.x >= 8:
      return -1
    else:
      return 1 if self.grid[GRIDSIZE[1]-self.y-1][self.x+2] % 2 == 1 else 0
    
  def southSouthStatus(self):
    if self.y <= 1:
      return -1
    else:
      return 1 if self.grid[GRIDSIZE[1]-self.y+1][self.x] % 2 == 1 else 0

  def westWestStatus(self):
    if self.x <= 1:
      return -1
    else:
      return 1 if self.grid[GRIDSIZE[1]-self.y-1][self.x-2] % 2 == 1 else 0

  def currentStatus(self):
    return 1 if self.grid[GRIDSIZE[1]-self.y-1][self.x] % 2 == 1 else 0

  def chooseAction(self):
    # At probability of epsilon, choose a random action
    randomChance = random.random()
    if randomChance <= EPSILON:
      choice = random.randint(0,4)
      return choice
    else:
      # get a list of actions that have the max value, randomly choose one of those
      choices = np.where(robby.QMatrix[robby.stateQIndex()] == max(robby.QMatrix[robby.stateQIndex()]))[0]
      choice = random.choice(choices)
      return choice

  def updateQMatrix(self, lastState, action, reward):
    lastValue = self.QMatrix[lastState, action]
    self.QMatrix[lastState, action] = lastValue + ETA*(reward + DISCOUNT_RATE*(max(robby.QMatrix[robby.stateQIndex()]))-lastValue)
    pass

  def moveWest(self):
    if self.westStatus() < 0:
      return -5
    else:
      self.grid[GRIDSIZE[1]-self.y-1][self.x] -= 2
      self.x -= 1
      self.grid[GRIDSIZE[1]-self.y-1][self.x] += 2
      return 0

  def moveEast(self):
    if self.eastStatus() < 0:
      return -5
    else:
      self.grid[GRIDSIZE[1]-self.y-1][self.x] -= 2
      self.x += 1
      self.grid[GRIDSIZE[1]-self.y-1][self.x] += 2
      return 0

  def moveNorth(self):
    if self.northStatus() < 0:
      return -5
    else:
      self.grid[GRIDSIZE[1]-self.y-1][self.x] -= 2
      self.y += 1
      self.grid[GRIDSIZE[1]-self.y-1][self.x] += 2
      return 0
      
  def moveSouth(self):
    if self.southStatus() < 0:
      return -5
    else:
      self.grid[GRIDSIZE[1]-self.y-1][self.x] -= 2
      self.y -= 1
      self.grid[GRIDSIZE[1]-self.y-1][self.x] += 2
      return 0

  def pickup(self):
    if self.grid[GRIDSIZE[1]-self.y-1][self.x] % 2 == 1:
      self.grid[GRIDSIZE[1]-self.y-1][self.x] -= 1
      return 10
    else:
      return -1

  def stateQIndex(self):
    # Converts the current state into an index into the Q-matrix
    index = 0
    for i, status in enumerate(self.getState()):
      #print("index adds",(1 + status)*(3**i), "for digit", status, "in position", i)
      index += (1 + status)*(3**i)
    return index

    

  actions = [moveNorth, moveEast, moveSouth, moveWest, pickup]

robby = Robby();
watchrobby.FPS = 60

print("Running training episodes")
for episode in range(N):
  if EPSILON > 0 and episode % 50 == 0:
    EPSILON -= 0.0025
  grid = initGrid()
  robby.reset(grid[:])
##  sequence = []
  for step in range(M):
    if episode % 100 == 0:
      watchrobby.render(robby.grid, episode, step)
##      sequence.append(robby.grid.tolist()[:])
    robby.doStep()
  if episode % 100 == 0:
    print("reward for episode", str(episode) + ":", robby.reward)
##    watchrobby.watchEpisode(sequence, episode)

print("Running test episodes")
EPSILON = 0.1
robby.Learn = False
testRewards = []
for episode in range(N):
  grid = initGrid()
  robby.reset(grid)
  for step in range(M):
    robby.doStep()
  testRewards.append(robby.reward)
print("Average sum of rewards per episode:", np.mean(testRewards))
print("Standard deviation of sum of rewards per episode:", np.std(testRewards))
watchrobby.quit()

