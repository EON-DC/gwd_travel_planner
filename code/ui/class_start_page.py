from PyQt5.QtWidgets import QWidget

from ui_start_page import Ui_start_page


class StartPage(QWidget, Ui_start_page):
    def __init__(self):
        super().__init__()
        self.setupUi(self)