from PyQt5.QtWidgets import QWidget

from ui.ui_location_item import Ui_location_item

class LocationItem(QWidget, Ui_location_item):
    def __init__(self, name, adress):
        super().__init__()
        self.setupUi(self)
        self.name = name
        self.adress = adress
        self.set_text_label()

    def set_text_label(self):
        self.label_name.setText(self.name)
        self.label_adress.setText(self.adress)
        self.setStyleSheet("""
    border-style: outset;
    border-width: 2px;
    border-color: beige;""")

