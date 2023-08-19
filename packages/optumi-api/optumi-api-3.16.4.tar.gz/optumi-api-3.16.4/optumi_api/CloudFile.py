##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .CloudFileVersion import CloudFileVersion

import optumi_core as optumi
from optumi_core.exceptions import OptumiException

from typing import List


class CloudFile:
    """A class for managing individual files in Optumi cloud storage."""

    def __init__(self, path: str, versions: List[CloudFileVersion]):
        """Constructor for CloudFile object that describes one file with one or more versions in Optumi cloud storage.

        Args:
            path (str): The path to one file in cloud storage.
            versions (list of CloudFileVersion): A list of CloudFileVersion objects representing different versions of the given file.

        Raises:
            OptumiException: Raised if the versions list is empty, or if the path is not consistent across all versions in the list.
        """
        if not versions:
            raise OptumiException("Missing CloudFile versions")
        self._path = path
        # Sort files by newest to oldest modification time
        self._versions = sorted(versions, key=lambda version: version.modified)
        # Make sure all versions have the proper path
        for v in versions:
            if v.path != path:
                raise OptumiException("CloudFile has inconsistent versions")

    def download(self, wait: bool = True):
        """Download the newest version of the file in Optumi cloud storage.

        Args:
            wait (bool, optional): A boolean indicating whether the download should wait for completion before returning. Defaults to True.
        """
        # Download newest version
        self._versions[0].download(wait)

    def remove(self):
        """Remove all versions of the file from Optumi cloud storage."""
        print("Removing file", self)
        optumi.core.delete_files(
            [x.hash for x in self._versions],
            [x.path for x in self._versions],
            [x.created for x in self._versions],
            "",
        )

    @property
    def versions(self):
        """Obtain the list of all versions of the file in Optumi cloud storage.

        Returns:
            A list of CloudFileVersion objects sorted from newest to oldest.
        """
        return self._versions

    @property
    def path(self):
        """Obtain the path to the file in Optumi cloud storage.

        Returns:
            str: Path to the file.
        """
        return self._path

    def __str__(self):
        return self._path + " (" + str(len(self._versions)) + (" versions)" if len(self._versions) > 1 else " version)")
