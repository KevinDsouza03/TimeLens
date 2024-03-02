import pandas as pd # For writing to CSV
from retrieveFocus import getFocused
from datetime import datetime # Provides Timestamp for what was focused at what time.

path_to_folder = "results"

def storeFocus():
    # Get the current time
    now = datetime.now()
    # Get the current focused window
    focused = getFocused()
    # Create a dict to store the focused window and the time.
    data = {
        "Time Monitored": now.strftime("%H:%M:%S"),
        "Focused": focused
    }
    # Create a dataframe from the dict
    df = pd.DataFrame(data, index=[0])
    # Create a CSV file to store the dataframe. Appends to EOF if exists.
    df.to_csv(path_to_folder + "/focus.csv", index=False, mode="a", header=False)

