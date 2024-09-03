import os
import pandas as pd
from win32gui import GetWindowText, GetForegroundWindow
from datetime import datetime
import win32process  # For PID
import psutil  # Gives PID info

path_to_folder = "results"
csv_file = path_to_folder + "/focus.csv"
def storeFocus():
    # Get the current focused window
    file_exists = os.path.isfile(csv_file)
    data = getFocused() #HWND object
    if file_exists:
        prev = pd.read_csv(csv_file)['Focused'].iloc[-1]
        print(prev)
        if prev == data['Focused']:
            return
    # Create a dict to store the focused window and the time
    # Create a dataframe from the dict
    df = pd.DataFrame([data])
    # Create a CSV file to store the dataframe. Append to EOF if it exists, else write headers.
    df.to_csv(csv_file, index=False, mode="a", header=not file_exists)

# Gets the focused window's title.
# Returns a dictionary with date-time, focused window title, and program name.
def getFocused():
    HWND = GetForegroundWindow()
    tid, pid = win32process.GetWindowThreadProcessId(HWND)
    time = datetime.now()  # Corrected this line
    data = {
        "Date": time.strftime("%m/%d/%Y"),
        "Time": time.strftime("%H:%M:%S"),
        "Focused": GetWindowText(HWND),
        "Program": psutil.Process(pid).name(),
    }
    return data

def processFocus():
    """
    Think about what you want to see from our current data collection.

    *Each Seperation here will be a different file, as constantly re-calculating this is too inefficient
    Goes from specific to broader outlooks

    1. Total time on Program
    2. Most used program in general *Can be accomplished by sorting via Total Time
    3. Context Switching, How often are we task switching
        - Average time spent focused on a task.
        - How often are we switching, hourly.
    4. What time of the day are we the most productive? Morning, Afternoon, e.t.c
    
    
    1. Day specific time calculating (Grouping via Date)
    
    1. Monthly Insights

    1. Time distribution by Category: Classify specific apps (Work, Personal, Entertainment) and display how its broken down


    """