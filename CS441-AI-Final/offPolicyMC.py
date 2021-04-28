"""
CS 441 Group Final Project
Off Policy Method

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
GAMMA = 0.9  # Rate of discount.
EPISODES = 100000
MAX_STEPS = 100


class MonteCarloLearningAgent:

    def __init__(self, action_space_size, observation_space_size):
        self.actions = list(range(action_space_size))
        self.QMatrix = np.random.rand(observation_space_size, action_space_size)
        self.cumulative_weights = np.full((observation_space_size, action_space_size), 1)
        self.totalReward = 0
        self.totalWeight = 1

    @staticmethod
    def choose_action_training():
        """ The behavior policy is to select a random action from the available ones
        This has full coverage of the off policy that we are training.
        There are 6 possible actions from all states
            - 0: move south
            - 1: move north
            - 2: move east
            - 3: move west
            - 4: pickup passenger
            - 5: drop off passenger

        :return: Action index to take
        """
        return random.choice(list(range(6)))

    def choose_action_trained(self, state):
        """ Selects the action based on the best action according to the trained policy

        :param state: The current state
        :return: Action index to take
        """
        return np.argmax(self.QMatrix[state])

    def update_values_first_visit(self, states, rewards, actions):
        """ Updates the values for the the states once the run is complete.
        Only give a reward for the last (most recent) time that state was seen in the run.

        :param states: The states taken
        :param rewards: The rewards to give to the state
        :param actions: The action taken from that state
        :return: None
        """
        # Value of reward returned from each time step
        ret_g = 0
        self.totalWeight = 1
        firstVisitDict = {}
        # Get the index of each state. Starting from the end
        for idx in reversed(range(len(states))):
            ret_g = GAMMA * ret_g + rewards[idx]
            if (states[idx], actions[idx]) not in firstVisitDict:
                firstVisitDict[(states[idx], actions[idx])] = 1
                self.cumulative_weights[states[idx]][actions[idx]] += self.totalWeight
                state_action_weight = self.cumulative_weights[states[idx]][actions[idx]]
                q_value = self.QMatrix[states[idx]][actions[idx]]
                new_q_value = q_value + (self.totalWeight/state_action_weight) * (ret_g - q_value)
                self.QMatrix[states[idx]][actions[idx]] = new_q_value

                if actions[idx] == int(np.where(self.QMatrix[states[idx]] == max(self.QMatrix[states[idx]]))[0][0]):
                    # W * 1/ (b(At|St)  # Where b(At|St) is 1/6 because there are 6 actions randomly chosen
                    self.totalWeight = self.totalWeight * (1/(1/6))


def custom_render(self, mode='human'):
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


if __name__ == '__main__':
    #file = open('offPolicyData_training.csv', 'w')
    env = gym.make('Taxi-v3')
    env.render = custom_render

    monteCarlo = MonteCarloLearningAgent(env.action_space.n, env.observation_space.n)

    # Training
    for i_episode in range(EPISODES):
        done = False
        EPSILON = EPSILON-(1.0/EPISODES)
        observation = env.reset()
        statesVisited = []
        stateRewards = []
        actions_taken = []
        monteCarlo.totalReward = 0
        monteCarlo.totalWeight = 1

        for t in range(MAX_STEPS):
            if monteCarlo.totalWeight == 0:
                break
            ##        if i_episode % 5000 == 0:
            ##            env.render(env)
            ##            print(observation, "\n\n--------------------------------------")
            action = monteCarlo.choose_action_training()
            observation, reward, done, info = env.step(action)

            statesVisited.append(observation)
            actions_taken.append(action)
            stateRewards.append(reward)
            monteCarlo.totalReward += reward
            if done:
                #print("Episode", i_episode+1, "finished after", t+1, "time steps. Final Reward:", monteCarlo.totalReward)
                break

        #if done or i_episode % 100 == 0:
        #    file.write(f'{i_episode+1},{monteCarlo.totalReward}\n')

        monteCarlo.update_values_first_visit(statesVisited, stateRewards, actions_taken)

    ##    if i_episode % 5000 == 0:
    ##        print("Episode recap:\nState\t|\tReward")
    ##        for i in range(len(statesVisited)):
    ##            print(statesVisited[i], "\t|\t",stateRewards[i])
    #file.close()

    # Trained Runs
    file = open('offPolicyData_trained.csv', 'w')

    for i_episode in range(EPISODES):
        done = False
        EPSILON = 0.1
        observation = env.reset()
        statesVisited = []
        stateRewards = []
        actions_taken = []
        monteCarlo.totalReward = 0

        for t in range(MAX_STEPS):
            action = monteCarlo.choose_action_trained(observation)
            observation, reward, done, info = env.step(action)
            # statesVisited.append(observation)
            # actions_taken.append(action)
            # stateRewards.append(reward)
            monteCarlo.totalReward += reward

            if i_episode == 99990:
                print(f"State: {observation} Action: {action} Reward: {reward}")
            if done:
                #print("Episode", i_episode+1, "finished after", t+1, "time steps. Final Reward:", monteCarlo.totalReward)
                break

        if done or i_episode % 100 == 0:
            file.write(f'{i_episode+1},{monteCarlo.totalReward}\n')


    env.close()
    file.close()
