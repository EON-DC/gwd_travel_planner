# 배포전 확인!
# UI 파일 삭제, database main 버전

import sys

from PyQt5 import QtCore, QtGui, QtWidgets
import class_main_window_controller
from class_dbconnect import DBConnector
from class_csv_reader import CSVReader


def main():
    app = QtWidgets.QApplication(sys.argv)
    dbconn = DBConnector()
    dbconn.create_tables()  # 배포전 확인! 이 라인 삭제해야함
    c_reader = CSVReader(dbconn)

    main_window = class_main_window_controller.WindowController(dbconn)
    main_window.start_page.show()

    sys.excepthook = lambda exctype, value, traceback: show_error_message(str(value), traceback)

    app.exec_()


def show_error_message(message, traceback):
    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(QtWidgets.QMessageBox.Critical)
    msg_box.setWindowTitle("Error")
    msg_box.setText(message)
    msg_box.exec_()
    traceback.print_exc()


if __name__ == '__main__':
    main()
