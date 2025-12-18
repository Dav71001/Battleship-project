import random
from .utils import create_empty_board, print_board
from .ship_input import get_player_ships
from .bot_generation import generate_bot_ships


def bot_choose_move(board, memory):
    """Select bot move based on memory"""

    def get_adjacent_cells(x, y):
        moves = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 10 and 0 <= ny < 10 and board[nx][ny] in ['.', 'S']:
                moves.append((nx, ny))
        return moves

    if memory["mode"] == "random":
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if board[x][y] in ['.', 'S']:
                return x, y

    if memory["mode"] == "target":
        x0, y0 = memory["hits"][0]

        if memory["axis"]:
            directions = [(-1,0),(1,0)] if memory["axis"] == "horizontal" else [(0,-1),(0,1)]
            for dx, dy in directions:
                nx, ny = x0 + dx, y0 + dy
                if 0 <= nx < 10 and 0 <= ny < 10 and board[nx][ny] in ['.', 'S']:
                    return nx, ny
            memory["mode"] = "random"
            memory["hits"] = []
            memory["axis"] = None
            return bot_choose_move(board, memory)

        else:
            adj = get_adjacent_cells(x0, y0)
            if adj:
                return random.choice(adj)
            memory["mode"] = "random"
            memory["hits"] = []
            return bot_choose_move(board, memory)


def mark_surrounding_as_miss(board, ship_cells):
    """Mark all 8 surrounding cells around a ship as miss (O)"""
    for x, y in ship_cells:
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 10 and 0 <= ny < 10 and board[nx][ny] == '.':
                    board[nx][ny] = 'O'


def is_ship_destroyed(board, ship):
    """Check if a ship is fully destroyed"""
    return all(board[x-1][y-1] == 'X' for x, y in ship)


def play_game():
    print("=== Battleship ===")

    player_board = create_empty_board()
    bot_board = create_empty_board()

    player_ships = get_player_ships()
    bot_ships = generate_bot_ships()

    for ship in player_ships:
        for x, y in ship:
            player_board[x-1][y-1] = 'S'

    for ship in bot_ships:
        for x, y in ship:
            bot_board[x-1][y-1] = 'S'

    bot_memory = {"mode": "random", "hits": [], "axis": None}

    player_turn = True
    turn = 1

    while True:
        print(f"\nTurn {turn}")

        if player_turn:
            print("\nYour shots on bot:")
            print_board(bot_board, hide_ships=True)

            move = input("Enter coordinates x,y (or 'q' to quit): ")
            if move.lower() in ['q', 'quit', 'exit']:
                print("Game exited.")
                break

            try:
                x, y = map(int, move.split(','))
                x -= 1
                y -= 1
                if not (0 <= x < 10 and 0 <= y < 10):
                    raise ValueError
            except:
                print("Invalid input.")
                continue

            if bot_board[x][y] == 'S':
                print("Hit!")
                bot_board[x][y] = 'X'

                for ship in bot_ships:
                    if (x+1, y+1) in ship and is_ship_destroyed(bot_board, ship):
                        print("You destroyed a bot ship!")
                        mark_surrounding_as_miss(bot_board, [(sx-1, sy-1) for sx, sy in ship])
                        break

            elif bot_board[x][y] in ['X','O']:
                print("Already shot here. Try again.")
                continue
            else:
                print("Miss!")
                bot_board[x][y] = 'O'
                player_turn = False

        else:
            while True:
                bx, by = bot_choose_move(player_board, bot_memory)

                if player_board[bx][by] == 'S':
                    print(f"Bot hit at {bx+1},{by+1}!")
                    player_board[bx][by] = 'X'
                    bot_memory["hits"].append((bx, by))

                    if len(bot_memory["hits"]) == 1:
                        bot_memory["mode"] = "target"
                    elif len(bot_memory["hits"]) >= 2 and not bot_memory["axis"]:
                        x0, y0 = bot_memory["hits"][0]
                        x1, y1 = bot_memory["hits"][1]
                        bot_memory["axis"] = "horizontal" if x0 != x1 else "vertical"

                    for ship in player_ships:
                        if (bx+1, by+1) in ship and is_ship_destroyed(player_board, ship):
                            print("Bot destroyed your ship!")
                            mark_surrounding_as_miss(player_board, [(sx-1, sy-1) for sx, sy in ship])
                            bot_memory = {"mode": "random", "hits": [], "axis": None}
                            break

                    continue

                else:
                    print(f"Bot missed at {bx+1},{by+1}!")
                    player_board[bx][by] = 'O'
                    break

            player_turn = True

        print("\nYour board:")
        print_board(player_board)
        print("\nYour shots on bot:")
        print_board(bot_board, hide_ships=True)

        if not any('S' in row for row in player_board):
            print("\n=== BOT WINS ===")
            break
        if not any('S' in row for row in bot_board):
            print("\n=== YOU WIN ===")
            break

        turn += 1


if __name__ == "__main__":
    play_game()
