import subprocess
from _winapi import CREATE_NO_WINDOW

import chess
from models import Stockfish

stockfish = Stockfish("stockfish_15_win_x64_avx2/stockfish_15_x64_avx2.exe")
column = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


base_board = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]


def checking_cur_board(board):
    if stockfish.is_fen_valid(board):
        stockfish.set_fen_position(board)
        return True
    else:
        return False


def make_matrix_board(board):
    end_board = []
    correct_board = {'r': 'bR', 'n': 'bN', 'b': 'bB', 'q': 'bQ', 'k': 'bK', 'p': 'bp',
                     'P': 'wp', 'R': 'wR', 'N': 'wN', 'B': 'wB', 'Q': 'wQ', 'K': 'wK'}
    pieces = board.split(" ", 1)[0]
    rows = pieces.split("/")
    for row in rows:
        cur_board = []
        for cell in row:
            if cell.isdigit():
                for i in range(0, int(cell)):
                    cur_board.append('--')
            else:
                cur_board.append(correct_board[cell])
        end_board.append(cur_board)
    return end_board


# Преобразование хода по FEN в координаты матрицы
def transition_board(fen_move):
    norm_move = [1, 2, 3, 4]
    for item in range(len(fen_move)):
        if fen_move[item].isdigit():
            norm_move[item-1] = (7 - (int(fen_move[item]) - 1))
        else:
            norm_move[item + 1] = column.index(fen_move[item])
    return norm_move


def getting_col(digit):
    return column[digit]


def get_computer_move():
    move_for_info = stockfish.get_best_move_time(1250)
    stockfish.make_moves_from_current_position([move_for_info])
    computer_move = move_for_info[0:4]
    computer_move = transition_board(computer_move)
    return move_for_info, computer_move


def check_pawn_transformations(move):
    if stockfish.is_move_correct(move):
        return True
    return False


def check_correct_move(move):
    if stockfish.is_move_correct(move):
        stockfish.make_moves_from_current_position([move])
        return True
    return False


def get_cur_position():
    cur_position = stockfish.get_fen_position()
    cur_position = make_matrix_board(cur_position)
    return cur_position


def get_student_move(flag_move_player=None):
    if flag_move_player:
        file_name = 'white_move.txt'
    elif flag_move_player == False:
        file_name = 'black_move.txt'
    else:
        file_name = 'student_move.txt'
    with open(file_name, 'r', encoding='utf-8') as file_student:
        text_info = file_student.readlines()
        if len(text_info) < 3 or (len(text_info) > 2 and text_info[2].strip() == ""):
            return -1
    with open(file_name, 'w', encoding='utf-8') as file_student:
        cur_board = stockfish.get_fen_position().split(' ')
        file_student.write(cur_board[0] + " " + cur_board[1] + "\n")
        file_student.write("0\n")

    return text_info[2].strip()


def broadcast_move(flag_move_player=None):
    if flag_move_player:
        file_name = 'white_move.txt'
    elif flag_move_player == False:
        file_name = 'black_move.txt'
    else:
        file_name = 'student_move.txt'
    with open(file_name, 'w', encoding='utf-8') as file_student:
        cur_board = stockfish.get_fen_position().split(' ')
        file_student.write(cur_board[0]+" "+cur_board[1] + "\n")
        file_student.write("1\n")


def get_end_game(flag_move_player):
    board = chess.Board(stockfish.get_fen_position())
    if board.is_stalemate():
        if flag_move_player:
            return 'Черные поставили пат.'
        else:
            return 'Белые поставили пат.'
    else:
        if flag_move_player:
            return 'Черные поставили мат.'
        else:
            return 'Белые поставили мат.'
