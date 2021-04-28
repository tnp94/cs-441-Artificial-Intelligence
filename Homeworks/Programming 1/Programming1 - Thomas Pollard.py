# Thomas Pollard
# Programming 1
# CS441 Artificial Intelligence
# Winter 2021

import random
import math
import numpy as np
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any
import time

start = time.time()

# Maximum number of states to search
# WARNING -- This program does not check if initial states are solvable
# WARNING -- I have MAX_STEPS set to 4 million to attempt to find A* 15 puzzle solutions
# Lower MAX_STEPS to 1 million if not using guaranteed solvable puzzles
MAX_STEPS = 500000
# Print the solution sequence in the shell?
PRINT_SOLUTION = False

# Puzzle activation flags
DO_FIFTEEN_PUZZLE = False
DO_EIGHT_PUZZLE = True

class eightPuzzleProblem:
  # This is the eightPuzzleProblem class.
  # It contains a goal test, heuristics, and transformation model (actions) methods
  def __init__(self, initialState, pathCost = 0):
    self.initialState = initialState

  def goalTest(self, state):
    # True is reached the goal
    if state == [1, 2, 3, 4, 5, 6, 7, 8, 'b']:
      return True
    else:
      return False

  def left(state = None):
    # Returns the state as a result of moving the blank to the left, if it's a legal move
    if state:
      newState = state[:]
      index = newState.index('b')
      if index % 3 == 0:
        raise Exception("Attempted to move left, but blank is on the left")
      else:
        newState[index], newState[index-1] = newState[index-1], newState[index]
      return newState
    
  def right(state = None):
    # Returns the state as a result of moving the blank to the right, if it's a legal move
    if state:
      newState = state[:]
      index = newState.index('b')
      if index % 3 == 2:
        raise Exception("Attempted to move right, but blank is on the right")
      else:
        newState[index], newState[index+1] = newState[index+1], newState[index]
      return newState

  def up(state = None):
    # Returns the state as a result of moving the blank up, if it's a legal move
    if state:
      newState = state[:]
      index = newState.index('b')
      if math.floor(index/3) == 0:
        raise Exception("Attempted to move up, but blank is on the top")
      else:
        newState[index], newState[index-3] = newState[index-3], newState[index]
      return newState
    
  def down(state = None):
    # Returns the state as a result of moving the blank down, if it's a legal move
    if state:
      newState = state[:]
      index = newState.index('b')
      if math.floor(index/3) == 2:
        raise Exception("Attempted to move down, but blank is on the bottom")
      else:
        newState[index], newState[index+3] = newState[index+3], newState[index]
      return newState

  def h1(self, state):
    # Heuristic for number of tiles misplaced
    squaresMisplaced = 0
    for i in range(8):
      if state[i] != i+1:
        squaresMisplaced += 1
    return squaresMisplaced

  def h2(self, state):
    # Heuristic for manhattan distance of each tile
    totalDistance = 0
    for i in range(8):
      thisDistance = 0
      thisDistance += abs((state.index(i+1) % 3) - (i % 3))
      thisDistance += abs(math.floor(state.index(i+1)/3.0) - math.floor(i / 3.0))
      totalDistance += thisDistance
    return totalDistance


  def h3(self, state):
    # My heuristic is the average of h1 and h2
    return (eightPuzzleProblem.h1(self, state) + eightPuzzleProblem.h2(self, state))/2

  # List containers for the heuristic and action functions available
  heuristics = [h1, h2, h3]
  actions = [left, right, up, down]

