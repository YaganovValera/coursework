#!/urs/bin/python3
#-*- coding: utf-8 -*-

import time
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
import sys

from settings_Game import *
from HillCipher import *

STATUS_game = False
Players = []                    # Имена игроков (0 объект - игрок за черных, 1 объект - игрок белых)

CELL_selection = []             # Для подсветки выброной фигуры
flag_draw_board = False         # Начальная отрисовка пользовательской доски
flag_move_player = False        # Смена хода (False - ход черных, True - ход белых)
flag_make_move = False          # Сделан ход (False - нет, True - да)
flag_pawn_replacement = False   # Для события когда пешка доходит доконца

USER_board = []                 # Доска пользователя в матричном виде
USER_move = ''                  # Ход человека


# Класс отвечающий за стартовое окно
class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("Qt_form/qt_login.ui", self)

        self.line_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_btn.clicked.connect(lambda: self.personal_ac())
        self.registr_btn.clicked.connect(lambda: self.registr())

    def personal_ac(self):
        global username
        username = self.line_username.text().strip()
        password = self.line_password.text().strip()
        if check_login(username, password, 'Вход'):
            self.line_username.setText('')
            self.line_password.setText('')
            widget.setFixedWidth(900)
            widget.setFixedHeight(715)
            widget.setCurrentWidget(account_window)
        else:
            error = QMessageBox()
            error.setWindowTitle("Ошибка\t\t\t\t\t")
            error.setText("Введены неверные данные.")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()

    def registr(self):
        self.line_username.setText('')
        self.line_password.setText('')
        widget.setCurrentWidget(new_ac_window)


# Класс отвечающий за окно регистрации
class Registration(QMainWindow):
    def __init__(self):
        super(Registration, self).__init__()
        loadUi("Qt_form/qt_registration.ui", self)

        self.new_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.replay_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.creat_ac_btn.clicked.connect(lambda: self.login_window(True))
        self.back_btn.clicked.connect(lambda: self.login_window(False))

    def login_window(self, flag):
        if flag:
            username = self.new_username.text().strip()
            password = self.new_password.text().strip()
            replay_password = self.replay_password.text().strip()
            if password != replay_password:
                error = QMessageBox()
                error.setWindowTitle("Ошибка\t\t\t\t\t")
                error.setText("Пароли не совпадают!")
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
                return False
            if check_login(username, password, 'Регистрация'):
                flag = False
            else:
                error = QMessageBox()
                error.setWindowTitle("Ошибка\t\t\t\t\t")
                error.setText("Введены неверный данные!")
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.setDetailedText(" Требования к паролю:\n"
                                      "1) Пароль может состоять из: \n"
                                      "- Латинского и русского алфавита\n"
                                      "- знаков препинания ('.', '!', '?', '_')\n"
                                      "- цифр (0-9)\n"
                                      "2) Длина пароля должна быть не менее 8 и не более 30\n"
                                      "Требования к логину: \n"
                                      " Длина логина должна быть не менее 2 и не более 50\n\n"
                                      "Примечание: Если все требования выполняются, но программа выдает ошибку."
                                      " Это означает,что такой аккаунт уже существует.")
                error.exec_()
        if not flag:
            self.new_username.setText('')
            self.new_password.setText('')
            self.replay_password.setText('')
            return widget.setCurrentWidget(login_window)


