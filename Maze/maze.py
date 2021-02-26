"""
Labirinto no qual o lagarto deve passar por obstáculos até chegar no ponto final
O labirinto é uma matriz N+1xN+1, no qual N é passado por parâmetro pelo usuário,
No qual N deve ser maior ou igual a 4. Pois senão, não é possivel adicionar obstáculos para obstruir a passagem do agente.

Orientação dos eixos do labirinto:
    -> x (Cresce para direita)
    \/ y (Cresce para baixo)

Autor: Felipe Churuyuki Chinen
"""
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class Maze(tk.Tk, object):
    def __init__(self, N, pixels = 40, p0_lizard = [1,1]):
        super(Maze, self).__init__()
        # Tamanho do labirinto
        self.N = N
        # Quantos pixels terão cada quadrado
        self.pixels = pixels
        self.sum_reward = 0
        # Informações sobre os obstáculos/árvores
        self.trees = np.array([]) # Lista que contém a tupla [x,y] da posição de cada árvore
        self.trees_widgets = [] # Contém o widget de cada árvore
        self.img_tree = None
        self.create_trees() # Função que popula a lista self.trees
        # self.img_treeobstacle = None # 

        # Informações sobre o grilo
        self.cricket_pos = np.array([self.N - 2, self.N - 2])
        self.img_cricket = None

        # Informações sobre o lagarto
        self.lizard_pos = np.array(p0_lizard)
        self.lizard_p0 = np.array(p0_lizard)
        self.lizard_widget = None
        self.img_lizard = None

        self.step_img = None

        # Criando o ambiente visual
        self.create_visual()
        
    # PARTE GRÁFICA

    def print_trees(self):
        print(str(self.trees))

    def create_visual_trees(self):
        img_tree = Image.open("imgs/treeconverted.png")
        self.img_treeobstacle = ImageTk.PhotoImage(img_tree)
        for tree_pos in self.trees:
            tree_widget = self.canvas_widget.create_image(self.pixels * tree_pos[0], self.pixels * tree_pos[1], anchor = 'nw', image=self.img_treeobstacle)
            self.trees_widgets.append(tree_widget)

    def create_visual_cricket(self):
        self.img_cricket = Image.open("imgs/cricketconverted.png")
        self.img_cricket = ImageTk.PhotoImage(self.img_cricket)
        self.cricket_widget = self.canvas_widget.create_image(self.pixels * self.cricket_pos[0], self.pixels * self.cricket_pos[1], anchor = 'nw', image=self.img_cricket)
        
    def create_visual_lizard(self):
        img_lizard = Image.open("imgs/lizardconverted.png")
        self.img_lizard = ImageTk.PhotoImage(img_lizard)
        self.lizard_widget = self.canvas_widget.create_image(self.pixels * self.lizard_pos[0], self.pixels * self.lizard_pos[1], anchor = 'nw', image=self.img_lizard)

    def create_visual_step(self, best_trajectory):
        img_step = Image.open("imgs/footstepconverted.png")
        self.step_img = ImageTk.PhotoImage(img_step)
        intial_pos = self.lizard_p0
        for action in best_trajectory:
            if action == 0: # Para cima
                intial_pos[1] += self.pixels
                
                self.step_widget = self.canvas_widget.create_image(self.pixels * intial_pos[0], self.pixels * intial_pos[1], anchor = 'nw', image=self.step_img)

            elif action == 1: # Para baixo
                intial_pos[1] -= self.pixels
                self.step_widget = self.canvas_widget.create_image(self.pixels * intial_pos[0], self.pixels * intial_pos[1], anchor = 'nw', image=self.step_img)


            elif action == 2: # Para esquerda
                intial_pos[0] -= self.pixels
                self.step_widget = self.canvas_widget.create_image(self.pixels * intial_pos[0], self.pixels * intial_pos[1], anchor = 'nw', image=self.step_img)

            else: # para direita
                intial_pos[0] += self.pixels
                self.step_widget = self.canvas_widget.create_image(self.pixels * intial_pos[0], self.pixels * intial_pos[1], anchor = 'nw', image=self.step_img)

    def create_visual(self):
        self.canvas_widget = tk.Canvas(self,  bg='white',
                                       height=self.N * self.pixels,
                                       width=self.N * self.pixels)

        # Creating grid lines
        self.create_visual_trees()
        self.create_visual_cricket()
        self.create_visual_lizard()
        for column in range(0, self.N * self.pixels, self.pixels):
            x0, y0, x1, y1 = column, 0, column, self.N * self.pixels
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')
        for row in range(0, self.N * self.pixels, self.pixels):
            x0, y0, x1, y1 = 0, row, self.N * self.pixels, row
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')
        
        # Packing everything
        self.canvas_widget.pack()

    def create_trees(self):
        """
        Como o labirinto é uma matriz quadrada, devemos definir quais ações são possíveis em cada quadrado.
        Estou definindo que nas bordas do labirinto, haverá árvores, assim como na em sua diagonal
        """
        trees = []
        for tree in range(0, self.N):
            trees.append([tree, 0]) # Criando árvores da borda inferior
            trees.append([tree, self.N-1]) # Criando árvores da borda superior
            trees.append([self.N-1, tree]) # Criando árvores da borda lateral direita
            trees.append([0, tree]) # Criando árvores da borda lateral da esquerda
            if tree != self.N - 2:
                trees.append([self.N - tree -1, tree]) # Criando árvores na diagonal
        self.trees = trees # Tirando as duplicatas


    # A função que atualiza o ambiente
    def render(self):
        self.update()

    # Reseta o ambiente após a finalização do jogo(No final de cada episódio).
    def reset(self):
        
        self.sum_reward = 0
        # Updating agent
        self.canvas_widget.delete(self.lizard_widget)
        self.lizard_pos = self.lizard_p0
        self.lizard_widget = self.canvas_widget.create_image(self.pixels * self.lizard_pos[0], self.pixels * self.lizard_pos[1], anchor = 'nw', image=self.img_lizard)
        self.update()

        # Return observation
        #return self.canvas_widget.coords(self.agent)

    def render_best_trajectory(self, best_trajectory):
        self.canvas_widget.delete(self.lizard_widget)
        self.create_visual_step(best_trajectory)

    # LÓGICA DO JOGO

    def get_next_pos(self, action):
        a = np.array([0, 0])
        if action == 0: # Para cima
            a[1] += self.pixels
            self.canvas_widget.move(self.lizard_widget,a[0], a[1])
            return self.lizard_pos + [0,1]
        elif action == 1: # Para baixo
            a[1] -= self.pixels
            self.canvas_widget.move(self.lizard_widget,a[0], a[1])
            return self.lizard_pos - [0,1]
        elif action == 2: # Para esquerda
            a[0] -= self.pixels
            self.canvas_widget.move(self.lizard_widget,a[0], a[1])
            return self.lizard_pos - [1,0]
        else: # para direita
            a[0] += self.pixels
            self.canvas_widget.move(self.lizard_widget,a[0], a[1])
            return self.lizard_pos + [1,0]
            
        # Chamar a função que atualiza a posição do lagarto(Para a parte visual)

    def update_lizard_pos(self, new_pos):
        self.lizard_pos = new_pos

    def get_lizard_pos(self):
        return self.lizard_pos

    def get_cricket_pos(self):
        return self.cricket_pos


    def posible_actions(self, cur_pos):
        """
        Definimos a ação da seguinte maneira:
        1 - Andar para baixo
        2 - Andar para cima
        3 - Andar para esquerda
        4 - Andar para direita

        Para verificar as possíveis ações, devemos então verificar o que tem nos objetos adjacentes ao agente.
        Assim:
        Se cur_pos + [0,1](Andar para cima) == árvore
        OU
        Se cur_pos - [0,1](Andar para baixo) == árvore
        OU
        se cur_pos - [1,0](Andar para esquerda) == árvore
        OU
        Se cur_pos + [1,0](Andar para direita) == árvore
        Então
        Remove ação
        """
        actions = np.array([0, 1, 2, 3]) # A priori, todas as ações são possiveis
        for tree_pos in self.trees:
            if np.array_equal(cur_pos + [0,1], tree_pos): # Para baixo
                actions = np.delete(actions, np.argwhere(actions == 0))
            if np.array_equal(cur_pos - [0,1], tree_pos): # Para cima
                actions = np.delete(actions, np.argwhere(actions == 1))
            if np.array_equal(cur_pos - [1,0], tree_pos):# Para esquerda
                actions = np.delete(actions, np.argwhere(actions == 2))
            if np.array_equal(cur_pos + [1,0], tree_pos): # Para direita
                actions = np.delete(actions, np.argwhere(actions == 3))
        return actions

    def last_reward(self):
        if np.array_equal(self.lizard_pos, self.cricket_pos):
            self.sum_reward += 10

    def get_reward(self):
        if np.array_equal(self.lizard_pos, self.cricket_pos):
            self.sum_reward += 10
            return 10
        else:
            self.sum_reward -= 1
            return -1

    def terminate(self):
        if np.array_equal(self.lizard_pos, self.cricket_pos):
            print("Sua recompensa total foi: "+str(self.sum_reward))
            return True
        else:
            return False

    def t(self):
        GG = False
        while GG == False:
            self.render()
            print("actions: "+str(self.posible_actions(self.lizard_pos)))
            action = int(input("digite sua action: 0 up 1 down 2 left 3 right"))
            self.update_pos(action)
            GG = self.terminate()
        self.reset()
        GG = False
        while GG == False:
            self.render()
            print("actions: "+str(self.posible_actions(self.lizard_pos)))
            action = int(input("digite sua action: 0 up 1 down 2 left 3 right"))
            self.update_pos(action)
            GG = self.terminate()

    def get_sum_reward(self):
        return self.sum_reward

if __name__ == '__main__':
    maze = Maze(5)
    maze.t()
    maze.mainloop()