# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\Ui_Main.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(235, 213)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.logInButton = QtWidgets.QPushButton(self.centralwidget)
        self.logInButton.setObjectName("logInButton")
        self.gridLayout.addWidget(self.logInButton, 0, 0, 1, 1)
        self.takeScreenShotButton = QtWidgets.QPushButton(self.centralwidget)
        self.takeScreenShotButton.setObjectName("takeScreenShotButton")
        self.gridLayout.addWidget(self.takeScreenShotButton, 1, 0, 1, 1)
        self.takeSelectionScreenShotButton = QtWidgets.QPushButton(self.centralwidget)
        self.takeSelectionScreenShotButton.setObjectName("takeSelectionScreenShotButton")
        self.gridLayout.addWidget(self.takeSelectionScreenShotButton, 2, 0, 1, 1)
        self.takeWindowScreenShotButton = QtWidgets.QPushButton(self.centralwidget)
        self.takeWindowScreenShotButton.setObjectName("takeWindowScreenShotButton")
        self.gridLayout.addWidget(self.takeWindowScreenShotButton, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PostIt"))
        self.logInButton.setText(_translate("MainWindow", "Log In"))
        self.takeScreenShotButton.setText(_translate("MainWindow", "Full Screen"))
        self.takeSelectionScreenShotButton.setText(_translate("MainWindow", "Selection"))
        self.takeWindowScreenShotButton.setText(_translate("MainWindow", "Window"))

