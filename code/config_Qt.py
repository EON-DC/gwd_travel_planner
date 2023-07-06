from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QFont


def font_save():
    fontDB = QtGui.QFontDatabase()
    fontDB.addApplicationFont("../fonts/GANGWONSTATE-SemiBold.otf")


def set_font_style(widget):
    widget: QtWidgets.QWidget
    widget.setFont(QFont("강원특별자치도체 SemiBold"))
