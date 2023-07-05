# 배포전 확인!
# UI 파일 삭제, database main 버전

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3 
import pandas as pd
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium

import class_mainwindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = class_mainwindow.MainWindow()
    # main_window.start_page.show()
    # main_window.first_trip.show()
    # main_window.prev_trip.show()
    main_window.select_planner.show()

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
