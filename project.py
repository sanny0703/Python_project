
from my_module import TaskManager



def main():
    manager = TaskManager()
    manager.load_tasks()  # Load tasks from a file at startup

    print("Welcome to the Task Management System!")
    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. List Tasks")
        print("4. Search Tasks")
        print("5. Save Tasks")
        print("6. Mark Complete")
        print("7. Exit")

        choice = input("Select an option (1-7): ")
        handle_choice(choice, manager)


def handle_choice(choice, manager):
    if choice == '1':
        add_task(manager)
    elif choice == '2':
        remove_task(manager)
    elif choice == '3':
        list_tasks(manager)
    elif choice == '4':
        search_tasks(manager)
    elif choice == '5':
        save_tasks(manager)
    elif choice == '6':
        mark_complete(manager)
    elif choice == '7':
        exit_program(manager)
    else:
        print("Invalid choice. Please select a valid option.")


def add_task(manager):
    name = input("Enter task name: ")
    priority = input("Enter priority (low, medium, high): ").lower()
    due_date = input("Enter due date (YYYY-MM-DD) or leave blank for today: ")
    category = input("Enter category (optional): ")
    dependencies = input("Enter dependencies (comma-separated task names, optional): ").split(',')
    dependencies = [dep.strip() for dep in dependencies if dep.strip()]  # Clean up dependencies
    print(manager.add_task(name, priority, due_date if due_date else None, category, dependencies))


def remove_task(manager):
    name = input("Enter task name to remove: ")
    print(manager.remove_task(name))


def list_tasks(manager):
    filter_category = input("Enter category to filter (or leave blank for all): ")
    tasks = manager.list_tasks(filter_category if filter_category else None)
    print("\nCurrent Tasks:")
    
    for task in tasks:
        print(task)  # Uses __str__()


def search_tasks(manager):
    keyword = input("Enter keyword to search for: ")
    found_tasks = manager.search_tasks(keyword)
    
    if found_tasks:
        print("\nSearch Results:")
        for task in found_tasks:
            print(task)
    else:
        print("No tasks found with that keyword.")


def save_tasks(manager):
    manager.save_tasks()
    print("Tasks saved successfully.")


def mark_complete(manager):
    name = input("Enter task name to mark completed: ")
    print(manager.mark_task_complete(name))


def exit_program(manager):
    manager.save_tasks()  # Save tasks before exiting
    print("Exiting the program.")
    exit()


if __name__ == "__main__":
    main()
