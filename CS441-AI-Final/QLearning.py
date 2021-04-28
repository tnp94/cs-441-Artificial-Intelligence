"""
CS 441 Group Final Project

Thomas Pollard
Michael Kay
David Hawbaker
Gregory Hairfield
Andrew Ruskamp-White

"""
import gym
import numpy as np
import random

EPSILON = 1
ETA = 0.2
GAMMA = 0.9  # Rate of discount.
EPISODES = 100000
MAX_STEPS = 100

class QLearningAgent():
    def __init__(self, actionSpaceSize, observationSpaceSize):
        self.actions = list(range(actionSpaceSize))
        # Changing default to -100 to help with late episode oscillations btwn two states not prev visited.
##        self.QMatrix = np.full((observationSpaceSize, actionSpaceSize), -100)
##        self.QMatrix = np.random.rand(observationSpaceSize, actionSpaceSize)
        self.QMatrix = np.zeros((observationSpaceSize, actionSpaceSize))
        # the two represents two items we're saving: Running average and the number of times the State/Action pair
        # have been visited. [0] is running average [1] is number of visits.

    def chooseAction(self, observation):
        # Epsilon greedy policy
        # Choose the best option available or choose random at probability of epsilon
        if random.random() <= EPSILON:
            actionIndex = random.choice(self.actions)
        else:
            # get a list of actions that have the max value, randomly choose one of those
            choices = np.where(self.QMatrix[observation] == max(self.QMatrix[observation]))[0]
            actionIndex = random.choice(choices)
        return actionIndex

                
    def updateQMatrix(self, lastState, observation, action, reward):
        lastValue = self.QMatrix[lastState, action]
        self.QMatrix[lastState, action] = lastValue + ETA*(reward + GAMMA*(max(self.QMatrix[observation]))-lastValue)
        pass





def customRender(self, mode='human'):
    out = self.desc.copy().tolist()
    out = [[c.decode('utf-8') for c in line] for line in out]
    taxi_row, taxi_col, pass_idx, dest_idx = self.decode(self.s)

    def ul(x): return "_" if x == " " else x
    if pass_idx < 4:
        out[1 + taxi_row][2 * taxi_col + 1] = '○'

        pi, pj = self.locs[pass_idx]
        out[1 + pi][2 * pj + 1] = out[1 + pi][2 * pj + 1].lower()
    else:  # passenger in taxi
        out[1 + taxi_row][2 * taxi_col + 1] = '◙'

    di, dj = self.locs[dest_idx]
    out[1 + di][2 * dj + 1] = out[1 + di][2 * dj + 1].lower()
    print("\n".join(["".join(row) for row in out]) + "\n")
    if self.lastaction is not None:
        print(["South", "North", "East", "West", "Pickup", "Dropoff"][self.lastaction])
    else:
        print("\n")
        
file = open('qLearnData.csv', 'w')
env = gym.make('Taxi-v3')
env.render = customRender

qLearn = QLearningAgent(env.action_space.n, env.observation_space.n)

for i_episode in range(EPISODES):
    done = False
    EPSILON = EPSILON-(1.0/EPISODES)
    observation = env.reset()
    totalReward = 0
    for t in range(MAX_STEPS):
        lastState = observation
        action = qLearn.chooseAction(observation)
        observation, reward, done, info = env.step(action)
        totalReward += reward

        qLearn.updateQMatrix(lastState, observation, action, reward)
        if done:
##            print("Episode", i_episode+1, "finished after", t+1, "timesteps. Final Reward:", totalReward)
            break
    if i_episode % 100 == 0:
##        print("Episode", i_episode+1, "finished after", t+1, "timesteps. Final Reward:", totalReward)
        file.write(f'{i_episode+1},{totalReward}\n')

    
##    if i_episode % 5000 == 0:
##        print("Episode recap:\nState\t|\tReward")
##        for i in range(len(statesVisited)):
##            print(statesVisited[i], "\t|\t",stateRewards[i])
env.close()
file.close()
