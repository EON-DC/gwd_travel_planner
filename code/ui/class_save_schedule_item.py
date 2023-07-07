from PyQt5.QtWidgets import QWidget

from ui.ui_save_schedule_item import Ui_save_schedule_item
# from ui_save_schedule_item import Ui_save_schedule_item

class SaveScheduleItem(QWidget, Ui_save_schedule_item):
    def __init__(self, name, start_date, end_date, main_window):
        super().__init__()
        self.setupUi(self)
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.main_window = main_window

        self.mouseDoubleClickEvent = lambda x: self.double_click_widget()

        self.set_text_schedule()

    def set_text_schedule(self):
        self.label_schedule_name.setText(f"{self.name}")
        self.label_date.setText(f"{self.start_date} ~ {self.end_date}")

    def double_click_widget(self):
        print(f"{self.name}")
        #todo: timeline 수정 이동 로직
        self.main_window.move_to_edit_timeline()
        self.main_window.prev_trip.close()
