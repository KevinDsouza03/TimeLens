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
    focused = getFocused()
    # Create a dict to store the focused window and the time
    data = {
        "Time": [now.strftime("%H:%M:%S")],
        "Focused": [focused]
    }
    # Create a dataframe from the dict
    df = pd.DataFrame(data)
    # Check if the file exists to determine if headers should be written
    file_exists = os.path.isfile(csv_file)
    # Create a CSV file to store the dataframe. Append to EOF if it exists, else write headers.
    df.to_csv(csv_file, index=False, mode="a", header=not file_exists)

