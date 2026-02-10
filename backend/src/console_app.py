"""
Placeholder console application for Phase I of the Todo application.
This would be replaced with a full implementation for the in-memory console app.
"""

def main():
    print("Todo Application - Console Mode")
    print("This is a placeholder for the in-memory console application.")
    print("Commands available: create, list, complete, delete, exit")

    while True:
        command = input("\nEnter command: ").strip()

        if command.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        elif command.startswith('create '):
            task = command[7:]  # Remove 'create ' prefix
            print(f"Creating task: {task}")
        elif command == 'list':
            print("Listing tasks...")
            # In a real implementation, this would show tasks
        elif command.startswith('complete '):
            task_id = command[9:]  # Remove 'complete ' prefix
            print(f"Completing task with ID: {task_id}")
        elif command.startswith('delete '):
            task_id = command[7:]  # Remove 'delete ' prefix
            print(f"Deleting task with ID: {task_id}")
        else:
            print("Unknown command. Available commands: create, list, complete, delete, exit")


if __name__ == "__main__":
    main()