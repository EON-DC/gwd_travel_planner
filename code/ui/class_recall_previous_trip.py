from PyQt5.QtWidgets import QWidget

from ui.ui_recall_previous_trip import Ui_recall_proevious_trip


class RecallPreviousTrip(QWidget, Ui_recall_proevious_trip):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
