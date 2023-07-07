from PyQt5.QtWidgets import QWidget

from ui.ui_location_item import Ui_location_item
# from ui_location_item import Ui_location_item

class LocationItem(QWidget, Ui_location_item):
    def __init__(self, name, address, category=None):
        super().__init__()
        self.setupUi(self)
        self.name = name
        self.address = address
        self.category = category

        self.set_text_location()

    def set_text_location(self):
        self.label_name.setText(f"{self.name}")
        self.label_adress.setText(f"{self.address}")



