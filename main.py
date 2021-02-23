from game import lizardgame
from qtable import qtable
import numpy as np
from os import system
import time
import pprint
import matplotlib.pyplot as plt

# Defining the variables
"""

Validar trajetória
fazer graficos
comentar melhor o código
melhorar o jogo

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

    0 = empty_0
    1 = empty_1
    2 = five_crickets
    3 = empty_3
    4 = bird
    5 = empty_ 5    
    6 = one_cricket 
    7 = empty_7 
    8 = empty_8 

"""

def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

system('clear')
q_values = {
    0 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
    , 1 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
    , 2 : { 1 : 10, 2 : 0, 3 : 0, 4 : 0}
    , 3 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
    , 4 : { 1 : -10, 2 : 0, 3 : 0, 4 : 0}
    , 5 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
    , 6 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
    , 7 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
    , 8 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
}
print("dict: " + str(q_values))

n_iterations = 200
table = qtable(v0 = q_values, decay_rate=0.9, min_steps=n_iterations)

cur_step = 1
best_score = 0
won = 0
loss = 0
still_learning = True
gg = False # Termina o jogo
terminate = False # Termina o algoritmo

trajectory = []
score_y = []


while terminate == False:
    G = lizardgame()
    gg = False
    old_pos = -99
    last_action = -99
    while gg == False:
        for print_i in range(6,-1, -3):
            for i in range(0, 3):
                j = print_i + i
                if j == G.get_lizardpos():
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
        G.print_reward()
        print("Score: " + str(G.get_sum_reward()))
        if (old_pos != -99):
            print('old pos: '+str(old_pos) + ' last action: ' + str(last_action))
        print('You are in '+ str(G.get_lizardpos()))
        
        old_pos = G.get_lizardpos()
        #time.sleep(1)
        actions = G.posible_action(old_pos)
        if old_pos != 2 and old_pos != 4:
            """
            Q Learning Answer
            """
            a = table.choose_action(actions, G.get_lizardpos())
            last_action = a
            print('chosen action' +str(last_action))
            next_s_a = []
            # new_pos = s'
            new_pos = G.new_pos(a, old_pos)
            # candidates_next_action = candidates to be a'
            candidates_next_action = G.posible_action(new_pos)
            next_s_a.append([new_pos, candidates_next_action])
            table.update_q(next_s_a, a,G.get_lizardpos(), G.reward_cur_pos())
            G.update_lizardpos(new_pos)
            trajectory.append(a)
            #system('clear')
        else:
            a = table.choose_action(actions, G.get_lizardpos())
            last_action = a
            print('chosen action' +str(last_action))
            next_s_a = []
            # new_pos = s'
            new_pos = G.new_pos(a, old_pos)
            # candidates_next_action = candidates to be a'
            candidates_next_action = G.posible_action(new_pos)
            next_s_a.append([new_pos, candidates_next_action])
            G.reward_cur_pos()
            # table.update_q(next_s_a, a,G.get_lizardpos(), G.reward_cur_pos())
            #G.update_lizardpos(a, old_pos)
            score = G.get_sum_reward()
            score_y.append(score)
            if cur_step > 700:
                table.update_trajectory_list(trajectory, score) # Só adiciona na lista de trajetórias se convergiu
            #print('Lista de Trajetórias: ' + str(table.unique_trajectory))
            print('Última trajetória: ' + str(trajectory))
            trajectory = []
            table.print_qtable()
            if score > 0:
                won += 1
            else:
                loss += 1
            if best_score < score:
                best_score = score
            cur_step+=1
            print("step: " + str(cur_step))
            terminate = table.check_threshold(cur_step)
            print('Egreedy = ' + str(table.egreedy))
            gg = True
        print("QTable:")
        table.print_qtable()
"""
x = np.arange(1, len(score_y))
plt.plot(score_y)
plt.show()
"""


#y_av = movingaverage(score_y, 20)
plt.plot(score_y,"r")
plt.show()