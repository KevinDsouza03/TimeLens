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
    print(data['Focused'])
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
            program TEXT,
            session_end BOOLEAN DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS program_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program TEXT UNIQUE,  -- Ensure the program column is unique
            total_time TEXT, 
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS general_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_context_switches INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    connection.commit()
    connection.close()


# This function processes every stat thats in the program scope.
def programStats():
    connection = sqlite3.connect(db_file)   
    df = pd.read_sql("SELECT * FROM focus_logs",connection)
    #The first thing is to add a tracking ended entry. So...
    # Now by entry, I want to get a total time/add up datetimes. Join "Date" and "Time" then just sum up?
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    df = df.sort_values(by=['datetime'])

    # Current datetime - next datetime
    df['timespent'] = df['datetime'].shift(-1) - df['datetime']
    # For the last row, set a default time (e.g., 5 seconds), as there's no next row
    df.iloc[-1, df.columns.get_loc('timespent')] = pd.Timedelta(seconds=5)

    total_time_per_program = df.groupby('program')['timespent'].sum()


    #Task: Storing insights FOR EACH PROGRAM into the database
    insights_data = {
        'total_time': total_time_per_program
        #Add more data here as needed
    }
    cursor = connection.cursor()

    # Insert or update insights for each program
    for program, total_time in total_time_per_program.items():

        # Insert or update the row for the program
        cursor.execute('''
            INSERT INTO program_insights (program, total_time)
            VALUES (?, ?)
            ON CONFLICT(program) DO UPDATE SET 
            total_time = excluded.total_time,
            last_updated = CURRENT_TIMESTAMP
        ''', (program, str(total_time)))
    
    connection.commit()
    connection.close()

def dayStats():
    #Todo
    return

def monthStats():
    #Todo
    return

def overallStats():
    #Todo
    return

#Main function to call all others
def processFocus():
    """
    Think about what you want to see from our current data collection.

    *Each Seperation here will be a different table in db, as constantly re-calculating this is too inefficient
    Goes from specific to broader outlooks

    Per Program
    1. Total time on Program DONE
    2. Most used program in general *Can be accomplished by sorting via Total Time DONE
    3. Average time spent focused on a program.
    
    Per Session: Between Session End entries
    1. 

    Per Day
    1. Day specific time calculating (Grouping via Date)
    
    Per Month
    1. Monthly Insights

    Overarching insights
    1. Time distribution by Category: Classify specific apps (Work, Personal, Entertainment) and display how its broken down
        - Categorize common applications. Make the user do it currently? Selecting an "intention" per focus session, and it categorizes it then. 

    2. Context Switching, How often are we task switching
        - Track time when "program" changes, and we can mark that down in the db. Then afterwards, can group by program and that gives us a 
            "how long we stay focused on program"
                - Can repurpose the normal calculation for time. Instead of "sum" it can be mean? Line 105
                - Also have a col w a counter for each time we switch.

    3. What time of the day are we the most productive? Morning, Afternoon, e.t.c
    

    potential changes:
    - Making a 'datetime' column in each program might be repetitive. Could maybe just make that the entire column? Or is it not that much
        repeated work?
    """
    connection = sqlite3.connect(db_file) 
    cursor = connection.cursor() 
    time = datetime.now() 
    # Insert a session end marker
    cursor.execute('''
        INSERT INTO focus_logs (date, time, focused, program, session_end)
        VALUES (?, ?, ?, ?, ?)
    ''', (time.strftime("%m/%d/%Y"), time.strftime("%H:%M:%S"), 'Session End', 'None', True))

    connection.commit()
    connection.close()
    programStats()
    return