from .base_command import BaseCommand
import os
import shutil
from typing import List

class ChangeDirectoryCommand(BaseCommand):
    def __init__(self, options: List[str], args: List[str]) -> None:
        """
        Initialize the ChangeDirectoryCommand object.

        Args:
            options (List[str]): List of command options.
            args (List[str]): List of command arguments.
        """
        super().__init__(options, args)

        # Override the attributes inherited from BaseCommand
        self.description = 'Change the current working directory'
        self.usage = 'Usage: cd [options] [directory]'

        # TODO 7-1: Initialize any additional attributes you may need.
        # Refer to list_command.py, grep_command.py to implement this.
        self.name = 'cd'
        self.options = options

        self.path = self.current_path
        self.destination_dir = self.args[0] if args else ''

    def execute(self) -> None:
        """
        Execute the cd command.
        Supported options:
            -v: Enable verbose mode (print detailed information)
        
        TODO 7-2: Implement the functionality to change the current working directory.
        You may need to handle exceptions and print relevant error messages.
        """
        verbose = '-v' in self.options

        if verbose:
            print(f"cd: changing directory to '{self.destination_dir}'")

        # Change working directory
        try:
            os.chdir(os.path.join(self.path, self.destination_dir))
            BaseCommand.update_current_path(os.getcwd())
        except FileNotFoundError as e:
            print(f"cd: cannot change directory to '{self.destination_dir}': {e}")
