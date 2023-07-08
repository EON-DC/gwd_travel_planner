from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QAction, QMenu

from ui.ui_location_item import Ui_location_item

from class_location import Location


# from ui_location_item import Ui_location_item

class LocationItem(QWidget, Ui_location_item):
    def __init__(self, location_obj :Location, select_planner):
        super().__init__()
        self.setupUi(self)
        # self.main_window = main_window
        self.location_obj = location_obj
        self.name = location_obj.name
        self.address = location_obj.address
        self.category = location_obj.category
        self.set_text_location()
        self.select_planner = select_planner
        self.right_clicked = None  # 우클릭 시 값 넘겨주는 변수

    def set_text_location(self):
        self.label_name.setText(f"{self.name}")
        self.label_adress.setText(f"{self.address}")

    def set_web_location(self):
        self.select_planner.set_location_web_view(self.location_obj)

    # # todo: 일단 대기
    # def mousePressEvent(self, event):
    #     now_idx = self.select_planner.stackedWidget.currentIndex()
    #
    #     if now_idx == 2:
    #         if event.buttons() & Qt.RightButton:
    #             self.right_clicked = "Right"
    #             # print("Right")
    #             self.select_planner.temp.append(self.label_name.text())
    #             print(self.select_planner.temp)
    #
    #             # self.select_planner.right = "추가"
    #             # print(self.select_planner.right)
    #         else:
    #             pass
    #
    #     elif now_idx == 3:
    #         if event.buttons() & Qt.RightButton:
    #             self.right_clicked = "Right"
    #             # print("Right")
    #             self.select_planner.temp.remove(self.label_name.text())
    #             print(self.select_planner.temp)
    #
    #             # self.select_planner.right = "삭제"
    #             # print(self.select_planner.right)
    #         else:
    #             pass






