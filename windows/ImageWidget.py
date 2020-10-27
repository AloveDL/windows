from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
import os


class ImageWidget(QtWidgets.QWidget):
    # 单选,上一个被选择的对象
    prevSelected = None
    myclicked = QtCore.pyqtSignal(int)
    """
    Use this widget to display image.
    """

    def __init__(self):
        super(ImageWidget, self).__init__()
        self.id = 0
        self.displayText = ''  # 显示的文字
        self.version = ''
        self.status = 0
        self.path = ''
        self.showStatus = True
        self.selected = False
        self.isHightlight = False
        self.thumb = QtGui.QImage()
        self.initAttrib()

    def initAttrib(self):
        self.name_font = QtGui.QFont()
        self.bg_color = QtGui.QColor(50, 50, 50)
        self.hightlight = QtGui.QColor(255, 255, 255, 100)
        self.edge_size = 5
        self.pen_selected = QtGui.QPen(QtGui.QColor(255, 255, 0))
        self.pen_selected.setWidth(self.edge_size)
        self.pen_selected.setJoinStyle(QtCore.Qt.MiterJoin)

    #        self.setToolTip('aaaa\nbbbb\ncccc')

    def assetFile(self):
        return self.path + "_asset_.txt"

    def thumbFile(self):
        return self.path + "_thumb_.png"

    def informationFile(self):
        return self.path + "_information_.txt"

    def getPublishPath(self):
        current_version = self.version
        if not current_version:
            current_version = '000'
        new_version = int((current_version)) + 1
        return '%s/%03d' % (self.path, new_version)

    def getVersionPath(self, version):
        return '%s/%s' % (self.path, version)

    def getCurrentVersionPath(self):
        return self.getVersionPath(self.version)

    def setThumb(self, thumb=None):
        if not thumb:
            thumb = self.thumbFile()
        if os.path.isfile(thumb):
            self.thumb.load(thumb)
            self.repaint()
            return True

    def paintAsThumb(self, painter):
        name_height = max(self.height() * 0.15, 20)
        name_ty = self.height() - self.edge_size * 2
        # draw background
        painter.fillRect(self.rect(), self.bg_color)
        painter.drawImage(self.rect(), self.thumb)
        # draw hightlight
        if self.isHightlight and not self.selected:
            painter.fillRect(self.rect(), self.hightlight)
        # draw name
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
        self.name_font.setPixelSize(name_height)
        painter.setFont(self.name_font)
        # 脚标字符
        painter.drawText(self.edge_size, name_ty, str(self.displayText))

        if self.status:
            title_height = self.edge_size + name_height
            p1 = QtCore.QPoint(0, 0)
            p2 = QtCore.QPoint(0, title_height)
            p3 = QtCore.QPoint(title_height, 0)
            painter.setPen(QtCore.Qt.NoPen)
            painter.fillRect(0, 0, self.width(), title_height, QtGui.QColor(40, 40, 40, 40))
            if self.status == 1:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
            elif self.status == 2:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0)))
            elif self.status == 3:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 255)))
            painter.drawConvexPolygon(p1, p2, p3)

        if self.version:
            version_x = self.width() - self.edge_size - name_height * 1.5
            version_y = name_height
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
            painter.drawText(version_x, version_y, '%s' % self.version)

        # draw selected
        if self.selected:
            painter.setPen(self.pen_selected)
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawRect(self.edge_size / 2, self.edge_size / 2, \
                             self.width() - self.edge_size, self.height() - self.edge_size)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self.paintAsThumb(painter)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.setSelected()

    def mouseDoubleClickEvent(self, event):
        self.emit(pyqtSignal('doubleClick'))

    def enterEvent(self, event):
        self.isHightlight = True
        self.repaint()

    def leaveEvent(self, event):
        self.isHightlight = False
        self.repaint()

    # 设定当前为选中状态
    def setSelected(self):
        # 取消其他缩略图的选择状态, 当前设为选择状态
        if ImageWidget.prevSelected != None:
            ImageWidget.prevSelected.selected = False
            ImageWidget.prevSelected.repaint()
        self.selected = True
        self.repaint()
        ImageWidget.prevSelected = self

        self.onWidgetClicked()
        self.sender(pyqtSignal("click"), self.id)

    def onWidgetClicked(self):
        print('on widget clicked')