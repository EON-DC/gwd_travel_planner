from PyQt5 import QtGui
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QBoxLayout, QListWidgetItem, QCompleter

from ui.class_location_item import LocationItem
# from class_location_item import LocationItem
# from ui_select_planner import Ui_select_planner
from ui.ui_select_planner import Ui_select_planner

from class_plan_date import PlanDate


class SelectPlanner(QWidget, Ui_select_planner):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window

        self.schedule_list = list()
        self.location_list = list()

        self.top_obj_list = [self.label_select_date, self.lineEdit_search, self.toolBtn_search]
        self.rec_btn_list = [self.btn_rec_attraction, self.btn_rec_hotel]

        # 상단 객체 초기 숨김
        for top_obj in self.top_obj_list:
            top_obj.setVisible(False)

        # 왼쪽 상단 버튼 초기 숨김
        for btn_hide in self.rec_btn_list:
            btn_hide.setVisible(False)

        self.btn_selection_1.setEnabled(False)

        self.btn_back.mousePressEvent = lambda x: self.page_move("back")

        self.btn_selection_1.clicked.connect(lambda x: self.page_move("select_date"))
        self.btn_selection_2.clicked.connect(lambda x: self.page_move("move_list"))
        self.btn_selection_3.clicked.connect(lambda x: self.page_move("move_list"))

        self.btn_rec_attraction.clicked.connect(lambda x: self.rec_change("attraction"))
        self.btn_rec_hotel.clicked.connect(lambda x: self.rec_change("hotel"))

        self.label_attraction_more.mousePressEvent = lambda x: self.rec_change("attraction")
        self.label_hotel_more.mousePressEvent = lambda x: self.rec_change("hotel")

        self.btn_selection_4.clicked.connect(lambda x: self.save_schedule("save"))

        self.toolBtn_search.clicked.connect(lambda x: self.search_location("search"))

        self.calendarWidget.clicked.connect(lambda qdate: self.set_plan_date(qdate))

        # 자동 완성 기능
        search_text = ["무상광자", "봄 감자", "광주인력개발원", "abc"]
        completer = QCompleter(search_text)

        self.lineEdit_search.setCompleter(completer)

        # self.test_init()
        self.location_list = self.main_window.db_connector.get_recommended_attraction()
        self.set_location_item_list()
        self.set_schedule_item_list()

    # 캘린더 값을 받는 함수
    def set_plan_date(self, qdate_obj, option=None):
        qdate_obj: QDate
        date_str = qdate_obj.toString("yyyy-MM-dd")  # 선택된 데이터 스트링
        date_obj = PlanDate.str_date_parser(date_str)  # date_time 오브젝트로 반환

        if option is None:  # self.main_window : plan_date -> 컨트롤러파일에 있는 것
            if (self.main_window.start_date_str is not None and self.main_window.end_date_str is not None):
                option = 'start'
                self.main_window.start_date_str = date_str
                self.main_window.end_date_str = None
                self.label_few_date.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 14))
                self.label_few_date.setAlignment(Qt.AlignCenter)
                self.label_few_date.setText("종료일을 선택해주세요")

            elif self.main_window.start_date_str is None:
                option = 'start'
                self.main_window.start_date_str = date_str
                self.label_few_date.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 14))
                self.label_few_date.setAlignment(Qt.AlignCenter)
                self.label_few_date.setText("종료일을 선택해주세요")

            elif self.main_window.end_date_str is None:
                option = 'end'
                self.main_window.end_date_str = date_str

                start_date = PlanDate.str_date_parser(self.main_window.start_date_str)
                end_date = PlanDate.str_date_parser(self.main_window.end_date_str)
                trip_duration = end_date - start_date
                if trip_duration.days >= 0:
                    self.label_few_date.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 22))
                    self.label_few_date.setAlignment(Qt.AlignCenter)
                    self.label_few_date.setText(f"{trip_duration.days + 1} DAY")
                    self.btn_selection_1.setEnabled(True)
                else:
                    self.label_few_date.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 14))
                    self.label_few_date.setAlignment(Qt.AlignCenter)
                    self.label_few_date.setText("시작일을 다시 선택해주세요")  # 시작일을 다시 설정해주라고 멘트 변경 시키기
                    self.btn_selection_1.setEnabled(False)

        elif option == 'start':
            self.main_window.start_date_str = date_str
        elif option == 'end':
            self.main_window.end_date_str = date_str

        self.set_label_date(date_str, option)

    def set_label_date(self, date_str, option):
        if option == 'start':
            self.label_start_date.setText(date_str)
        elif option == 'end':
            self.label_end_date.setText(date_str)


    # 검색 기능 함수
    def search_location(self, s):
        search_text = self.lineEdit_search.text()
        self.stackedWidget.setCurrentIndex(2)
        self.label_gwd.setText("검색 결과")
        self.label_rec.setText("결과 목록")
        # todo: 자동완성 기능 추가, 검색 결과 출력되도록 addwidget 기능 추가(이 부분을 어떻게 하면 좋을까)

    # 화면 첫 시작 시 셋팅
    def show(self):
        self.stackedWidget.setCurrentIndex(0)
        # self.label_select_date.hide()
        # self.lineEdit_search.hide()
        # self.toolBtn_search.hide()
        self.init_title_label()
        super().show()

    # first_trip에서 받은 스케줄명을 상단 스케즐명에 출력 시키기
    def init_title_label(self):
        if self.main_window.trip_name is not None:
            self.label_schedule_name.setText(self.main_window.trip_name)
        else:
            self.label_schedule_name.setText("스케줄명")

    # 추천 장소 리스트 출력 함수 + 검색 결과 리스트 출력
    def set_location_item_list(self):       # 주소 리스트위젯화
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        rec_list_widget = self.listWidget_rec_location  # 리스트위젯 인스턴스화
        layout.addWidget(rec_list_widget)
        self.setLayout(layout)

        for idx, list_item in enumerate(self.location_list):
            item = QListWidgetItem(rec_list_widget)
            custom_widget = LocationItem(list_item)
            item.setSizeHint(custom_widget.sizeHint())  # item에 custom_widget 사이즈 알려주기
            rec_list_widget.setItemWidget(item, custom_widget)
            rec_list_widget.addItem(item)


    # 선택한 일정 리스트 출력 함수
    def set_schedule_item_list(self):        # todo: 타임라인에 맞춰 리스트화 시키기
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        select_location_list_widget = self.listWidget_select_list  # 선택 목록 리스트위젯 인스턴스화
        layout.addWidget(select_location_list_widget)
        self.setLayout(layout)

        for idx, list_item in enumerate(self.schedule_list):
            item = QListWidgetItem(select_location_list_widget)
            custom_widget = LocationItem(list_item)
            item.setSizeHint(custom_widget.sizeHint())  # item에 custom_widget 사이즈 알려주기
            select_location_list_widget.setItemWidget(item, custom_widget)
            select_location_list_widget.addItem(item)


    def add_list_location_item(self, name, address, category):
        temp_list = [name, address, category]
        self.location_list.append(temp_list)

    def add_list_schedule_item(self, name, address, category):
        temp_list = [name, address, category]
        self.schedule_list.append(temp_list)

    # def test_init(self):
    #     self.add_list_location_item("광주인력개발원", "광주광역시 광산구 소촌로 152번길 37", "기술학원")
    #     self.add_list_location_item("광주패밀리랜드", "광주광역시 북구 우치로 677 광주패밀리랜드", "테마공원")
    #     self.add_list_location_item("전남대학교", "광주광역시 북구 용봉로 77", "국립대학교")
    #     self.add_list_location_item("광주충장로우체국", "광주광역시 동구 충장로 94", "우체국")
    #
    #     self.add_list_schedule_item("광주패밀리랜드", "광주광역시 북구 우치로 677 광주패밀리랜드", "테마공원")
    #     self.add_list_schedule_item("전남대학교", "광주광역시 북구 용봉로 77", "국립대학교")

    def page_move(self, btn):
        if btn == "back":
            for btn_hide in self.rec_btn_list:
                btn_hide.setVisible(False)

            now_idx = self.stackedWidget.currentIndex()
            self.stackedWidget.setCurrentIndex(now_idx - 1)

            if now_idx == 0:
                print("이전 위젯으로 이동")
                self.close()

            if now_idx == 1:
                for top_obj in self.top_obj_list:
                    top_obj.setVisible(False)

            elif now_idx == 3:
                self.stackedWidget.setCurrentIndex(1)

        elif btn == "select_date":  # 날짜 선택 완료 버튼 클릭 시
            print("날짜 선택 완료")
            self.stackedWidget.setCurrentIndex(1)
            for top_obj in self.top_obj_list:
                top_obj.setVisible(True)

        elif btn == "move_list":    # 담긴 일정 목록으로 이동
            self.stackedWidget.setCurrentIndex(3)

            for btn_hide in self.rec_btn_list:
                btn_hide.setVisible(False)

    def rec_change(self, btn):
        self.stackedWidget.setCurrentIndex(2)

        for btn_show in self.rec_btn_list:
            btn_show.setVisible(True)

        if btn == "attraction":
            # print("추천 장소 리스트위젯")
            self.label_rec.setText("추천 장소")

        elif btn == "hotel":
            # print("추천 호텔 리스트위젯")
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
        for top_obj in self.top_obj_list:
            top_obj.setVisible(True)
