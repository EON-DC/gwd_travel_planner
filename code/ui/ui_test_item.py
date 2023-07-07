#!/usr/bin/env python
# coding: utf-8

# 예제 내용
# * QListWidget을 사용하여 아이템을 표시

__author__ = "Deokyu Lim <hong18s@gmail.com>"

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QPushButton
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt


class Item(QWidget):
    def __init__(self, btn_name):
        # QWidget.__init__(self, flags=Qt.Widget)     # super().__init__() 으로 써도 됨
        super().__init__()
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        # addWidget 예시
        pb = QPushButton(btn_name)
        layout.addWidget(pb)
        layout.setSizeConstraint(QBoxLayout.SetFixedSize)   # 위젯이 콘텐츠에 따라 고정된 크기를 가지도록 함
        self.setLayout(layout)  # 창의 메인 레이아웃으로 설정함


class Form(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.viewer = QListWidget(self)
        self.viewer.setDragDropMode(QAbstractItemView.DragDrop)
        self.viewer.setDefaultDropAction(QtCore.Qt.MoveAction)
        layout.addWidget(self.viewer)
        self.setLayout(layout)

        item = QListWidgetItem(self.viewer)
        custom_widget = Item("1번 위젯")

        # item은 custom_widget의 사이즈를 알지 못하므로 알려줘야 한다
        item.setSizeHint(custom_widget.sizeHint())  # 권장 크기를 반환, 위젯의 기하학을 관리하기 위해 Qlayout에서 사용됨
                                                    # sizehint는 레이아웃 내부에 있는 위젯에 사용되므로 최상위 창에는 사용되지 않음
        self.viewer.setItemWidget(item, custom_widget)
        self.viewer.addItem(item)

        item_2 = QListWidgetItem(self.viewer)
        custom_widget_2 = Item("2번 위젯")
        item_2.setSizeHint(custom_widget.sizeHint())
        self.viewer.setItemWidget(item_2, custom_widget_2)
        self.viewer.addItem(item_2)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())