from PyQt5.QtWidgets import QWidget, QHBoxLayout

from ui.class_location_item import LocationItem
from ui.ui_select_planner import Ui_select_planner

# 연습용 위젯
class SelectPlanner(QWidget, Ui_select_planner):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_recomend_location()

    def set_recomend_location(self):
        attration_layout = QHBoxLayout(self.widget_rec_attraction)
        self.widget_rec_attraction.setLayout(attration_layout)
        attration_layout.addWidget(LocationItem("국수집", "소촌동"))
        attration_layout.addWidget(LocationItem("꽃집", "소촌동"))
        attration_layout.addWidget(LocationItem("족발집", "소촌동"))
        attration_layout.addWidget(LocationItem("김밥집", "소촌동"))