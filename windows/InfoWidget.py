from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QDockWidget, QWidget, QTreeWidget, QVBoxLayout, QTreeWidgetItem, QHeaderView


class InfoWidget(QDockWidget):
    def __init__(self, parent=None):
        super(InfoWidget, self).__init__()

        self.setWindowTitle('图像分析结果')
        self.setFeatures(QDockWidget.NoDockWidgetFeatures | QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetMovable)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.dock_widget_contents = QWidget()
        self.setWidget(self.dock_widget_contents)

        self.info_tree = QTreeWidget(self.dock_widget_contents)

        self.layout = QVBoxLayout(self.dock_widget_contents)
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(4, 0, 0, 10)
        self.layout.addWidget(self.info_tree)
        self.root = QTreeWidgetItem(self.info_tree)

        self.dock_widget_contents.setMinimumWidth(400)
        self.setup()


    def setup(self):
        self.info_tree.header().hide()
        self.info_tree.setColumnCount(3)
        # self.info_tree.setColumnWidth(0, 100)
        # self.info_tree.setColumnWidth(1, 100)
        # self.info_tree.setColumnWidth(2, 100)
        self.info_tree.setHeaderLabels(['Key','Value',''])
        self.info_tree.header().setSectionResizeMode(QHeaderView.ResizeMode(3))
        self.root.setText(0, "信息")
        self.root.setText(1, "")
        self.n_item_basic_info = QTreeWidgetItem(self.root)
        self.n_item_basic_info.setText(0, "子切片信息: ")
        self.n_item_index = self.add_item(self.n_item_basic_info, '目标编号：', '-')
        self.n_item_width = self.add_item(self.n_item_basic_info, '切片宽度：', '-')
        self.n_item_height = self.add_item(self.n_item_basic_info, '切片高度：', '-')
        self.n_item_is_pos = self.add_item(self.n_item_basic_info, '是否存在阳性区域：', '-')
        self.n_item_rate = self.add_item(self.n_item_basic_info, '阳性区域占比：', '-')

        self.item_basic_info = QTreeWidgetItem(self.root)
        self.item_basic_info.setText(0, '当前全切片信息：')
        self.item_index = self.add_item(self.item_basic_info, '全切片编号：', '-')
        self.item_width = self.add_item(self.item_basic_info, '全切片宽度：', '-')
        self.item_height = self.add_item(self.item_basic_info, '全切片高度：', '-')
        self.item_channels = self.add_item(self.item_basic_info, '通道数：', '-')
        self.item_rate = self.add_item(self.item_basic_info, '阳性区域占比：', '-')
        self.item_pixel_acc = self.add_item(self.item_basic_info, '平均像素精度：', '-')
        self.item_dice = self.add_item(self.item_basic_info, 'Dice：', '-')
        self.item_jaccard = self.add_item(self.item_basic_info, 'jaccard：', '-')
        self.item_recall = self.add_item(self.item_basic_info, 'recall: ', '-')
        self.item_precision = self.add_item(self.item_basic_info, 'precision: ', '-')
        self.info_tree.addTopLevelItem(self.root)
        self.info_tree.expandAll()
    def add_head(self, head_name):
        print("x")
        head = QTreeWidgetItem(self.root)
        head.setText(0, head_name)
        # head.setBackground(1, QBrush(QColor(240, 240, 240)))
        # head.setBackground(2, QBrush(QColor(240, 240, 240)))
        # head.setForeground(1, QBrush(Qt.gray))
        # head.setForeground(2, QBrush(Qt.gray))
        # # self.info_tree.addTopLevelItem(head)
        # head.setExpanded(True)
        return head

    def add_item(self, head, name, value):
        # print("s")
        item = QTreeWidgetItem(head)
        item.setText(0, name)
        item.setText(1, value)
        item.setTextAlignment(1, Qt.AlignRight)
        item.setFlags(Qt.NoItemFlags)
        # head.addChild(item)
        return item

    # def set_info(self, info_dict):
    #     self.item_index.setData(2, 2, info_dict['index'])
    #     # self.item_position.setData(2, 2, info_dict['position'])
    #     self.item_width.setData(2, 2, info_dict['width'])
    #     self.item_height.setData(2, 2, info_dict['height'])
    #     self.item_score.setData(2, 2, info_dict['score'])
    #
    # def clear_info(self):
    #     self.item_index.setData(2, 2, '-')
    #     # self.item_position.setData(2, 2, '-')
    #     self.item_width.setData(2, 2, '-')
    #     self.item_height.setData(2, 2, '-')
    #     self.item_score.setData(2, 2, '-')
