import os

if __name__ == '__main__':
    os.system('pyuic5 ui/ui_login_widget.ui -o ui_login_widget.py')
    os.system('pyuic5 ui/ui_vital_widget.ui -o ui_vital_widget.py')
    os.system('pyuic5 ui/ui_patient_finder.ui -o ui_patient_finder.py')