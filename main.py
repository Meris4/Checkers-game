from piece import Piece
import pickle
import time
import hashlib

class Board():
    def __init__(self, mandatory_remove, moves_dict=None):
        self.board = [[""] * 8 for _ in range(8)]
        self.initialize_board()
        self.draw_board()
        self.blue = 12
        self.red = 12
        self.current_player = "blue"
        self.mandatory_remove = mandatory_remove
        self.moves_dict = moves_dict if moves_dict else {}

    def initialize_board(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Piece('blue', row, col) if row < 3 else (Piece('red', row, col) if row > 4 else None)
                else:
                    self.board[row][col] = None

    # Metoda za iscrtavanje table
    def draw_board(self):
        print("   A  B  C  D  E  F  G  H")
        for i in range(8):
            print(i + 1, end=" ")
            for j in range(8):
                if (i + j) % 2 == 0:
                    print("\u001b[47m\u001b[30m   \u001b[0m", end="")  # Belo polje
                else:
                    if self.board[i][j] is None:
                        print("\u001b[100m\u001b[37m   \u001b[0m", end="")  # Crno polje (sivo)
                    else:
                        if self.board[i][j].color == 'blue' and self.board[i][j].king:
                            print("" * 1, "\u001b[34m★\u001b[0m", end=" " * 1)  # Plava zvezdica
                        elif self.board[i][j].color == 'red' and self.board[i][j].king:
                            print("" * 1, "\u001b[31m★\u001b[0m", end=" " * 1)  # Crvena zvezdica
                        
                        elif self.board[i][j].color == 'blue':
                            print("" * 1, "\u001b[34m⬤\u001b[0m", end=" " * 1)  # Plavi kružić
                        elif self.board[i][j].color == 'red':
                            print("" * 1, "\u001b[31m⬤\u001b[0m", end=" " * 1)  # Crveni kružić
            
            print("", i + 1)
        print("   A  B  C  D  E  F  G  H")

    def move_piece(self, start_pos, end_pos):
        start_x, start_y = start_pos
        end_x, end_y = end_pos

        start_piece = self.board[start_x][start_y]
        if start_piece is None or start_piece.color != self.current_player:
            return False, None

        possible_moves, possible_removes = self.get_possible_moves(start_pos, self.mandatory_remove)
        if self.mandatory_remove and possible_removes and end_pos not in possible_removes:
            return False, None
        elif not self.mandatory_remove and end_pos not in possible_moves:
            return False, None          

        

        captured_piece = None
        if abs(start_x - end_x) == 2 and abs(start_y - end_y) == 2:
            jumped_x = (start_x + end_x) // 2
            jumped_y = (start_y + end_y) // 2
            captured_piece = self.board[jumped_x][jumped_y]
            self.board[jumped_x][jumped_y] = None
            if captured_piece.color == 'blue':
                self.blue -= 1
            else:
                self.red -= 1

        self.board[end_x][end_y] = start_piece
        self.board[start_x][start_y] = None

        king_before = start_piece.king
        if (end_x == 0 and start_piece.color == 'blue') or (end_x == 7 and start_piece.color == 'red'):
            start_piece.king = True

        self.current_player = "red" if self.current_player == "blue" else "blue"
        

        return True, (captured_piece, (start_x, start_y), (end_x, end_y), king_before)
    
    def board_state_hash(self):
        # board_str = str(self.board)
        # return hashlib.sha256(board_str.encode()).hexdigest()
        board_str = ""
        for row in self.board:
            for piece in row:
                if piece is None:
                    board_str += "None,"
                else:
                    piece_str = f"{piece.color}{"K" if piece.king else ""},"
                    board_str += piece_str
        return hashlib.sha256(board_str.encode()).hexdigest()
    
    def save_move_to_dict(self, move, board_hash):
        self.moves_dict[board_hash] = move
        # print("Board hash koji se cuva: ", board_hash)

    # Vracanje poteza na prethodno stanje
    def undo_move(self, move_info):
        captured_piece, start_pos, end_pos, king_before = move_info
        start_x, start_y = start_pos
        end_x, end_y = end_pos

        piece = self.board[end_x][end_y]
        self.board[start_x][start_y] = piece
        self.board[end_x][end_y] = None

        if captured_piece:
            self.board[(start_x + end_x) // 2][(start_y + end_y) // 2] = captured_piece
            if captured_piece.color == "blue":
                self.blue += 1
            else:
                self.red += 1

        piece.king = king_before
        self.current_player = "red" if self.current_player == "blue" else "blue"

    def get_possible_moves(self, start_pos, mandatory_remove):
        start_x, start_y = start_pos
        possible_moves = []
        possible_remove = []

        start_piece = self.board[start_x][start_y]
        if start_piece is None or start_piece.color != self.current_player:
            return possible_moves

        direction = 1 if start_piece.color == "blue" else -1
        directions = [-1, 1] if start_piece.king else [direction]

        for dir in directions:
            new_x = start_x + dir
            for dir_y in [-1, 1]:
                new_y = start_y + dir_y
                if 0 <= new_x < 8 and 0 <= new_y < 8 and self.board[new_x][new_y] is None:
                    possible_moves.append((new_x, new_y))

                if 0 <= new_x + dir < 8 and 0 <= new_y + dir_y < 8:
                    jumped_piece = self.board[new_x][new_y]
                    if jumped_piece and jumped_piece.color != start_piece.color and self.board[new_x + dir][new_y + dir_y] is None:
                        possible_moves.append((new_x + dir, new_y + dir_y))
                        possible_remove.append((new_x + dir, new_y + dir_y))

        return possible_moves, possible_remove
    

def evaluate(board, color):
    score = 0
    for row_idx, row in enumerate(board.board):
        for col_idx, piece in enumerate(row):
            if piece:
                if piece.color == color:
                    score += 10
                    if col_idx == 0 or col_idx == 7:
                        score += 2
                    if piece.king:
                        score += 8
                    if row_idx == 0 or row_idx == 7:
                        score += 2
                else:
                    score -= 10
                    if col_idx == 0 or col_idx == 7:
                        score -= 2
                    if piece.king:
                        score -= 8
                    if row_idx == 0 or row_idx == 7:
                        score -= 2
            
    return score

def has_moves(board, color):
    for row in range(8):
        for col in range(8):
            if board.board[row][col] and board.board[row][col].color == color:
                if board.get_possible_moves((row, col), board.mandatory_remove):
                    print("Ima poteza!", color)
                    
                    return True
    print("Nema poteza! ", color)
    return False


def game_over(board, mandatory_remove):
    return board.blue == 0 or board.red == 0


def save_moves(moves_dict, file_name):
    with open(file_name, "wb") as file:
        pickle.dump(moves_dict, file)

    
def load_moves(file_name):
    try:
        with open(file_name, "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        pass


def minimax(board, depth, alpha, beta, maximizing_player, color, mandatory_remove, start_time, time_limit, current_depth = 0):
    hash_board = board.board_state_hash()

    if hash_board in board.moves_dict:
        return evaluate(board, color)
    
    if depth == 0 or game_over(board, mandatory_remove): 
        return evaluate(board, color)

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_possible_moves(board, color, mandatory_remove):
            valid_move, move_info = board.move_piece(move[0], move[1])
            if not valid_move:
                continue


            eval = minimax(board, depth - 1, alpha, beta, False, color, mandatory_remove, start_time, time_limit, current_depth + 1)
            board.undo_move(move_info)
            # print("Uvecaj")
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha or (time.time() - start_time) > time_limit:
                break

        return max_eval
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_possible_moves(board, get_opponent_color(color), mandatory_remove):
            valid_move, move_info = board.move_piece(move[0], move[1])
            if not valid_move:
                continue
            eval = minimax(board, depth - 1, alpha, beta, True, color, mandatory_remove, start_time, time_limit, current_depth + 1)
            board.undo_move(move_info)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha or (time.time() - start_time) > time_limit:
                break
        
        return min_eval

def get_opponent_color(color):
    return 'red' if color == 'blue' else 'blue'

def get_all_possible_moves(board, color, mandatory_remove):
    all_possible_moves = []
    all_possible_removes = []
    for row in range(8):
        for col in range(8):
            if board.board[row][col] and board.board[row][col].color == color:
                moves, possible_removes = board.get_possible_moves((row, col), mandatory_remove)
                if mandatory_remove and possible_removes:
                    for move in possible_removes:
                        all_possible_removes.append(((row, col), move))
                    
                for moves in moves:
                    all_possible_moves.append(((row, col), moves))
    
    if mandatory_remove and all_possible_removes:
        return all_possible_removes
    else:
        return all_possible_moves


def game_dialog(mandatory_remove):
    
    moves_dictionary = {}
    if mandatory_remove:
        moves_dictionary = load_moves("moves.pkl")
    else:
        moves_dictionary = load_moves("moves2.pkl")
    board = Board(mandatory_remove, moves_dictionary)  # Inicijalizacija table
    
    current_color = 'blue'  # Pocetna boja igraca

    while not game_over(board, mandatory_remove):
        if current_color == 'red':
            # Crveni igrac koristi minimax algoritam s alfa-beta rezanjem da odabere potez
            best_move = None
            max_eval = float('-inf')
            start_time = time.time()
            time_limit = 2.85  # Vremensko ogranicenje od 3 sekunde
            board_hash = board.board_state_hash()
            all_possible_moves = get_all_possible_moves(board, "red", mandatory_remove)
            if not all_possible_moves:
                print("Crveni igrac nema mogucih poteza. Pobednik je plavi takmicar!")
                break


            # Provjera da li je potez vec izracunat i spremljen u recniku
            if board_hash in board.moves_dict:
                best_move = board.moves_dict[board_hash]
                if best_move:
                    board.move_piece(best_move[0], best_move[1])
                    letter1 = chr(best_move[0][1] + ord('A'))
                    letter2 = chr(best_move[1][1] + ord('A'))
                    print()
                    if board.board[best_move[1][0]][best_move[1][1]].color == "red" and best_move[1][0] == 0:
                        board.board[best_move[1][0]][best_move[1][1]].king = True
                    board.draw_board()
                    print(f"Kompjuter:  {best_move[0][0] + 1}{letter1} --> {best_move[1][0] + 1}{letter2}\n")
                    current_color = 'blue'

            else:
                for move in get_all_possible_moves(board, 'red', mandatory_remove):
                    valid_move, move_info = board.move_piece(move[0], move[1])
                    if not valid_move:
                        continue
                    if (board.blue + board.red <= 12):
                        depth = 6
                    elif (board.blue + board.red <= 8):
                        depth = 7
                    else:
                        depth = 5
                    eval = minimax(board, depth, float('-inf'), float('inf'), False, 'red', board.mandatory_remove, start_time, time_limit)
                    board.undo_move(move_info)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = move
                    if (time.time() - start_time) > time_limit:
                        break
                if board_hash not in board.moves_dict:
                    board.save_move_to_dict(best_move, board_hash)
                if best_move:
                    board.move_piece(best_move[0], best_move[1])
                    letter1 = chr(best_move[0][1] + ord('A'))
                    letter2 = chr(best_move[1][1] + ord('A'))
                    print()
                    if board.board[best_move[1][0]][best_move[1][1]].color == "red" and best_move[1][0] == 0:
                        board.board[best_move[1][0]][best_move[1][1]].king = True
                    
                    board.draw_board()
                    print(f"Kompjuter:  {best_move[0][0] + 1}{letter1} --> {best_move[1][0] + 1}{letter2}\n")
                    current_color = 'blue'
        else:
            win = False
            exit = False
            while True:
                all_possible_moves = get_all_possible_moves(board, "blue", mandatory_remove)
                if not all_possible_moves:
                    print("Plavi igrac nema mogucih poteza. Pobednik je crveni takmicar!")
                    win = True
                    break
                # Plavi igrac unosi svoj potez preko konzole
                exit = False 
                valid_move = False
                while not valid_move:
                    start_pos = input("Unesite koordinate figure koju zelite da pomerite (npr. 3B) ili pritisnite X za izlazak: ").upper().strip()

                    exit = False
                    if start_pos == "X":
                        print("Izlazak iz igre.")
                        exit = True
                        break
                    
                    if start_pos == "":
                        continue

                    separated = list(start_pos)
                    if len(separated) == 1:
                        print("Neispravan unos. Molimo unesite ponovo.")
                        continue

                    try:
                        start_x = int(start_pos[0]) - 1
                        start_y = ord(start_pos[1]) - ord('A')

                        if not (0 <= start_x < 8 and 0 <= start_y < 8):
                            print("Neispravne koordinate. Molimo unesite ponovo.")
                            continue

                        

                        if board.board[start_x][start_y] is None and (start_x + start_y) % 2 == 0:
                            print("Nije dozvoljeno koristiti bela polja!")
                            continue

                        if board.board[start_x][start_y] is None:
                            print("Na izabranoj poziciji nema figure. Molimo unesite ponovo.")
                            continue

                        

                        if board.board[start_x][start_y].color != 'blue':
                            print("Nije dozvoljeno pomeranje protivnicke figure. Molimo unesite ponovo.")
                            continue

                        valid_move = True
                    except ValueError:
                        print("Neispravan unos. Molimo unesite ponovo.")
                        continue

                if exit:
                    break

                back = False
                while True:
                    print("Moguci potezi: ")
                    i = 1
                    moves = {}
                    all_possible_moves = get_all_possible_moves(board, "blue", mandatory_remove)  
                    possible_moves, possible_removes = board.get_possible_moves((start_x, start_y), board.mandatory_remove)
                    

                    if mandatory_remove:
                        exist = False
                        for possible_remove in possible_removes:
                            for possible_remove in possible_removes:
                                if possible_remove == possible_remove:
                                    number = possible_remove[0] + 1
                                    letter = chr(possible_remove[1] + ord('A'))
                                    print(f"[{i}] {number}{letter}", end = ", ")
                                    exist = True
                                    moves[i] = possible_remove
                                    i += 1
                        if not exist:
                            for possible_move in possible_moves:
                                for all_possible_move in all_possible_moves:
                                    if all_possible_move[0] == (start_x, start_y) and all_possible_move[1] == possible_move:
                                        number = possible_move[0] + 1
                                        letter = chr(possible_move[1] + ord('A'))
                                        print(f"[{i}] {number}{letter}", end = ", ")
                                        moves[i] = possible_move
                                        i += 1
                    else:
                        for possible_move in possible_moves:
                                for all_possible_move in all_possible_moves:
                                    if all_possible_move[0] == (start_x, start_y) and all_possible_move[1] == possible_move:
                                        number = possible_move[0] + 1
                                        letter = chr(possible_move[1] + ord('A'))
                                        print(f"[{i}] {number}{letter}", end = ", ")
                                        moves[i] = possible_move
                                        i += 1
                            
                    print()


                    end_pos = input("Unesite redni broj poteza koji zelite da odigrate ili pritisnite N za nazad: ").upper().strip()
                    if end_pos == "":
                        continue

                    if end_pos == "N":
                        
                        back = True
                        break

                    try:
                        move_index = int(end_pos)

                        if move_index not in moves:
                            print("Neispravan redni broj. Molimo unesite ponovo.")
                            continue

                        end_pos = moves[move_index]
                        end_x, end_y = end_pos

                        break
                    except ValueError:
                        print("Neispravan unos. Molimo unesite ponovo.")
                
                if back:
                    continue

                # Pomeranje figure
                board.move_piece((start_x, start_y), (end_x, end_y))
                if board.board[end_x][end_y].color == 'blue'and end_x == 7:
                    board.board[end_x][end_y].king = True
                    # print("Plava figura na poziciji ", end_x, end_y, " je postala dama.")
                board.draw_board()
                
                current_color = 'red'
                break
            if win:
                break
        if exit:
            break   
        # if win:
        #     break
    

    if board.blue == 0:
        print("Pobednik je crveni takmicar!")
    elif board.red == 0:
        print("Pobednik je plavi takmicar!")
    if mandatory_remove:
        save_moves(board.moves_dict, "moves.pkl")
    else:
        save_moves(board.moves_dict, "moves2.pkl")
    print("Kraj igre.\n")


# Glavna petlja za pokretanje igre
if __name__ == "__main__":
    
    while True:
        print("Dobrodosli u igru dame! \n")
        print("Odaberite rezim igre: ")
        print("[1] Obavezno uklanjanje protivnickih figura ")
        print("[2] Bez obaveznog uklanjanja protivnickih figura")
        print("[X] Izlazak iz igre")

        choose = input("Unesite redni broj: ")
        if choose == "1":
            print("Izabrali ste rezim igre sa obaveznim uklanjanjem protivnickih figura.")
            game_dialog(mandatory_remove=True)
        elif choose == "2":
            print("Izabrali ste rezim igre bez obaveznog uklanjanja protivnickih figura.")
            game_dialog(mandatory_remove=False)
        elif choose.upper() == "X":
            print("Izlazak iz igre.")
            break
        else:
            print("Pogresan unos! Molimo vas pokusajte ponovo.")
        
        
