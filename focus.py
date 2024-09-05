import os
import pandas as pd
from win32gui import GetWindowText, GetForegroundWindow
from datetime import datetime
import win32process  # For PID
import psutil  # Gives PID info
import sqlite3

db_file = 'results/focus.db'

#First, we check if table exists, reference createTable()
#Next, we get our data and establish connection to the db. After that, we query to check the last program and check for change
#If not, input into db, otherwise return nothing
def storeFocus():
    # Get the current focused window
    createTable()
    data = getFocused() #HWND object
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT focused FROM focus_logs ORDER BY id DESC LIMIT 1               
    ''') #SELECTED focused column from the last input.
    last_focused = cursor.fetchone()

    if last_focused and last_focused[0] == data['Focused']:
        connection.close()
        return
    
    cursor.execute('''
        INSERT INTO focus_logs (date, time, focused, program)
        VALUES (?, ?, ?, ?)
    ''', (data['Date'], data['Time'], data['Focused'], data['Program']))
    connection.commit()
    connection.close()
    #Ensure we close connections

    

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

#If table doesnt exist, it gets created
def createTable():
    connection = sqlite3.connect(db_file) #A connection to the database
    cursor = connection.cursor() #Allows us to execute SQL

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS focus_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            focused TEXT,
            program TEXT
        )
    ''')

    connection.commit()
    connection.close()

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