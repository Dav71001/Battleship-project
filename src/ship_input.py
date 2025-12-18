import csv

BOARD_SIZE = 10
SHIP_SIZES = [4,3,3,2,2,2,1,1,1,1]

def get_player_ships():
    """
    Ask the player to enter ships coordinates and save them to CSV.
    Format: list of coordinates per ship, e.g.
    4, [(1,1),(1,2),(1,3),(1,4)]
    """
    ships = []
    print("Enter player ships coordinates (or 'q' to quit):")
    for size in SHIP_SIZES:
        while True:
            coords = input(f"Ship of size {size} (format x1,y1 x2,y2 ...): ")
            
            # Check for quit
            if coords.lower() in ['q', 'quit', 'exit']:
                print("Game exited.")
                exit()  
            
            coords_list = parse_input(coords)
            if validate_ship(coords_list, ships, size):
                ships.append(coords_list)
                break
            else:
                print("Invalid placement, try again.")

    save_ships_to_csv(ships, "data/player_ships.csv")
    return ships

def parse_input(input_str):
    # Convert input string to list of tuples
    try:
        return [tuple(map(int, x.split(','))) for x in input_str.strip().split()]
    except:
        return []

def validate_ship(ship, existing_ships, size):
    # Check ship size
    if len(ship) != size:
        return False
    # Check board boundaries
    for x,y in ship:
        if x<1 or x>BOARD_SIZE or y<1 or y>BOARD_SIZE:
            return False
    # Check overlap and adjacency (including diagonal)
    for ex_ship in existing_ships:
        for ex_x, ex_y in ex_ship:
            for x,y in ship:
                if max(abs(x-ex_x), abs(y-ex_y)) <= 1:
                    return False
    return True

def save_ships_to_csv(ships, filename):
    # Save ships to CSV
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for ship in ships:
            writer.writerow([len(ship)] + ship)

