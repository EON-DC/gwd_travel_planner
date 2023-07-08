from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QAction, QMenu

from ui.ui_location_item import Ui_location_item

from class_location import Location


# from ui_location_item import Ui_location_item

class LocationItem(QWidget, Ui_location_item):
    def __init__(self, select_planner, location_obj: Location = None):
        super().__init__()
        self.setupUi(self)
        if isinstance(location_obj, int):
            dummy_data = location_obj  # int 1
            self.frame_2.setStyleSheet("""* {background-color:#232323;}""")
            self.label_name.setStyleSheet("""color: white;""")
            self.name = f"{dummy_data} 일차"
            self.address = '드래그를 하여 일정 순서를 정해주세요'
            self.category = '구분'
            self.set_text_location()
            return
        self.location_obj = location_obj
        self.name = location_obj.name
        self.address = location_obj.address
        self.category = location_obj.category
        self.set_text_location()
        self.select_planner = select_planner

        self.mouseDoubleClickEvent = lambda x: self.set_web_location()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

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



    def show_context_menu(self, position):
        context_menu = QMenu(self)
        # Create actions for the context menu
        action1 = QAction("추가하기", self)
        context_menu.addAction(action1)
        action1.triggered.connect(self.handle_action1)
        context_menu.exec_(self.mapToGlobal(position))

    def handle_action1(self):
        self.select_planner.schedule_list.append(self.location_obj)
        print(self.select_planner.schedule_list)
