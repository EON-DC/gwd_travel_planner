import os

if __name__ == '__main__':
    os.system('pyuic5 ui/start_page.ui -o ui/ui_start_page.py')
    os.system('pyuic5 ui/first_trip.ui -o ui/ui_first_trip.py')
    os.system('pyuic5 ui/recall_previous_trip.ui -o ui/ui_recall_previous_trip.py')
    os.system('pyuic5 ui/recommended_place.ui -o ui/ui_recommended_place.py')
    os.system('pyuic5 ui/select_place_list.ui -o ui/ui_select_place_list.py')
    os.system('pyuic5 ui/select_schedule.ui -o ui/ui_select_schedule.py')

