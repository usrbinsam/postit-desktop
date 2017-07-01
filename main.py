import sys, platform

from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *

from ui.Ui_Main import Ui_MainWindow
from selector import RectangularSelectionWindow
from utils import *
import wrappers

if RUNNING_IN_HELL:
    import win32gui

    def getWindowUnderCursor(p):
        return win32gui.WindowFromPoint((p.x(), p.y()))
    def getWindowDimensions(WId):
        return win32gui.GetWindowRect(WId)
    def getWindowText(WId):
        return win32gui.GetWindowText(WId).encode("UTF-8")
    def getCurrentWindow():
        return win32gui.GetCapture()

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # screenshot the whole desktop
        self.takeScreenShotButton.clicked.connect(self.shootFullScreen)

        # screenshot a selection
        self.takeSelectionScreenShotButton.clicked.connect(self.rectangularSelection)
        self.selectorWindows = [ ]

        """
        1. get ID/dimensions of the window under the cursor
        2. draw box around the window
        3. repeat when cursor point is no longer inside dimensions
        """
        # screenshot a window
        self.takeWindowScreenShotButton.clicked.connect(self.enableWindowSelectionMode)
        self.highlightWindows = [ ]
        self.currentGeometry = QRect()
        self.currentWId = -1
        self.setMouseTracking(True)
        self.windowSelectionMode = False

        self.trayIcon = QSystemTrayIcon(self)

    def shootWindowId(self, WId):
        screen = self.windowHandle().screen()
        pixmap = screen.grabWindow(WId)

        self.promptSavePixmap(pixmap)
    
    def enableWindowSelectionMode(self):

        if RUNNING_IN_STEVE_JOBS:
            fn = wrappers.captureWindow()

        elif RUNNING_IN_HELL:
            self.windowSelectionMode = True
            self.setMouseTracking(True)
    
    def disableWindowSelectionMode(self):
        self.windowSelectionMode = False
        self.setMouseTracking(True)
        ## TODO: cleanup remaining highlight boxes

    def mouseIsMoving(self, pos):

        if not self.windowSelectionMode:
            return

        pos = self.mapFromGlobal(self.mapToGlobal(pos))
        print("cursor is at X: {}, Y: {}".format(pos.x(), pos.y()))

        if self.currentWId == -1:

            self.rememberWindowAtPos(pos)
            ## TODO: draw box here
        
        elif self.currentWId > 0 and not self.currentGeometry.contains(pos):
            print("moved outside of previous window dimensions")
            self.rememberWindowAtPos(pos)

    def rememberWindowAtPos(self, pos):

        WId = getWindowUnderCursor(pos)
        if WId == 0:
            print("cursor is on the desktop, ignored")
            return

        if WId == self.currentWId:
            print("EH?! grabbed the same window even the cursor moved outside of it...")

        self.currentWId = WId
        self.currentGeometry = QRect(*getWindowDimensions(WId))

        print("stored WId {} ({}) @ {}".format(WId, getWindowText(WId), self.currentGeometry))

    def rectangularSelection(self):

        if RUNNING_IN_STEVE_JOBS:
            wrappers.captureSelection()
        elif RUNNING_IN_HELL:
            self.showSelectors(RectangularSelectionWindow)

    def shootFullScreen(self):

        shots = [ ]

        w = 0
        h = 0

        for screen in QGuiApplication.screens():

            rect = screen.geometry()
            shot = screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())

            w += shot.width()
            if h < shot.height(): # in case one screen is larger than the other
                h = shot.height()

            shots.append(shot)

        pixmap = QPixmap(w, h)
        painter = QPainter(pixmap)
        pixmap.fill(Qt.black)

        p = 0

        for ss in shots:
            painter.drawPixmap(QPoint(p, 0), ss)
            p += ss.width()

        painter.end()

        self.promptSavePixmap(pixmap)

    def showSelectors(self, selectorClass):

        self.selectorWindows = [ ]
        desktop = qApp.desktop()

        for i in range(desktop.screenCount()):
            selector = selectorClass()
            self.selectorWindows.append(selector)

            selector.setGeometry(desktop.screenGeometry(i))

            selector.selectionCanceled.connect(self.hideSelectors)
            selector.selectionMade.connect(self.selectionMade)

            selector.showFullScreen()
            selector.windowHandle().setScreen(qApp.screens()[i])

    def hideSelectors(self):
        
        for selector in self.selectorWindows:
            selector.hide()

    def selectionMade(self, pixmap):

        self.hideSelectors()
        self.promptSavePixmap(pixmap)

    def promptSavePixmap(self, pixmap):

        path = QFileDialog.getSaveFileName(self, "Save Screenshot", 
            "Screenshot {}.png".format(QDateTime.currentDateTime().toString("dd-MM-yy h.mm.ss.z")))

        if path[0]:
            pixmap.save(path[0], "PNG")

    def closeEvent(self, event):

        if RUNNING_IN_STEVE_JOBS:
            if not event.spontaneous() and not self.isVisible():
                return

        QMessageBox.information(self, "Systray",
            "I'm running in the system tray. "
            "Use <b>Quit</b> from the tray menu to end me."
        )
        self.hide()
        event.ignore()
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())