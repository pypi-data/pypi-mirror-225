##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi
from optumi_core.exceptions import (
    OptumiException,
)

from .Workload import Workload

import json, os

from typing import List


class Workloads(list):
    """A class for retrieving a list of workloads."""

    def __init__(self, files: List[Workload] = []):
        """Constructor for an object that represents all workloads or a specific subset of workloads.

        Args:
            files (list of Workload, optional): List of Workload objects. Defaults to [].
        """
        super().__init__(files)

    @classmethod
    def list(cls, status: str = None):
        """Obtain a list of all workloads, optionally matching a given status.

        Args:
            status (str, optional): The status of the workload to match, if any. Can be one of "queued", "launching", "running", "completed".

        Returns:
            list of workloads: A list of Workload objects matching the criteria.

        Raises:
            OptumiException: Raised if an unexpected status is provided.
        """
        if status != None and not status in Workload.status_values:
            raise OptumiException("Unexpected workload status '" + status + "', expected one of " + str(Workload.status_values))

        workloads = Workloads()

        user_information = json.loads(optumi.core.get_user_information(True).text)

        # Add apps from user information if they don't already exist
        if "jobs" in user_information:
            for app_map in user_information["jobs"]:
                try:
                    workload = Workload.reconstruct(app_map)
                    if (status is None) or (workload.status == status):
                        workloads.append(workload)
                except:
                    pass
        return workloads

    @classmethod
    def current(cls):
        """Obtain the Workload object representing the current workload.

        Returns:
            Workload: The Workload object representing the current workload running on an Optumi dynamic machine.

        Raises:
            OptumiException: Raised if this method is not called on a machine that was dynamically allocated by Optumi.
        """
        if not "OPTUMI_MOD" in os.environ:
            raise OptumiException("Workloads.current() only supported on Optumi dynamic machines.")

        user_information = json.loads(optumi.core.get_user_information(True).text)

        # Add apps from user information if they don't already exist
        if "jobs" in user_information:
            for app_map in user_information["jobs"]:
                for module in app_map["modules"]:
                    if module["uuid"] == os.environ["OPTUMI_MOD"]:
                        return Workload.reconstruct(app_map)

        raise OptumiException("No current workload")
