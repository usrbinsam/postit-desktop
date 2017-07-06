import win32gui

def getWindowUnderCursor(p):
    return win32gui.WindowFromPoint((p.x(), p.y()))

def getWindowDimensions(WId):
    return win32gui.GetWindowRect(WId)

def getWindowText(WId):
    return win32gui.GetWindowText(WId).encode("UTF-8")

def getCurrentWindow():
    return win32gui.GetCapture()
