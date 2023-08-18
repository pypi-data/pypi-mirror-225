# using Click implementation
import datetime
import os
import re
import subprocess
from functools import wraps

from pathlib import Path
from typing import List

import click  # CLI magic
from git import Repo

from todotree.Errors.TodoFileNotFound import TodoFileNotFound
from todotree.Errors.DoneFileNotFound import DoneFileNotFound
from todotree.Errors.ConfigFileNotFound import ConfigFileNotFound
from todotree.Taskmanager import Taskmanager, task_to_done
from todotree.config import Config


# Click Replaces:
# Argparse
#
# NOTE: this file cannot be in a class. See: https://github.com/pallets/click/issues/601
# But context and variable ferrying can be done using the context option.
# We just call the context 'self' and hope the issue does resolve itself.
# https://click.palletsprojects.com/en/8.1.x/commands/#nested-handling-and-contexts

def common_options(function):
    """
    Wrapper that defines common functions.

    It should be used as a decorator: `@common_options`

    This function will be needed when we want to support both
    `todotree cd --verbose` and `todotree --verbose cd`
    """
    @wraps(function)
    @click.option('--config-path', default=None, help="Path to the configuration file.")
    @click.option('--todo-file', default=None, help="Path to the todo.txt file, overrides --config.")
    @click.option('--done-file', default=None, help="Path to the done.txt file, overrides --config.")
    @click.option('--verbose', is_flag=True, help="Increases verbosity in messages.", is_eager=True)
    @click.option('--quiet', is_flag=True, help="Do not print messages, only output. Useful in scripts.", is_eager=True)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper


@click.group()
@common_options
@click.pass_context
def root(self: click.Context, config_path: Path, todo_file: Path, done_file: Path, verbose: bool, quiet: bool):
    """todotree main help."""
    # ^ This text also shows up in the help command.
    # Root click group. This manages all the command line interactions.
    # ensure that ctx.obj exists and is a dict
    self.ensure_object(dict)
    initialize(config_path, done_file, quiet, self, todo_file, verbose)
    # Pass to another command.
    pass


def initialize(config_path, done_file, quiet, self, todo_file, verbose):
    # parsing arguments.
    config = Config()
    try:
        if config_path is not None:
            config.read_from_file(config_path)
    except ConfigFileNotFound as e:
        handle_config_file_not_found(e, self, config_path)
    if todo_file is not None:
        config.todo_file = todo_file
    if done_file is not None:
        config.done_file = done_file
    if verbose:
        config.verbose = True
    if quiet:
        config.quiet = True
    # creating variables a la __init__.
    self.obj["config"] = config
    self.obj["task_manager"] = Taskmanager(configuration=config)


def handle_config_file_not_found(e, self, config_path):
    """Handle when a """
    click.echo(self.obj["config"].consoleWarn + " The config.yaml file could not be found.")
    if self.obj["config"].verbose:
        click.echo(f"The config file should be located at {config_path}")
        click.echo(e)
    click.echo("The default options are now used.")


def handle_todo_file_not_found(e, self):
    """Inform the user that the todo.txt was not found."""
    click.echo(f"{self.obj['config'].consoleError} The todo.txt could not be found.")
    click.echo(
        f"{self.obj['config'].consoleError} It searched at the following location: {self.obj['config'].todo_file}")
    if self.obj["config"].verbose:
        click.echo(e)


@root.command('add', short_help='Add a task to the task list')
@click.argument('task', type=str)  # , short_help = 'Task To Add')
@click.pass_context
def add(self, task: str):
    try:
        self.obj["task_manager"].add_task_to_file(task.strip() + "\n")
        commit_exit("add", self.obj["config"])
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)


@root.command('addx', short_help='Add a task and immediately mark it as done')
@click.argument('task', type=str)
@click.pass_context
def add_x(self, task):
    try:
        f = open(self.obj["config"].done_file, "a")
        done = task_to_done(
            task.strip())
        f.write(done)
        click.echo(done)
    except FileNotFoundError as e:
        handle_done_file_not_found(e, self)
        exit(1)


