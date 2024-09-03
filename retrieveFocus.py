from win32gui import GetWindowText, GetForegroundWindow
from datetime import datetime
import win32process  # For PID
import psutil  # Gives PID info

# Gets the focused window's title.
# Returns a dictionary with date-time, focused window title, and program name.
def getFocused():
    HWND = GetForegroundWindow()
    tid, pid = win32process.GetWindowThreadProcessId(HWND)
    time = datetime.now()  # Corrected this line
    data = {
        "DateTime": time.strftime("%m/%d/%Y, %H:%M:%S"),
        "Focused": GetWindowText(HWND),
        "Program": psutil.Process(pid).name(),
    }
    return data