class fifteenPuzzleProblem:
  def __init__(self, initialState, pathCost = 0):
    self.initialState = initialState

  def goalTest(self, state):
    if state == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 'b']:
      return True
    else:
      return False
  
  def result(self, state, action):
    return action(state)

  def left(state = None):
    # Returns the state as a result of moving the blank to the left, if it's a legal move
    if state:
      newState = state[:]
      index = newState.index('b')
      if index % 4 == 0:
        raise Exception("Attempted to move left, but blank is on the left")
      else:
        newState[index], newState[index-1] = newState[index-1], newState[index]
      return newState
    
  def right(state = None):
    # Returns the state as a result of moving the blank to the right, if it's a legal move
    if state:
      newState = state[:]
      index = newState.index('b')
      if index % 4 == 3:
        raise Exception("Attempted to move right, but blank is on the right")
      else:
        newState[index], newState[index+1] = newState[index+1], newState[index]
      return newState

  def up(state = None):
    # Returns the state as a result of moving the blank up, if it's a legal move
    if state:
      newState = state[:]
      index = newState.index('b')
      if math.floor(index/4) == 0:
        raise Exception("Attempted to move up, but blank is on the top")
      else:
        newState[index], newState[index-4] = newState[index-4], newState[index]
      return newState
    
  def down(state = None):
    # Returns the state as a result of moving the blank down, if it's a legal move
    if state:
      newState = state[:]
      index = newState.index('b')
      if math.floor(index/4) == 3:
        raise Exception("Attempted to move down, but blank is on the bottom")
      else:
        newState[index], newState[index+4] = newState[index+4], newState[index]
      return newState

  def h1(self, state):
    # Heuristic for number of tiles misplaced
    squaresMisplaced = 0
    for i in range(15):
      if state[i] != i+1:
        squaresMisplaced += 1
    return squaresMisplaced

  def h2(self, state):
    # Heuristic for manhattan distance of each tile
    totalDistance = 0
    for i in range(15):
      thisDistance = 0
      thisDistance += abs((state.index(i+1) % 4) - (i % 4))
      thisDistance += abs(math.floor(state.index(i+1)/4) - math.floor(i / 4))
      totalDistance += thisDistance
    return totalDistance


  def h3(self, state):
    # My heuristicis the average of h1 and h2
    return (fifteenPuzzleProblem.h1(self, state) + fifteenPuzzleProblem.h2(self, state))/2

  # List containers for the heuristic and action functions available
  heuristics = [h1, h2, h3]
  actions = [left, right, up, down]

def hashState(state):
  # Hashes the state as a string and returns the hash
  return hash(str(state))

class Node:
  # Node class to contain relevant node data
  def __init__(self, state, parent = None, action = None, pathCost = 0):
    self.state = state[:]
    self.parent = parent
    self.action = action
    self.pathCost = pathCost

    
  def childNode(self, problem, action):
    # Creates a child node with a state that's the result of the action performed, if possible
    try:
      newNode = Node(action(self.state), self, action, self.pathCost+1)
      return newNode
    except:
      pass

def createRandomEightState():
  # Uses the Fisher-Yates shuffle algorithm to produce a random state
  state = [1, 2, 3, 4, 5, 6, 7, 8, 'b']
  for i in range(len(state)):
    destination = random.randint(i,len(state)-1)
    state[i], state[destination] = state[destination], state[i]

  # These are some of the solvable test states I used
  #state = [3,5,'b',7,2,6,4,8,1]
  #state = [5,2,7,6,'b',4,3,8,1]
  #state = [4,'b',1,2,7,5,6,3,8]
  return state

def createRandomFifteenState():
  # Uses the Fisher-Yates shuffle algorithm to produce a random state
  state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 'b']
  for i in range(len(state)):
    destination = random.randint(i,len(state)-1)
    state[i], state[destination] = state[destination], state[i]


  # These are some of the solvable test states I used
  # I verified solvability by attempting to recreate them and see if it allowed them at the following link
  # https://www.jaapsch.net/puzzles/javascript/fifteenj.htm
  #state = ['b', 9, 10, 11, 4, 1, 15, 5, 8, 3, 12, 14, 6, 7, 13, 2]
  #state = [10, 7, 'b', 2, 1, 13, 3, 15, 4, 14, 11, 9, 5, 6, 8, 12]
  #state = [9, 12, 4, 10, 14, 3, 1, 'b', 7, 11, 6, 13, 8, 2, 15, 5]
  #state = [10, 6, 5, 13, 12, 15, 1, 11, 9, 8, 4, 2, 3, 'b', 14, 7]
  #state = [4, 'b', 9, 10, 11, 13, 7, 3, 15, 2, 5, 8, 12, 1, 14, 6]
  return state


@dataclass(order=True)
class HeapItemWrapper():
  # Wraps items for priority queue so that it only compares the path costs and ignores comparing nodes
  # Used https://docs.python.org/3/library/queue.html as reference
  priority: int
  node: Any=field(compare=False)

