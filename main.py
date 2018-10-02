from application import App

def main():
    """
    Chamada principal do programa.
    """
    matrix_start = [
        [2,0,3],
        [1,7,4],
        [6,8,5]
    ]

    matrix_end = [
        [1,2,3],
        [8,0,4],
        [7,6,5]
    ]

    app = App(matrix_start, matrix_end)
    app.solve()
    app.display_solution()
    

if __name__ == '__main__':
    main()