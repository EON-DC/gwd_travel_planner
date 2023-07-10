from PyQt5 import QtGui
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QMessageBox, QBoxLayout, QListWidgetItem, QVBoxLayout, QCompleter, QMenu, QAction, \
    QFileDialog, QListWidget
from PyQt5.QtWidgets import QWidget, QMessageBox, QBoxLayout, QListWidgetItem, QVBoxLayout, QCompleter, QMenu

from ui.class_location_item import LocationItem
# from class_location_item import LocationItem
# from ui_select_planner import Ui_select_planner
from ui.ui_select_planner import Ui_select_planner

# from class_rec_location_item import RecommendLocationItem
from ui.class_rec_location_item import RecommendLocationItem

from class_plan_date import PlanDate

import random
from class_folium_factory import FoliumMapFactory
from class_excel_converter import ExcelConverter

from class_time_line import TimeLine


class SelectPlanner(QWidget, Ui_select_planner):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window

        self.schedule_list = list()
        # self.rec_location_obj_list_from_db = list()

        # self.top_obj_list = [self.label_select_date, self.lineEdit_search, self.toolBtn_search]
        self.rec_btn_list = [self.btn_rec_attraction, self.btn_rec_hotel]

        # 상단 객체 초기 숨김
        # for top_obj in self.top_obj_list:
        #     top_obj.setVisible(False)
        self.label_select_date.setVisible(False)

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

        # self.toolBtn_search.clicked.connect(lambda x: self.search_location("search"))

        self.calendarWidget.clicked.connect(lambda qdate: self.set_plan_date(qdate))

        self.btn_refresh.clicked.connect(lambda x: self.set_refresh("refresh"))

        # 자동 완성 기능
        # search_text = ["무상광자", "봄 감자", "광주인력개발원", "abc"]
        # completer = QCompleter(search_text)
        #
        # self.lineEdit_search.setCompleter(completer)

        # self.test_init()
        self.rec_location_obj_list_from_db = self.main_window.db_connector.find_all_location()
        self.total_hotel = [x for x in self.rec_location_obj_list_from_db if x.category in ['0', 0, '숙소']]
        self.total_attraction = [x for x in self.rec_location_obj_list_from_db if x.category in ['1', 1, '명소']]
        self.set_location_item_list()
        self.folium_factory = FoliumMapFactory()  # Folium 팩토리
        self.web_view = QWebEngineView(self)
        self.excel_converter = ExcelConverter()  # 엑셀 저장 기능 인스턴스

        # selected list widget 트리거 설정
        self.listWidget_select_list.itemPressed.connect(lambda x: self.read_schedule_item_list())
        # recommend widget 설정
        self.clear_recommend_widget_inner()
        self.init_list_widget()
        # 복구용 스냅샷
        self.snap_shot_list = None

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
    # def search_location(self, s):
    #     search_text = self.lineEdit_search.text()
    #     self.stackedWidget.setCurrentIndex(2)
    #     self.label_gwd.setText("검색 결과")
    #     self.label_rec.setText("결과 목록")
    #     # todo: 검색 결과 출력되도록 addwidget 기능 추가(이 부분을 어떻게 하면 좋을까)

    # 화면 첫 시작 시 셋팅
    def show(self):
        self.stackedWidget.setCurrentIndex(0)
        self.folium_factory.clear()
        self.init_web_engine_layout()

        # for top_obj in self.top_obj_list:
        #     top_obj.setVisible(False)
        self.label_select_date.setVisible(False)

        self.label_select_date.setText("yyyy.mm.dd ~ yyyy.mm.dd")
        self.init_title_label()
        self.set_schedule_item_list()
        super().show()

    def init_web_engine_layout(self):
        if self.widget_folium.layout() is None:
            v_layout = QVBoxLayout(self.widget_folium)
            v_layout.addWidget(self.web_view)
            self.widget_folium.setLayout(v_layout)
        if self.label is not None:
            self.label.deleteLater()
            self.label = None
        self.set_location_web_view()

    # first_trip에서 받은 스케줄명을 상단 스케즐명에 출력 시키기
    def set_location_web_view(self, location_obj=None):
        if location_obj is not None:
            self.folium_factory.set_location(location_obj)
        self.folium_factory.set_folium_map()
        self.web_view.setHtml(self.folium_factory.make_html())

    def init_title_label(self):
        if self.main_window.trip_name is not None:
            self.label_schedule_name.setText(self.main_window.trip_name)
        else:
            self.label_schedule_name.setText("스케줄명")

    # 추천 장소 리스트 출력 함수 + 검색 결과 리스트 출력
    def set_location_item_list(self, option=None):  # 주소 리스트위젯화
        rec_list_widget = self.listWidget_rec_location
        selected_list = list()
        rec_list_widget.clear()
        if option == 'attraction':
            selected_list = self.total_attraction.copy()
        elif option == 'hotel':
            selected_list = self.total_hotel.copy()
        else:
            return

        for idx, list_item in enumerate(selected_list):
            item = QListWidgetItem(rec_list_widget)
            custom_widget = LocationItem(self, list_item)
            item.setSizeHint(custom_widget.sizeHint())  # item에 custom_widget 사이즈 알려주기
            rec_list_widget.setItemWidget(item, custom_widget)
            rec_list_widget.addItem(item)

    def init_list_widget(self):
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        select_location_list_widget = self.listWidget_select_list  # 선택 목록 리스트위젯 인스턴스화
        layout.addWidget(select_location_list_widget)
        self.setLayout(layout)
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        rec_list_widget = self.listWidget_rec_location  # 리스트위젯 인스턴스화
        layout.addWidget(rec_list_widget)
        self.setLayout(layout)

    # 선택한 일정 리스트 출력 함수
    def set_schedule_item_list(self):  
        self.listWidget_select_list.clear()
        select_location_list_widget = self.listWidget_select_list

        duration = 1
        if self.main_window.start_date_str is not None and self.main_window.end_date_str is not None:
            duration = PlanDate.get_duration(self.main_window.start_date_str, self.main_window.end_date_str)

        if len(self.schedule_list) != 0 and isinstance(self.schedule_list[0], list):  # 2중 리스트인 상태
            copy_schedule_list = list()
            for idx, list_ in enumerate(self.schedule_list):
                if isinstance(list_, list):
                    copy_schedule_list.append(idx + 1)
                    copy_schedule_list.extend(list_)
                else:
                    copy_schedule_list.append(list_)
        else:
            copy_schedule_list = self.schedule_list.copy()
            for i in range(duration, 0, -1):
                copy_schedule_list.insert(0, i)

        for idx, list_item in enumerate(copy_schedule_list):
            item = QListWidgetItem(select_location_list_widget)
            custom_widget = LocationItem(self, list_item)
            item.setSizeHint(custom_widget.sizeHint())  # item에 custom_widget 사이즈 알려주기
            select_location_list_widget.setItemWidget(item, custom_widget)
            select_location_list_widget.addItem(item)

    # select location 읽어들이고 현 schedule list로 저장하기
    def read_schedule_item_list(self):
        list_widget = self.listWidget_select_list
        temp_list = list()
        result_list = list()
        index = 0
        while index < list_widget.count():
            item = list_widget.item(index)
            customWidget = list_widget.itemWidget(item)
            customWidget: LocationItem
            if customWidget.category == '구분':
                if index != 0:
                    result_list.append(temp_list.copy())
                    temp_list.clear()
                index += 1
                continue
            temp_list.append(customWidget.location_obj)
            index += 1
        result_list.append(temp_list)
        self.schedule_list.clear()
        self.schedule_list = result_list
        if self.main_window.timeline is not None:
            self.main_window.timeline.location_list = result_list

    def add_list_location_item(self, name, address, category):
        temp_list = [name, address, category]
        self.rec_location_obj_list_from_db.append(temp_list)

    def add_list_schedule_item(self, name, address, category):
        temp_list = [name, address, category]
        self.schedule_list.append(temp_list)

    def set_refresh(self, btn):
        if btn == "refresh":
            self.schedule_list = self.snap_shot_list.copy()
            self.set_schedule_item_list()

    def clear_recommend_widget_inner(self):
        # for location in random.sample(self.rec_location_obj_list_from_db, 4):
        #     layout.addWidget(RecommendLocationItem(self, location))


        random_pick_hotel_location = random.sample(self.total_hotel, 4)
        random_pick_attraction_location = random.sample(self.total_attraction, 4)

        a_layout = self.frame_rec_attraction.layout()
        frame = self.frame_rec_attraction
        while a_layout.count():
            item = a_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for location in random_pick_attraction_location:
            a_layout.addWidget(RecommendLocationItem(self, location))

        h_layout = self.frame_rec_hotel.layout()
        frame = self.frame_rec_hotel
        while h_layout.count():
            item = h_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        for location in random_pick_hotel_location:
            h_layout.addWidget(RecommendLocationItem(self, location))

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
                # for top_obj in self.top_obj_list:
                #     top_obj.setVisible(False)
                self.label_select_date.setVisible(False)

            elif now_idx == 3:
                self.stackedWidget.setCurrentIndex(1)


        elif btn == "select_date":  # 날짜 선택 완료 버튼 클릭 시
            print("날짜 선택 완료")
            self.stackedWidget.setCurrentIndex(1)

            # for top_obj in self.top_obj_list:
            #     top_obj.setVisible(True)
            self.show_plan_date_title()


        elif btn == "move_list":
            self.stackedWidget.setCurrentIndex(3)
            # 스케줄 일정대로 위젯 생성
            self.snap_shot_list = self.schedule_list.copy()
            self.set_schedule_item_list()
            for btn_hide in self.rec_btn_list:
                btn_hide.setVisible(False)
    def show_plan_date_title(self):
        self.label_select_date.setVisible(True)
        self.label_select_date.setText(f"{self.main_window.start_date_str} ~ {self.main_window.end_date_str}")
    def rec_change(self, btn):
        self.stackedWidget.setCurrentIndex(2)

        for btn_show in self.rec_btn_list:
            btn_show.setVisible(True)

        if btn == "attraction":
            # print("추천 장소 리스트위젯")
            self.label_rec.setText("추천 장소")
            self.set_location_item_list("attraction")

        elif btn == "hotel":
            # print("추천 호텔 리스트위젯")
            self.label_rec.setText("추천 호텔")
            self.set_location_item_list("hotel")
    def save_schedule(self, btn):
        # mainwindow timeline obj 저장 로직
        self.read_schedule_item_list()
        # location list 로 변환
        location_list = self.schedule_list.copy()
        s_date = self.main_window.start_date_str
        e_date = self.main_window.end_date_str
        t_name = self.main_window.trip_name
        if hasattr(self.main_window.timeline, "time_line_id"):
            self.main_window.db_connector.delete_timeline_by_id(self.main_window.timeline.time_line_id)
            self.main_window.db_connector.insert_timeline(self.main_window.timeline)
        else:
            self.main_window.timeline = self.main_window.db_connector.create_time_line_obj(location_list, s_date,
                                                                                           e_date, t_name)

        # db connector로 timeline obj 생성 및 main window 저장

        print("일정 선택 완료")
        check = QMessageBox.about(self, "확인", "일정이 저장되었습니다. 불러오기를 통해 확인하실 수 있습니다.")
        save_excel_dialog = QMessageBox.question(self, "엑셀 저장", "엑셀파일로 저장하시겠습니까?")
        if save_excel_dialog == QMessageBox.Yes:
            save_path_file_name, _, = QFileDialog.getSaveFileName(self, '일정 파일 저장', './')
            self.excel_converter.set_timeline(self.main_window.timeline)
            self.excel_converter.save_excel_file(save_path_file_name)

        self.main_window.first_trip.close()
        self.main_window.prev_trip.close()
        self.main_window.initialize_variable()
        self.close()

    def move_to_edit_timeline(self):
        self.stackedWidget.setCurrentIndex(3)

        # for top_obj in self.top_obj_list:
        #     top_obj.setVisible(True)
        self.label_select_date.setVisible(True)
        self.show_plan_date_title()
