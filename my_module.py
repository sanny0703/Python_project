import json
from datetime import datetime, timedelta


# Decorators

def log_action(func):
    """Decorator to log actions performed on tasks."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Action performed: {func.__name__}, Result: {result}")
        return result
    return wrapper


def validate_task(func):
    """Decorator to validate task input."""
    def wrapper(self, *args, **kwargs):
        if not args or not isinstance(args[0], str) or not args[0].strip():
            raise ValueError("Task name must be a non-empty string.")
        return func(self, *args, **kwargs)
    return wrapper


# Classes
class Task:
    PRIORITY_LEVELS = {"low": 1, "medium": 2, "high": 3}

    def __init__(
        self, name, priority="medium", due_date=None, category=None, dependencies=None, completed=False
    ):
        self.name = name
        self.completed = completed
        self.priority = priority
        self.due_date = due_date if due_date else datetime.now().strftime("%Y-%m-%d")
        self.category = category
        self.dependencies = dependencies if dependencies else []

    @log_action
    @validate_task
    def mark_completed(self):
        """Mark the task as completed."""
        self.completed = True
        return f"Task '{self.name}' marked as completed."

    def is_overdue(self):
        """Check if the task is overdue."""
        return (
            datetime.strptime(self.due_date, "%Y-%m-%d") < datetime.now()
            and not self.completed
        )

    def __str__(self):
        """Return a user-friendly string representation of the task."""
        return f"Task: {self.name} | Completed: {'Yes' if self.completed else 'No'} | Priority: {self.priority} | Due: {self.due_date} | Category: {self.category} | Dependencies: {', '.join(self.dependencies) if self.dependencies else 'None'}"

    def __lt__(self, other):
        """Less than comparison based on priority and due date."""

        if self.PRIORITY_LEVELS[self.priority] == self.PRIORITY_LEVELS[other.priority]:
            return self.due_date < other.due_date
        return (
            self.PRIORITY_LEVELS[self.priority] < self.PRIORITY_LEVELS[other.priority]
        )

    @log_action
    def __add__(self, other):
        """Combine dependencies of two tasks."""
        if isinstance(other, Task):
            combined_dependencies = list(
                set(self.dependencies) | set(other.dependencies))
            return Task(name=f"{self.name} & {other.name}", dependencies=combined_dependencies)
        return NotImplemented

    def __call__(self):
        """Allow the task to be called to get its name."""
        return self.name

    def __repr__(self):
        """Return an unambiguous string representation of the task."""
        return f"Task(name={self.name!r}, priority={self.priority!r}, due_date={self.due_date!r}, completed={self.completed!r})"
    
    def __iter__(self):
        """Return an iterator over the dependencies."""
        self._iter_index = 0  # Initialize the index for iteration
        return self
    
    def __next__(self):
        if self._iter_index < len(self.dependencies):
            dependency = self.dependencies[self._iter_index]
            self._iter_index += 1
            return dependency

        else:
            raise StopIteration # Signal that the iteration is complete
        
    @staticmethod
    def get_priority_levels():
        """Return the available priority levels."""
        return Task.PRIORITY_LEVELS    


class TaskManager:

    def __init__(self):
        self.tasks = []

    @log_action
    def add_task(self, name, priority="medium", due_date=None, category=None, dependencies=None):
        task = Task(name, priority, due_date, category, dependencies)
        self.tasks.append(task)
        self.tasks.sort()  # Sort tasks by priority and due date
        return f"Task '{name}' added."

    @log_action
    def remove_task(self, name):
        for task in self.tasks:
            if task.name == name:
                self.tasks.remove(task)
                return f"Task '{name}' removed."
        return f"Task '{name}' not found."
    
    @log_action
    def mark_task_complete(self, name):
        for task in self.tasks:
            if task.name == name:
                task.completed = True
                return f"Task '{name}' marked complete."
        return f"Task '{name}' not found."

    @log_action
    def list_tasks(self, filter_category=None):
        """List all tasks, sorted by priority and due date."""
        tasks_to_display = self.tasks
        if filter_category:
            tasks_to_display = [
                task for task in self.tasks if task.category == filter_category]
        overdue_tasks = [
            task for task in tasks_to_display if task.is_overdue()]
        if overdue_tasks:
            print("\nOverdue Tasks:")
            for task in overdue_tasks:
                print(task)
        return sorted(tasks_to_display)

    @log_action
    def save_tasks(self, filename='tasks.json'):
        """Save tasks to a JSON file."""
        with open(filename, 'w') as f:

            json.dump([task.__dict__ for task in self.tasks], f)

    @log_action
    def load_tasks(self, filename='tasks.json'):
        """Load tasks from a JSON file."""
        try:
            with open(filename, 'r') as f:
                tasks_data = json.load(f)
                self.tasks = [Task(**task) for task in tasks_data]
        except FileNotFoundError:
            print("No saved tasks found.")

    @log_action
    def search_tasks(self, keyword):
        """Search for tasks containing the keyword."""
        return [task for task in self.tasks if keyword.lower() in task.name.lower()]
    
    @log_action
    def sort_tasks(self, key=lambda task: task.priority):
        """
        Sorts the tasks based on a given key function.
        :param key: A lambda function that defines the sorting criteria (default is by priority).
        """
        self.tasks.sort(key=key)

    @log_action
    def filter_tasks(self, condition=lambda task: not task.completed):
        """
        Filters tasks based on a given condition.
        :param condition: A lambda function that defines the filtering criteria (default is to find incomplete tasks).
        :return: A list of tasks that meet the condition.
        """
        return list(filter(condition, self.tasks))
    
    @classmethod
    @log_action
    def create_task(cls, name, priority="medium", due_date=None, category=None, dependencies=None):
        """Class method to create a new task."""
        return Task(name, priority, due_date, category, dependencies)


    @classmethod
    def get_all_tasks(cls, task_manager):
        """Class method to get all tasks from a TaskManager instance."""
        return task_manager.tasks
    



