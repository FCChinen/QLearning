"""
Q-Learning algorithm based on:
    Q-Learning Explained - A Reinforcement Learning Technique:
    
    youtube.com/watch?v=RNvCVVJaA&ab_channel=deeplizard
    
    or:

    https://deeplizard.com/learn/video/qhRNvCVVJaA
Author: Felipe C Chinen
"""
import numpy as np
import random as rd


class qtable:
    """
    v0 are the initial values for the Q-Table.
    """
    def __init__(self, v0 = {}, alpha = 0.7 , discount = 0.99, egreedy = 1, decay_rate = 0.1, min_steps = 1000):
        self.values = v0 # QTable
        self.alpha = alpha # Taxa de aprendizado
        self.discount = discount # Taxa de desconto
        self.egreedy = egreedy # Epsilon Greedy
        self.decay_rate = decay_rate # Taxa de decaimento

        # As variáveis daqui para frente, são apenas para verificar performance

        self.trajectories = [] # Lista que conterá as trajetórias que irão conter cada estado percorrido
        self.stop_rate = 0.025 # Fator adicionado, quando a trajetória passar de fator, o algoritmo irá finalizar e irá printar a melhor trajetória e o seu melhor resultado
        self.min_steps = min_steps
        self.unique_trajectory = [] # Lista que contém as trajetórias sem repetição
        self.trajectories_score = {} # Dicionário que contém os scores de cada trajetória.
        self.n_best_values = 3 # 


    def explore(self, actions, cur_state):
        choice = rd.randint(0, actions.size -1)
        return actions[choice]

    def exploit(self, actions, cur_state):
        _, action = self.max_q_next_state(cur_state, actions)
        print('vai explorar: estado: ' + str(cur_state)+ ' ação escolhida: '+ str(action))
        return action


    def max_q_next_state(self, cur_state, actions): # Essa função retorna a próxima ação a ser tomada e o valor da qtable
        max_q = float('-inf') # minus infinite for the first max_q
        best_action = -7
        print("cur state: "+str(cur_state))
        print("actions: "+str(actions))
        for action in actions:
            #print("action: "+ str(action) + " state: " + str(cur_state))
            cur_q = self.values[cur_state][action]
            print('estado = '+ str(cur_state) + ', q = '+str(cur_q) + 'action: ' + str(action))
            if cur_q > max_q:
                max_q = cur_q
                best_action = action
        if max_q == float('-inf'):
            print('Bug no MAX Q NEXT STATE')
        print('melhor action: ' + str(best_action) + ' melhor q: ' + str(max_q))
        return max_q, best_action

    def update_q(self, next_s_a, taken_action, cur_state, cur_reward):
        # next_s_a = Q(s', a') é uma lista que contém a tupla 
        # Calculo do próximo valor da qtable
        # Falta codar a parte do next state!!!
        # Você tem que achar a melhor ação para o próximo estado
        # No momento está achando o do estado corrente!!!!!!
        # só fazer um loop para iterar sobre a tupla estado e ação verificar o melhor e retornar.
        # Provavelmente o algoritmo irá convergir!!
        # Obtendo o melhor q e a melhor ação
        best_q = float('-inf')
        # best_action = -1
        for candidate_best_states in next_s_a:
            s, a = candidate_best_states
            best_q_aux, _ = self.max_q_next_state(s, a)
            if s == 1:
                print('s = 1 a = ' + str(a) + ' q =' + str(best_q_aux))
            if (best_q_aux > best_q):
                best_q = best_q_aux
                #best_action = best_action_aux


        # Obtendo o valor do Valor aprendido(Learning Value)
        l_value = cur_reward + best_q 

        # Equação: new Q = 1 - alpha & old Q + alfa * learned value
        self.values[cur_state][taken_action] = (1-self.alpha)*self.values[cur_state][taken_action] + self.alpha*(l_value)

    def choose_action(self, actions, cur_state):
        self.egreedy *= self.decay_rate # Multiplicando pela taxa de decaimento, aumentando a chance do agente explorar ao invés de aprender
        rng = rd.random()
        print('rng = '+str(rng)+' egreedy = '+str(self.egreedy))
        if rng < self.egreedy: # Compara o fator egreedy com um valor aleatório.
            
            return self.explore(actions, cur_state) # Aprende no caso de ser menor que egreedy
        else:
            return self.exploit(actions, cur_state) # Explora caso seja maior

    # Funções abaixo NÃO pertencem necessariamente ao QLearning, no entanto, é uma maneira para verificar a sua performance

    def print_qtable(self):
        print(str(self.values))

    def update_trajectory_list(self, last_trajectory, score):
        # trajectories.append(last_trajectory)
        if last_trajectory in self.unique_trajectory: # Verifica se a trajetória já está na lista de trajetórias
            self.trajectories_score[self.unique_trajectory.index(last_trajectory)]["count"] += 1 # Se estiver aumenta um no contador
        else:
            self.unique_trajectory.append(last_trajectory) # Se não estiver adicinoa na lista
            self.trajectories_score[self.unique_trajectory.index(last_trajectory)] = {"score" : 0, "count" : 0} # Adiciona um novo valor para a trajetória
            self.trajectories_score[self.unique_trajectory.index(last_trajectory)]["score"] = score # Atribui o valor da sua pontuação
            self.trajectories_score[self.unique_trajectory.index(last_trajectory)]["count"] = 1 # Inicializa o contador como 1

    def check_threshold(self, steps):
        if steps > self.min_steps:
            return True
        else:
            return False