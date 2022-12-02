import chess
import chess.engine
from stockfish import Stockfish

stockfish = Stockfish("stockfish_15_win_x64_avx2/stockfish_15_x64_avx2.exe")

board = chess.Board()


class startBoard:
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
    if board!=None:
        if stockfish.is_fen_valid(board):
            stockfish.set_fen_position(board)
            return True
        else:
            return False
    cur_position = stockfish.get_fen_position()
    return stockfish.is_fen_valid(cur_position)


def make_matrix_board(board):
    end_board = []
    pieces = board.split(" ", 1)[0]
    rows = pieces.split("/")
    for row in rows:
        cur_board = []
        for thing in row:
            if thing.isdigit():
                for i in range(0, int(thing)):
                    cur_board.append('--')
            else:
                if thing == 'r':
                    cur_board.append('bR')
                if thing == 'n':
                    cur_board.append('bN')
                if thing == 'b':
                    cur_board.append('bB')
                if thing == 'q':
                    cur_board.append('bQ')
                if thing == 'k':
                    cur_board.append('bK')
                if thing == 'p':
                    cur_board.append('bP')
                if thing == 'P':
                    cur_board.append('wP')
                if thing == 'R':
                    cur_board.append('wR')
                if thing == 'N':
                    cur_board.append('wN')
                if thing == 'B':
                    cur_board.append('wB')
                if thing == 'Q':
                    cur_board.append('wQ')
                if thing == 'K':
                    cur_board.append('wK')
        end_board.append(cur_board)
    return end_board


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


def getting_col(digit):
    if digit == 0:
        return 'a'
    elif digit == 1:
        return 'b'
    elif digit == 2:
        return 'c'
    elif digit == 3:
        return 'd'
    elif digit == 4:
        return 'e'
    elif digit == 5:
        return 'f'
    elif digit == 6:
        return 'g'
    elif digit == 7:
        return 'h'


def get_computer_move():
    best_move = stockfish.get_best_move()
    stockfish.make_moves_from_current_position([best_move])
    best_move = transition_board(best_move)
    return best_move


def check_correct_move(move):
    try:
        if stockfish.is_move_correct(move):
            stockfish.make_moves_from_current_position([move])
            return True
        return False
    except:
        return False


def get_cur_position():
    cur_position = stockfish.get_fen_position()
    cur_position = make_matrix_board(cur_position)
    return cur_position


def get_student_move(kol_move):
    with open('student_move.txt') as file_student:
        move_student = file_student.read().split('\n')
        if len(move_student) >= kol_move:
            move = move_student[kol_move-1]
            return move
        return -1

