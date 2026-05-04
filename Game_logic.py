class Board:
    def __init__(self,rows=9, cols=9):
        self.rows = 9
        self.cols = 9
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def print_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(f"{self.grid[i][j]:>3}", end=" ")
            print()


    def create_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = "0"


    def enter_value(self):
        while True:
            row = (input(f"\nEnter row detail for value: "))
            if row == "q":
                break
            col = (input(f"\nEnter column detail for value: "))
            if col == "q":
                break
            row = int(row)
            col = int(col)
            value = int(input(f"\nEnter value for row {row}, column {col}: "))
            self.grid[row - 1][col - 1] = value



