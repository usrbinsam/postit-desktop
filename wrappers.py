import subprocess
import tempfile

def screencapture(windowSelection=False, outputFile='', imgFormat="png", delay=0,
    noShadow=False, noSound=False, noMetaData=False):
    """ `screencapture' command line util wrapper for macOS.
    refer to `man 1 screencapture' for a reference to the options below on macOS """

    args = [ "screencapture"
        , "-i"                           ## interactive mode
        , "-t{}".format(imgFormat)      ## image format (default is PNG for screencapture)
    ]

    if windowSelection:
        args.append("-W")

    if delay:
        args.append("-T{}".format(delay))

    if noShadow:
        args.append("-o")

    if noSound:
        args.append("-x")

    if noMetaData:
        args.append("-r")

    if not outputFile:
        fh, name = tempfile.mkstemp(suffix="." + imgFormat)
        outputFile = name
        
    args.append(outputFile)
    subprocess.call(args)

    return outputFile

def captureWindow():
    return screencapture(windowSelection=True)

def captureSelection():
    return screencapture()