def handle_done_file_not_found(e, self):
    """Inform the user that the done.txt was not found."""
    click.echo(self.obj["config"].consoleError + " The done.txt could not be found.")
    click.echo(
        f"{self.obj['config'].consoleError} It searched at the following location: {self.obj['config'].done_file}")
    if self.obj["config"].verbose:
        click.echo(e)


@root.command('append', short_help='append append_string to task_nr')
@click.argument('task_nr', type=int)
@click.argument('append_string')
@click.pass_context
def append(self, task_nr: int, append_string: str):
    # Disable fancy imports, because they are not needed.
    self.obj['config'].enable_project_folder = False
    # Import tasks.
    try:
        self.obj["task_manager"].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)

    click.echo(self.obj["task_manager"].append_to_task(task_nr, append_string.strip()))
    commit_exit("append", self.obj["config"])


@root.command('context',
              short_help='list task in a tree, by context',
              help='list a tree, of which the first node is the context, the second nodes are the tasks')
@click.pass_context
def context(self):
    try:
        self.obj['task_manager'].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)
    # Print due tree.
    click.echo(self.obj['task_manager'].print_context_tree())
    exit()


@root.command('cd',
              short_help='print directory of the todo.txt directory',
              help='print directory of the todo.txt directory'
              )
@click.pass_context
def cd(self):
    config_path: Path = Path(self.obj['config'].todo_folder)
    if self.obj['config'].verbose:
        click.echo(f"{self.obj['config'].consoleGood} The location to the data folder is: ")

    if config_path.is_absolute():
        # Then the configured path is printed.
        click.echo(str(config_path))
        exit()
    # Then the relative path is resolved to be absolute.
    base_path: Path = Path.home()
    full_path: Path = base_path / config_path
    click.echo(str(full_path))
    exit()


@root.command('do',
              short_help='mark task as done and move it to the done.txt'
              )
@click.argument('task_numbers', type=list)  # type=list[int]
@click.pass_context
def do(self, task_numbers: List[str]):
    # Convert to ints.
    task_numbers = [int(i) for i in task_numbers]
    # Marking something as Done cannot be done with fancy imports
    # So we disable them.
    self.obj['config'].enable_project_folder = False
    try:
        self.obj['task_manager'].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)
    try:
        completed_tasks = self.obj["task_manager"].mark_as_done(task_numbers)
    except DoneFileNotFound as e:
        handle_done_file_not_found(e, self)
        exit(1)
    # Print the results
    click.echo(self.obj['config'].consoleGood + " Tasks marked as done:")
    click.echo(completed_tasks)
    commit_exit("do", self.obj["config"])


@root.command('due',
              short_help='List tasks by their due date'
              )
@click.pass_context
def due(self):
    # Disable fancy imports, because they do not have due dates.
    self.obj['config'].enable_project_folder = False
    # Import tasks.
    try:
        self.obj['task_manager'].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)
    # Print due tree.
    click.echo(self.obj['task_manager'].print_by_due())
    exit()


@root.command('edit',
              short_help='open the todo.txt in $EDITOR (or nano)'
              )
@click.pass_context
def edit(self):
    # Disable fancy imports.
    self.obj['config'].enable_project_folder = False
    program = os.getenv("EDITOR") if os.getenv("EDITOR") else "/usr/bin/nano"
    f = self.obj["config"].todo_file
    click.echo("Editing {} with {}".format(f, program))
    subprocess.run([program, f])
    commit_exit("edit", self.obj["config"])


@root.command('filter',
              short_help='only show tasks containing the search term.'
              )
@click.argument('search_term')
@click.pass_context
def filter_list(self, search_term):
    try:
        self.obj["task_manager"].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)
    self.obj["task_manager"].filter_by_string(search_term)
    click.echo(self.obj["task_manager"])


@root.command('list', short_help='List tasks')
@click.pass_context
def list_tasks(self):
    try:
        self.obj["task_manager"].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)
    click.echo(self.obj["task_manager"])


@root.command('list_done', short_help='List tasks which are marked as done')
@click.pass_context
def list_done(self):
    try:
        self.obj["task_manager"].list_done()
    except DoneFileNotFound as e:
        handle_done_file_not_found(e, self)
        exit(1)


