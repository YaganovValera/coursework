from stockfish import Stockfish

stockfish = Stockfish("stockfish_15_win_x64_avx2/stockfish_15_x64_avx2.exe")


class startBoard():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]


def checking_cur_board(board=None):
    if board != None:
        return stockfish.is_fen_valid(board)
    cur_position = stockfish.get_fen_position()
    return stockfish.is_fen_valid(cur_position)


def make_matrix_board(board):  # type(board) == chess.Board()
    pgn = board
    foo = []  # Final board
    pieces = pgn.split(" ", 1)[0]
    rows = pieces.split("/")
    for row in rows:
        foo2 = []  # This is the row I make
        for thing in row:
            if thing.isdigit():
                for i in range(0, int(thing)):
                    foo2.append('--')
            else:
                if thing == 'r':
                    foo2.append('bR')
                if thing == 'n':
                    foo2.append('bN')
                if thing == 'b':
                    foo2.append('bB')
                if thing == 'q':
                    foo2.append('bQ')
                if thing == 'k':
                    foo2.append('bK')
                if thing == 'p':
                    foo2.append('bP')
                if thing == 'P':
                    foo2.append('wP')
                if thing == 'R':
                    foo2.append('wR')
                if thing == 'N':
                    foo2.append('wN')
                if thing == 'B':
                    foo2.append('wB')
                if thing == 'Q':
                    foo2.append('wQ')
                if thing == 'K':
                    foo2.append('wK')
        foo.append(foo2)
    return foo


def transition_board(fen_move):
    norm_move = [1, 2, 3, 4]
    for item in range(len(fen_move)):
        if fen_move[item].isdigit():
            norm_move[item-1] = (7 - (int(fen_move[item]) - 1))
        elif fen_move[item] == 'a':
            norm_move[item+1] = 0
        elif fen_move[item] == 'b':
            norm_move[item+1] = 1
        elif fen_move[item] == 'c':
            norm_move[item+1] = 2
        elif fen_move[item] == 'd':
            norm_move[item+1] = 3
        elif fen_move[item] == 'e':
            norm_move[item+1] = 4
        elif fen_move[item] == 'f':
            norm_move[item+1] = 5
        elif fen_move[item] == 'g':
            norm_move[item+1] = 6
        elif fen_move[item] == 'h':
            norm_move[item+1] = 7
    return norm_move


def get_computer_move():
    best_move = stockfish.get_best_move()
    stockfish.make_moves_from_current_position([best_move])
    best_move = transition_board(best_move)
    return best_move
