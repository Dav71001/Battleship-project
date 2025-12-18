from colorama import Fore, Style, init


init(autoreset=True)

BOARD_SIZE = 10

def create_empty_board():
    """
    Create an empty 10x10 board filled with '.'
    """
    return [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def print_board(board, hide_ships=False):
    """
    Print the board with colors:
    - '.' empty cell
    - 'S' ship (hidden if hide_ships=True)
    - 'X' hit (red)
    - 'O' miss (blue)
    """

    print("   " + " ".join(str(i) for i in range(1, BOARD_SIZE+1)))
    

    for i, row in enumerate(board, start=1):
        display_row = []
        for cell in row:
            if cell == 'X':
                display_row.append(Fore.RED + 'X' + Style.RESET_ALL)  
            elif cell == 'O':
                display_row.append(Fore.BLUE + 'O' + Style.RESET_ALL) 
            elif cell == 'S':
                if hide_ships:
                    display_row.append('.')
                else:
                    display_row.append(Fore.GREEN + 'S' + Style.RESET_ALL)
            else:
                display_row.append('.')  
        print(f"{i:2} " + " ".join(display_row))