def greedyBestFirstSearch(problem, heuristic):
  # Solves the puzzle problem using best first search, stopping after MAX_STEPS if a solution was not reached
  # Creates a node as the starting r
  steps = 0
  node = Node(problem.initialState, None, None, 0)
  frontier = PriorityQueue()
  heapItem = HeapItemWrapper(heuristic(heuristic, node.state), node)
  frontier.put(heapItem)
  visited = {}
  visited[hashState(node.state)] = node.pathCost
  
  while True:
    #print(frontier.qsize())
    if steps >= MAX_STEPS:
      print("FAILURE. Reached maximum number of steps.")
      return False
    if frontier.empty():
      print("FAILURE. Solution not found...")
      return False
    else:
      node = frontier.get().node
      if problem.goalTest(node.state) == True:
        solution(node, steps)
        return
      else:
        steps += 1
        
        # This is to monitor progress instead of staring at a blank terminal hoping its working
        if steps % 100000 == 0:
          print(steps)
          
        for action in problem.actions:
          newNode = node.childNode(problem, action)
          if newNode:
            stateHash = hashState(newNode.state)
            
            # State not visited, add it to the frontier and record it as visited with it's path cost
            if stateHash not in visited:
              visited[stateHash] = newNode.pathCost
              heapItem = HeapItemWrapper(heuristic(heuristic, newNode.state), newNode)
              frontier.put(heapItem)


def aStar(problem, heuristic):
  # Solves the puzzle problem using A* search, stopping after MAX_STEPS if a solution was not reached
  steps = 0
  node = Node(problem.initialState, None, None, 0)
  frontier = PriorityQueue()
  heapItem = HeapItemWrapper(heuristic(heuristic, node.state) + node.pathCost, node)
  frontier.put(heapItem)
  visited = {}
  visited[hashState(node.state)] = node.pathCost
  while True:
    if steps >= MAX_STEPS:
      print("FAILURE. Reached maximum number of steps.")
      return
    if frontier.empty():
      print("FAILURE. Solution not found...")
      return False
    else:
      node = frontier.get().node
      if problem.goalTest(node.state) == True:
        solution(node, steps)
        return
      else:
        steps += 1

        # This is to monitor progress instead of staring at a blank terminal hoping its working
        if steps % 200000 == 0:
          print(steps)

        # Check if each action is possible.
        for action in problem.actions:
          newNode = node.childNode(problem, action)
          if newNode:
            # Now check if the new node state has been visited before.
            stateHash = hashState(newNode.state)

            # State not visited, add it to the frontier and record it as visited with it's path cost
            if stateHash not in visited:
              visited[stateHash] = newNode.pathCost
              heapItem = HeapItemWrapper(heuristic(heuristic, newNode.state) + newNode.pathCost, newNode)
              frontier.put(heapItem)

            # State visited, only add it to the frontier if it is a cheaper path cost than the existing node
            else:
              if newNode.pathCost < visited[stateHash]:
                visited[stateHash] = newNode.pathCost
                heapItem = HeapItemWrapper(heuristic(heuristic, newNode.state) + newNode.pathCost, newNode)
                frontier.put(heapItem)

def solution(node, steps):
  # Starts from the solution node and uses a stack to walk back to parent and print the solution
  stack = []
  while node:
    stack.append(node)
    node = node.parent

  actionCount = len(stack)
  if PRINT_SOLUTION and len(stack) < 100:
    # Print the states and actions along the solution path
    while stack:
      node = stack.pop()
      print(node.state)
    
      # Below prints the solution steps with their transition names
      #if node.action:
        #print("\n", node.action.__name__)
      #print(np.reshape(np.array(node.state),(3,3)))

      
  print("Solution of ", actionCount-1, " moves found after ", steps, " steps")



if DO_FIFTEEN_PUZZLE:
  # Get an initial 15 problem state and pass it to each heuristic that the problem has
  startFifteenState = createRandomFifteenState()
  print(np.reshape(np.array(startFifteenState),(4,4)))
  problem = fifteenPuzzleProblem
  for heuristic in problem.heuristics:
    # Greedy best first searches
    print("Attempting greedy best first search on the " + problem.__name__ + " with heuristic " + heuristic.__name__)
    greedyBestFirstSearch(problem(startFifteenState), heuristic)

  for heuristic in problem.heuristics:
    # A* searches
    print("Attempting A* search on the " + problem.__name__ + " with heuristic " + heuristic.__name__)
    aStar(problem(startFifteenState), heuristic)

if DO_EIGHT_PUZZLE:
  # Get an initial 8 problem state and pass it to each heuristic that the problem has
  startState = createRandomEightState()
  print(np.reshape(np.array(startState),(3,3)))
  problem = eightPuzzleProblem
  for heuristic in problem.heuristics:
    # Greedy best first searches
    print("Attempting greedy best first search on the " + problem.__name__ + " with heuristic " + heuristic.__name__)
    greedyBestFirstSearch(problem(startState), heuristic)

  for heuristic in problem.heuristics:
    # A* searches
    print("Attempting A* search on the " + problem.__name__ + " with heuristic " + heuristic.__name__)
    aStar(problem(startState), heuristic)

end = time.time()

print("That took", end-start, "time to run")
