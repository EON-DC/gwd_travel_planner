from PyQt5.QtWidgets import QWidget, QMessageBox
# from ui_first_trip import Ui_first_trip
from ui.ui_first_trip import Ui_first_trip


class FirstTrip(QWidget, Ui_first_trip):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window

        self.btn_back.mousePressEvent = lambda x: self.page_move("back")
        self.btn_next.mousePressEvent = lambda x: self.page_move("next")

        self.lineedit_schedule_name.returnPressed.connect(self.get_schedule_name)

    def page_move(self, btn):
        if btn == "back":
            print("이전")
            self.close()

        elif btn == "next":
            print("다음")
            self.main_window.select_planner.show()

    def get_schedule_name(self):
        self.schedule_name = self.lineedit_schedule_name.text()
        self.lineedit_schedule_name.setText("")
        print("스케줄명:", self.schedule_name)
        self.check_mesagge()

    def check_mesagge(self):
        check = QMessageBox.question(self, "확인", f'"{self.schedule_name}"로 하시겠습니까?',
                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if check == QMessageBox.Yes:
            QMessageBox.about(self, "알림", "저장이 완료되었습니다.")

        elif check == QMessageBox.No:
            QMessageBox.about(self, "알림", "다시 입력해주세요.")

        print(self.schedule_name)
