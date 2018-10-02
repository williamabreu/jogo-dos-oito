import copy


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
