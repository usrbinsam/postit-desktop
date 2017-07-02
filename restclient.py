import json
import requests
from bs4 import BeautifulSoup

from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *

from ui.Ui_LoginDialog import Ui_LoginDialog

def getLoginToken(address, email, password, timeout=15):
    """ attempt to get a login token. KeyError means invalid username or password"""

    client = requests.session()

    soup = BeautifulSoup(client.get(address, timeout=timeout).text, "html.parser")
    csrf = soup.find('input', { 'name': "csrf_token" })['value']

    login_data = json.dumps({
        "email": email,
        "password": password,
        "csrf_token": csrf
    })

    r = client.post(address, data=login_data, headers={ "content-type": "application/json" }, timeout=timeout).json()

    ## if there's a login failure here, the server will report back whether the username or password was wrong.
    ## https://github.com/mattupstate/flask-security/issues/673

    return r['response']['user']['authentication_token']

def uploadFile(address, token, path):
    """ KeyError means the upload failed """

    headers = {
        "content-type": "application/json",
        "Authentication-Token": token
    }

    files = {
        "image": open(path, 'rb')
    }

    return requests.post(address, headers=headers, files=files).json()['url']

class UploadThread(QThread):

    resultReady = pyqtSignal(str, object)

    def __init__(self, addr, token, path, parent=None):
        super(UploadThread, self).__init__(parent)

        self.addr = addr
        self.path = path
        self.token = token

    def run(self):
        url, error = None, None

        try:
            uploadFile(self.addr, self.token, self.path)
        except Exception as e:
            error = e
        
        self.resultReady.emit(url, error)

class LoginThread(QThread):

    resultReady = pyqtSignal(str, object)

    def __init__(self, addr, email, password, parent=None):
        super(LoginThread, self).__init__(parent)

        self.addr = addr
        self.email = email
        self.password = password

    def run(self):
        token, error = None, None

        try:
            token = getLoginToken(self.addr, self.email, self.password)
        except Exception as e:
            error = e

        self.resultReady.emit(token, error)

class LoginDialog(QDialog, Ui_LoginDialog):
    def __init__(self, parent):
        super(LoginDialog, self).__init__(parent)
        self.setupUi(self)

        self.loginToken = None
        self.thread = QThread(self)

    def accept(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        addr = QSettings(QSettings.IniFormat, QSettings.UserScope, "GliTch_ Is Mad Studios", "PostIt").value("internet/address")

        self.thread = LoginThread(addr + "/login",
            self.emailAddressLineEdit.text(),
            self.passwordLineEdit.text(), self)
        self.thread.resultReady.connect(self.gotToken)
        self.thread.start()
    
    def reject(self):
        if self.thread.isRunning():
            self.thread.terminate()

        super().reject()

    def gotToken(self, token, error):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        if token and not error:
            self.loginToken = token
            super().accept()
        else:
            msg = ''
            if isinstance(error, KeyError):
                msg = "Invalid username or password."
            else:
                msg = str(error)

            QMessageBox.critical(self, "Login Failed", msg)
