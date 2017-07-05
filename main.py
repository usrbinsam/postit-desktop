import os, sys, platform

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from ui.Ui_Main import Ui_MainWindow

from selector import RectangularSelectionWindow
from utils import *
import wrappers

from restclient import LoginDialog, UploadThread

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

        self.logInButton.clicked.connect(self.loginUser)

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

        icon = QIcon("static/angry.svg")
        icon.setIsMask(True)
        self.setWindowIcon(icon)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(icon)
        self.trayIcon.show()
        self.trayIcon.setContextMenu(self.createMenu())

        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope,
            "GliTch_ Is Mad Studios", "PostIt")

        self.readSettings()

        self.uploadThreads = [ ]

        self.readEnvironment()

    def createMenu(self):
        menu = QMenu(self)
        menu.addAction("Desktop Screenshot", self.shootFullScreen)
        menu.addAction("Window Screenshot", self.enableWindowSelectionMode)
        menu.addAction("Select Area", self.rectangularSelection)
        menu.addSeparator()
        menu.addAction("Show", self.show)
        menu.addAction("Quit", self.close)
        return menu

    def readSettings(self):

        if self.settings.contains("internet/authToken"):
            self.authToken = self.settings.value("internet/authToken")

        if not self.settings.contains("internet/address"):
            self.settings.setValue("internet/address", "https://nsfw.run")

    def loginUser(self):

        diag = LoginDialog(self)
        if diag.exec_():
            self.settings.setValue("internet/authToken", diag.loginToken)

    def shootWindowId(self, WId):
        screen = self.windowHandle().screen()
        pixmap = screen.grabWindow(WId)

        self.promptSavePixmap(pixmap)

    def enableWindowSelectionMode(self):

        if RUNNING_IN_STEVE_JOBS:
            fn = wrappers.captureWindow()
            if fn:
                self.startUpload(fn)

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
            fn = wrappers.captureSelection()
            if fn:
                self.startUpload(fn)

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

        io = Pixmap2StringIO(pixmap)

        self.startUpload(self, io)

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

    def startUpload(self, path):
        thread = UploadThread(
            self.settings.value("internet/address") + "/api/upload",
            self.settings.value("internet/authToken"),
            path, self)

        thread.resultReady.connect(self.uploadComplete)
        thread.start()
        self.uploadThreads.append(thread)

    def uploadComplete(self, uri, error):

        if uri and not error:

            clipboard = QGuiApplication.clipboard()
            clipboard.setText(self.settings.value("internet/address") + uri)
            self.trayIcon.showMessage("Upload Complete", "Image upload complete. The URL is in your clipboard.")

        else:
            QMessageBox.critical(self, "Upload Error", str(error))
            raise error

    def purgeAllThreads(self):
        for thread in self.uploadThreads:
            if thread.isRunning():
                thread.terminate()

    def closeEvent(self, event):

        if RUNNING_IN_STEVE_JOBS:
            if not event.spontaneous() and not self.isVisible():
                return

        QMessageBox.information(self, "Systray",
            "I'm running in the system tray. "
            "Use Quit from the tray menu to end me."
        )
        self.hide()
        event.ignore()

    def readEnvironment(self):

        if os.environ.get("POSTIT_SHOW_ON_STARTUP", False) :
            self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    #mw.show()
    sys.exit(app.exec_())