"""
Author - Thomas Pollard
This module uses pygame to display Robby the Robot.

It takes a grid as an argument where empty spaces are 0, cans are 1,
Robby is 2, and spaces with a can AND Robby is 3. You can modify the
draw conditionals in the render function to match your grid output.

You can either compile a list of grids and watch the whole episode with the
watchEpisode function, or you can call render on your grid during each step
that you want to observe.

Be sure to call quit() after your program is done.

======== USAGE EXAMPLES ========
1. Calling render function to draw each step every 100 episodes.

  for step in range(STEP_LIMIT):
    if episode % 100 == 0:
      watchrobby.render(robby.grid, episode, step)
    robby.doStep()

2. Calling watchEpisode function to watch a sequence of steps for an episode.

  sequence = []
  for step in range(STEP_LIMIT):
    if episode % 100 == 0:
      sequence.append(robby.grid.tolist()[:])
    robby.doStep()
  if episode % 100 == 0:
    watchrobby.watchEpisode(sequence, episode)
"""

import pygame

WIDTH = 50
HEIGHT = 50
MARGIN = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60
GRID_WIDTH = 10
GRID_HEIGHT = 10

clock = pygame.time.Clock()
pygame.init()
WINDOW_SIZE = [555, 555]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Robby the robot")
screen.fill(BLACK)

def watchEpisode(gridSequence, episode):
  """
  Pass in a list of grids, one for each step in the episode, as well as the episode number.
  If using a numpy array to encapsulate the grid, call tolist() on it before storing
  it in the sequence list. See usage example 2.
  """
  for step, grid in enumerate(gridSequence):
    pygame.display.set_caption("Robby the robot episode: " + str(episode) + " step: " + str(step))
    render(grid, episode, step)

  
def render(grid, episode, step):
  """
  Pass in a grid to be rendered, will only draw one step and will need to be called each step.
  See usage example 1.
  """
  pygame.display.set_caption("Robby the robot episode: " + str(episode) + " step: " + str(step))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
  for row in range(GRID_HEIGHT):
    for column in range(GRID_WIDTH):
      if grid[column][row] >= 2:
        color = RED
      else:
        color = WHITE
      pygame.draw.rect(screen,color,[(MARGIN + WIDTH) * column + MARGIN,(MARGIN + HEIGHT) * row + MARGIN,WIDTH,HEIGHT])
      if grid[column][row] % 2 == 1:
        color = BLACK
        pygame.draw.circle(screen,color,((MARGIN + WIDTH) * column + MARGIN + int(WIDTH/2),(MARGIN + HEIGHT) * row + MARGIN + int(HEIGHT/2)),int(WIDTH/4))
  clock.tick(FPS)
  pygame.display.flip()

def quit():
  pygame.quit()
