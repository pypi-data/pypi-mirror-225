##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi
from optumi_core.exceptions import OptumiException

import os, datetime, time
from uuid import uuid4

STORAGE_TOTAL = 0
STORAGE_LIMIT = 1024 * 1024 * 1024 * 1024  # Assume the largest storage total


# Support downloading object under a different name
# Add log and summary objects that support a download function
# Shared between local storage and cloud storage
class LocalFile:
    """A class for managing local files that can be uploaded to Optumi cloud storage.

    Example:
        fs = opt.LocalFile(path)
    """

    def __init__(
        self,
        path: str,
    ):
        """Constructor for a LocalFile object.

        Args:
            path (str): The path to the local file.
        """
        self._path = optumi.utils.normalize_path(path)

        if not os.path.isfile(self._path):
            raise OptumiException("File '" + self._path + "' is a directory. Use opt.LocalStorage to expand a directory recursively.")

    def upload(self, wait: bool = True):
        """Upload a local file to Optumi cloud storage.

        Args:
            wait (bool, optional): A boolean indicating whether the upload should wait until it is complete before returning. Defaults to True.
        """
        key = str(uuid4())
        print("Uploading file...", self)
        optumi.core.upload_files(key, [self._path], True, STORAGE_TOTAL, STORAGE_LIMIT, True)

        if wait:
            while True:
                progress = optumi.core.get_upload_progress([key])
                time.sleep(0.2)
                if progress[key]["progress"] < 0:
                    break

            print("...completed")

    @property
    def path(self):
        """Obtain the path to the file.

        Returns:
            str: The path to the file.
        """
        return self._path

    @property
    def hash(self):
        """Obtain a hash of the file content.

        Returns:
            str: A hash of the file content.
        """
        return optumi.utils.hash_file(self._path)

    @property
    def size(self):
        """Obtain the size of the local file.

        Returns:
            int: The size of the local file in bytes.
        """
        return os.path.getsize(self._path)

    @property
    def created(self):
        """Obtain the date and time when the file was created.

        Returns:
            str: A string containing the date and time when the file was created, in ISO 8601 format.
        """
        return datetime.datetime.utcfromtimestamp(os.stat(self._path).st_ctime).isoformat() + "Z"

    @property
    def modified(self):
        """Obtain the date and time when the file was last modified.

        Returns:
            str:  A string containing the date and time when the file was created, in ISO 8601 format.
        """
        return datetime.datetime.utcfromtimestamp(os.stat(self._path).st_mtime).isoformat() + "Z"

    def __str__(self):
        return self.path + " " + str(self.size) + " " + self.modified
