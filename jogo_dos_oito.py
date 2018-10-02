# -*- coding: utf-8 -*-

import copy
import math
import bisect


class Node:
    """
    Representa um nó no grafo A*.
    """
    def __init__(self, board, action, cost, parent):
        """
        Instancia um novo nó A*.

        :param board: o estado do tabuleiro (type: Board)
        :param action: a ação que leva de volta ao nó anterior (type: 2-tuple)
        :param cost: o custo total do caminho desde o nó inicial até este, componente "g" de A* (type: int)
        :param parent: o nó anterior (type: Node)
        """
        self.board = board
        self.action = action
        self.cost = cost
        self.parent = parent
        self.estimate = cost + board.h() # função "f" de A*
    
    def expand(self):
        """
        Retorna a lista de nós possíveis para ir a partir daqui.
        """
        nodes = []

        for action in self.board.valid_moves():
            board = copy.deepcopy(self.board)
            board.move(action)

            nodes.append(Node(board, action, self.cost + 1, self))
        
        return nodes

    def __eq__(self, rhs):
        """
        Verificação de igualdade entre nós pela configuração do tabuleiro.
        """        
        if isinstance(rhs, Node):
            return self.board._tiles == rhs.board._tiles
        else:
            return rhs == self

    def __lt__(self, rhs):
        """
        Verificação de ordenação entre nós pela estimativa "f" de A*.
        """
        return self.estimate < rhs.estimate


class Board:
    """
    Representa o estado do tabuleiro.
    """
    def __init__(self, matrix):
        """
        Instancia um novo tabuleiro.

        :param matrix: a matriz que representa o estado inicial do tabuleiro, numerada de 0 a 8, sendo 0 o vazio. (type: list)
        """
        self._size = size = 3

        # validação da entrada
        temp = []
        for line in matrix:
            temp.extend(line)
        temp.sort()
        if len(temp) != 9 or temp != list(range(size**2)):
            raise ValueError("Invalid matrix on constructor")
        
        self._tiles = matrix

        # posição do espaço vazio
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    self._empty = (j, i)
        
        # posições finais do jogo
        self.goals = {
            1: (0, 0), 
            2: (1, 0), 
            3: (2, 0), 
            4: (0, 1), 
            5: (1, 1), 
            6: (2, 1), 
            7: (0, 2), 
            8: (1, 2), 
            9: (2, 2), 
            0: (2, 2)
        }
    
    def solve(self):
        """
        Retorna a lista de 2-tuples com os movimentos para resolver o jogo.
        """
        frontier = [Node(self, None, 0, None)]
        explored = []

        while True:
            # pop the lowest value from the frontier (sorted using bisect, so pop(0) is the lowest)
            node = frontier.pop(0)

            # if the current node is at the goal state, we're done! 
            if node.board.h() == 0:
                # recursively compile a list of all the moves
                moves = []
                while node.parent:
                    moves.append(node.action)
                    node = node.parent
                moves.reverse()

                return moves 
            else:
                # we're not done yet:
                # expand the node, and add the new nodes to the frontier, as long
                # as they're not in the frontier or explored list already
                for new_node in node.expand():
                    if new_node not in frontier and new_node not in explored:
                        # use bisect to insert the node at the proper place in the frontier
                        bisect.insort(frontier, new_node)
                
                explored.append(node)
    
    def h(self):
        """
        Função "h" heurística de A*, retorna a distância de Manhattan 
        entre a posição atual e a posição final no jogo.
        """
        h = 0
        for y, row in enumerate(self._tiles):
            for x, tile in enumerate(row):
                h += math.fabs(x - self.goals[tile][0]) + \
                     math.fabs(y - self.goals[tile][1])
        return h
    
    def move(self, position):
        """
        Muda o estado do tabuleiro movendo o espaço branco para a posição dada.

        :param position: a posição para onde deve ir (type: 2-tuple)
        """
        x, y = position
        e_x, e_y = self._empty

        # valida se a posição de movimento e o espaço braco são vizinhos
        if (math.fabs(x - e_x) == 1) ^ (math.fabs(y - e_y) == 1):
            # troca os dois de lugar
            self._tiles[y][x], self._tiles[e_y][e_x] = 0, self._tiles[y][x]
            self._empty = x, y # atualiza a posição do espaço branco
        else:
            raise ValueError("Invalid move")

    def valid_moves(self):
        """
        Retorna a lista de posições posíveis para onde o espaço branco pode ir.
        """
        x, y = self._empty
        valid_moves = []

        if x > 0: 
            valid_moves.append((x - 1, y))
        if y > 0: 
            valid_moves.append((x, y - 1))
        if x < self._size - 1: 
            valid_moves.append((x + 1, y))
        if y < self._size - 1: 
            valid_moves.append((x, y + 1))

        return valid_moves
    
    def __str__(self):
        """
        Representação do tabuleiro em string.
        """
        string = ''
        for i in range(len(self._tiles)):
            for j in range(len(self._tiles[i])):
                element = self._tiles[i][j]
                if element == 0:
                    string += '  '
                else:
                    string += str(element) + ' '
            string += '\n'
        return string
            




if __name__ == '__main__':
    matrix = [
        [1,8,7],
        [3,5,0],
        [4,6,2]
    ]
    b = Board(matrix)
    s = b.solve()
    print(b)
    for move in s:
        raw_input()
        b.move(move)
        print(b)
