import datetime
import math
import os
import pathlib
import re
import shutil
from tempfile import (  # https://docs.python.org/3/library/tempfile.html
    NamedTemporaryFile,
)
from todotree.Errors.TodoFileNotFound import TodoFileNotFound
from todotree.Errors.DoneFileNotFound import DoneFileNotFound
from todotree.Errors.ProjectFolderError import ProjectFolderError
from todotree.Task import Task
from todotree.Tree import Tree
from todotree.config import Config

# regexes
t_date_pattern = re.compile(r"t:(\d{4})-(\d{2})-(\d{2})")
due_date_pattern = re.compile(r"due:(\d{4})-(\d{2})-(\d{2})")
project_pattern = re.compile(r"\+\S+")
context_pattern = re.compile(r"@\w+")
priority_pattern = re.compile(r"^\([a-zA-Z]\)")

DEBUG = False


def task_to_done(tsk):
    """
    Format the task String to a done state, by adding x 2020-02-02 in front of it.
    :param tsk:
    :return:
    """
    if type(tsk) == Task:  # Flatten to string
        tsk = tsk.raw_string
    done = "x " + str(datetime.date.today()) + " " + tsk
    return done


def task_to_undone(tsk):
    """
    Removes the x 2020-02-02 part so the task can be added to the task file list
    :param tsk:
    :return:
    """
    # 13 is the number of chars of "x 2020-02-02 "
    undone = str.strip(tsk[13:])
    return undone


