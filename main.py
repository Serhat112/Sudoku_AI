import pyautogui
import Game_logic
import AI_agent
import Vision_processor
import Auto_player
import time


def main():
    print("\n=====================================")
    print("      SUDOKU AI & AUTO-PLAYER")
    print("=====================================")

    # 1. Aşama: Sabit Koordinatlar
    region = (45, 348, 626, 622)
    image_path = "captured_sudoku.png"

    print(f"\n[SİSTEM] Sudoku tahtası taranıyor...")
    pyautogui.screenshot(image_path, region=region)

    try:
        vision = Vision_processor.SudokuVision(image_path)
        extracted_grid = vision.process_image()

        if extracted_grid is None:
            print("[HATA] Görüntü işlenemedi.")
            return

        # Boş yerleri bilmek için orijinali sakla
        original_grid = [row[:] for row in extracted_grid]

        board = Game_logic.Board()
        board.grid = extracted_grid

        print("\nOkunan Sudoku:")
        board.print_board()

        print("\n[AI] Çözüm aranıyor...")
        solver = AI_agent.SudokuSolver(board)

        if solver.solve():
            # solver.solve() artık board.grid'i doğrudan güncelledi!
            solver.print_solution()

            # Bot için temiz bir kopya alıyoruz
            final_solution = [row[:] for row in board.grid]

            # DEBUG: Bakalım bu sefer 0 mı gelecek rakam mı?
            print(f"[DEBUG] Main içindeki ilk hücre: {final_solution[0][0]}")

            answer = input("\nÇözüm web sitesine otomatik yazılsın mı? (e/h): ")
            if answer.lower() == 'e':
                Auto_player.solve_on_website(original_grid, final_solution)
        else:
            print("\n[HATA] Çözüm bulunamadı!")

    except Exception as e:
        print(f"\n[KRİTİK HATA]: {e}")


if __name__ == "__main__":
    main()