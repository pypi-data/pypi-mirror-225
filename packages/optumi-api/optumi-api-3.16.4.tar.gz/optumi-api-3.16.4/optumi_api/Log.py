##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .utils import fixBackspace, fixCarriageReturn

import optumi_core as optumi


class Log:
    """A class for downloading the log file created by running a workload."""

    def __init__(self, name: str, output: list):
        """Constructor to initialize the Log object and creates a new log file.

        Args:
            name (str): The name for the new log file.
            output (list of str): Lines of text representing the log entries to store in the logfile.
        """
        self._name = name
        self._output = output

    def download(self, path: str = None):
        """Download the log file from Optumi cloud storage to the given file path.

        Args:
            path (str, optional): The file path where the log file will be stored. If not provided, the log file will be created in the current working directory and named as specified during initialization. Defaults to None.
        """
        f_name = optumi.utils.normalize_path(self._name.split("/")[-1] + ".log" if path is None else path, False)
        with open(f_name, "w+") as f:
            f.write(fixBackspace(fixCarriageReturn("".join([x[0] for x in self._output]))))
        print("Log saved to " + f_name)
