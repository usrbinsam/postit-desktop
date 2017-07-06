# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/Ui_Main.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(235, 191)
        MainWindow.setMouseTracking(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/static/angry.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.shootDesktopBn = QtWidgets.QPushButton(self.centralwidget)
        self.shootDesktopBn.setObjectName("shootDesktopBn")
        self.gridLayout.addWidget(self.shootDesktopBn, 1, 0, 1, 1)
        self.shootAreaBn = QtWidgets.QPushButton(self.centralwidget)
        self.shootAreaBn.setObjectName("shootAreaBn")
        self.gridLayout.addWidget(self.shootAreaBn, 2, 0, 1, 1)
        self.shootWindowBn = QtWidgets.QPushButton(self.centralwidget)
        self.shootWindowBn.setObjectName("shootWindowBn")
        self.gridLayout.addWidget(self.shootWindowBn, 3, 0, 1, 1)
        self.loginBn = QtWidgets.QPushButton(self.centralwidget)
        self.loginBn.setObjectName("loginBn")
        self.gridLayout.addWidget(self.loginBn, 0, 0, 1, 1)
        self.preferencesBn = QtWidgets.QPushButton(self.centralwidget)
        self.preferencesBn.setObjectName("preferencesBn")
        self.gridLayout.addWidget(self.preferencesBn, 4, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "POST It"))
        self.shootDesktopBn.setText(_translate("MainWindow", "Full Screen"))
        self.shootAreaBn.setText(_translate("MainWindow", "Selection"))
        self.shootWindowBn.setText(_translate("MainWindow", "Window"))
        self.loginBn.setText(_translate("MainWindow", "Log In"))
        self.preferencesBn.setText(_translate("MainWindow", "Preferences"))

import resource_rc
