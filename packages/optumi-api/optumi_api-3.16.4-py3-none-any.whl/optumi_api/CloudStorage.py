##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi

from .CloudFile import CloudFile
from .CloudFileVersion import CloudFileVersion

import json, time
from uuid import uuid4

from typing import List


# Support downloading object under a different name
class CloudStorage(list):
    """A class for managing a group of files in Optumi cloud storage.

    The class methods list() and find() produce a CloudStorage object that contain the requested list of files
    found in cloud storage while the methods download() and remove() operate on the list of files contained in
    the CloudStorage object itself.
    """

    def __init__(self, files: List[CloudFile] = []):
        """Constructor for an object that represents all files or a specific subset of files in cloud storage.

        The CloudStorage object can perform "download", "remove", "list" and "find" operation on files of interest.

        Args:
            files (list of CloudFile, optional): List of CloudFile objects in cloud storage. Defaults to [] which refers to all files in cloud storage. XXX This is not correct
        """
        super().__init__(files)

    def download(self, wait: bool = True):
        """Download the newest version of the list of files contained in the current CloudStorage object from Optumi cloud storage.

        Args:
            wait (bool, optional): A boolean indicating whether the download should wait for completion before returning. Defaults to True.
        """
        if len(self) > 0:
            key = str(uuid4())
            print("Downloading", "files..." if len(self) > 1 else "file...")
            for f in self:
                print(f)
            optumi.core.download_files(
                key,
                [x.versions[0].hash for x in self],
                [x.versions[0].path for x in self],
                [x.versions[0].size for x in self],
                False,
                None,
            )

            if wait:
                while True:
                    progress = optumi.core.get_download_progress([key])
                    time.sleep(0.2)
                    if progress[key]["progress"] < 0:
                        break

                print("...completed")

    def remove(self):
        """Remove all versions of the list of files contained in the current CloudStorage object from Optumi cloud storage."""

        if len(self) > 0:
            print("Removing", "files..." if len(self) > 1 else "file...")
            for f in self:
                print(f)
            hashes = []
            paths = []
            created = []

            for cloud_file in self:
                for version in cloud_file.versions:
                    hashes.append(version.hash)
                    paths.append(version.path)
                    created.append(version.created)

            optumi.core.delete_files(
                hashes,
                paths,
                created,
                "",
            )
            print("...completed")

    @classmethod
    def list(cls):
        """List all files in Optumi cloud storage.

        Returns:
            CloudStorage: A list of all CloudFile objects in cloud storage.
        """
        res = optumi.core.list_files()
        response = json.loads(res.text)
        files = CloudStorage()
        versions = {}

        for i in range(len(response["files"])):
            path = response["files"][i]
            version = CloudFileVersion(
                path,
                response["hashes"][i],
                response["filessize"][i],
                response["filescrt"][i],
                response["filesmod"][i],
            )
            if path in versions:
                versions[path].append(version)
            else:
                versions[path] = [version]

        for path in versions:
            files.append(CloudFile(path, versions[path]))

        return files

    @classmethod
    def find(cls, match: str = "", contains: str = ""):
        """Find all files in Optumi cloud storage matching a given file name or containing a substring.

        Args:
            match (str, optional): File name to match. Defaults to "".
            contains (str, optional): Substring to match anywhere in the file path. Defaults to "".

        Returns:
            CloudStorage: All matching files in the cloud.
        """
        if match:
            return CloudStorage(
                x for x in CloudStorage.list() if optumi.utils.normalize_path(match, strict=False) == optumi.utils.normalize_path(x.path, strict=False)
            )
        elif contains:
            return CloudStorage(x for x in CloudStorage.list() if str(contains) in optumi.utils.normalize_path(x.path, strict=False))
        else:
            return CloudStorage()

    def __str__(self):
        return str([str(x) for x in self])
