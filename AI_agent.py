class SudokuSolver:
    def __init__(self, board_obj):
        # ÖNEMLİ: Kopyalamıyoruz, doğrudan main'den gelen board objesine referans alıyoruz
        self.board_obj = board_obj
        self.grid = board_obj.grid
        self.rows = 9
        self.cols = 9

    def is_valid(self, row, col, val):
        """Verilen pozisyona val sayısı konabilir mi?"""
        for j in range(self.cols):
            if self.grid[row][j] == val:
                return False
        for i in range(self.rows):
            if self.grid[i][col] == val:
                return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.grid[i][j] == val:
                    return False
        return True

    def find_empty(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def solve(self):
        """Backtracking ile sudoku çöz"""
        empty = self.find_empty()
        if not empty:
            # Çözüm bittiğinde, güncel grid'i board objesine geri yazıyoruz (Garanti olsun)
            self.board_obj.grid = self.grid
            return True

        row, col = empty
        for val in range(1, 10):
            if self.is_valid(row, col, val):
                self.grid[row][col] = val

                if self.solve():
                    return True

                # Burası önemli: Yanlış yolsak 0'la, ama çözüm bulunduysa buraya girmeyiz
                self.grid[row][col] = 0

        return False

    def print_solution(self):
        print("\n" + "=" * 37)
        print("           AI Solution")
        print("=" * 37)
        for i in range(self.rows):
            for j in range(self.cols):
                print(f"{self.grid[i][j]:>3}", end=" ")
                if (j + 1) % 3 == 0 and j < 8:
                    print("|", end=" ")
            print()
            if (i + 1) % 3 == 0 and i < 8:
                print("-" * 37)
        print("=" * 37)