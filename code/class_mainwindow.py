import sys

from PyQt5.QtWidgets import *

from ui.class_start_page import StartPage
from ui.class_first_trip import FirstTrip
from ui.class_recall_previous_trip import RecallPreviousTrip
from ui.class_select_planner import SelectPlanner


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.start_page = StartPage()       # 시작페이지 페이지
        self.first_trip = FirstTrip()       # 처음 여행 페이지
        self.prev_trip = RecallPreviousTrip()   # 이전 여행 페이지
        self.select_planner = SelectPlanner()   # 스케줄러 페이지



















