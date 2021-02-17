"""
The game is a 3x3 matrix as described below:

6 7 8
3 4 5
0 1 2

0 = empty_0
1 = empty_1
2 = five_crickets
3 = empty_3
4 = bird
5 = empty_ 5
6 = one_cricket
7 = empty_7
8 = empty_8

The actions that the lizard can take are:
1 = up
2 = down
3 = left
4 = right


Author: Felipe Churuyuki Chinen
"""
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
            return 1
        else:
            self.sum_reward -= 1
            return -1 # Empty tile

    def get_sum_reward(self):
        return self.sum_reward

    def print_reward(self):
        print('Your reward was: ' + str(self.reward_cur_pos()))

    def check_end(self):
        if self.lizardpos == 2 or self.lizardpos == 4:
            return True
        else:
            return False
    
    def posible_action(self):
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

    def update_lizardpos(self, action, old_pos):
        new_pos = -1
        if action == 1: # up
            new_pos = old_pos + 3
        elif action == 2: # down
            new_pos = old_pos - 3
        elif action == 3: # left
            new_pos = old_pos -1
        elif action == 4: # right
            new_pos = old_pos + 1
        
        self.lizardpos = new_pos

    def get_lizardpos(self):
        return self.lizardpos

    # Only for testing purpose
    def game(self):
        gg = False
        while gg == False:
            for print_i in range(6,-1, -3):
                for i in range(0, 3):
                    j = print_i + i
                    if j == self.get_lizardpos():
                        print('L', end = '')
                    elif j == 2:
                        print('5', end = '')
                    elif j == 4:
                        print('B', end = '')
                    elif j == 6:
                        print('1', end = '')
                    else:
                        print('0', end = '')
                    if (j+1)%3 == 0:
                        print('')
            print('')
            self.print_reward()
            print('You are in '+ str(self.get_lizardpos()))
            old_pos = get_lizardpos()
            actions = self.posible_action()
            if not(self.check_end()):
                print(actions)
                a = int(input('What action do you want to take?'))
                self.update_lizardpos(a, old_pos    )
                system('clear')
            else:
                print('G G')
                gg = True