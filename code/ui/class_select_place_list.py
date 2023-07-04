from PyQt5.QtWidgets import QWidget

from ui_select_place_list import Ui_select_place_list


class SelectPlace(QWidget, Ui_select_place_list):
    def __init__(self):
        super().__init__()
        self.setupUi(self)