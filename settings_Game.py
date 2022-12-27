import subprocess
from _winapi import CREATE_NO_WINDOW

import chess
from models import Stockfish

stockfish = Stockfish("stockfish_15_win_x64_avx2/stockfish_15_x64_avx2.exe")
column = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


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
    move_for_info = stockfish.get_best_move()
    stockfish.make_moves_from_current_position([move_for_info])
    computer_move = transition_board(move_for_info)
    return move_for_info, computer_move


def check_correct_move(move):
    if stockfish.is_move_correct(move):
        stockfish.make_moves_from_current_position([move])
        return True
    return False


def get_cur_position():
    cur_position = stockfish.get_fen_position()
    cur_position = make_matrix_board(cur_position)
    return cur_position


def get_student_move(kol_move):                         # режимы компьютер-программа, человек-программа
    with open('student_move.txt') as file_student:
        move_student = file_student.read().split('\n')
        if len(move_student) == kol_move:
            move = move_student[kol_move-1]
            if len(move) == 0:
                return -1
            return move
        return -1


def student_play(kol_move, flag_move_player):
    if flag_move_player:
        with open('white_move.txt') as file_student:
            move_student = file_student.read().split('\n')
            if len(move_student) == kol_move:
                move = move_student[kol_move - 1]
                if len(move) == 0:
                    return -1
                return move
            return -1
    else:
        with open('black_move.txt') as file_student:
            move_student = file_student.read().split('\n')
            if len(move_student) == kol_move:
                move = move_student[kol_move - 1]
                if len(move) == 0:
                    return -1
                return move
            return -1


def broadcast_move(move, flag_move_player=None):
    if flag_move_player:
        with open('white_move.txt', 'a', encoding='utf-8') as file_student:
            file_student.write("\nХод противника: " + move)
    elif flag_move_player == None:
        with open('student_move.txt', 'a', encoding='utf-8') as file_student:
            file_student.write("\nХод противника: " + move)
    else:
        with open('black_move.txt', 'a', encoding='utf-8') as file_student:
            file_student.write("\nХод противника: " + move)


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
