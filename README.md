# Battleship-project# Battleship Game (Console)

Console implementation of the classic Battleship game in Python.

## Rules
- Board size: 10x10
- Ships:
  - 1 ship of size 4
  - 2 ships of size 3
  - 3 ships of size 2
  - 4 ships of size 1
- Ships cannot touch each other (even diagonally)
- If a player hits a ship, they get another turn
- Game ends when all ships of one side are destroyed

## Bot behavior
- Random shooting at first
- After a hit, the bot targets adjacent cells
- After two hits, the bot locks shooting direction
- Returns to random mode after ship destruction

## How to run
```bash
pip install -r requirements.txt
python main.py
