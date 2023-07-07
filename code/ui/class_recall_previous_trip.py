from PyQt5.QtWidgets import QWidget, QBoxLayout, QListWidgetItem
# from ui_recall_previous_trip import Ui_recall_proevious_trip
from ui.ui_recall_previous_trip import Ui_recall_proevious_trip
from ui.class_save_schedule_item import SaveScheduleItem


class RecallPreviousTrip(QWidget, Ui_recall_proevious_trip):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window
        # self.save_schedule_trip = SaveScheduleItem()

        self.schedule_list = list()     # 빈 리스트 선언해주기

        self.btn_back.mousePressEvent = lambda x: self.page_move("back")

        self.test_init()
        self.import_save_trip()

    def page_move(self, btn):
        if btn == "back":
            print("이전")
            self.close()

    def import_save_trip(self):
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        viewer = self.listwidget_save_trip
        layout.addWidget(viewer)
        self.setLayout(layout)

        for idx, item_list in enumerate(self.schedule_list):
            item = QListWidgetItem(viewer)
            custom_widget = SaveScheduleItem(f"{item_list[0]}",
                                             f"{item_list[1]}",
                                             f"{item_list[2]}",
                                             self.main_window)
            item.setSizeHint(custom_widget.sizeHint())
            viewer.setItemWidget(item, custom_widget)
            viewer.addItem(item)

    def add_list_saved_item(self, name, start_str, end_str):
        temp_list = [name, start_str, end_str]
        self.schedule_list.append(temp_list)

    def test_init(self):
        self.add_list_saved_item("봄 감자가 맛있단다", "2023.07.03", "2023.07.08")
        self.add_list_saved_item("내 여름휴가는 어디에", "2023.08.03", "2023.08.08")
        self.add_list_saved_item("장마가 거의 끝나가고 있어요", "2023.07.06", "2023.07.20")
        self.add_list_saved_item("광주인력개발원", "2023.07.03", "2023.07.08")






