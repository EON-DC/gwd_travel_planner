from PyQt5.QtWidgets import QWidget

from ui_select_schedule import Ui_select_schedule


class SelectSchedule(QWidget, Ui_select_schedule):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
