from win32gui import GetWindowText, GetForegroundWindow

#Gets the focused window's title.
#Returns a string.
def getFocused():
    return GetWindowText(GetForegroundWindow())