class Taskmanager:
    """Manages the tasks."""

    task_list: list[Task] = []
    """List Without empty lines"""

    task_full_list: list[Task] = []
    """List With empty lines"""

    config: Config = Config()
    """Configuration settings for the application."""

    placeholder_task: str
    """
    A placeholder task string. This is used when there is a project which does not have a task.
    """

    def __init__(self, configuration: Config = config):
        self.config = configuration
        self.placeholder_task = self.config.emptyProjectString

    # Imports

    def import_tasks(self):
        """
        Import the tasks and projects from files.
        """
        self._import_from_todo_txt()
        if self.config.enable_project_folder:
            self._import_projecttree_folder()

    def _import_from_todo_txt(self):
        """
        Imports the todos from the file to the Taskmanager object.
        :return:
        """
        try:
            with open(self.config.todo_file, 'r') as f:
                content = f.readlines()
                self.task_list = []
                for i, task in enumerate(content):
                    # Skip empty lines.
                    if task.strip() == "":
                        continue
                    self.task_list.append(Task(i + 1, task.strip()))
        except FileNotFoundError as e:
            raise TodoFileNotFound from e

    def filter_t_date(self):
        """
        Removes Tasks from the Taskmanager where the t:date is later than today.
        """
        start_list = self.task_list.copy()  # Iterable copy.
        for task in start_list:
            if task.t_date is None:
                # We cannot compare today to NoneType.
                continue
            if task.t_date > datetime.date.today():
                self.task_list.remove(task)

    def filter_block(self):
        """
        Removes Tasks from the Taskmanager where the task is blocked by some other task.
        """
        # Detect all block items.
        block_list = []
        for task in self.task_list:
            block_list.append(task.blocks)
        # Flatten the list of lists to a normal list.
        block_list_items = [item for sublist in block_list for item in sublist]
        # Blocked / Blocked by filtering
        start_list = self.task_list.copy()
        for task in start_list:
            # Check if there is a task which is blocked by another task.
            intersection = list(filter(lambda x: x in block_list_items, task.blocked))
            if intersection:
                self.task_list.remove(task)

    def _import_projecttree_folder(self):
        """
        Adds the directory TODOTXT_PROJECTTREE_FOLDER to the project trees.
        if TODOTXT_PROJECTTREE_FOLDER is empty, the home folder is used.
        Each folder is considered to be a project.
        Any folder/project which does not have a task called "XX Add Task to this Project" in the projecttree print.
        This is defined by self.emptyProjectString
        :return: Nothing
        """
        try:
            p = pathlib.Path(self.config.project_tree_folder)
            for i in p.glob("*/"):
                proj = os.path.basename(i)
                # Check if there is a task with that project.
                does_project_task_exist = any(proj in ttt.projects for ttt in self.task_list)
                if not does_project_task_exist:
                    # add gibberish task as placeholder.
                    tmp_task = Task(-1, self.placeholder_task)
                    tmp_task.projects = [proj]
                    self.task_list.append(tmp_task)
        except FileNotFoundError as e:
            raise ProjectFolderError(f"An error occurred while processing the projects folder: {e}")

    #  readonly methods.

    def __str__(self):
        self.task_list.sort(key=lambda x: x.priority)
        if self.config.quiet:
            s = ""
        elif self.config.verbose:
            s = self.config.consoleGood + "The todo list is: \n"
        else:
            s = self.config.consoleGood + " Todos\n"

        number_of_digits = int(math.ceil(math.log(len(self.task_list) + 1, 10)))
        for tsk in self.task_list:
            # Number (if applicable).
            s += str(tsk.i).zfill(number_of_digits)
            # Whitespace.
            s += " "
            # Task information self.
            s += str(tsk.stripped_string)
            # new line.
            s += str("\n")
        return s

    def list_done(self):
        """
        List the done.txt with numbers to revive them.
        :return:
        """
        try:
            with open(self.config.done_file, "r") as f:
                lines = f.readlines()
        except FileNotFoundError as e:
            raise DoneFileNotFound from e
        for i, line in reversed(list(enumerate(lines))):
            print(i, line, end="")

    def filter_by_string(self, filter_string):
        """
        Filters the task list by whether `filter_string` occurred in the task.
        """
        self.task_list = [item for item in self.task_list if filter_string in item.raw_string]

    def print_by_due(self):
        """
        Prints the task list sorted by due date, up to max_days_ahead days.
        :return:
        """
        return str((Tree(self.task_list, "due_date_band", config=self.config)))

    def print_project_tree(self) -> str:
        """
        print the projecttree
        :return:
        """
        return str((Tree(self.task_list, "projects", config=self.config)))

    def print_context_tree(self) -> str:
        """
        print the context tree
        :return:
        """
        return str((Tree(self.task_list, "contexts", config=self.config)))

    #  Write Only Methods

    def write_todo_to_file(self):
        """
        Write the results back to a file.
        :return:
        """
        # Write to new file.
        self.task_list.sort(key=lambda x: x.i)
        #  Delete=false is needed for windows, I hope that somebodies temp folder won't be clobbered with this..
        try:
            with NamedTemporaryFile("w+t", newline="", delete=False) as temp_file:
                # may strip new lines by using task list.
                for n in self.task_list:
                    temp_file.write(str(n.raw_string))
                    temp_file.write("\n")
                temp_file.flush()
                shutil.copy(temp_file.name, self.config.todo_file)
        except FileNotFoundError as e:
            raise TodoFileNotFound from e

    def change_t_date(self, date, task_number):
        """
        Adds or changes the t:date
        :param date: The new t:date to add.
        :param task_number: The task number to add the new date to.
        :return: The updated task.
        """
        tsk = self.task_full_list[task_number - 1]
        tsk.change_t_date(date)
        self.write_todo_to_file()
        print(self.config.consoleGood, "Scheduled task: ")
        print(tsk.raw_string)
        return tsk

    def change_priority(self, priority: str, task_number):
        """
        Adds or changes the priority of a task.
        :param priority:
        :param task_number:
        :return:
        """
        tsk = self.task_list[task_number - 1]
        tsk.update_priority(priority)
        self.write_todo_to_file()
        return tsk

    def add_task_to_file(self, tsk: str):
        """
        Adds a task to a file. Returns the task with its assigned number.
        :param tsk:
        :return:
        """
        try:
            with open(self.config.todo_file, 'a') as f:
                f.write(tsk)
        except FileNotFoundError as e:
            raise TodoFileNotFound from e
        # return the line number
        return len(self.task_list) + 1

    def append_to_task(self, task_number: int, task_string: str) -> str:
        """
        Appends :param task_string: to :param task_number:
        It :return: the result.
        """
        self.task_list[task_number - 1].append_to_task_string(task_string)
        self.write_todo_to_file()
        return self.task_list[task_number - 1].raw_string

    def mark_as_done(self, line_numbers):
        """
        Marks the task as done, removes it from the task file and adds it to done.txt
        :param line_numbers:
        :return:
        """
        # Get and remove completed task
        completed_tasks = []
        line_numbers.sort()
        # Delete the tasks from the end to the start.
        line_numbers.reverse()
        for num in line_numbers:
            completed_tasks.append(self.task_list[num - 1])
            del self.task_list[num - 1]
        # Save the new task list.
        self.write_todo_to_file()
        # Convert completed tasks to done tasks.
        done_tasks = map(lambda x: task_to_done(x), completed_tasks)
        # Append the results to done.txt
        try:
            with open(self.config.done_file, "a") as f:
                for completed_task in done_tasks:
                    f.write(completed_task + "\n")
        except FileNotFoundError as e:
            raise DoneFileNotFound from e
        return done_tasks

    def revive_task(self, line_number):
        """
        Gets task from done.txt and adds it to the task file.
        The task does not get removed.
        :param line_number:
        :return:
        """
        # Fetch Task
        try:
            with open(self.config.done_file) as f:
                done_tasks = f.readlines()
        except FileNotFoundError as e:
            raise DoneFileNotFound from e
        tsk = done_tasks[line_number - 1]
        tsk = task_to_undone(tsk)
        # Add task
        self.add_task_to_file(tsk)
        return tsk
