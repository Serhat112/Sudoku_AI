# Sudoku AI - Automatic Solution Bot

This project is an AI system that automatically solves Sudoku puzzles and directly solves them on websites.

## Features

- **Image Processing**: Automatically recognizes Sudoku from screenshots
- **Artificial Intelligence**: CNN-based digit recognition system
- **Automatic Solution**: Solves Sudoku with logical algorithms
- **Automatic Bot**: Automatically writes solution to website

## Files

- `main.py` - Main program
- `Vision_processor.py` - Image processing and digit recognition
- `AI_agent.py` - Sudoku solving algorithms
- `Game_logic.py` - Sudoku logic and control
- `Auto_player.py` - Auto-writing bot for website
- `Model_net.py` - CNN architecture
- `Train_cnn.py` - Model training script
- `digit_cnn.pth` - Trained model weights

## Installation

```bash
# Install required libraries
pip install torch torchvision opencv-python numpy pynput

# Download project from GitHub
git clone https://github.com/Serhat112/Sudoku_AI.git
```

## Usage

### 1. Solve with Screenshot
```bash
python main.py sudoku.png
```

### 2. Automatic Bot on Website
```bash
python main.py
# Bot starts after 5 seconds
# Click on first cell and watch the bot work
```

## How It Works?

1. **Image Processing**: Finds Sudoku grid in screenshot
2. **Digit Recognition**: Recognizes digits in each cell with CNN
3. **Solution**: Solves Sudoku with backtracking algorithm
4. **Auto Writing**: Writes solution to website with `pynput`

## Bot Usage

1. Open Sudoku website
2. Run the program
3. Click on first cell within 5 seconds
4. Bot will automatically write the entire solution
5. To find grid coordinates, use pyautogui.screenshot() and pyautogui.displayMousePosition()
## Notes

- Model trained with MNIST data
- Bot only writes to empty cells
- Waits 0.15 seconds after each digit
- Navigates with arrow keys

## Development

To retrain the model:
```bash
python Train_cnn.py
```

For debug mode, check debug_cells folder.