class Chess_Board(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.move_for_info = ''
        self.computer_move = []
        self.correct_student_move = True
        self.end_game = []

    def run(self):
        global STATUS_game, USER_board, flag_move_player, Players, flag_draw_board, USER_move, flag_make_move, flag_pawn_replacement
        try:
            while STATUS_game:
                time.sleep(0.75)
                if flag_draw_board:
                    if "Человек" in Players:
                        if Players[int(flag_move_player)] == "Человек":
                            if len(USER_move) >= 4 and flag_pawn_replacement:
                                if check_correct_move(USER_move):
                                    self.move_for_info = USER_move
                                    self.computer_move = transition_board(USER_move[0:4])
                                    USER_board = get_cur_position()
                                    flag_make_move = True
                                    flag_move_player = not flag_move_player
                                    broadcast_move()
                                USER_move = ''
                                flag_pawn_replacement = False
                            else:
                                continue
                        else:
                            student_move = get_student_move()
                            if student_move == -1:
                                continue
                            if not self.check_student_move(student_move):
                                self.correct_student_move = False
                                break

                    elif "Компьютер" in Players:
                        if Players[int(flag_move_player)] == "Компьютер":
                            self.move_for_info, self.computer_move = get_computer_move()
                            USER_board = get_cur_position()
                            broadcast_move()
                            flag_move_player = not flag_move_player
                            flag_make_move = True
                        else:
                            student_move = get_student_move()
                            if student_move == -1:
                                continue
                            if not self.check_student_move(student_move):
                                self.correct_student_move = False
                                break
                    else:
                        student_move = student_play(flag_move_player)
                        if student_move == -1:
                            continue
                        if not self.check_student_move(student_move):
                            self.correct_student_move = False
                            break
                        else:
                            broadcast_move(flag_move_player)

                    STATUS_game = checking_cur_board()
                    if not STATUS_game:
                        self.end_game = get_end_game(flag_move_player)
                    else:
                        board = chess.Board(stockfish.get_fen_position())
                        if board.is_insufficient_material():
                            self.end_game = 'Ничья из-за недостаточного материала.'
                            STATUS_game = False
                            self.clear_file()
                else:
                    self.correct_student_move = True
                    self.move_for_info = ''
                    flag_draw_board = True
                    continue
        except Exception as e:
            print(e)

    def check_student_move(self, student_move):
        global flag_make_move, flag_move_player, USER_board, STATUS_game
        if check_correct_move(student_move):
            self.move_for_info = student_move
            self.computer_move = transition_board(student_move[0:4])
            USER_board = get_cur_position()
            flag_move_player = not flag_move_player
            flag_make_move = True
            return True
        else:
            self.move_for_info = student_move
            STATUS_game = False
            return False


# Класс отвечающий за личный кабинет
class Personal_account(QMainWindow):
    def __init__(self):
        super(Personal_account, self).__init__()
        loadUi("Qt_form/qt_personal_ac.ui", self)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.draw_player_timer(flag_move_player))

        self.start_board()
        self.game = Chess_Board()
        self.player_color = ["черных", "белых"]
        self.count_move_white = 1
        self.count_move_black = 1
        self.start_time = 0
        self.cur_time = 0
        self.flag_white_p = False
        self.flag_black_p = False

        self.textEdit_player_white.setReadOnly(True)
        self.textEdit_player_black.setReadOnly(True)

        self.btn_start_Game.clicked.connect(lambda: self.settings_Game())
        self.btn_start_Game.clicked.connect(lambda: self.game.start())
        self.exit_btn.clicked.connect(lambda: self.exit())
        self.table_chess_board.cellClicked.connect(self.cell_click)
        self.table_chess_board.cellDoubleClicked.connect(self.cell_doubleclick)
        self.horizontalSlider.valueChanged.connect(self.set_time)

        self.timer_draw_move = QtCore.QTimer()
        self.timer_draw_move.timeout.connect(lambda: self.draw_move())

    def set_time(self, value):
        self.label_time.setText(str(value))

    def start_board(self):
        self.restart_board()
        self.textEdit_player_black.setText('')
        self.textEdit_player_white.setText('')
        self.cur_board = startBoard()
        self.draw_cur_board()

    def draw_cur_board(self):
        try:
            for i in range(self.table_chess_board.rowCount()):
                for j in range(self.table_chess_board.columnCount()):
                    item = QTableWidgetItem()
                    if self.cur_board.board[i][j] != "--":
                        icon = QtGui.QIcon()
                        icon.addPixmap(QtGui.QPixmap('img/'+self.cur_board.board[i][j]+'.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        item.setIcon(icon)
                    if (i + j) % 2 != 0:
                        brush = QtGui.QBrush(QtGui.QColor(170, 102, 6))
                    else:
                        brush = QtGui.QBrush(QtGui.QColor(255, 209, 99))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    item.setBackground(brush)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.table_chess_board.setItem(i, j, item)
        except Exception as e:
            print(e)

    def check_board(self, board):
        if checking_cur_board(board):
            self.cur_board.board = make_matrix_board(board)
            self.draw_cur_board()
            return True
        else:
            return False

    def check_comboBox(self):
        white = self.player_white_comboBox.currentText()
        black = self.player_black_comboBox.currentText()
        if (white == black == "Человек") or (white == black == "Компьютер") \
                or (white == "Человек" and black == "Компьютер") or (white == "Компьютер" and black == "Человек"):
            return False
        self.players = [black, white]
        return True

    def settings_Game(self):
        global STATUS_game, USER_board, Players, flag_move_player, flag_draw_board
        self.restart_board()
        self.l_timer_white.setText(self.label_time.text()+":00")
        self.l_timer_black.setText(self.label_time.text()+":00")
        txt_user_board = self.txt_start_board.text().strip()
        if txt_user_board != '' and txt_user_board[-1] == 'w':
            flag_move_player = True
        else:
            flag_move_player = False
        txt_user_board += " - - 0 1"
        if self.check_comboBox():
            if self.check_board(txt_user_board):

                if ('Человек' in self.players) or ('Компьютер' in self.players):
                    with open('student_move.txt', 'w', encoding='utf8') as file_student:
                        file_student.write(self.txt_start_board.text().strip() + '\n')
                        if self.players[int(flag_move_player)] == 'Программа студента' and int(flag_move_player) == 0:
                            file_student.write("1\n")
                        elif self.players[int(flag_move_player)] == 'Программа студента' and int(flag_move_player) == 1:
                            file_student.write("1\n")
                        else:
                            file_student.write("0\n")
                else:
                    with open('white_move.txt', 'w', encoding='utf8') as file_student:
                        file_student.write(self.txt_start_board.text().strip()+'\n')
                        if int(flag_move_player) == 1:
                            file_student.write("1\n")
                        else:
                            file_student.write("0\n")
                    with open('black_move.txt', 'w', encoding='utf8') as file_student:
                        file_student.write(self.txt_start_board.text().strip() + '\n')
                        if int(flag_move_player) == 0:
                            file_student.write("1\n")
                        else:
                            file_student.write("0\n")

                self.timer.start(1000)
                self.timer_draw_move.start(500)
                STATUS_game = True
                self.start_time = int(self.label_time.text()) * 60

                USER_board = self.cur_board.board
                Players = self.players
                flag_draw_board = False
                self.textEdit_player_black.setText('')
                self.textEdit_player_white.setText('')

            else:
                self.start_board()
                self.error_user_board()
        else:
            self.start_board()
            self.error_user_board()

    def draw_player_timer(self, timer_color):
        global STATUS_game, flag_make_move
        if timer_color and not flag_make_move:
            cur_timer = self.l_timer_white.text().split(':')
        elif not timer_color and not flag_make_move:
            cur_timer = self.l_timer_black.text().split(':')
        else:
            return
        if int(cur_timer[1]) == 0 and int(cur_timer[0]) != 0:
            cur_timer = [int(cur_timer[0])-1, 59]
        elif int(cur_timer[1]) != 0:
            cur_timer = [int(cur_timer[0]), int(cur_timer[1])-1]
        if cur_timer[0] == 0 and cur_timer[1] == 0:
            if timer_color:
                STATUS_game = False
                self.game_result.setText("Поражение белых, т.к закончилось время.")
                flag_make_move = False
                self.timer_draw_move.stop()
                self.timer.stop()
                self.game.exit()
            else:
                STATUS_game = False
                self.game_result.setText("Поражение черных, т.к закончилось время.")
                flag_make_move = False
                self.timer_draw_move.stop()
                self.timer.stop()
                self.game.exit()
        if timer_color:
            if cur_timer[1] < 10:
                self.l_timer_white.setText(str(cur_timer[0])+":0"+str(cur_timer[1]))
            else:
                self.l_timer_white.setText(str(cur_timer[0]) + ":" + str(cur_timer[1]))
        else:
            if cur_timer[1] < 10:
                self.l_timer_black.setText(str(cur_timer[0]) + ":0" + str(cur_timer[1]))
            else:
                self.l_timer_black.setText(str(cur_timer[0]) + ":" + str(cur_timer[1]))

    def draw_move(self):
        global STATUS_game, USER_board, Players, flag_move_player, flag_draw_board, flag_make_move
        try:
            if not self.game.correct_student_move:
                self.timer_draw_move.stop()
                self.timer.stop()
                self.game.exit()
                STATUS_game = False
                self.clear_file()
                self.error_student()
                self.game.correct_student_move = True

            elif flag_make_move:
                for cell in range(0, len(self.game.computer_move), 2):
                    item = QtWidgets.QTableWidgetItem()
                    x = int(self.game.computer_move[cell])
                    y = int(self.game.computer_move[cell + 1])
                    if USER_board[x][y] != "--":
                        icon = QtGui.QIcon()
                        icon.addPixmap(QtGui.QPixmap('img/'+USER_board[x][y]+'.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        item.setIcon(icon)
                    if (x + y) % 2 != 0:
                        brush = QtGui.QBrush(QtGui.QColor(170, 102, 6))
                    else:
                        brush = QtGui.QBrush(QtGui.QColor(255, 209, 99))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    item.setBackground(brush)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.table_chess_board.setItem(x, y, item)

                # Отрисовка взятия на проходе
                if (USER_board[int(self.game.computer_move[2])][int(self.game.computer_move[3])] == "wp"
                        and int(self.game.computer_move[0]) == 3) or \
                        (USER_board[int(self.game.computer_move[2])][int(self.game.computer_move[3])] == "bp"
                         and int(self.game.computer_move[0]) == 4)\
                        and int(self.game.computer_move[1]) != int(self.game.computer_move[3]):
                    x = int(self.game.computer_move[0])
                    y = int(self.game.computer_move[3])
                    item = QtWidgets.QTableWidgetItem()
                    if USER_board[x][y] != "--":
                        icon = QtGui.QIcon()
                        icon.addPixmap(QtGui.QPixmap('img/' + USER_board[x][y] + '.png'), QtGui.QIcon.Normal,
                                       QtGui.QIcon.Off)
                        item.setIcon(icon)
                    if (x + y) % 2 != 0:
                        brush = QtGui.QBrush(QtGui.QColor(170, 102, 6))
                    else:
                        brush = QtGui.QBrush(QtGui.QColor(255, 209, 99))
                    brush.setStyle(QtCore.Qt.SolidPattern)
                    item.setBackground(brush)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.table_chess_board.setItem(x, y, item)

                flag_make_move = False
                if not flag_move_player:
                    self.cur_time = int(self.l_timer_white.text().split(":")[0])*60 + \
                                    int(self.l_timer_white.text().split(":")[1])
                    self.textEdit_player_white.setText(self.textEdit_player_white.toPlainText()
                                                       + str(self.count_move_white)
                                                       + ") Ход: " + self.game.move_for_info + " / Время на ход: "
                                                       + str(self.start_time-self.cur_time) + " сек;\n")
                    self.start_time = int(self.l_timer_black.text().split(":")[0])*60 + \
                                      int(self.l_timer_black.text().split(":")[1])
                    self.count_move_white += 1
                else:
                    self.cur_time = int(self.l_timer_black.text().split(":")[0]) * 60 + \
                                    int(self.l_timer_black.text().split(":")[1])
                    self.textEdit_player_black.setText(self.textEdit_player_black.toPlainText() + str(self.count_move_black)
                                                       + ") Ход: " + self.game.move_for_info + " / Время на ход: "
                                                       + str(self.start_time-self.cur_time) + " сек;\n")
                    self.start_time = int(self.l_timer_white.text().split(":")[0]) * 60 + \
                                      int(self.l_timer_white.text().split(":")[1])
                    self.count_move_black += 1

                if not STATUS_game:
                    if len(self.game.end_game) != 0:
                        self.game_result.setText(self.game.end_game)
                        self.timer_draw_move.stop()
                        self.timer.stop()
                        self.game.exit()
                        self.clear_file()
        except Exception as e:
            print(e)

    def error_student(self):
        global Players, flag_move_player
        error = QMessageBox()
        error.setWindowTitle("Ошибка со стороны студента!\t\t\t\t\t")
        error.setText("Введены неверный данные со стороны " + self.player_color[flag_move_player])
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.setDetailedText("Со стороны программы студента были введены следующие данные: " + self.game.move_for_info)
        error.exec_()

    def restart_board(self):
        global STATUS_game, USER_board, Players, flag_move_player, flag_draw_board, USER_move, flag_make_move
        STATUS_game = False
        Players = []
        flag_draw_board = False
        flag_move_player = False
        flag_make_move = False
        USER_board = []
        USER_move = ''
        self.timer.start(2000)
        self.timer.stop()
        self.count_move_white = 1
        self.count_move_black = 1
        self.flag_black_p = False
        self.flag_white_p = False
        self.l_timer_white.setText("10:00")
        self.l_timer_black.setText("10:00")
        self.game_result.setText('')
        self.clear_file()

    def clear_file(self):
        with open('student_move.txt', 'w', encoding='utf-8') as file_student:
            file_student.write('')
        with open('black_move.txt', 'w', encoding='utf-8') as file_student:
            file_student.write('')
        with open('white_move.txt', 'w', encoding='utf-8') as file_student:
            file_student.write('')

    def cell_click(self, row, col):
        global USER_move, flag_move_player, Players, USER_board, USER_move, STATUS_game, CELL_selection, flag_pawn_replacement
        if STATUS_game and Players[flag_move_player] == "Человек":
            letter = getting_col(col)
            digit = str(8 - row)
            move = letter + digit
            if len(USER_move) < 2 and USER_board[row][col] != "--":
                CELL_selection = [row, col]
                self.cell_selected(CELL_selection, True)
                USER_move += move
                if USER_board[row][col] == "wp" and row == 1:
                    self.flag_white_p = True
                elif USER_board[row][col] == "bp" and row == 6:
                    self.flag_black_p = True
                else:
                    self.flag_white_p = False
                    self.flag_black_p = False
            elif len(USER_move) == 2:
                USER_move += move
                self.cell_selected(CELL_selection, False)
                if self.flag_black_p and row == 7:
                    self.choos_figure()
                elif self.flag_white_p and row == 0:
                    self.choos_figure()
                flag_pawn_replacement = True
                self.flag_white_p = False
                self.flag_black_p = False

    def choos_figure(self):
        error = QMessageBox()
        error.setWindowTitle("Выбор фигуры.\t\t\t\t\t")
        error.setText("Если вы хотите выбрать Ферзя, то нажмите Ok. Если вы нажмете кнопку No, то замените пешку на коня.")
        error.setStandardButtons(QMessageBox.Ok | QMessageBox.No )
        error.buttonClicked.connect(self.info_btn)
        error.exec_()

    def info_btn(self, btn):
        global USER_move
        if btn.text() == 'OK':
            USER_move += 'q'
        else:
            USER_move += 'n'

    def cell_doubleclick(self, row, col):
        try:
            global USER_move, flag_move_player, Players, USER_board, USER_move, STATUS_game, CELL_selection
            if STATUS_game and Players[flag_move_player] == "Человек":
                letter = getting_col(col)
                digit = str(8 - row)
                move = letter + digit
                if USER_board[row][col] != "--":
                    self.cell_selected(CELL_selection, False)
                    CELL_selection = [row, col]
                    self.cell_selected(CELL_selection, True)
                    USER_move = move
                    if USER_board[row][col] == "wp" and row == 1:
                        self.flag_white_p = True
                    elif USER_board[row][col] == "bp" and row == 6:
                        self.flag_black_p = True
                    else:
                        self.flag_white_p = False
                        self.flag_black_p = False
                else:
                    USER_move = ''
        except Exception as e:
            print(e)

    def cell_selected(self, cell_data, flag_rendering):
        try:
            item = QtWidgets.QTableWidgetItem()
            x = cell_data[0]
            y = cell_data[1]
            if USER_board[x][y] != "--":
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap('img/' + USER_board[x][y] + '.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item.setIcon(icon)
            if flag_rendering:
                brush = QtGui.QBrush(QtGui.QColor(266, 167, 72))
            else:
                if (x + y) % 2 != 0:
                    brush = QtGui.QBrush(QtGui.QColor(170, 102, 6))
                else:
                    brush = QtGui.QBrush(QtGui.QColor(255, 209, 99))
            brush.setStyle(QtCore.Qt.SolidPattern)
            item.setBackground(brush)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_chess_board.setItem(x, y, item)
        except Exception as e:
            print(e)

    def error_user_board(self):
        error = QMessageBox()
        error.setWindowTitle("Ошибка\t\t\t\t\t")
        error.setText("Введены неверный данные!")
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.setDetailedText("Данные должны быть представлены по стандарту FEN.(А именно должна быть стартовая расстановка и цвет игрока, который начинает игру)\n"
                              "Пример начальной расстановки: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w.\n"
                              "\n"
                              "В игре отсутствуют следующие режимы: Человек/Человек; Компьютер/Человек; Компьютер/Компьютер.")
        error.exec_()

    def exit(self):
        error = QMessageBox()
        error.setWindowTitle("Предупреждение\t\t\t\t\t")
        error.setText("Вы уверены что хотите выйти из личного кабинета?")
        error.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        error.buttonClicked.connect(self.click_btn)
        error.exec_()

    def click_btn(self, btn):
        if btn.text() == 'OK':
            self.start_board()
            self.txt_start_board.setText('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w')
            self.horizontalSlider.setValue(10)
            self.timer_draw_move.stop()
            self.timer.stop()
            self.game.exit()
            widget.setFixedWidth(560)
            widget.setFixedHeight(350)
            widget.setCurrentWidget(login_window)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()
    new_ac_window = Registration()
    account_window = Personal_account()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(login_window)
    widget.addWidget(new_ac_window)
    widget.addWidget(account_window)
    widget.setFixedWidth(560)
    widget.setFixedHeight(350)
    widget.show()
    sys.exit(app.exec_())

