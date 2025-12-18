import random
import csv
from .ship_input import BOARD_SIZE, SHIP_SIZES, validate_ship

def generate_bot_ships():
    ships = []
    for size in SHIP_SIZES:
        while True:
            ship = random_ship(size)
            if validate_ship(ship, ships, size):
                ships.append(ship)
                break
    save_ships_to_csv(ships, "data/bot_ships.csv")
    return ships

def random_ship(size):

    direction = random.choice(['H','V'])
    if direction=='H':
        x = random.randint(1, BOARD_SIZE)
        y = random.randint(1, BOARD_SIZE-size+1)
        return [(x, y+i) for i in range(size)]
    else:
        x = random.randint(1, BOARD_SIZE-size+1)
        y = random.randint(1, BOARD_SIZE)
        return [(x+i, y) for i in range(size)]

def save_ships_to_csv(ships, filename):

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for ship in ships:
            writer.writerow([len(ship)] + ship)

