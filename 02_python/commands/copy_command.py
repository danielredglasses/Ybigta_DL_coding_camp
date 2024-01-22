from .base_command import BaseCommand
import os
import shutil
from typing import List

class CopyCommand(BaseCommand):
    def __init__(self, options: List[str], args: List[str]) -> None:
        """
        Initialize the CopyCommand object.

        Args:
            options (List[str]): List of command options.
            args (List[str]): List of command arguments.
        """
        super().__init__(options, args)

        # Override the attributes inherited from BaseCommand
        self.description = 'Copy a file or directory to another location'
        self.usage = 'Usage: cp [source] [destination]'

        # TODO 6-1: Initialize any additional attributes you may need.
        # Refer to list_command.py, grep_command.py to implement this.
        self.name = 'cp'
        self.options = options

        self.path = self.current_path
        self.source_dir = self.args[0] if args else ''
        self.destination_dir = self.args[1] if len(args) > 1 else ''

        if '/' in self.source_dir:
            self.file_name = self.source_dir.split('/')[-1]
        else:
            self.file_name = self.source_dir

    def execute(self) -> None:
        """
        Execute the copy command.
        Supported options:
            -i: Prompt the user before overwriting an existing file.
            -v: Enable verbose mode (print detailed information)
        
        TODO 6-2: Implement the functionality to copy a file or directory to another location.
        You may need to handle exceptions and print relevant error messages.
        You may use the file_exists() method to check if the destination file already exists.
        """
        prompt_overwrite = '-i' in self.options
        verbose = '-v' in self.options

        if verbose:
            print(f"cp: copying '{self.source_dir}' to '{self.destination_dir}'")

        # Check if source_dir is valid
        if not os.path.exists(self.source_dir):
            raise FileNotFoundError(f"mv: {self.source_dir}: No such file or directory")
        if not os.path.exists(self.destination_dir):
            raise FileNotFoundError(f"mv: {self.destination_dir}: No such file or directory")
        
        # Copy file
        if self.file_exists(self.destination_dir, self.file_name):
            target_path = os.path.join(self.destination_dir, self.file_name)
            if prompt_overwrite:
                overwrite = input(f"cp: overwrite '{target_path}'? (y/n)")
                while True:
                    if overwrite == 'y' or overwrite == 'n':
                        break
                    else:
                        print('Enter y or n')
                        overwrite = input(f"cp: overwrite '{target_path}'? (y/n)")

                if overwrite == 'y':
                    os.remove(os.path.join(self.path, target_path))
                    shutil.copyfile(os.path.join(self.path, self.source_dir), os.path.join(self.path, self.destination_dir, self.file_name))
            else:
                os.remove(os.path.join(self.path, target_path))
                shutil.copyfile(os.path.join(self.path, self.source_dir), os.path.join(self.path, self.destination_dir, self.file_name))
        else:
            shutil.copyfile(os.path.join(self.path, self.source_dir), os.path.join(self.path, self.destination_dir, self.file_name))

    def file_exists(self, directory: str, file_name: str) -> bool:
        """
        Check if a file exists in a directory.
        Feel free to use this method in your execute() method.

        Args:
            directory (str): The directory to check.
            file_name (str): The name of the file.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        file_path = os.path.join(directory, file_name)
        return os.path.exists(file_path)