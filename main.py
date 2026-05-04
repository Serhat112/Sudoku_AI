import Game_logic
import AI_agent


def main():
    print("\nSudoku AI Solver!")
    print("START filling the board(q to end)")
    board = Game_logic.Board()
    board.create_board()
    board.print_board()
    board.enter_value()
    print("\nBoard after user input:")
    board.print_board()
    print("\nSudoku ready. AI solving...")
    solver = AI_agent.SudokuSolver(board)
    
    if solver.solve():
        solver.print_solution()
    else:
        print("Unsolvable!")






if __name__ == "__main__":
    main()
