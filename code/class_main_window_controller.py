from PyQt5.QtWidgets import *



from class_excel_converter import ExcelConverter
from class_time_line import TimeLine
from class_plan_date import PlanDate
from ui.class_first_trip import FirstTrip
from ui.class_recall_previous_trip import RecallPreviousTrip
from ui.class_select_planner import SelectPlanner
from ui.class_start_page import StartPage
# from ui.class_location_item import LocationItem


class WindowController(QWidget):
    def __init__(self, db_connector):
        super().__init__()
        self.trip_name = None  # 여행 이름
        self.db_connector = db_connector    #db연결 인스턴스
        self.plan_date = None
        self.timeline = None
        self.start_date_str = None
        self.end_date_str = None
        self.start_page = StartPage(self)  # 시작페이지 페이지
        self.first_trip = FirstTrip(self)  # 처음 여행 페이지
        self.prev_trip = RecallPreviousTrip(self)  # 이전 여행 페이지
        self.select_planner = SelectPlanner(self)  # 스케줄러 페이지

    def initialize_variable(self):
        self.trip_name = None  # 여행 이름
        self.plan_date = None
        self.timeline = None
        self.start_date_str = None
        self.end_date_str = None

    def set_timeline(self, time_line_obj):
        if isinstance(time_line_obj, TimeLine):
            self.timeline = time_line_obj
            self.plan_date = time_line_obj.plan_date
            self.start_date_str = PlanDate.date_obj_to_str(time_line_obj.plan_date.start_date)
            self.end_date_str = PlanDate.date_obj_to_str(time_line_obj.plan_date.end_date)
            self.trip_name = time_line_obj.trip_name
            # 리스트 수정
            self.select_planner.schedule_list = time_line_obj.location_list.copy()

        else:
            QMessageBox.about(self, "알림", "이전 저장 정보를 불러오는데 실패했습니다.")


    def move_to_edit_timeline(self):
        print("수정화면으로 이동하였습니다.")
        self.select_planner.show()
        self.select_planner.move_to_edit_timeline()
