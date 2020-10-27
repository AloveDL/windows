from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QDockWidget, QListWidget, QListView, QAbstractItemView, QListWidgetItem


class TifWidget(QDockWidget):
    select_item_index = pyqtSignal(int)

    def __init__(self):
        super(TifWidget, self).__init__()

        self.slice_view_list = []
        self.show_status = False

        self.setWindowTitle('全切片列表')
        # self.view_dock_widget = QDockWidget('目标切片', self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setFixedWidth(200)
        self.setStyleSheet(
            ".QDockWidget:title{"
            "text-align:center;"
            "border:0;"
            "background-color:lightgray;"
            "}"
        )

        self.view_list = QListWidget()
        self.view_list.setResizeMode(QListView.Adjust)
        self.view_list.setViewMode(QListView.IconMode)
        self.view_list.setMovement(QListView.Static)
        self.view_list.setIconSize(QSize(200, 200))

        max_width_constraint = "QListView::item{max-width:%d;}" % 208
        self.view_list.setStyleSheet(self.view_list.setStyleSheet(max_width_constraint))
        self.view_list.setTextElideMode(Qt.ElideLeft)
        self.view_list.setSpacing(2)
        self.view_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # view_list.setItemDelegate(NoFocusDelegate())

        self.view_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.view_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.view_list.itemClicked.connect(self.slice_select)

        self.setWidget(self.view_list)

    def set_slice_view(self, slice_image_list):
        if self.show_status is True:
            return
        self.slice_view_list = []
        for i, slice_image in enumerate(slice_image_list):
            slice_qimage = QImage(slice_image.data, slice_image.shape[1], slice_image.shape[0],
                                  slice_image.shape[1] * slice_image.shape[2], QImage.Format_RGB888)
            slice_pix = QPixmap.fromImage(slice_qimage)

            if slice_pix.width() > 200 or slice_pix.height() > 200:
                slice_pix = slice_pix.scaled(200, 200, Qt.KeepAspectRatio)

            list_item = QListWidgetItem()
            # list_item.setSizeHint(QSize(200, slice_image.shape[0]))

            # image_layout = QHBoxLayout()
            # image_widget = QWidget()
            # image_widget.setLayout(image_layout)

            # image_label = QLabel()
            # image_label.setFixedWidth(200)
            # image_layout.addWidget(image_label)

            # image_label.setPixmap(slice_pix)

            pix_icon = QIcon(slice_pix)

            list_item.setIcon(pix_icon)
            self.view_list.addItem(list_item)
            # self.view_list.setItemWidget(list_item, image_widget)
            self.slice_view_list.append(list_item)

        self.show_status = True

    def slice_select(self):
        for i in range(len(self.slice_view_list)):
            if self.slice_view_list[i].isSelected() is True:
                self.select_item_index.emit(i)

    def clear_view_list(self):
        self.show_status = False
        self.slice_view_list.clear()
        self.view_list.clear()

    def show_view_list(self):
        for slice_item in self.slice_view_list:
            slice_item.show()