@root.command('print_raw', short_help='print todo.txt without any formatting or filtering')
@click.pass_context
def print_raw(self):
    try:
        with open(self.obj["task_manager"].config.todo_file, "r") as f:
            click.echo(f.read())
    except FileNotFoundError as e:
        handle_todo_file_not_found(e, self)


@root.command('priority', short_help='set new priority to task')
@click.argument('task_number', type=int)
@click.argument('new_priority', type=str)
@click.pass_context
def priority(self, task_number, new_priority):
    # Disable fancy imports.
    self.obj['config'].enable_project_folder = False
    # Run task.
    try:
        self.obj["task_manager"].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)
    self.obj["task_manager"].change_priority(
        priority=(new_priority.upper()), task_number=task_number)


@root.command('project', short_help='print tree by project')
@click.pass_context
def project(self):
    # Import tasks.
    try:
        self.obj["task_manager"].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)
    # Print due tree.
    click.echo(self.obj['task_manager'].print_project_tree())
    exit()


@root.command('revive', short_help='Revive a task that was accidentally marked as done.')
@click.argument('done_number', type=int)
@click.pass_context
def revive(self, done_number):
    try:
        click.echo(self.obj["task_manager"].revive_task(done_number))
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)
    except DoneFileNotFound as e:
        handle_done_file_not_found(e, self)
        exit(1)
    commit_exit("revive", self.obj["config"])


@root.command('schedule', short_help='hide task until date.',
              help='hide the task until the date given. If new_date is not in ISO format (yyyy-mm-dd), '
                   'then it tries to figure out the date with the `date` program, which is only in linux.'
              )
@click.pass_context
@click.argument('task_number', type=int)
@click.argument('new_date', type=str)
def schedule(self, task_number, new_date):
    # Disable fancy imports, because they do not have t dates.
    self.obj['config'].enable_project_folder = False

    date = " ".join(new_date)
    date_pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
    if not date_pattern.match(date):
        # Try to use the `date` utility.
        dat = subprocess.run(
            ["date", "-d " + date, "+%F "],
            capture_output=True,
            encoding="utf-8"
        )
        date = dat.stdout.strip()
    try:
        self.obj["task_manager"].import_tasks()
        self.obj["task_manager"].change_t_date(date, task_number)
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)

    commit_exit("schedule", self.obj["config"])


@root.group()
@click.pass_context
def stale():
    """
    Use the stale system.

    This uses a stale.txt file to store tasks which you want to hide for a long time.
    You will need to manually move them back into todo.txt using this system.
    If you want tasks to disappear for a known time, use the `schedule` command.
    """
    # TODO: Make working again.
    # stale_manager = Taskmanager(
    #    config.consoleGood,
    #    config.consoleWarn,
    #    config.consoleError,
    #    file="stale.txt",
    #    done="todo.txt"
    # )
    # stale_manager.__import_from_todo_txt()


@stale.command('list')
@click.pass_context
def stale_list():
    """
    List tasks in stale.txt
    """
    # print(stalemgr)
    pass


@stale.command('restore')
@click.pass_context
def stale_restore(self, task_numbers):
    """
    move task from stale.txt back to todo.txt
    :param: task_numbers
    """
    # nums = self.check_ints(task_numbers)
    # taskmgr.revive_task(nums, remove_from_done=True)
    # self.commit_exit(action)


@stale.command('prune', short_help='move task from todo.txt to the stale.txt')
@click.pass_context
def stale_prune(self, task_numbers):
    pass  # TODO: implement.
    # nums = self.check_ints(aux)
    # taskmgr.mark_as_done(nums, change_string=False)
    # self.commit_exit(action)


#  End Region Command Definitions.
#  Setup Click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
cli = click.CommandCollection(
    sources=[root],
    context_settings=CONTEXT_SETTINGS
)


#  Setup Main

def commit_exit(action: str, config: Config):
    """
    Commit the files with git before exiting.

    :param config: The configuration parameters.
    :param action: The name of the action, such as list or add.
    """
    if config.git_mode != "Local":
        exit()
    repo = Repo(config.todo_folder)

    # Git add.
    repo.index.add('*')

    # Git commit.
    time = datetime.datetime.now().isoformat()
    repo.index.commit(message=time + action)

    if config.git_mode == "Full":
        # Git push.
        repo.remote().push()


if __name__ == '__main__':
    cli()
