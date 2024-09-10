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
            average_time TEXT,
            context_switch INTEGER,
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
    """
    Per Program
        1. Total time on Program DONE
        2. Most used program in general *Can be accomplished by sorting via Total Time DONE
        3. So, sum up until we reach a different program, then at the end of df we average that. Average_time, more of a total one.  DONE
    """
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
    cursor = connection.cursor()

    # Next code is to calcuate average_time. I did this by summing up until we context switch (change programs), then average those sums.
    total_time_per_program = {}
    program_switch_counts = {}
    previous_program = None
    program_start_time = None


    for i, row in df.iterrows():
        current_program = row['program']
        
        # First entry handling
        if previous_program is None:  
            previous_program = current_program
            program_start_time = row['datetime']
            continue

        # When program changes, we sum from current datetime to start datetime. Giving us a total spent before context switching.
        if current_program != previous_program or row.get('session_end', False):
            time_spent = row['datetime'] - program_start_time

            # Update total time and switch count for the previous program
            if previous_program not in total_time_per_program:
                total_time_per_program[previous_program] = time_spent
                program_switch_counts[previous_program] = 1
            else:
                total_time_per_program[previous_program] += time_spent
                program_switch_counts[previous_program] += 1

            #Store our program counts into the dictionary above, and the intial variables for later calculation.
            previous_program = current_program
            program_start_time = row['datetime']

    #Last program handling
    if previous_program is not None:
        time_spent = pd.Timedelta(seconds=5)
        if previous_program not in total_time_per_program:
            total_time_per_program[previous_program] = time_spent
            program_switch_counts[previous_program] = 1
        else:
            total_time_per_program[previous_program] += time_spent
            program_switch_counts[previous_program] += 1

    #Average calc, total / context switches
    average_time_per_program = {
        program: total_time / program_switch_counts[program] 
        for program, total_time in total_time_per_program.items()
    }
    
    #Database updating
    for program, total_time in total_time_per_program.items():
        average_time = average_time_per_program[program]
        context_switch = program_switch_counts[program]
        #put new rows here and update query accordingly
        cursor.execute('''
            INSERT INTO program_insights (program, total_time, average_time, context_switch)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(program) DO UPDATE SET 
            total_time = excluded.total_time,
            average_time = excluded.average_time,
            context_switch = excluded.context_switch,
            last_updated = CURRENT_TIMESTAMP
        ''', (program, str(total_time), str(average_time), context_switch))
    
    connection.commit()
    connection.close()

def dayStats():
    #Todo
    """
    Per Day
        1. Day specific time calculating (Grouping via Date)
    """
    return

def monthStats():
    #Todo
    """
    Per Month
        1. Monthly Insights
    """
    return

def overallStats():
    #Todo
    """
    Overarching insights
        1. Time distribution by Category: Classify specific apps (Work, Personal, Entertainment) and display how its broken down
            - Categorize common applications. Make the user do it currently? Selecting an "intention" per focus session, and it categorizes it then. 

        2. Context Switching, How often are we task switching
            - Track time when "program" changes, and we can mark that down in the db. Then afterwards, can group by program and that gives us a 
                "how long we stay focused on program"
                    - 
                    - Also have a col w a counter for each time we switch.

        3. What time of the day are we the most productive? Morning, Afternoon, e.t.c
    """
    return

#Main function to call all others
def processFocus():
    """
    Think about what you want to see from our current data collection.

    *Each Seperation here will be a different table in db, as constantly re-calculating this is too inefficient
    Goes from specific to broader outlooks
    Per Session: Between Session End entries
    1. 

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