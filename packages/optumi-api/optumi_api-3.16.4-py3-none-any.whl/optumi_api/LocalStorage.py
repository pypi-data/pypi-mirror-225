##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .LocalFile import LocalFile

import optumi_core as optumi

import time, os
from pathlib import Path
from uuid import uuid4
from typing import Union, List


STORAGE_TOTAL = 0
STORAGE_LIMIT = 1024 * 1024 * 1024 * 1024  # Assume the largest storage total


class LocalStorage(list):
    """A class for uploading files to Optumi cloud storage."""

    def __init__(self, files: Union[str, LocalFile, List[str], List[LocalFile]] = []):
        """Constructor for a LocalStorage object.

        Args:
            files (LocalFile or str or list of LocalFile or list of str, optional): List of local files, useful for performing batch uploads. Defaults to [].
        """
        _files = []
        if type(files) is str:
            for path in optumi.utils.expand_path(files):
                _files.append(LocalFile(path))
        elif type(files) is LocalFile:
            _files.append(files)
        else:
            for f in files:
                if type(f) is str:
                    for path in optumi.utils.expand_path(f):
                        _files.append(LocalFile(path))
                else:
                    _files.append(f)
        super().__init__(_files)

    def upload(self, wait: bool = True):
        """Upload the list of local files to Optumi cloud storage.

        Args:
            wait (bool, optional): Upload the local version of a file to cloud storage. If 'wait' is True, it will wait until the download is complete before returning. Defaults to True.
        """
        if len(self) > 0:
            key = str(uuid4())
            print("Uploading", "files..." if len(self) > 1 else "file...")
            for f in self:
                print(f)
            optumi.core.upload_files(
                key,
                [x.path for x in self],
                True,
                STORAGE_TOTAL,
                STORAGE_LIMIT,
                True,
            )

            if wait:
                while True:
                    progress = optumi.core.get_upload_progress([key])
                    time.sleep(0.2)
                    if progress[key]["progress"] < 0:
                        break

                print("...completed")

    def __str__(self):
        return str([str(x) for x in self])
