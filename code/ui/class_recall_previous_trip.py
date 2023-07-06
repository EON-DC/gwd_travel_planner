from PyQt5.QtWidgets import QWidget
# from ui_recall_previous_trip import Ui_recall_proevious_trip
from ui.ui_recall_previous_trip import Ui_recall_proevious_trip


class RecallPreviousTrip(QWidget, Ui_recall_proevious_trip):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window

        self.btn_back.mousePressEvent = lambda x: self.page_move("back")
        self.btn_next.mousePressEvent = lambda x: self.page_move("next")


    def page_move(self, btn):
        if btn == "back":
            print("이전")
            self.close()

        elif btn == "next":
            print("다음")
            self.main_window.select_planner.show()