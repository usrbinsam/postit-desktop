import platform
import io

from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *

RUNNING_IN_HELL = platform.system() == 'Windows'
RUNNING_IN_STEVE_JOBS = platform.system() == 'Darwin'
RUNNING_IN_GANOO_LOONIX = platform.system() == 'Linux'

def Pixmap2StringIO(pixmap):

    byteArray = QByteArray()
    buffer = QBuffer(byteArray)

    buffer.open(QIODevice.WriteOnly)
    pixmap.save(buffer, "PNG")

    strio = io.StringIO(byteArray)
    strio.seek(0)

    return strio
