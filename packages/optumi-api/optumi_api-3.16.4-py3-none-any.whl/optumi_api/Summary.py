##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .utils import collapseUpdates

import optumi_core as optumi

from typing import List, Tuple


class Summary:
    """An internal helper class for obtaining a workload summary."""

    def __init__(
        self,
        name: str,
        initializing_lines: List[Tuple[str, str]],
        preparing_lines: List[Tuple[str, str]],
        running_lines: List[Tuple[str, str]],
    ):
        """Internal constructor for a Summary object.

        Args:
            name (str): the name that will be used to create the summary file.
            initializing_lines (list of (str, str)): The summary lines
            preparing_lines (list of (str, str))): The preparing lines
            running_lines (list of (str, str)): The running lines
        """
        self._name = name
        self._initializing_lines = initializing_lines
        self._preparing_lines = preparing_lines
        self._running_lines = running_lines

    def download(self, path: str = None):
        """Download the workload summary to the given file path.

        Args:
            path (str, optional): The file path where the summary should be stored. If not provided, the summary will be created in the current working directory under the filename specified during initialization. Defaults to None.
        """
        f_name = optumi.utils.normalize_path(self._name.split("/")[-1] + ".summary" if path is None else path, False)
        with open(f_name, "w+") as f:
            f.write(collapseUpdates(self._initializing_lines + self._preparing_lines + self._running_lines))
        print("Summary saved to " + f_name)

    def __str__(self):
        return str(self._name)
