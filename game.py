
import numpy as np
from os import system

class lizardgame:
    def __init__(self, lizardpos0 = 0):
        self.lizardpos = lizardpos0
        self.sum_reward = 0
        """
        if self.lizardpos == 0:
            # Up, right
            return np.array([1,4])
        elif self.lizardpos == 1:
            # Up, left, right
            return np.array([1,3,4])
        elif self.lizardpos == 3:
            # Up, down, right
            return np.array([1,2,4])
        elif self.lizardpos == 5:
            # Up, down, left
            return np.array([1,2,3])
        elif self.lizardpos == 6:
            # Down, right
            return np.array([2,4])
        elif self.lizardpos == 7:
            # Down, left, right
            return np.array([2,3,4])
        elif self.lizardpos == 8:
            # Down, left
            return np.array([2,3])
        """

    def reward_cur_pos(self):
        if self.lizardpos == 2: # Five crickets
            self.sum_reward += 10
            return 10
        elif self.lizardpos == 4: # Bird
            self.sum_reward -= 10
            return -10
        elif self.lizardpos == 6: # One Cricket
            self.sum_reward += 1
            return -1
        else:
            self.sum_reward -= 1
            return -1 # Empty tile

    def get_sum_reward(self):
        return self.sum_reward

    def print_reward(self):
        print('Your reward was: ' + str(self.sum_reward))

    def check_end(self):
        if self.lizardpos == 2 or self.lizardpos == 4:
            return True
        else:
            return False
    
    def posible_action(self, cur_pos):
        if cur_pos == 0:
            # Up, right
            return np.array([1,4])
        elif cur_pos == 1:
            # Up, left, right
            return np.array([1,3,4])
        elif cur_pos == 3:
            # Up, down, right
            return np.array([1,2,4])
        elif cur_pos == 5:
            # Up, down, left
            return np.array([1,2,3])
        elif cur_pos == 6:
            # Down, right
            return np.array([2,4])
        elif cur_pos == 7:
            # Down, left, right
            return np.array([2,3,4])
        elif cur_pos == 8:
            # Down, left
            return np.array([2,3])
        elif cur_pos == 2: # Estado final, essas ações só existem para funcionar o QTable :x
            # Up, left
            return np.array([1, 3])
        else: # Estado final, essas ações só existem para funcionar o QTable :x
            return np.array([1,2,3,4])

    def new_pos(self, action, old_pos):
        if action == 1: # up
            new_pos = old_pos + 3
        elif action == 2: # down
            new_pos = old_pos - 3
        elif action == 3: # left
            new_pos = old_pos -1
        elif action == 4: # right
            new_pos = old_pos + 1
        return new_pos

    def update_lizardpos(self, new_pos):
        self.lizardpos = new_pos

    def get_lizardpos(self):
        return self.lizardpos