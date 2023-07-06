from PyQt5.QtWidgets import QWidget
# from ui_start_page import Ui_start_page
from ui.ui_start_page import Ui_start_page


class StartPage(QWidget, Ui_start_page):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window


        self.btn_new_trip.clicked.connect(lambda x: self.page_move("new_trip"))
        self.btn_prev_trip.clicked.connect(lambda x: self.page_move("prev_trip"))

    def page_move(self, btn):
        if btn == "new_trip":
            print("새로운 여행 떠나기")
            self.main_window.first_trip.show()

        elif btn == "prev_trip":
            print("이전 여행 불러오기")
            self.main_window.prev_trip.show()

        else:
            pass