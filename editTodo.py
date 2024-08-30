import pandas as pd
import json
from datetime import datetime
import os
import inquirer

path_to_folder = "results"

def addTodo(todoItem):
    # Get the current time
    now = datetime.now()
    data = {
        "Todo Item": todoItem,
        "Date Added": now.strftime("%m/%d/%Y"),
        "Time Added": now.strftime("%H:%M:%S"),
    }

    # Write to CSV file
    csv_file_path = f"{path_to_folder}/todo.csv"
    df = pd.DataFrame([data])

    # Append to CSV if it exists, otherwise create it
    if os.path.exists(csv_file_path):
        df.to_csv(csv_file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_file_path, index=False)

    print(f"Added '{todoItem}' to your to-do list.")

def delTodo():
    # Load the CSV file
    df = pd.read_csv(f"{path_to_folder}/todo.csv")
    
    # If the CSV is empty, there's nothing to delete
    if df.empty:
        print("The to-do list is empty.")
        return

    # Display the list of items to the user for selection
    questions = [
        inquirer.List(
            "todo_item",
            message="Which to-do item do you want to delete?",
            choices=df["Todo Item"].tolist()
        )
    ]
    
    selected_item = inquirer.prompt(questions)["todo_item"]

    # Filter out the selected item
    df = df[df["Todo Item"] != selected_item]
    
    # Save the updated DataFrame back to the CSV file
    df.to_csv(f"{path_to_folder}/todo.csv", index=False)
    
    print(f"Removed '{selected_item}' from your to-do list.")