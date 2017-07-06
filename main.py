import os, sys, platform, webbrowser

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from utils import *

from ui.Ui_Main import Ui_MainWindow
from selector import RectangularSelectionWindow

if RUNNING_IN_STEVE_JOBS:
    import wrappers_mac as wrappers
elif RUNNING_IN_HELL:
    import wrappers_win32 as wrappers

from restclient import LoginDialog, UploadThread, UploadHandleThread

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.shootDesktopBn.clicked.connect(self.shootFullScreen)
        self.shootAreaBn.clicked.connect(self.rectangularSelection)
        self.shootWindowBn.clicked.connect(self.enableWindowSelectionMode)
        self.loginBn.clicked.connect(self.loginUser)

        self.selectorWindows    = [ ]
        self.highlightWindows   = [ ]
        self.uploadThreads      = [ ]
        self.lastUpload         = ''
        self.currentGeometry    = QRect()
        self.currentWId         = -1

        icon = QIcon(":static/angry.svg")
        icon.setIsMask(True)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(icon)
        self.trayIcon.show()
        self.trayIcon.setContextMenu(self.createMenu())
        self.trayIcon.messageClicked.connect(self.openLastUpload) ## this is never triggered on macOS. sorry

        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope,
            "GliTch_ Is Mad Studios", "PostIt")

        self.readSettings()        

    def openLastUpload(self):
        webbrowser.open_new_tab(self.lastUpload)

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
        else:
            self.loginUser()

        if not self.settings.contains("internet/address"):
            self.settings.setValue("internet/address", "https://nsfw.run")

    def loginUser(self):

        diag = LoginDialog(self)
        if diag.exec_():
            self.settings.setValue("internet/authToken", diag.loginToken)

    def shootWindowId(self, WId):
        screen = self.windowHandle().screen()
        pixmap = screen.grabWindow(WId)

        self.uploadHandle(pixmap2bytesIO(pixmap))

    def enableWindowSelectionMode(self):

        if RUNNING_IN_STEVE_JOBS:
            fn = wrappers.captureWindow()
            if fn:
                self.uploadFile(fn)

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
                self.uploadFile(fn)

        else:
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

        self.uploadHandle(pixmap2bytesIO(pixmap))

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

    def selectionMade(self, screen, x, y, w, h):

        self.hideSelectors()

        pixmap = screen.grabWindow(0, x, y, w, h)

        strIO = pixmap2bytesIO(pixmap)
        self.uploadHandle(strIO)

    def uploadFile(self, path):
        """ used for uploading a file on the file-system """
        thread = UploadThread(
            self.settings.value("internet/address") + "/api/upload",
            self.settings.value("internet/authToken"),
            path, self)

        thread.resultReady.connect(self.uploadComplete)
        thread.start()
        self.uploadThreads.append(thread)

    def uploadHandle(self, handle):
        """ used for uploading a file-like object that has a .read() method """
        thread = UploadHandleThread(
            self.settings.value("internet/address") + "/api/upload",
            self.settings.value("internet/authToken"),
            handle, self)

        thread.resultReady.connect(self.uploadComplete)
        thread.start()
        self.uploadThreads.append(thread)

    def uploadComplete(self, uri, error):

        if uri and not error:

            URL = self.settings.value("internet/address") + uri

            clipboard = QGuiApplication.clipboard()
            clipboard.setText(URL)
            self.lastUpload = URL
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

        if self.isVisible():
            QMessageBox.information(self, "Systray",
                "I'm running in the system tray. "
                "Use Quit from the tray menu to end me."
            )
            event.ignore()
            self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
