from game import lizardgame
from qtable import qtable
import numpy as np
from os import system
import time
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
system('clear')
q_values = {
    0 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
    , 1 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
    , 2 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
    , 3 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
    , 4 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
    , 5 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
    , 6 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
    , 7 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
    , 8 : { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
}
print("dict: " + str(q_values))

table = qtable(q_values)

max_step = 20
cur_step = 0
best_score = 0
won = 0
loss = 0
step_only_exploit = -1
still_learning = True

while cur_step <= max_step:
    # 1 iteration of the game
    G = lizardgame()
    gg = False
    old_pos = -99
    last_action = -99
    decay_rate = 0.01 # 
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
        if (old_pos != -99):
            print('old pos: '+str(old_pos) + ' last action: ' + str(last_action))
        print('You are in '+ str(G.get_lizardpos()))
        print("step: " + str(cur_step))
        old_pos = G.get_lizardpos()
        #time.sleep(1)
        actions = G.posible_action()
        if not(G.check_end()): 
            #print(actions)
            # a = int(input('What action do you want to take?'))
            """
            Q Learning Answer
            """
            a = table.choose_action(actions, G.get_lizardpos())
            last_action = a
            table.update_q(G.get_lizardpos(), G.posible_action(), a, G.reward_cur_pos())
            G.update_lizardpos(a, old_pos)
            #system('clear')
        else:
            print('G G')
            score = G.get_sum_reward()
            table.print_qtable()
            if score > 0:
                won += 1
            else:
                loss += 1
            if best_score < score:
                best_score = score
            gg = True
    new_egreedy = table.egreedy - decay_rate # multiplicar ao invés de subtrair
    if new_egreedy >= 0:
        table.egreedy = new_egreedy
        print(str('egreedy: '+str(table.egreedy)))
    elif still_learning == True:
        still_learning = False
        step_only_exploit = cur_step
    cur_step+=1

        

print('won: ' + str(won) + ' times of ' + str(max_step) + ' total tries')
print('best score: ' + str(best_score))
print('stop learning at iteration: ' + str(step_only_exploit))