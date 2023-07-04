from PyQt5.QtWidgets import QWidget

from ui_recommended_place import Ui_recommended_place


class RecommendedPlace(QWidget, Ui_recommended_place):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
