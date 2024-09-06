from focus import storeFocus, processFocus
from time import sleep
import editTodo
import inquirer
import startVisualize
#.\env\Scripts\activate

def main():
    print("Welcome to Time Manager." + "\n" + "Press Ctrl+C to exit.")
    #CLI Based At the moment.
    #questions: A question list for what the user wants to do.
    questions = [
        inquirer.List("Activity", message="What would you like to do?", choices=['Track Usage', 'Work Session', 'Add Todo', 'Visualize', 'Exit'])
    ]
    selection_choice = inquirer.prompt(questions)
    while selection_choice["Activity"] != "Exit":
        if selection_choice["Activity"] == "Track Usage":
            print("Tracking Usage...")
            while True:
                try:
                    storeFocus()
                    sleep(1) # Wait 5 seconds before next iteration.
                except KeyboardInterrupt:
                    print("Tracking stopped. Processing data")
                    processFocus()
                    #Put in estimated time? Figure that out
                    break
        elif selection_choice["Activity"] == "Work Session":
            print("Starting Work Session...")
        elif selection_choice["Activity"] == "Add Todo":
            print("Adding Todo...")
            editTodo.addTodo(input("What would you like to add to your todo list? "))
        elif selection_choice["Activity"] == "Visualize":
            print("Starting Visualization Session...")
            startVisualize.start()
        selection_choice = inquirer.prompt(questions)


main()