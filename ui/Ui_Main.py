# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\Ui_Main.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(266, 263)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.takeSelectionScreenShotButton = QtWidgets.QPushButton(self.centralwidget)
        self.takeSelectionScreenShotButton.setObjectName("takeSelectionScreenShotButton")
        self.gridLayout.addWidget(self.takeSelectionScreenShotButton, 1, 0, 1, 1)
        self.takeScreenShotButton = QtWidgets.QPushButton(self.centralwidget)
        self.takeScreenShotButton.setObjectName("takeScreenShotButton")
        self.gridLayout.addWidget(self.takeScreenShotButton, 0, 0, 1, 1)
        self.takeWindowScreenShotButton = QtWidgets.QPushButton(self.centralwidget)
        self.takeWindowScreenShotButton.setObjectName("takeWindowScreenShotButton")
        self.gridLayout.addWidget(self.takeWindowScreenShotButton, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PostIt"))
        self.takeSelectionScreenShotButton.setText(_translate("MainWindow", "Selection"))
        self.takeScreenShotButton.setText(_translate("MainWindow", "Full Screen"))
        self.takeWindowScreenShotButton.setText(_translate("MainWindow", "Window"))

