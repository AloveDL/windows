import sys
import cv2
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QIODevice, Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import *

from TargetView import TargetView
from DebugInfo import DebugInfo
from InfoWidget import InfoWidget
from ViewList import ViewList
from TifWidget import TifWidget


class DetectionWindow(QMainWindow):
    def __init__(self):
        super(DetectionWindow, self).__init__()

        self.slice_image_list = []  # 放置tif文件路径

        self.setWindowTitle('胃癌组织病理辅助诊断系统')
        self.setGeometry(400, 200, 800, 600)
        self.showMaximized()
        self.width = self.width()
        self.height = self.height()
        # 菜单栏
        self.menu_bar = self.menuBar()
        # 文件选项
        self.menufile = QMenu("文件", self)
        self.menufile.setObjectName("menufile")
        self.menu_bar.addMenu(self.menufile)
        #导入
        self.action_open_file = QAction('导入', self.menufile)
        self.action_open_file.setStatusTip('导入.')
        self.action_open_file.triggered.connect(self.open_file)

        self.menufile.addAction(self.action_open_file)
        #批量导入
        self.action_batch_open = QAction('批量导入', self.menufile)
        self.action_batch_open.setStatusTip('批量导入')
        self.action_batch_open.triggered.connect(self.batch_open)

        self.menufile.addAction(self.action_batch_open)
        # 编辑
        self.action_clear_info = QAction('分析', self)
        self.action_clear_info.setStatusTip('分析.')
        self.action_clear_info.triggered.connect(self.analysis)

        self.menu_bar.addAction(self.action_clear_info)
        # 可视化
        self.action_visual = QAction('可视化', self)
        self.action_visual.setStatusTip('可视化.')
        self.action_visual.triggered.connect(self.visualize)

        self.menu_bar.addAction(self.action_visual)

        # 日志
        self.dialog = QAction('日志', self)
        self.dialog.setStatusTip('日志.')
        self.dialog.triggered.connect(self.dialog_info)

        self.menu_bar.addAction(self.dialog)

        self.target_view = TargetView()
        self.setCentralWidget(self.target_view)
        self.target_view.setBackgroundBrush(QBrush(QColor(214, 214, 214), Qt.SolidPattern))

        self.create_dock_windows()

    def create_dock_windows(self):

        self.dock_view_list = ViewList()
        self.dock_view_list.select_item_index.connect(self.select_item_change)
        # self.view_dock_widget.setWidget(self.view_list)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_view_list)

        self.dock_slice_info = InfoWidget()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_slice_info)
        self.dock_slice_info.setMinimumWidth(self.width*0.5)
        self.dock_slice_info.setMinimumHeight(self.height*0.4)

        self.dock_slice_tif = TifWidget()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_slice_tif)
        self.dock_slice_tif.setMinimumWidth(self.width*0.5)
        self.dock_slice_tif.setFixedHeight(self.height*0.5)


        self.dock_debug_info = DebugInfo()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_debug_info)
        self.dock_debug_info.setMinimumWidth(self.width*0.5)
        self.dock_debug_info.setFixedHeight(self.height*0.4)


        self.dock_debug_info.set_text_browser('')
        version_file = QFile("Version.txt")
        version_file.open(QIODevice.ReadOnly)
        ver_info = str(version_file.readAll(), encoding='utf-8')
        version_file.close()
        self.dock_debug_info.set_head_info(ver_info)

    def open_file(self):
        try:
            file_path = QFileDialog.getOpenFileName(self, '选择图像文件', '.',
                                                        # "All Files (*.*);; "
                                                        "Tiff Image (*.tif;*.tiff);; "
                                                        "General Image (*.bmp;*.jpg;*.png);;")
            # txt_path = QFileDialog.getOpenFileName(self, '选择检测结果', './images',
            #                                         # "All Files (*.*);; "
            #                                         "TXT  (*.txt);;")
            image_path = file_path[0]
            image_name = image_path.split('.')[0].split('/')[-1]
            txt_path = 'D:/share/{}/{}.txt'.format(image_name, image_name)
            if os.path.exists(image_path) and os.path.exists(txt_path):
                self.analysis()
            image = cv2.imread(image_path, 1)

            boxes = []
            slice_image_list = []
            for line in open(txt_path).readlines():
                box = [float(x) for x in line.strip().split(' ')]
                boxes.append(box)

                slice_image = image[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                slice_image = slice_image.copy()

                slice_image_list.append(slice_image)

            self.boxes_info = boxes
            self.slice_image_list = slice_image_list

            self.target_view.set_image(image)
            self.target_view.set_boxes(self.boxes_info)
        except:
            pass

    def batch_open(self):
        startDirectory = "C://"
        os.startfile(startDirectory)

    def analysis(self):
        self.target_view.clear_target_view()
        self.dock_view_list.clear_view_list()
        # self.dock_slice_info.clear_info()

        self.boxes_info.clear()
        self.slice_image_list.clear()

    def visualize(self):
        self.target_view.show_boxes()
        self.dock_view_list.set_slice_view(self.slice_image_list)

    def dialog_info(self):
        print(self)

    def select_item_change(self, connect):
        self.target_view.focus_box(int(connect))
        box_info = self.boxes_info[connect]
        info_dict = {}
        info_dict['index'] = connect + 1
        info_dict['position'] = '({}, {})'.format(box_info[0], box_info[1])
        info_dict['width'] = box_info[2] - box_info[0]
        info_dict['height'] = box_info[3] - box_info[1]
        info_dict['score'] = box_info[4]
        self.dock_slice_info.set_info(info_dict)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DetectionWindow()
    demo.show()
    sys.exit(app.exec_())
