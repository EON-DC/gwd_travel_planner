from PyQt5.QtWidgets import *

from ui.class_first_trip import FirstTrip
from ui.class_recall_previous_trip import RecallPreviousTrip
from ui.class_select_planner import SelectPlanner
from ui.class_start_page import StartPage


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.start_page = StartPage(self)       # 시작페이지 페이지
        self.first_trip = FirstTrip(self)       # 처음 여행 페이지
        self.prev_trip = RecallPreviousTrip(self)   # 이전 여행 페이지
        self.select_planner = SelectPlanner(self)   # 스케줄러 페이지



















