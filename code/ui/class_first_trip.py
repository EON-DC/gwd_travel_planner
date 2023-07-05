from PyQt5.QtWidgets import QWidget

from ui.ui_first_trip import Ui_first_trip


class FirstTrip(QWidget, Ui_first_trip):
    def __init__(self):
        super().__init__()
        self.setupUi(self)