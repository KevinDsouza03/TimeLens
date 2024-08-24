import os
import pandas as pd
from retrieveFocus import getFocused
from datetime import datetime

path_to_folder = "results"
csv_file = path_to_folder + "/focus.csv"
def storeFocus():
    # Get the current time
    now = datetime.now()
    # Get the current focused window
    file_exists = os.path.isfile(csv_file)
    focused = getFocused()
    if file_exists:
        prev = pd.read_csv(csv_file)['Focused'].iloc[-1]
        print(prev)
        if prev == focused:
            return
    # Create a dict to store the focused window and the time
    data = {
        "Time": [now.strftime("%H:%M:%S")],
        "Focused": [focused]
    }
    # Create a dataframe from the dict
    df = pd.DataFrame(data)
    # Check if the file exists to determine if headers should be written
    # Create a CSV file to store the dataframe. Append to EOF if it exists, else write headers.
    df.to_csv(csv_file, index=False, mode="a", header=not file_exists)

