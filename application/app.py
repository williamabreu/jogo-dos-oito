from game import Board

class App:
    """
    Representa a aplicação CLI.
    """
    def __init__(self, start_matrix, end_matrix):
        self.board = Board(start_matrix, end_matrix)
        self.solution = None
    
    def solve(self):       
        print('Solving...')
        self.solution = self.board.solve()
        print()
    
    def display_solution(self):
        print('# Initial #'.center(13))
        print()
        print(self.board)
        print()
        
        for i, pos in enumerate(self.solution):
            input('Press ENTER to continue')
            print()
            self.board.move(pos)            
            print('# {} #'.format(i+1).center(13))
            print()
            print(self.board)
            print()