import pandas as pd # For writing to CSV
import json
from datetime import datetime # Provides Timestamp for when item was added to the list.

path_to_folder = "results"

def addTodo(todoItem):
    # Get the current time
    now = datetime.now()
    data = {
        "Date Added": now.strftime("%m/%d/%Y"),
        "Time Added": now.strftime("%H:%M:%S"),
        "Todo Item": todoItem
    }
    

    print("Added " + todoItem + " to your todo list.")

def delTodo():
    #Remove Row with selected entry. Utilize inquirer to select which row to delete.
    df = pd.read_csv(path_to_folder + "/todo.csv")
    