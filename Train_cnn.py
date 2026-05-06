import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from Model_net import DigitCNN


def train():
    print("Model eğitimi başlıyor. Veri seti indiriliyor...")

    # Görselleri normalize et ve PyTorch Tensor'üne çevir
    transform = transforms.Compose([
        transforms.RandomAffine(
            degrees=15,  # Döndürme (Rotation yerine burada tek seferde yapıyoruz)
            translate=(0.1, 0.1),  # Kaydırma
            scale=(0.8, 1.1),  # %80 ile %110 arası büyüklük
            shear=5  # Hafifçe yana yatırma (İtalik fontlar için harikadır)
        ),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    # MNIST Dataset
    train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

    model = DigitCNN()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    model.train()
    epochs = 7
    for epoch in range(epochs):
        running_loss = 0.0
        correct = 0
        total = 0

        model.train()  # Eğitim modu
        for batch_idx, (data, target) in enumerate(train_loader):
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            _, predicted = torch.max(output.data, 1)
            total += target.size(0)
            correct += (predicted == target).sum().item()

        accuracy = 100 * correct / total
        print(f"Epoch {epoch + 1}/{epochs} -> Loss: {running_loss / len(train_loader):.4f} | Accuracy: %{accuracy:.2f}")

    torch.save(model.state_dict(), "digit_cnn.pth")
    print("Yapay Zeka modeli başarıyla eğitildi ve 'digit_cnn.pth' olarak kaydedildi!")


if __name__ == "__main__":
    train()