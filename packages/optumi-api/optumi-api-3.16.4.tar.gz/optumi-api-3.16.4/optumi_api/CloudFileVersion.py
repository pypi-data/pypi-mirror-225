##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi
import time
from uuid import uuid4


class CloudFileVersion:
    """A class for managing versions of individual files in Optumi cloud storage."""

    def __init__(
        self,
        path: str,
        hash: str,
        size: int,
        created: str,
        modified: str,
    ):
        """Constructor of a CloudFileVersion object.

        Args:
            path (str): The location of the file in the cloud.
            hash (str): The hash of the file content.
            size (int): The size, in bytes, of the file.
            created (str): A string containing the date and time for when the file was created, in ISO 8601 format.
            modified (str): A string containing the date and time for when the file was last modified, in ISO 8601 format.
        """
        self._path = path
        self._hash = hash
        self._size = size
        self._created = created
        self._modified = modified

    def download(self, wait: bool = True):
        """Download the file from Optumi cloud storage onto the local machine.

        Args:
            wait (bool, optional): A boolean indicating whether the download should wait for completion before returning. Defaults to True.
        """
        key = str(uuid4())
        print("Downloading file", self)
        optumi.core.download_files(key, [self._hash], [self._path], [self._size], False, None)

        if wait:
            while True:
                progress = optumi.core.get_download_progress([key])
                time.sleep(0.2)
                if progress[key]["progress"] < 0:
                    break

            print("...completed")

    def remove(self):
        """Remove the file from Optumi cloud storage."""
        print("Deleting file", self)
        optumi.core.delete_files([self._hash], [self._path], [self._created], "")

    @property
    def path(self):
        """Obtain the location of the file in Optumi cloud storage.

        Returns:
            str: The location of the file in cloud storage.
        """
        return self._path

    @property
    def hash(self):
        """Obtain the hash of the file in Optumi cloud storage.

        Returns:
            str: The hash of the file version content.
        """
        return self._hash

    @property
    def size(self):
        """Obtain the size of the file in Optumi cloud storage.

        Returns:
            int: The size, in bytes, of the file version.
        """
        return self._size

    @property
    def created(self):
        """Obtain the date and time when the file was created.

        Returns:
            str: A string containing the date and time when the file was created, in ISO 8601 format.
        """
        return self._created

    @property
    def modified(self):
        """Obtain the date and time when the file was last modified.

        Returns:
            str: A string containing the date and time when the file was last modified modified, in ISO 8601 format.
        """
        return self._modified

    def __str__(self):
        return (
            self.path
            + " "
            + str(self.size)
            # + " "
            # + self.created
            + " "
            + self.modified
            # + " "
            # + self.hash
        )

    def __repr__(self):
        return self.__str__()
