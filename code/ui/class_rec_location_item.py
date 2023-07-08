from PyQt5.QtWidgets import QWidget

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QAction, QMenu

from ui.rec_item import Ui_rec_item_widget

from class_location import Location


# from ui_location_item import Ui_location_item

class RecommendLocationItem(QWidget, Ui_rec_item_widget):

    def __init__(self, select_planner, location_obj: Location = None):
        super().__init__()
        self.setupUi(self)

        self.location_obj = location_obj
        self.name = location_obj.name
        self.address = location_obj.address
        self.category = location_obj.category
        self.set_text_location()
        self.select_planner = select_planner

        if self.category == 0 or self.category == '숙소':
            self.setStyleSheet(self.hotel_sheet)
        else:
            self.setStyleSheet(self.attraction_sheet)

        self.mouseDoubleClickEvent = lambda x: self.set_web_location()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def set_text_location(self):
        self.label_name.setText(f"{self.name}")
        self.label_adress.setText(f"{self.address}")

    def set_web_location(self):
        self.select_planner.set_location_web_view(self.location_obj)

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

    hotel_sheet = """
    #frame_41{
    	background-color: rgb(255, 203, 203);
    }
    #frame_42{
    	background-color: rgb(255, 247, 247);
    }
    """

    attraction_sheet = """
    #frame_41{
    	background-color: rgb(170, 255, 255);
    }
    #frame_42{
    	background-color: rgb(222, 253, 255);
    }
    """
