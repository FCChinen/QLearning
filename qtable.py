"""
Q-Learning algorithm based on:
    Q-Learning Explained - A Reinforcement Learning Technique
    youtube.com/watch?v=RNvCVVJaA&ab_channel=deeplizard
    or:
    https://deeplizard.com/learn/video/qhRNvCVVJaA

What is necessary to this algorithm works?
Q-Table: Is a table(Or a matrix) that contains the reward value of every action that the agent may take. It is initially zero, because the agent does not know anything about the environment.
Update Q-Table function: Everytime that the agent takes an action, the Q-Table must be updated to the value of the taken action. This way, the agent can learn when exploring.
Epsilon Greedy(e): This variable is to define when to EXPLORE or to EXPLOIT. It means that when you know nothing about the environment you should explore(update the Q-Table with valid values) and when the Q-Table has enough information, you should EXPLOIT, so you know where to go to maximize the the reward function. The epsilon usually is initially set to 1(100% probability that the agent will explore) and eventually this value is decreased, increasing the chance to the EXPLOIT what it had already learned. So the more they explore the more greedy they become to exploit!
RNG: To evalute if the agent will either explore or exploit, we generate a random number -> if RNG < e then explore else exploit.
Alpha: Denotes the learning rate. This parameter indicates how easily it will the new Q-Value will overwrite the old Q-Value.

New Q-Value Equation:
 q_new = (1 - Alpha) * q_old + Alpha * LearnedValue

Learned Value: Is the current reward plus the discount factor multiplied per the maximum reward of the next action.


Is a good thing to do a Max steps, in case the of some interation takes too much steps to terminate.
q(s', a')
s -> s'
Author: Felipe C Chinen
"""

import numpy as np
import random as rd

class qtable:
    """
    v0 are the initial values for the Q-Table.
    """
    def __init__(self, v0 = {}, alpha = 0.7 , discount = 0.99, egreedy = 1):
        self.values = v0 # QTable
        self.alpha = alpha
        self.discount = discount
        self.egreedy = egreedy

    def explore(self, actions, cur_state):
        choice = rd.randint(0, actions.size -1)
        return actions[choice]

    def exploit(self, actions, cur_state):
        _, action = self.max_q_next_state(actions, cur_state)
        return action


    def max_q_next_state(self, actions, cur_state):
        max_q = float('-inf') # minus infinite for the first max_q
        best_action = -7
        #print(str(actions))
        for action in actions:
            print("cur_q: "+ str(action) + " " + str(cur_state))
            cur_q = self.values[cur_state][action]
            if cur_q > max_q:
                max_q = cur_q
                best_action = action
        if max_q == float('-inf'):
            print('Bug no MAX Q NEXT STATE')
        return max_q, best_action

    def update_q(self, q_state, next_actions, taken_action,cur_reward):
        #learned value
        best_q, best_action = self.max_q_next_state(next_actions, q_state)
        l_value = cur_reward + best_q

        # new Q = 1 - alpha & old Q + alfa * learned value
        self.values[q_state][taken_action] = (1-self.alpha)*self.values[q_state][best_action] + self.alpha*(l_value)

    def choose_action(self, actions, cur_state):
        if rd.random() < self.egreedy: # RNG to check if either is going to explore or going to exploit.
            return self.explore(actions, cur_state)
        else:
            return self.exploit(actions, cur_state)

    def print_qtable(self):
        print(str(self.values))