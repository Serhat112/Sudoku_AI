import torch.nn as nn
import torch.nn.functional as f

class DigitCNN(nn.Module):
    def __init__(self):
        super(DigitCNN, self).__init__()
        # Girdi: 1 kanal (Siyah-Beyaz), Çıktı: 16 özellik haritası
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        # 28x28 boyutundaki görsel iki kez havuzlamadan (pooling) sonra 7x7 boyutuna düşer
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(f.relu(self.conv1(x)))
        x = self.pool(f.relu(self.conv2(x)))
        x = x.view(-1, 32 * 7 * 7)
        x = f.relu(self.fc1(x))
        x = self.fc2(x)
        return x