##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi


class Program:
    """A class for obtaining the program associated with a workload."""

    def __init__(self, name: str, run_num: str, program: str):
        """Constructor for Program object and associated program file.

        Args:
            name (str): The name that will be used to create the program file.
            run_num (str): The run number associated with the program.
            program (str): The program itself.
        """
        self._name = name
        self._run_num = run_num
        self._program = program

    def download(self, path: str = None):
        """Download the program and store it as file with the given path.

        Args:
            path (str, optional): The path where the program file should be stored. If not provided, the program file will be created in the current working directory with its name specified during initialization. Defaults to None.
        """
        extension = "." + self._name.split(".")[-1]
        f_name = optumi.utils.normalize_path(
            self._name.split("/")[-1].replace(extension, "-" + str(self._run_num) + extension) if path is None else path,
            False,
        )
        with open(f_name, "w+") as f:
            f.write(self._program)
        print("Program saved to " + f_name)
