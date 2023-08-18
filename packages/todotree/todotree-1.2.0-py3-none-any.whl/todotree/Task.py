import re
from datetime import datetime, date, timedelta

from typing import List, Optional

from todotree.Errors.TaskParseError import TaskParseError

t_date_pattern = re.compile(r"t:(\d{4})-(\d{2})-(\d{2})")
project_pattern = re.compile(r"\+\S+")
context_pattern = re.compile(r"@\w+")
priority_pattern = re.compile(r"^\([a-zA-Z]\)")
# due dates
# format due:yyyy-mm-dd (once)
due_date_pattern = re.compile(r"due:(\d{4})-(\d{2})-(\d{2})")
# format duy:mm-dd (yearly)
due_month_pattern = re.compile(r"duy:(\d{2})-(\d{2})")
# format dum:dd (monthly)
due_day_pattern = re.compile(r"dum:(\d{2})")

# block / blocked by
# both b:string and by:string need to be in the task list for the task containing by:string to be filtered out.
block_pattern = re.compile(r"(bl:)(\w+)")  # format: bl:string
blocked_by_pattern = re.compile(r"(by:)(\w+)")  # format: by:string


class Task:
    """
    Instantiation of a single task.
    """

    t_date_all = []
    """All t dates of a task."""

    due_date_all = []
    """All due dates of a task"""

    raw_string = ""
    """raw un formatted string"""

    i = 0
    """Task Number"""

    priority = 684
    """Priority as an integer"""

    priority_string = ""
    """priority as a String."""

    projects: List[str] = []
    """List of all projects"""

    contexts: List[str] = []
    """List of all contexts"""

    write_string = ""
    """string to write to the file. (A) bla bla bla t:yyyy-mm-dd"""

    stripped_string = ""
    """String for printing by removing stuff"""

    blocks: List[str] = []
    """List of all block identifiers."""

    blocked: List[str] = []
    """List of all blocked by identifiers"""

    @property
    def t_date(self) -> Optional[date]:
        """Latest t date."""
        return max(self.t_date_all) if len(self.t_date_all) > 0 else None
    # FUTURE: t_date Setter.

    @property
    def due_date(self) -> Optional[date]:
        """Earliest due date."""
        return min(self.due_date_all) if len(self.due_date_all) > 0 else None
    # FUTURE: due_date setter. https://mathspp.com/blog/pydonts/properties

    @property
    def due_date_band(self) -> str:
        """
        Returns the time until the due date lapses in human-readable language.
        """
        if self.due_date is None:
            return "No due date."
        # List with options.
        difference = self.due_date - datetime.today().date()
        if difference < timedelta(days=0):
            return "Overdue"
        if difference < timedelta(days=1):
            return "Due today"
        if difference < timedelta(days=2):
            return "Due tomorrow"
        if difference < timedelta(days=7):
            return "Due in the next 7 days"
        return "Due date further than the next 7 days"

    def __init__(self, i: int, task_string: str):
        # Reset values to a default state.
        self.due_date_all = []
        self.t_date_all = []
        self.stripped_string = None
        self.projects = []
        self.contexts = []
        self.blocked = []
        self.blocks = []
        self.i = i
        # Parse the various properties from the task.
        if task_string:  # task is not empty
            self.raw_string = task_string.strip()  # Remove whitespace and the \n.
            self.write_string = task_string
            self.stripped_string = task_string  # Start with full string.

            # Parse the various items.
            self.__parse_priority(task_string)

            self.__parse_project(task_string)
            self.__parse_context(task_string)
            self.__parse_t_date(task_string)
            self.__parse_due_date(task_string)
            self.__parse_due_month(task_string)
            self.__parse_due_day(task_string)
            self.__parse_block_list(task_string)
            self.__parse_blocked_by_list(task_string)

            # Set some print string.
            self.stripped_string = self.strip_t_date()

    def __parse_priority(self, task_string):
        """
        Parse the priority from the `task_string`.
        """
        if priority_pattern.match(task_string):
            with_parentheses = priority_pattern.match(task_string).group(0)
            self.priority_string = with_parentheses[1]
            self.priority = ord(self.priority_string.upper()) - 65
            priority_pattern.sub("", self.stripped_string)

    def __parse_project(self, task_string):
        """
        Parse the projects from the `task_string`.
        """
        if project_pattern.search(task_string):
            projects_with_plus = project_pattern.findall(task_string)
            for p in projects_with_plus:
                self.projects.append(re.sub(r"\+", "", p))

    def __parse_context(self, task_string):
        """
        Parse the contexts from the `task_string`.
        """
        if context_pattern.search(task_string):
            context_with_at = context_pattern.findall(task_string)
            for c in context_with_at:
                self.contexts.append(re.sub(r"@", "", c))

    def __parse_t_date(self, task_string):
        """
        Parse the t_dates from the `task_string`.
        """
        for year, month, day in t_date_pattern.findall(task_string):
            try:
                # Add t:date to the t date list.
                self.t_date_all.append(datetime(int(year), int(month), int(day)).date())
            except ValueError:
                raise TaskParseError(f"This task has an incorrect t:date.{year}-{month}-{day}")

    def __parse_due_date(self, task_string):
        """
        Parse the due date from the `task_string`.
        """
        for year, month, day in due_date_pattern.findall(task_string):
            try:
                self.due_date_all.append(datetime(int(year), int(month), int(day)).date())
            except ValueError:
                raise TaskParseError(f"This task has an incorrect due:date. date: {year}-{month}-{day}")

    def __parse_due_month(self, task_string):
        """
        Parse the dum date from the `task_string`.
        """
        for month, day in due_month_pattern.findall(task_string):
            try:
                self.due_date_all.append(datetime(datetime.today().year, int(month), int(day)).date())
            except ValueError:
                raise TaskParseError(f"This task has an incorrect dum:date. date: {month} {day}")

    def __parse_due_day(self, task_string):
        """
        Parses the duy date from `task_string`.
        """
        for day in due_day_pattern.findall(task_string):
            try:
                self.due_date_all.append(datetime(datetime.today().year, datetime.today().month, int(day)).date())
            except ValueError:
                raise TaskParseError(f"This task has an incorrect duy:date.")

    def __parse_blocked_by_list(self, task_string):
        """
        Parse the blocked by list.
        """
        for blocked_item in blocked_by_pattern.finditer(task_string):
            self.blocked.append(str(blocked_item.group(2)))

    def __parse_block_list(self, task_string):
        """
        Parse the block list.
        """
        for item in block_pattern.finditer(task_string):
            self.blocks.append(str(item.group(2)))

    # Reader methods.

    # Final Filters

    def stripped_for_due(self):
        """
        Strips the string for task manager due dates.
        :return: the string without the due dates.
        """
        self.strip_t_date()
        self.strip_due_date()
        return re.sub(r"\s+", " ", self.stripped_string)  # Remove whitespace.

    def stripped_for_project_tree(self):
        """
        Strips the string for task_manager.project_tree
        :return: a string useful for printing the project tree.
        """
        self.strip_t_date()
        self.strip_project_string()
        return re.sub(r"\s+", " ", self.stripped_string)  # Remove whitespace.

    def stripped_for_context_tree(self):
        """
        Strips the string for task_manager.context_tree
        :return: A string useful for printing the context tree.
        """
        self.strip_t_date()
        self.strip_context()
        return re.sub(r"\s+", " ", self.stripped_string)  # Remove whitespace.

    # Filter Building blocks

    def strip_t_date(self):
        """
        Removes t:xxxx-xx-xx entries from stripped_string.
        :return: the task string without t dates.
        """
        # FIXME: It leaves an extra space when removing. Please fix.
        stripped = self.stripped_string if self.stripped_string else self.raw_string
        stripped = t_date_pattern.sub("", stripped)
        self.stripped_string = stripped
        return stripped

    def strip_due_date(self):
        """
        Removes due:xxxx-xx-xx from stripped_string.
        :return: the task string without due dates.
        """
        stripped = self.stripped_string if self.stripped_string else self.raw_string
        stripped = due_date_pattern.sub(" ", stripped)
        stripped = due_month_pattern.sub(" ", stripped)
        stripped = due_day_pattern.sub(" ", stripped)
        self.stripped_string = stripped
        return stripped

    def strip_context(self):
        """
        Removes @context entries from stripped_string.
        :return: the task string without contexts.
        """
        stripped = self.stripped_string if self.stripped_string else self.raw_string
        stripped = context_pattern.sub(" ", stripped)
        self.stripped_string = stripped
        return stripped

    def strip_project_string(self):
        """
        Removes +project entries from stripped_string.
        :return: the task string without projects.
        """
        stripped = self.stripped_string if self.stripped_string else self.raw_string
        stripped = project_pattern.sub(" ", stripped)
        self.stripped_string = stripped
        return stripped

    def update_priority(self, new_priority: str) -> bool:
        """
        Adds or updates the priority.
        :param new_priority: the new priority
        :return: A value indicating whether it was added or updated.
        True means it was added. False that it was updated.
        """
        if self.priority < 600:
            self.raw_string = priority_pattern.sub("(" + new_priority + ")", self.raw_string)
        else:  # There was no priority.
            self.raw_string = "(" + new_priority + ") " + self.raw_string
        old_priority = self.priority
        self.priority = ord(new_priority.upper()) - 65
        return old_priority < 600

    def change_due(self, new_due: datetime) -> bool:
        """
        Updates the due date, or adds it if it does not exist.
        :param new_due:
        :return: True if it was added. False if the due date is updated.
        """
        is_added = False
        if self.due_date < datetime(9999, 12, 31).date():
            # There already are due dates, check if this is the closest to now.
            self.raw_string = due_date_pattern.sub(
                "due:" + new_due.strftime("%Y-%m-%d"), self.raw_string
            )
        else:
            # There was no due_date, substitute the default.
            self.raw_string += " due:" + new_due.strftime("%Y-%m-%d")
            is_added = True
        return is_added

    def append_to_task_string(self, added: str):
        """
        Appends to the task string. Unused.
        :param added: the string to append to this task.
        :return:
        """
        self.raw_string += " "
        self.raw_string += added.strip()
        self.stripped_string = self.strip_t_date().strip()

    def change_t_date(self, new_t_date: datetime):
        """
        Adds or updates the t:date
        :param new_t_date:
        :return:
        """
        if self.t_date > datetime(1, 1, 1).date():
            self.raw_string = t_date_pattern.sub("t:" + str(new_t_date), self.raw_string)
        else:
            self.raw_string += " t:" + str(new_t_date)

    def task_with_number(self):
        """
        Returns Task with its number.
        Hides the number if it is less or equal to zero.
        :return:
        """
        prefix = self.i if self.i > 0 else ""
        task = self.stripped_string if self.stripped_string is not None else ""  # TODO: Remove this line.
        return str(prefix) + " " + task

    def __str__(self):
        return self.task_with_number()
