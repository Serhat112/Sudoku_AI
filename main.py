import Game_logic
import AI_agent
import Vision_processor

def main():
    print("\nSudoku AI Solver with Vision!")

    image_path = "sudoku.png"
    print(f"Reading image: {image_path}...")

    try:
        vision = Vision_processor.SudokuVision(image_path)

        extracted_grid = vision.process_image()

        board = Game_logic.Board()
        board.grid = extracted_grid

        print("\nBoard extracted from image:")
        board.print_board()

        print("\nSudoku ready. AI solving...")
        solver = AI_agent.SudokuSolver(board)

        if solver.solve():
            solver.print_solution()
        else:
            print("\nUnsolvable!")
            print("İpucu: 'debug_cells' klasöründeki resimleri kontrol edin.")
            print("Yanlış okunan bir rakam Sudoku'yu imkansız hale getirir.")

    except Exception as e:
        print(f"System Failure: {e}")


if __name__ == "__main__":
    main()