from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *

class SelectorWindow(QDialog):

    selectionMade = pyqtSignal(QScreen, int, int, int, int)
    selectionCanceled = pyqtSignal()

    def __init__(self, parent=None):
        super(SelectorWindow, self).__init__(parent)

        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

class RectangularSelectionWindow(SelectorWindow):

    def __init__(self, parent=None):
        super(SelectorWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowOpacity(.50)
        self.rejected.connect(self.selectionCanceled.emit)

        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self._origin = QPoint()

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self._origin = self.mapFromGlobal(self.mapToGlobal(event.pos()))
            self.rubberBand.setGeometry(QRect(self._origin, QSize()))
            self.rubberBand.show()

    def mouseMoveEvent(self, event):

        pos = self.mapFromGlobal(self.mapToGlobal(event.pos()))
        if not self._origin.isNull():
            self.rubberBand.setGeometry(QRect(self._origin, pos).normalized())

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.rubberBand.hide()
            x, y, w, h = self.rubberBand.geometry().getRect()
            screen = self.windowHandle().screen()
            self.selectionMade.emit(screen, x, y, w, h)

"""
class RectWidget(QWidget):

    def __init__(self, parent=None):
        super(RectWidget, self).__init__(parent)
        self.setAttribute(Qt.WA_StaticContents) ## optimization

    def paintEvent(self, event):
        rect = event.rect()
        painter = QPainter(this)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.red)
        painter.drawRect(rect)


class WindowSelectionWindow(SelectorWindow):

    def __init__(self, parent=None):
        super(WindowSelectionWindow, self).__init__(parent)
        self.painter = QPainter()
        self.targetWId = 0
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def mouseMoveEvent(self, event):

        pos = self.mapFromGlobal(self.mapToGlobal(event.pos()))
        WId = getWindowUnderCursor(pos)
        self.targetWId = WId
        geometry = QRect(*getWindowDimensions(WId))

        print("WId {} Dimensions {}".format(WId, geometry))

        self.drawRectangle(geometry)

    def drawRectangle(self, geometry):

        r = RectWidget(self)
        r.setGeometry(geometry)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            screen = self.windowHandle().screen()
            pixmap = screen.grabWindow(self.targetWId)
            self.selectionMade.emit(pixmap)
"""
