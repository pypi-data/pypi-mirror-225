from typing import Optional

from pathlib import Path

import xdg_base_dirs as xdg
import yaml

from todotree.Errors import ConfigFileNotFound


class Config:
    """
    The configuration of todotree.
    """
    def __init__(self):
        #  Main variables.
        self.todo_folder: Path = xdg.xdg_data_home() / "todotree"
        """
        Path to the folder containing the data files.
        
        Relative paths are calculated from the HOME folder. 
        """

        self.project_tree_folder: Path = xdg.xdg_data_home() / "todotree" / "projects"
        """
        Path to the folder containing the projects.
        Defaults to the XDG_DATA_DIR/todotree/projects if not set.
        """

        self.todo_file = Path(self.todo_folder) / "todo.txt"
        """
        Path to the todo.txt file.
        """

        self.done_file = Path(self.todo_folder) / "done.txt"
        """
        Path to the done.txt file.
        """

        self.config_file: Optional[Path] = None
        """
        Path to the config file.
        
        Defaults to None if not set.
        """

        self.git_mode = "None"
        """The mode that git runs in. 
        - None: disables it,
        - Local: add and commits automatically,
        - Full: also pulls and pushes to a remote repo.
        """

        # Features - Enables or disables certain features.
        self.quiet = False
        """A value indicating whether to print anything except the output. Useful in scripts."""

        self.verbose = False
        """A value indicating whether to print more detailed messages."""

        self.enable_wishlist_folder = True
        """A value indicating whether to enable the wishlist folder functionality."""

        self.enable_project_folder = True
        """A value indicating whether to enable the project folder functionality."""

        #  Localization. #
        self.wishlistName = "wishlist"
        self.noProjectString = "No Project"
        self.noContextString = "No Context"
        self.emptyProjectString = "> (A) Todo: add next todo for this."

        #  Status Decorators.
        self.enable_colors: bool = True
        self.consoleGood: str = ' * '
        self.consoleWarn: str = ' ! '
        self.consoleError: str = '!!!'

        # Tree prints.
        self.t_print: str = " ├──"
        self.l_print: str = " │  "
        self.s_print: str = " └──"
        self.e_print: str = "    "

    def read(self, path: Optional[Path] = None):
        """
        Loads the configuration from the given file.

        If empty, reads from default locations.
        """
        if path is not None:
            self.read_from_file(path)
            return
        # xdg compliant directory.
        if Path(xdg.xdg_config_home() / "todotree" / "config.yaml").exists():
            self.read_from_file(Path(xdg.xdg_config_home() / "todotree" / "config.yaml"))
            return
        # xdg compliant directory if config file is considered "data".
        if Path(xdg.xdg_data_home() / "todotree" / "config.yaml").exists():
            self.read_from_file(Path(xdg.xdg_data_home() / "todotree" / "config.yaml"))
            return
        # No paths: use the defaults.
        return

    def read_from_file(self, file: Path):
        """Reads and parses yaml content from `file`."""
        self.config_file = file
        try:
            with open(file, 'r') as f:
                self.read_from_yaml(f.read())
        except FileNotFoundError as e:
            raise ConfigFileNotFound from e

    def read_from_yaml(self, yaml_content: str):
        """Reads and overrides config settings defined in `yaml_content`."""
        # Convert yaml to python object.
        yaml_object = yaml.safe_load(yaml_content)
        if yaml_object is None:
            return
        # Map each item to the self config.
        try:
            if yaml_object['main'] is not None:
                self.enable_wishlist_folder = yaml_object['main'].get('enable_wishlist_folder', self.enable_wishlist_folder)
                self.enable_project_folder = yaml_object['main'].get('enable_project_folder', self.enable_project_folder)
                self.git_mode = yaml_object['main'].get("git_mode", self.git_mode)
                self.quiet = yaml_object['main'].get("quiet", self.quiet)
                self.verbose = yaml_object['main'].get("verbose", self.verbose)
        except KeyError:
            # Then the section did not exist.
            pass
        try:
            if yaml_object['paths'] is not None:

                self.todo_folder = Path(yaml_object['paths'].get('folder', self.todo_folder)).expanduser()
                self.todo_file = Path(yaml_object['paths'].get('todo_file', Path(self.todo_folder) / "todo.txt")).expanduser()
                self.done_file = Path(yaml_object['paths'].get('done_file', Path(self.todo_folder) / "done.txt")).expanduser()
                self.project_tree_folder = Path(yaml_object['paths'].get('project_folder', self.project_tree_folder)).expanduser()
        except KeyError:
            # Then the section did not exist.
            pass
        try:
            if yaml_object['localization'] is not None:
                self.emptyProjectString = yaml_object['localization'].get('empty_project', self.emptyProjectString)
                self.wishlistName = yaml_object['localization'].get('wishlist_name', self.wishlistName)
                self.noProjectString = yaml_object['localization'].get('no_project', self.noProjectString)
                self.noContextString = yaml_object['localization'].get('no_context', self.noContextString)
        except KeyError:
            # Then the section did not exist.
            pass
        try:
            if yaml_object['decorators'] is not None:
                self.enable_colors = yaml_object['decorators'].get('enable_colors', self.enable_colors)
                self.consoleGood = yaml_object['decorators'].get('info', self.consoleGood)
                self.consoleWarn = yaml_object['decorators'].get('warning', self.consoleWarn)
                self.consoleError = yaml_object['decorators'].get('error', self.consoleError)
        except KeyError:
            # Then the section did not exist.
            pass
        try:
            if yaml_object['tree'] is not None:
                self.t_print = yaml_object['tree'].get('t', self.t_print)
                self.l_print = yaml_object['tree'].get('l', self.l_print)
                self.s_print = yaml_object['tree'].get('s', self.s_print)
                self.e_print = yaml_object['tree'].get('e', self.e_print)
        except KeyError:
            # Then the section did not exist.
            pass
