#!/urs/bin/python3
#-*- coding: utf-8 -*-
import time

from PyQt5 import QtWidgets, Qt, QtGui, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QAbstractItemView
import sys

from Game import *
from HillCipher import *

KEY_login = "encode123"

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
            widget.addWidget(account_window)
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


# Класс отвечающий за личный кабинет
class Personal_account(QMainWindow):
    def __init__(self):
        super(Personal_account, self).__init__()
        loadUi("qt_personal_ac.ui", self)
        self.start()

        self.exit_btn.clicked.connect(lambda: self.exit())
        self.btn_start_Game.clicked.connect(lambda: self.Game())


    def start(self):
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
                    item.textAlignment()
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.table_chess_board.setItem(i, j, item)
        except Exception as e:
            print(e)
            # self.start()
            # self.error_user_board()


    def Game(self):
        try:
            txt_user_board = self.txt_start_board.text().strip()
            if txt_user_board != '' and txt_user_board[-1] == 'w':
                flag_move_player = True
            else:
                flag_move_player = False
            txt_user_board += " - - 0 1"
            if self.check_board(txt_user_board):
                if self.check_comboBox():
                    black_player = self.player_black_comboBox.currentText()
                    white_player = self.player_white_comboBox.currentText()
                    players = [black_player, white_player]
                    while checking_cur_board():
                    # if "Человек" in players:
                    # for i in range(5):
                        if players[int(flag_move_player)] == "Человек":
                            # self.table_chess_board.cellClicked.connect(self.cellclicked)
                            # print("gg")
                            # flag_move_player = not flag_move_player
                            # self.computer_move = get_computer_move()
                            # self.cur_board.board[int(self.computer_move[2])][int(self.computer_move[3])] = \
                            #     self.cur_board.board[int(self.computer_move[0])][int(self.computer_move[1])]
                            #
                            # self.cur_board.board[int(self.computer_move[0])][int(self.computer_move[1])] = "--"
                            # flag_move_player = not flag_move_player
                            # self.draw_cur_board()
                            self.computer_move = get_computer_move()
                            self.cur_board.board[int(self.computer_move[2])][int(self.computer_move[3])] = \
                                self.cur_board.board[int(self.computer_move[0])][int(self.computer_move[1])]

                            self.cur_board.board[int(self.computer_move[0])][int(self.computer_move[1])] = "--"
                            flag_move_player = not flag_move_player
                            self.draw_cur_board()
                        else:
                            self.computer_move = get_computer_move()
                            self.cur_board.board[int(self.computer_move[2])][int(self.computer_move[3])] =\
                                self.cur_board.board[int(self.computer_move[0])][int(self.computer_move[1])]

                            self.cur_board.board[int(self.computer_move[0])][int(self.computer_move[1])] = "--"
                            flag_move_player = not flag_move_player
                            self.draw_cur_board()

                else:
                    self.error_user_board()
        except Exception as e:
            print(e)

    def cellclicked(self, row, col):
        print(row, col)

    def check_board(self, board):
        if checking_cur_board(board):
            self.cur_board.board = make_matrix_board(board)
            self.draw_cur_board()
            return True
        else:
            self.start()
            self.error_user_board()
            return False

    def check_comboBox(self):
        white = self.player_white_comboBox.currentText()
        black = self.player_black_comboBox.currentText()
        if (white == black == "Человек") or (white == black == "Компьютер") \
                or (white == "Человек" and black == "Компьютер") or (white == "Компьютер" and black == "Человек"):
            return False
        return True

    def draw_move(self):
        for cell in range(0, len(self.computer_move), 2):
            item = QtWidgets.QTableWidgetItem()
            x = int(self.computer_move[cell])
            y = int(self.computer_move[cell + 1])
            if self.cur_board.board[x][y] != "--":
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap('img/'+self.cur_board.board[x][y]+'.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                item.setIcon(icon)
            if (x + y) % 2 != 0:
                brush = QtGui.QBrush(QtGui.QColor(170, 102, 6))
            else:
                brush = QtGui.QBrush(QtGui.QColor(255, 209, 99))
            brush.setStyle(QtCore.Qt.SolidPattern)
            item.setBackground(brush)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_chess_board.setItem(x, y, item)
            self.table_chess_board.show()

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
            self.start()
            widget.removeWidget(account_window)
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
    widget.show()
    sys.exit(app.exec_())

