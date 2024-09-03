import os
import pandas as pd
from retrieveFocus import getFocused

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

