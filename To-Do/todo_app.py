import tkinter as tk
from tkinter import ttk, messagebox


# Class representing a single task
class Task:

    def __init__(self, description):
        self.description = description
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        return f"[{'✓' if self.completed else '✗'}] {self.description}"


# Class for managing multiple tasks
class TaskManager:

    def __init__(self):
        self.tasks = []

    def add_task(self, description):
        if description:  # Validate description
            self.tasks.append(Task(description))

    def view_tasks(self):
        return [str(task) for task in self.tasks]

    def mark_task_completed(self, task_id):
        if 0 < task_id <= len(self.tasks):
            self.tasks[task_id - 1].mark_completed()

    def delete_task(self, task_id):
        if 0 < task_id <= len(self.tasks):
            del self.tasks[task_id - 1]

    def save_tasks_to_file(self, filename='tasks.txt'):
        with open(filename, 'w') as file:
            for task in self.tasks:
                file.write(f"{task.description},{'1' if task.completed else '0'}\n")
        print("Tasks saved to file.")

    def load_tasks_from_file(self, filename='tasks.txt'):
        self.tasks = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    description, status = line.strip().split(',')
                    task = Task(description)
                    task.completed = (status == "1")
                    self.tasks.append(task)
            print("Tasks loaded from file.")
        except FileNotFoundError:
            print("File not found. No tasks loaded.")


# Class for the GUI of the task manager
class TaskManagerUI:

    def __init__(self, root):
        self.task_manager = TaskManager()
        self.task_manager.load_tasks_from_file()
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("400x500")
        self.create_widgets()
        self.update_task_listbox()

    # Create the widgets for the GUI
    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=6)
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TEntry", font=("Helvetica", 12), padding=6)
        style.configure("TListbox", font=("Helvetica", 12))
        
        # Set the style for Accent button
        style.configure("Accent.TButton", background="#4CAF50", foreground="#000000", padding=6)
        
        # Frame for the task list and scrollbar
        list_frame = ttk.Frame(self.root, padding="10 10 10 10")
        list_frame.pack(pady=20)

        self.task_listbox = tk.Listbox(list_frame, width=50, height=15, font=("Helvetica", 12))
        self.task_listbox.pack(side=tk.LEFT)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # Entry field for new tasks
        self.entry = ttk.Entry(self.root, width=50, font=("Helvetica", 12))
        self.entry.pack(pady=10)

        # Frame for buttons
        button_frame = ttk.Frame(self.root, padding="10 10 10 10")
        button_frame.pack(pady=10)

        # List of buttons and their associated actions
        buttons = [
            ("Add Task", self.add_task),
            ("Mark Completed", self.mark_task_completed),
            ("Delete Task", self.delete_task),
            ("Save & Exit", self.save_and_exit),
        ]

        for text, command in buttons:
            ttk.Button(button_frame, text=text, command=command, style="Accent.TButton").pack(side=tk.LEFT, padx=5)

    # Add a task to the task manager
    def add_task(self):
        description = self.entry.get()
        if description:
            self.task_manager.add_task(description)
            self.entry.delete(0, tk.END)
            self.update_task_listbox()
        else:
            messagebox.showwarning("Input Error", "Please enter a task description.")

    # Mark the selected task as completed
    def mark_task_completed(self):
        try:
            task_id = self.task_listbox.curselection()[0] + 1
            self.task_manager.mark_task_completed(task_id)
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    # Delete the selected task
    def delete_task(self):
        try:
            task_id = self.task_listbox.curselection()[0] + 1
            self.task_manager.delete_task(task_id)
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    # Save tasks to a file and exit the application
    def save_and_exit(self):
        self.task_manager.save_tasks_to_file()
        self.root.quit()

    # Update the listbox to reflect the current tasks
    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.view_tasks():
            self.task_listbox.insert(tk.END, task)
            if "✓" in task:
                self.task_listbox.itemconfig(tk.END, {'bg':'#e6ffee'})  # Very light green for completed tasks
            else:
                self.task_listbox.itemconfig(tk.END, {'bg':'#ffe6e6'})  # Very light red for pending tasks


if __name__ == "__main__":
    root = tk.Tk()
    TaskManagerUI(root)
    root.mainloop()
