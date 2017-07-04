# POST It

Upload screenshots to my web sharing service.

As of this writing, the web service is not public and neither is the code,
however the desktop and GUI code will remain open source for those who
wish to use the service. 

This will work on macOS (OS X 10.2 and later), Windows (XP and later), 
and most Linux desktop environments. Your mileage may vary with
Linux as it is currently untested.

Window selection screenshots do NOT work on Windows 7 yet.

**Don't bother downloading this yet.** The code is incomplete and there's no
public service for it to login to.

## How It Works

### macOS and OS X

I cheated on macOS and wrote a wrapper around the screencapture tool.
See `man 1 screencapture` on any macOS / OS X machine to see how this works.
Screenshots are directed to a tempfile then uploaded using an authentication
token.

### Windows

On Windows, full desktop screenshots are done by stitching together an
individual screenshot of each desktop. Black is painted around blank space
caused by different dimensions between desktops.

Rectangular screenshots are done by overlaying translucent window over
each desktop, then taking a screenshot of the area selected by the user's
cursor with a QRubberBand.

## Binary Downloads

Eventually I'll cut nightly binary releases for download once the project
is stable and fully functional across all platforms.

## Source

Currently, you'll need PyQt5, the python-requests library, and the bs4 library.
To cut an executable, use PyInstaller, or launch `main.py` directly.
