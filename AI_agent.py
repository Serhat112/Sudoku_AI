class SudokuSolver:
    def __init__(self, board):
        #copy grid
        self.grid = [row[:] for row in board.grid]
        self.rows = 9
        self.cols = 9
    
    def is_valid(self, row, col, val):
        """Verilen pozisyona val sayısı konabilir mi?"""
        # Satır kontrolü
        for j in range(self.cols):
            if self.grid[row][j] == val:
                return False
        
        # Sütun kontrolü
        for i in range(self.rows):
            if self.grid[i][col] == val:
                return False
        
        # 3x3 kutu kontrolü
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.grid[i][j] == val:
                    return False
        
        return True
    
    def find_empty(self):
        """Boş hücre bul (0 veya '0' olan)"""
        for i in range(self.rows):
            for j in range(self.cols):
                val = self.grid[i][j]
                if val == 0 or val == "0":
                    return (i, j)
        return None
    
    def solve(self):
        """Backtracking ile sudoku çöz"""
        empty = self.find_empty()
        
        # Boş hücre kalmadıysa çözüldü
        if not empty:
            return True
        
        row, col = empty
        
        # 1'den 9'a dene
        for val in range(1, 10):
            if self.is_valid(row, col, val):
                self.grid[row][col] = val
                
                # Rekürsif olarak devam et
                if self.solve():
                    return True
                
                # Geri al (backtrack)
                self.grid[row][col] = 0
        
        return False
    
    def print_solution(self):
        """Çözümü yazdır"""
        print("\n" + "="*37)
        print("           AI Solution")
        print("="*37)
        for i in range(self.rows):
            for j in range(self.cols):
                print(f"{self.grid[i][j]:>3}", end=" ")
                if (j + 1) % 3 == 0 and j < 8:
                    print("|", end=" ")
            print()
            if (i + 1) % 3 == 0 and i < 8:
                print("-" * 37)
        print("="*37)
