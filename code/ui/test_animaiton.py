import sys
import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore, QtGui
from PyQt5.QtCore import QPropertyAnimation, QSize, QPoint, QTimer, QMimeData, Qt
from PyQt5.QtGui import QMouseEvent, QDrag, QPixmap, QDragEnterEvent, QDropEvent, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QFrame, QLabel, QGraphicsEllipseItem, QDialog, \
    QListWidgetItem
from folium import Marker
from ui_sample import Ui_main
import io


class BetterWebView(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.load(QtCore.QUrl())
        self.focusProxy().installEventFilter(self)

    def eventFilter(self, source, event):
        if (
                self.focusProxy() is source
                and event.type() == QtCore.QEvent.MouseButtonPress
        ):
            event: QtGui.QMouseEvent
            print('x', event.x(), end=', ')
            print('y', event.y())
        return super().eventFilter(source, event)


class BetterFrame(QFrame):
    def __init__(self, *args):
        super().__init__(*args)
        # self.setStyleSheet("background-color: #333333")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mimeData = QMimeData()
            drag.setMimeData(mimeData)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            Qt.DropAction.dropAction = drag.exec()


class DraggableLabel(QLabel):
    def __init__(self, *args):
        super().__init__(*args)

        self.setAcceptDrops(True)
        self.setStyleSheet('background-color:white;')

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            # Create a MIME data object and set its data
            mime_data = QMimeData()
            mime_data.setText(self.text())

            # Create a drag object and set the MIME data
            drag = QDrag(self)
            drag.setMimeData(mime_data)

            # Set the pixmap for the drag
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            # Start the drag operation
            drag.exec_(Qt.CopyAction)

        super().mousePressEvent(event)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event: QMouseEvent):
        position = event.pos()
        self.move(position)


class MainWindow(QtWidgets.QWidget, Ui_main):
    att_marker_point = [(37.59224924, 129.0896915, '시설0'),
                        (37.60042576, 129.0784636, '시설1'),
                        (37.47837985, 129.1583016, '시설2'), ]

    hotel_marker_point = [(37.46357478, 129.0145123, '숙박0'),
                          (37.46357478, 129.0145123, '숙박1'),
                          (37.48716814, 129.1366706, '숙박2'), ]
    BANNER_WIDTH = 80

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.web_view = None
        self.folium_m = None
        self.set_map()
        self.set_btn_trigger()
        self.animation = None
        self.animation_timer = QTimer(self)
        self.set_drag_test()
        self.setAcceptDrops(True)
        self.stackedWidget_2.setAcceptDrops(True)
        self.page.setAcceptDrops(True)
        self.set_list_view()


    def set_list_view(self):
        entries = ['one', 'two', 'three', '철수', "영희", "멍멍", "왈왈"]

        model = QtGui.QStandardItemModel()
        self.listView.setModel(model)

        for i in entries:
            item = QtGui.QStandardItem(i)
            model.appendRow(item)



    def set_drag_test(self):
        self.bf = DraggableLabel('Drag me', self.page)
        # self.bf.setGeometry(QtCore.QRect(80, 200, 50, 80))
        self.bf.setObjectName("bf")
        self.frame = BetterFrame(self.page)
        self.frame.setGeometry(200, 200, 50, 50)



    def set_map(self):
        self.folium_m = folium.Map(
            location=[37.478188, 129.026796], zoom_start=13
        )
        layout = QVBoxLayout(self.widget)
        self.web_view = BetterWebView()
        layout.addWidget(self.web_view)
        self.widget.setLayout(layout)
        self.load_html()

    def set_btn_trigger(self):
        self.btn_location_1.clicked.connect(lambda state: self.set_map_view_location(MainWindow.att_marker_point[0]))
        self.btn_location_2.clicked.connect(lambda state: self.set_map_view_location(MainWindow.att_marker_point[1]))
        self.btn_location_3.clicked.connect(lambda state: self.set_map_view_location(MainWindow.att_marker_point[2]))
        self.btn_hide_banner.clicked.connect(lambda state: self.show_banners(False))
        self.btn_show_banner.clicked.connect(lambda state: self.show_banners(True))
        self.btn_1.clicked.connect(lambda state: self.set_stacked_widget_index(0))
        self.btn_2.clicked.connect(lambda state: self.set_stacked_widget_index(1))
        self.btn_3.clicked.connect(lambda state: self.set_stacked_widget_index(2))

    def set_stacked_widget_index(self, index):
        self.stackedWidget_2.setCurrentIndex(index)

    def set_map_view_location(self, tuple_):
        w_do = tuple_[0]
        k_do = tuple_[1]
        name = tuple_[2]

        self.folium_m = folium.Map(
            location=[w_do, k_do], zoom_start=13
        )
        self.load_html()

    def load_html(self):
        att_marker_group = folium.FeatureGroup(name="attraction").add_to(self.folium_m)
        hotel_marker_group = folium.FeatureGroup(name="hotel").add_to(self.folium_m)
        for tuple_ in MainWindow.att_marker_point:
            w_do = tuple_[0]
            k_do = tuple_[1]
            icon = folium.Icon(color='blue', icon='star', prefix='fa')
            att_marker_group.add_child(Marker((w_do, k_do), icon=icon).add_to(self.folium_m))
        for tuple_ in MainWindow.hotel_marker_point:
            w_do = tuple_[0]
            k_do = tuple_[1]
            icon = folium.Icon(color='red', icon='house', prefix='fa')
            hotel_marker_group.add_child(Marker((w_do, k_do), icon=icon).add_to(self.folium_m))
        data = io.BytesIO()
        self.folium_m.save(data, close_file=True)
        self.web_view.setHtml(data.getvalue().decode())

    def check_visible_widget(self, value):
        now_state = self.widget_banner.isVisible()
        if now_state != value:
            return True
        else:
            return False

    def show_banners(self, value):
        if not self.check_visible_widget(value):
            return
        if value is False:
            self.animation = QPropertyAnimation(self.widget_banner, b"size")
            self.animation.setDuration(300)
            self.animation.setStartValue(QSize(MainWindow.BANNER_WIDTH, self.widget_banner.height()))
            self.animation.setEndValue(QSize(0, self.widget_banner.height()))
            self.animation.start()
            self.animation_timer.singleShot(300, lambda: self.widget_banner.setVisible(False))
            # self.widget_banner.setVisible(False)
        else:
            # self.widget_banner.hide()
            self.animation = QPropertyAnimation(self.widget_banner, b"size")
            self.animation.setDuration(300)
            self.animation.setStartValue(QSize(0, self.widget_banner.height()))
            self.animation.setEndValue(QSize(MainWindow.BANNER_WIDTH, self.widget_banner.height()))
            self.animation.start()
            self.animation_timer.singleShot(0, lambda: self.widget_banner.setVisible(True))
            # self.widget_banner.setVisible(True)




def show_error_message(message, traceback):
    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(QtWidgets.QMessageBox.Critical)
    msg_box.setWindowTitle("Error")
    msg_box.setText(message)
    msg_box.exec_()
    traceback.print_exc()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.excepthook = lambda exctype, value, traceback: show_error_message(str(value), traceback)

    app.exec_()
    app.exec_()
