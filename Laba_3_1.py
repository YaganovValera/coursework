#!/urs/bin/python3
#-*- coding: utf-8 -*-
import time

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
import sys

from Game import *
from HillCipher import *

KEY_login = "stockfish"

STATUS_game = False
Players = []                # Имена игроков (0 объект - игрок за черных, 1 объект - игрок белых)

flag_draw_board = False     # Начальная отрисовка пользовательской доски
flag_move_player = False    # Смена хода (False - ход черных, True - ход белых)
flag_make_move = False      # Сделан ход (False - нет, True - да)

USER_board = []             # Доска пользователя в матричном виде
USER_move = ''              # Ход человека

# Класс отвечающий за стартовое окно
class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("qt_login.ui", self)
        self.login()

    def login(self):
        self.line_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_btn.clicked.connect(lambda: self.personal_ac())
        self.registr_btn.clicked.connect(lambda: self.registr())

    def personal_ac(self):
        global username
        username = self.line_username.text().strip()
        password = self.line_password.text()
        # if check_login(username, password, KEY_login):
        if True:
            self.line_username.setText('')
            self.line_password.setText('')
            widget.setFixedWidth(900)
            widget.setFixedHeight(790)
            widget.setCurrentWidget(account_window)
        else:
            error = QMessageBox()
            error.setWindowTitle("Ошибка\t\t\t\t\t")
            error.setText("Введен неверный логин или пароль.")
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
        loadUi("qt_registration.ui", self)
        self.registration()

    def registration(self):
        self.new_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.replay_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.creat_ac_btn.clicked.connect(lambda: self.login_window(True))
        self.back_btn.clicked.connect(lambda: self.login_window(False))

    def login_window(self, flag):
        if flag:
            username = self.new_username.text().strip()
            password = self.new_password.text()
            replay_password = self.replay_password.text()
            if password != replay_password:
                error = QMessageBox()
                error.setWindowTitle("Ошибка\t\t\t\t\t")
                error.setText("Пароли не совпадают!")
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.exec_()
                return False
            registr = check_registr(username, password, KEY_login)
            if registr ==True:
                flag = False
            else:
                error = QMessageBox()
                error.setWindowTitle("Ошибка\t\t\t\t\t")
                error.setText("Введены неверный данные!")
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.setDetailedText(" Требования к паролю:\n"
                                      "1) Пароль может состоять из: \n"
                                      "- Латинского алфавита (a-z; A-Z)\n"
                                      "- знаков препинания ('.', '!', '?', ',', '_')\n"
                                      "- цифр (0-9)\n"
                                      "2) Длина пароля должна быть не менее 8 и не более 30\n"
                                      "Требования к логину: \n"
                                      " Длина логина должна быть не менее 2 и не более 50\n\n"
                                      "Примечание: Если все требования выполняются, но программа выдает ошибку. Это значит,"
                                      " что пользователь с таким логином или паролем уже существует.")
                error.exec_()
        if not flag:
            self.new_username.setText('')
            self.new_password.setText('')
            self.replay_password.setText('')
            return widget.setCurrentWidget(login_window)


class Chess_Board(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.computer_move = []
        self.counter_move = 2

    def run(self):
        global STATUS_game, USER_board, flag_move_player, Players, flag_draw_board, USER_move, flag_make_move
        try:
            while STATUS_game:
                if flag_draw_board:
                    if "Человек" in Players:
                        if Players[int(flag_move_player)] == "Человек":
                            if len(USER_move) == 4:
                                if check_correct_move(USER_move):
                                    self.computer_move = transition_board(USER_move)
                                    USER_board = get_cur_position()
                                    flag_move_player = not flag_move_player
                                    flag_make_move = True
                                    time.sleep(1)
                                USER_move = ''
                        else:
                            student_move = get_student_move(self.count_move)
                            if student_move == -1:
                                continue
                            if check_correct_move(student_move):
                                self.computer_move = transition_board(student_move)
                                USER_board = get_cur_position()
                                flag_move_player = not flag_move_player
                                flag_make_move = True
                                self.count_move += 1
                                time.sleep(2)
                            else:
                                STATUS_game = False
                                print("149")
                                break
                    STATUS_game = checking_cur_board()
                else:
                    self.count_move = 2
                    flag_draw_board = True
                time.sleep(1)
        except Exception as e:
            print("157")
            print(e)


# Класс отвечающий за личный кабинет
class Personal_account(QMainWindow):
    def __init__(self):
        super(Personal_account, self).__init__()
        loadUi("qt_personal_ac.ui", self)
        self.start_board()
        self.game = Chess_Board()

        self.btn_start_Game.clicked.connect(lambda: self.settings_Game())
        self.btn_start_Game.clicked.connect(lambda: self.game.start())
        self.exit_btn.clicked.connect(lambda: self.exit())
        self.table_chess_board.cellClicked.connect(self.cell_click)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.draw_move())
        self.timer.start(1000)

    def start_board(self):
        self.restart_board()
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
        return True

    def settings_Game(self):
        global STATUS_game, USER_board, Players, flag_move_player, flag_draw_board
        self.restart_board()
        txt_user_board = self.txt_start_board.text().strip()
        if txt_user_board != '' and txt_user_board[-1] == 'w':
            self.flag_move_player = True
        else:
            self.flag_move_player = False
        txt_user_board += " - - 0 1"
        if self.check_board(txt_user_board):
            if self.check_comboBox():
                black_player = self.player_black_comboBox.currentText()
                white_player = self.player_white_comboBox.currentText()
                self.players = [black_player, white_player]
                STATUS_game = True
                USER_board = self.cur_board.board
                Players = self.players
                flag_move_player = self.flag_move_player
            else:
                self.start_board()
                self.error_user_board()
        else:
            self.start_board()
            self.error_user_board()

    def draw_move(self):
        global STATUS_game, USER_board, Players, flag_move_player, flag_draw_board, flag_make_move
        try:
            if flag_make_move:
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
                    flag_make_move = False
                if not STATUS_game:
                    flag_make_move = False
        except Exception as e:
            print("268")
            print(e)

    def restart_board(self):
        global STATUS_game, USER_board, Players, flag_move_player, flag_draw_board, USER_move, flag_make_move
        STATUS_game = False
        Players = []
        flag_draw_board = False
        flag_move_player = False
        flag_make_move = False
        USER_board = []
        USER_move = ''

    def cell_click(self, row, col):
        global USER_move, flag_move_player, Players, USER_board, USER_move, STATUS_game
        if STATUS_game and Players[flag_move_player] == "Человек":
            letter = getting_col(col)
            digit = str(8 - row)
            move = letter + digit
            if len(USER_move) < 2 and USER_board[row][col] != "--":
                USER_move += move
            elif len(USER_move) < 4:
                USER_move += move

    def error_user_board(self):
        error = QMessageBox()
        error.setWindowTitle("Ошибка\t\t\t\t\t")
        error.setText("Введены неверный данные!")
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.setDetailedText("Данные должны быть представлены по стандарту FEN.\n"
                              "Пример начальной расстановки: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w.\n"
                              "\n"
                              "В игре Человек не может играть против Компьютера и Человека. И компьютер не может играть против компьютера.")
        error.exec_()

    def exit(self):
        error = QMessageBox()
        error.setWindowTitle("Предупреждение\t\t\t\t\t")
        error.setText("Вы уверены что хотите выйти из лчного кабинета?")
        error.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        error.buttonClicked.connect(self.click_btn)
        error.exec_()

    def click_btn(self, btn):
        if btn.text() == 'OK':
            self.start_board()
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

