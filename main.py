import Game_logic
import AI_agent
import Vision_processor


def main():
    print("\nSudoku AI Solver with Vision!")

    # 1. Resimden veriyi oku
    image_path = "sudoku.png"
    print(f"Reading image: {image_path}...")

    try:
        vision = Vision_processor.SudokuVision(image_path)

        # DÜZELTME: Fonksiyonu parantezlerle ÇALIŞTIRIN
        extracted_grid = vision.process_image()

        # 2. Board nesnesini oluştur ve veriyi aktar
        board = Game_logic.Board()
        board.grid = extracted_grid

        print("\nBoard extracted from image:")
        board.print_board()

        # 3. AI Çözümü
        print("\nSudoku ready. AI solving...")
        solver = AI_agent.SudokuSolver(board)

        if solver.solve():
            solver.print_solution()
        else:
            print("\nUnsolvable!")
            print("İpucu: 'debug_cells' klasöründeki resimleri kontrol edin.")
            print("Yanlış okunan bir rakam Sudoku'yu imkansız hale getirir.")

    except Exception as e:
        print(f"Sistem Hatası: {e}")


if __name__ == "__main__":
    main()