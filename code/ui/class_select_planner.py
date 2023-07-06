from PyQt5.QtWidgets import QWidget, QMessageBox
# from ui_select_planner import Ui_select_planner
from ui.ui_select_planner import Ui_select_planner


# 연습용 위젯
class SelectPlanner(QWidget, Ui_select_planner):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window

        self.rec_btn_list = [self.btn_rec_attraction, self.btn_rec_hotel]

        # 왼쪽 상단 버튼 초기 숨김
        for btn_hide in self.rec_btn_list:
            btn_hide.setVisible(False)

        self.btn_back.mousePressEvent = lambda x: self.page_move("back")

        self.btn_selection_1.clicked.connect(lambda x: self.page_move("select_1"))
        self.btn_selection_2.clicked.connect(lambda x: self.page_move("select_2_3"))
        self.btn_selection_3.clicked.connect(lambda x: self.page_move("select_2_3"))

        self.btn_rec_attraction.clicked.connect(lambda x: self.rec_change("attraction"))
        self.btn_rec_hotel.clicked.connect(lambda x: self.rec_change("hotel"))

        self.label_attraction_more.mousePressEvent = lambda x: self.rec_change("attraction")
        self.label_hotel_more.mousePressEvent = lambda x: self.rec_change("hotel")

        self.btn_selection_4.clicked.connect(lambda x: self.save_schedule("save"))

    def page_move(self, btn):
        if btn == "back":
            for btn_hide in self.rec_btn_list:
                btn_hide.setVisible(False)

            now_idx = self.stackedWidget.currentIndex()
            self.stackedWidget.setCurrentIndex(now_idx - 1)

            if now_idx == 0:
                print("이전 위젯 이동")
                self.close()


            elif now_idx == 3:
                self.stackedWidget.setCurrentIndex(1)

        elif btn == "select_1":
            print("코스 추천")
            self.stackedWidget.setCurrentIndex(1)



        elif btn == "select_2_3":
            check = QMessageBox.question(self, "확인", "일정에 담겼습니다.\n확인해보시겠습니까?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if check == QMessageBox.Yes:
                self.stackedWidget.setCurrentIndex(3)

                for btn_hide in self.rec_btn_list:
                    btn_hide.setVisible(False)

            elif check == QMessageBox.No:
                pass

    def rec_change(self, btn):
        self.stackedWidget.setCurrentIndex(2)

        for btn_show in self.rec_btn_list:
            btn_show.setVisible(True)

        if btn == "attraction":
            print("장소")
            self.label_rec.setText("추천 장소")

        elif btn == "hotel":
            print("호텔")
            self.label_rec.setText("추천 호텔")



    def save_schedule(self, btn):
        print("일정 선택 완료")
        check = QMessageBox.about(self, "확인", "일정이 저장되었습니다.")
        self.main_window.first_trip.close()
        self.main_window.prev_trip.close()
        self.close()
