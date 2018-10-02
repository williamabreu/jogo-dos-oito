import math, bisect
from .node import Node


class Board:
    """
    Representa o estado do tabuleiro.
    """
    def __init__(self, matrix, goal):
        """
        Instancia um novo tabuleiro.

        :param matrix: a matriz que representa o estado inicial do tabuleiro, numerada de 0 a 8, sendo 0 o vazio. (type: list)
        :param goal: a matriz que representa o estado inicial do tabuleiro, numerada de 0 a 8, sendo 0 o vazio. (type: list)
        """
        self._size = size = 3

        # validação da entrada matrix
        temp = []
        for line in matrix:
            temp.extend(line)
        temp.sort()
        if len(temp) != 9 or temp != list(range(size**2)):
            raise ValueError("Invalid matrix on constructor")
        
        # validação da entrada goal
        temp = []
        for line in goal:
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
        
        # posições finais do jogo (y, x)
        self.goals = {}
        for i in range(len(goal)):
            for j in range(len(goal[i])):
                self.goals[goal[i][j]] = (j, i)
    
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
                string += ' '
                if element == 0:
                    string += '    '
                else:
                    string += str(element) + '   '
            string += '\n\n'
        return string[:-2]