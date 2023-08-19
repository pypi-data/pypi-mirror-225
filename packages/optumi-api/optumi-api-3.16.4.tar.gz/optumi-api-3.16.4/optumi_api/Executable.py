##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .NotebookConfig import create_config
from .Packages import Packages
from .LocalStorage import LocalStorage
from .Server import Server
from .Resource import Resource
from .Notifications import Notifications
from .Workload import Workload
from .EnvironmentVariables import EnvironmentVariables

import optumi_core as optumi
from optumi_core.exceptions import (
    NotLoggedInException,
    OptumiException,
)

import os, datetime, json
from typing import Union, List


class Executable:
    """A class for defining an executable program with optional environment and resource requirements."""

    program_types = ["python notebook", "python script", "docker container", "unknown"]

    def __init__(self, path: str, program_type="unknown"):
        """Constructor specifying a file path to the program and the type of the program.

        Args:
            path (str): the local path to the program
            program_type (str, optional): The type of the program. Can be one of "python notebook", "python script", "docker container" or "unknown". Defaults to "unknown".

        Raises:
            OptumiException: Raised if the program type is not specified properly.
        """
        self._path = optumi.utils.normalize_path(path)
        if not program_type in Executable.program_types:
            raise OptumiException("Unexpected program type '" + program_type + "', expected one of " + str(Executable.program_types))
        self._program_type = program_type

    def __utcnow(self):
        return datetime.datetime.utcnow().isoformat() + "Z"

    def launch(
        self,
        wait: bool = True,
        progress: str = "summary",
        packages: Packages = Packages(),
        files: LocalStorage = LocalStorage(),
        env: Union[EnvironmentVariables, List[EnvironmentVariables]] = [],
        resource: Union[Server, Resource] = None,
        notifications: Notifications = None,
        launch_mode: str = "job",
        max_runtime: int = -1
    ):
        """Launch an executable given a specific configuration.

        Args:
            wait (bool, optional): Whether or not to wait for the workload to finish execution before returning. Defaults to True.
            progress (str, optional): How much progress data to return with the launched workload. Can be one of "silent", "summary", "detail". Defaults to 'summary'.
            env (EnvironmentVariables or list of EnvironmentVariables, optional): Environment variables to configure before running the program.
            packages (Packages, optional):  Python packages required for executing the program. Defaults to empty.
            files (LocalStorage, optional): Any input files needed for the program's execution. Defaults to empty.
            resource (Server, Resource, optional): Server or Resource requirements for running the program. Defaults to None (meaning a GPU machine will be used).
            notifications (Notifications, optional): User notification options when running the container. Defaults to None.
            launch_mode (str, optional): The launch mode for running the program. Can be one of "session" or "job". Defaults to "job".
            max_runtime (int): The maximum runtime of the workload (in minutes). We will automatically terminate the workload if it runs for this long. This only applies to jobs, not session.

        Raises:
            OptumiException: Raised if any of the requirements are specified incorrectly.

        Returns:
            Workload: A workload representing the program.
        """

        if progress != None and not progress in Workload.progress:
            raise OptumiException("Unexpected progress '" + progress + "', expected one of " + str(Workload.progress))

        nb_config = create_config(
            program_type=self._program_type, packages=packages, files=files, env=env, resource=resource, notifications=notifications, launch_mode=launch_mode, max_runtime=max_runtime
        )

        with open(self._path, "r") as f:
            program = f.read()

        setup = json.loads(
            optumi.core.setup_notebook(
                optumi.utils.replace_home_with_tilde(self._path),
                self.__utcnow(),
                {
                    "path": optumi.utils.replace_home_with_tilde(self._path),
                    "content": program,
                },
                json.dumps(nb_config),
            ).text
        )

        # print(setup)

        workload_uuid = setup["uuid"]
        run_num = setup["runNum"]

        # this is necessary for the extension
        optumi.core.push_workload_initializing_update(workload_uuid, "Initializing")
        optumi.core.push_workload_initializing_update(workload_uuid, "stop")

        expanded = [f.path for f in files]

        hashes = [optumi.utils.hash_file(f) for f in expanded]
        stats = [os.stat(f) if os.path.isfile(f) else None for f in expanded]
        creation_times = [datetime.datetime.utcfromtimestamp(stat.st_ctime).isoformat() + "Z" if stat != None else None for stat in stats]
        last_modification_times = [datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat() + "Z" if stat != None else None for stat in stats]
        sizes = [str(stat.st_size) if stat else None for stat in stats]

        try:
            optumi.core.launch_notebook(
                nb_config["upload"]["requirements"],
                hashes,
                [optumi.utils.replace_home_with_tilde(path) for path in expanded],
                creation_times,
                last_modification_times,
                sizes,
                workload_uuid,
                self.__utcnow(),
            )
        except Exception as err:
            # Surppress this error so we can poll for the proper status message
            pass

        launch_status = optumi.get_launch_status(workload_uuid)

        # print(launch_status)

        module_uuid = launch_status["modules"][0] if "modules" in launch_status else None

        workload = Workload(
            optumi.utils.replace_home_with_tilde(self._path),
            program,
            workload_uuid,
            module_uuid,
            nb_config,
            run_num,
        )
        if wait:
            workload.wait(progress)
        return workload

    @property
    def path(self):
        """Obtain the file path of the executable.

        Returns:
            str: The file path of the executable program.
        """
        return self._path

    def __str__(self):
        return str(self._path)
