import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QTextBrowser, QSpacerItem, QPushButton, QSizePolicy, \
    QHBoxLayout


class DebugInfo(QDockWidget):
    def __init__(self, parent=None):
        super(DebugInfo, self).__init__()
        self.head_info = None

        self.setWindowTitle('日志')
        self.setFeatures(QDockWidget.NoDockWidgetFeatures | QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.dock_widget_contents = QWidget()
        self.setWidget(self.dock_widget_contents)

        self.info_text_browser = QTextBrowser(self.dock_widget_contents)
        self.info_text_browser.setReadOnly(True)

        self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.clear_button = QPushButton("清除记录", self.dock_widget_contents)

        self.hLayout = QHBoxLayout()
        self.hLayout.addItem(self.horizontal_spacer)
        self.hLayout.addWidget(self.clear_button)

        self.vLayout = QVBoxLayout(self.dock_widget_contents)
        self.vLayout.setSpacing(4)
        self.vLayout.setContentsMargins(4, 4, 4, 4)
        self.vLayout.addWidget(self.info_text_browser)
        self.vLayout.addLayout(self.hLayout)

        self.clear_button.clicked.connect(self.clear)

        # self.dock_widget_contents.setMinimumWidth(300)

    def set_head_info(self, head_info):
        self.head_info = head_info
        self.clear()

    def set_text_browser(self, text_info):
        pass

    def clear(self):
        self.info_text_browser.clear()
        if self.head_info is not None:
            self.info_text_browser.append(self.head_info)
            h = self.height()
            w = self.width()
            self.resize(w, 10)
            self.resize(w, h)
