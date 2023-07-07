import os

if __name__ == '__main__':
    os.system('pyuic5 ui/start_page.ui -o ui/ui_start_page.py')
    os.system('pyuic5 ui/first_trip.ui -o ui/ui_first_trip.py')
    os.system('pyuic5 ui/recall_previous_trip.ui -o ui/ui_recall_previous_trip.py')
    os.system('pyuic5 ui/select_planner.ui -o ui/ui_select_planner.py')
    os.system('pyuic5 ui/location_item.ui -o ui/ui_location_item.py')
    os.system('pyuic5 ui/save_schedule_item.ui -o ui/ui_save_schedule_item.py')

