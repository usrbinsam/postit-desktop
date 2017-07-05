# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\Ui_LoginDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        LoginDialog.setObjectName("LoginDialog")
        LoginDialog.resize(421, 189)
        self.gridLayout = QtWidgets.QGridLayout(LoginDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(LoginDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setObjectName("formLayout")
        self.emailAddressLabel = QtWidgets.QLabel(LoginDialog)
        self.emailAddressLabel.setObjectName("emailAddressLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.emailAddressLabel)
        self.emailAddressLineEdit = QtWidgets.QLineEdit(LoginDialog)
        self.emailAddressLineEdit.setObjectName("emailAddressLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.emailAddressLineEdit)
        self.passwordLabel = QtWidgets.QLabel(LoginDialog)
        self.passwordLabel.setObjectName("passwordLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.passwordLabel)
        self.passwordLineEdit = QtWidgets.QLineEdit(LoginDialog)
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.passwordLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(LoginDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(LoginDialog)
        self.buttonBox.accepted.connect(LoginDialog.accept)
        self.buttonBox.rejected.connect(LoginDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LoginDialog)

    def retranslateUi(self, LoginDialog):
        _translate = QtCore.QCoreApplication.translate
        LoginDialog.setWindowTitle(_translate("LoginDialog", "Login"))
        self.label.setText(_translate("LoginDialog", "<html><head/><body><p align=\"center\">Enter the email address and password you used to register at PostIt.</p><p align=\"center\">If you do not have an account, you can register <a href=\"http://localhost:5000/register\"><span style=\" text-decoration: underline; color:#0000ff;\">here</span></a>.</p></body></html>"))
        self.emailAddressLabel.setText(_translate("LoginDialog", "Email Address"))
        self.passwordLabel.setText(_translate("LoginDialog", "Password"))

