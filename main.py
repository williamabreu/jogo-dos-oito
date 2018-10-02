def main():
    """
    Chamada principal do programa.
    """
    matrix_start = [
        [1,8,7],
        [3,5,0],
        [4,6,2]
    ]

    matrix_end = [
        [1,2,3],
        [4,5,6],
        [7,8,0]
    ]

    app = App(matrix_start, matrix_end)
    app.solve()
    app.display_solution()
    

if __name__ == '__main__':
    main()