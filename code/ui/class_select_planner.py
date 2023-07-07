from PyQt5.QtWidgets import QWidget, QMessageBox, QBoxLayout, QListWidgetItem

from ui.class_location_item import LocationItem
# from class_location_item import LocationItem
# from ui_select_planner import Ui_select_planner
from ui.ui_select_planner import Ui_select_planner


class SelectPlanner(QWidget, Ui_select_planner):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window

        self.schedule_list = list()
        self.location_list = list()

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

        self.test_init()
        self.set_location_item_lsit()
        self.set_schedule_item_list()


    def show(self):
        self.stackedWidget.setCurrentIndex(0)
        self.init_title_label()
        super().show()

    def init_title_label(self):
        if self.main_window.trip_name is not None:
            self.label_schedule_name.setText(self.main_window.trip_name)
        else:
            self.label_schedule_name.setText("스케줄명")

    def set_location_item_lsit(self):       # 주소 리스트위젯화
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.viewer_1 = self.listWidget_rec_location  # 선택 목록 리스트위젯 인스턴스화
        layout.addWidget(self.viewer_1)
        self.setLayout(layout)

        for idx, list_item in enumerate(self.location_list):
            item = QListWidgetItem(self.viewer_1)
            custom_widget = LocationItem(f"{list_item[0]}",
                                         f"{list_item[1]}",
                                         f"{list_item[2]}")
            item.setSizeHint(custom_widget.sizeHint())  # item에 custom_widget 사이즈 알려주기
            self.viewer_1.setItemWidget(item, custom_widget)
            self.viewer_1.addItem(item)

    def set_schedule_item_list(self):        # 선택 일에 맞춰 변경되도록 설정하기(아직 대기)
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.viewer_2 = self.listWidget_select_list  # 선택 목록 리스트위젯 인스턴스화
        layout.addWidget(self.viewer_2)
        self.setLayout(layout)

        for idx, list_item in enumerate(self.schedule_list):
            item = QListWidgetItem(self.viewer_2)
            custom_widget = LocationItem(f"{list_item[0]}",
                                         f"{list_item[1]}",
                                         f"{list_item[2]}")
            item.setSizeHint(custom_widget.sizeHint())  # item에 custom_widget 사이즈 알려주기
            self.viewer_2.setItemWidget(item, custom_widget)
            self.viewer_2.addItem(item)

    def add_list_location_item(self, name, adress, category):
        temp_list = [name, adress, category]
        self.location_list.append(temp_list)

    def add_list_schedule_item(self, name, adress, category):
        temp_list = [name, adress, category]
        self.schedule_list.append(temp_list)

    def test_init(self):
        self.add_list_location_item("광주인력개발원", "광주광역시 광산구 소촌로 152번길 37", "기술학원")
        self.add_list_location_item("광주패밀리랜드", "광주광역시 북구 우치로 677 광주패밀리랜드", "테마공원")
        self.add_list_location_item("전남대학교", "광주광역시 북구 용봉로 77", "국립대학교")
        self.add_list_location_item("광주충장로우체국", "광주광역시 동구 충장로 94", "우체국")

        self.add_list_schedule_item("광주패밀리랜드", "광주광역시 북구 우치로 677 광주패밀리랜드", "테마공원")
        self.add_list_schedule_item("전남대학교", "광주광역시 북구 용봉로 77", "국립대학교")

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

    # def set_btn_trigger(self):
    #     self.btn_save.clicked.connect(lambda state: self.save_object('some_obj'))
    #
    # def save_object(self, some_obj):
    #     file_name, _, = QFileDialog.getSaveFileName(self, 'Save file', './')
    #     # todo: save excel logic

    def move_to_edit_timeline(self):
        self.stackedWidget.setCurrentIndex(3)
