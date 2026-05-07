from pynput.keyboard import Key, Controller
import time

keyboard = Controller()


def solve_on_website(original_grid, solved_grid):
    print("\n[DEBUG] Bot'a gelen tablo kontrol ediliyor...")
    # AI gerçekten çözmüş mü kontrol edelim (ilk 3 hücreyi yazdır)
    print(f"[DEBUG] Örnek çözülmüş hücreler: {solved_grid[0][0]}, {solved_grid[0][1]}, {solved_grid[0][2]}")

    print("\n[BOT] TARAYICIYA GEÇ VE İLK HÜCREYE TIKLA!")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    for r in range(9):
        for c in range(9):
            # Eğer orijinalde boşsa rakamı bas
            if original_grid[r][c] == 0:
                val = solved_grid[r][c]
                digit = str(val)

                if val != 0:
                    print(f"[{r + 1},{c + 1}] hücresine {digit} yazılıyor...")
                    # keyboard.type bazen sorun çıkarır, press/release daha garantidir
                    keyboard.press(digit)
                    time.sleep(0.05)
                    keyboard.release(digit)
                else:
                    print(f"!!! UYARI: [{r + 1},{c + 1}] için AI çözüm üretmemiş (Değer 0)!")

                time.sleep(0.15)  # Yazma sonrası bekleme

            # Navigasyon (Her zaman çalışmalı)
            if c < 8:
                keyboard.press(Key.right)
                keyboard.release(Key.right)
                time.sleep(0.08)

        # Satır sonu manevrası
        if r < 8:
            for _ in range(8):
                keyboard.press(Key.left)
                keyboard.release(Key.left)
                time.sleep(0.03)
            keyboard.press(Key.down)
            keyboard.release(Key.down)
            time.sleep(0.1)

    print("\n[BOT] GÖREV TAMAMLANDI!")