import os
import cv2
import numpy as np
import torch
from torchvision import transforms
from Model_net import DigitCNN

class SudokuVision:
    def __init__(self, image_path):
        self.image_path = image_path

        # Yapay zeka modelini yükle
        self.model = DigitCNN()
        if os.path.exists("digit_cnn.pth"):
            self.model.load_state_dict(torch.load("digit_cnn.pth"))
            self.model.eval()
        else:
            raise Exception("HATA: 'digit_cnn.pth' bulunamadı! Lütfen önce Train_cnn.py dosyasını çalıştırın.")

        # Debug klasör temizliği
        if not os.path.exists("debug_cells"):
            os.makedirs("debug_cells")
        else:
            for file in os.listdir("debug_cells"):
                try:
                    os.remove(os.path.join("debug_cells", file))
                except Exception:
                    pass

    def center_and_scale_digit(self, cell):
        """Rakamı kütle merkezine göre bulur ve 28x28'lik siyah tuvalin ortasına alır."""
        contours, _ = cv2.findContours(cell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None

        # En büyük konturu bul
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) < 15:  # Gürültü kontrolü
            return None

        x, y, w, h = cv2.boundingRect(c)
        digit = cell[y:y + h, x:x + w]

        # --- YENİ MANTIK ---

        # 1. Rakamı MNIST standartlarında 20x20'lik bir alana sığdır
        grid_size = 28
        target_size = 13

        if w > h:
            new_w = target_size
            new_h = int(h * (target_size / w))
        else:
            new_h = target_size
            new_w = int(w * (target_size / h))

        new_w, new_h = max(1, new_w), max(1, new_h)
        digit_resized = cv2.resize(digit, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # 2. Rakamın kütle merkezini hesapla (Moments)
        M = cv2.moments(digit_resized)
        if M["m00"] == 0:  # Boşsa güvenlik kontrolü
            return None

        # Rakamın kendi içindeki orta noktası
        cx_digit = int(M["m10"] / M["m00"])
        cy_digit = int(M["m01"] / M["m00"])

        # 3. 28x28 siyah arka plan oluştur
        canvas = np.zeros((grid_size, grid_size), dtype=np.uint8)

        # 4. Tuvalin (canvas) orta noktası
        cx_canvas = grid_size // 2
        cy_canvas = grid_size // 2

        # 5. Rakamın kütle merkezini tuvalin orta noktasına hizalayacak kaydırmayı hesapla
        offset_x = cx_canvas - cx_digit
        offset_y = cy_canvas - cy_digit

        # 6. Rakamı tuvale yerleştirirken sınır kontrollerini yap
        x_end = offset_x + new_w
        y_end = offset_y + new_h

        # Eğer rakam tuval dışına taşıyorsa, eski (matematiksel) merkezlemeye dön
        if offset_x < 0 or offset_y < 0 or x_end > grid_size or y_end > grid_size:
            start_x = (grid_size - new_w) // 2
            start_y = (grid_size - new_h) // 2
            canvas[start_y:start_y + new_h, start_x:start_x + new_w] = digit_resized
        else:
            # Kütle merkezine göre mükemmel yerleştirme
            canvas[offset_y:y_end, offset_x:x_end] = digit_resized

        # Son temizlik
        _, canvas = cv2.threshold(canvas, 127, 255, cv2.THRESH_BINARY)

        return canvas

    def process_image(self):
        img = cv2.imread(self.image_path)
        if img is None:
            raise Exception(f"Resim bulunamadı: {self.image_path}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 9, 75, 75)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)

        height, width = thresh.shape
        cell_h, cell_w = height // 9, width // 9
        board_data = []

        # PyTorch Tensor dönüşüm ayarları (MNIST standartlarında normalizasyon)
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])

        print("\n" + "=" * 35)
        print("   SUDOKU CNN AI PROCESSOR")
        print("=" * 35)

        for i in range(9):
            row_data = []
            for j in range(9):
                cell = thresh[i * cell_h:(i + 1) * cell_h, j * cell_w:(j + 1) * cell_w]

                # Çizgilerden kaçmak için %15 kırp
                p_h, p_w = int(cell_h * 0.15), int(cell_w * 0.15)
                cell_isolated = cell[p_h:-p_h, p_w:-p_w]

                # Rakamı ortala
                centered_digit = self.center_and_scale_digit(cell_isolated)

                if centered_digit is not None:
                    # Model tahmini
                    tensor_img = transform(centered_digit).unsqueeze(0)

                    with torch.no_grad():
                        output = self.model(tensor_img)
                        prediction = torch.argmax(output, dim=1).item()

                    # Sıfır sınıfı çıkarsa boş kabul et
                    if prediction > 0:
                        row_data.append(prediction)
                        print(f"[Hücre {i + 1},{j + 1}]: {prediction} OKUNDU.")
                        # Debug için kaydedelim (Ortalanmış halini göreceksin)
                        cv2.imwrite(f"debug_cells/okunan_{i + 1}_{j + 1}_val_{prediction}.png", centered_digit)
                    else:
                        row_data.append(0)
                        cv2.imwrite(f"debug_cells/hata_{i + 1}_{j + 1}.png", centered_digit)
                        print(f"[Hücre {i + 1},{j + 1}]: !!! OKUNAMADI (Sıfır Tahmini)")
                else:
                    row_data.append(0)
            board_data.append(row_data)

        print("=" * 35 + "\n")
        return board_data