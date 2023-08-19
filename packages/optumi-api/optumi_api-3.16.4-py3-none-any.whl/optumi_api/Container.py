##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##


from .NotebookConfig import create_config
from .Server import Server
from .Resource import Resource
from .Notifications import Notifications
from .Workload import Workload
from .ContainerRegistry import ContainerRegistry
from .EnvironmentVariables import EnvironmentVariables

import optumi_core as optumi
from optumi_core.exceptions import OptumiException

import datetime, json, re
from typing import Union, List


class Container:
    """A class for managing containers."""

    def __init__(self, image: str, registry: ContainerRegistry = None):
        """Constructor for a Container object taking a container image name and an optional container registry to pull from.

        Args:
            image (str): Container image name.
            registry (ContainerRegistry, optional): Registry containing the image. Defaults to None.

        Raises:
            OptumiException: Raised if an invalid container name is specified.
        """
        if not bool(re.match("^[a-zA-Z0-9][a-zA-Z0-9/_.-]+$", image)):
            raise OptumiException("Invalid container name '" + image + "'")
        self._image = image
        self._registry = registry

    def __utcnow(self):
        return datetime.datetime.utcnow().isoformat() + "Z"

    def launch(
        self,
        wait: bool = True,
        progress: str = "summary",
        env: Union[EnvironmentVariables, List[EnvironmentVariables]] = [],
        args: List[str] = [],
        resource: Union[Server, Resource] = None,
        notifications: Notifications = None,
        max_runtime: int = -1
    ):
        """Launch a container given a specific configuration.

        Args:
            wait (bool, optional): Whether or not to wait for the workload to finish execution before returning. Defaults to True.
            progress (str, optional): How much progress data to return with the launched workload. Can be one of "silent", "summary", "detail". Defaults to "summary".
            env (EnvironmentVariables or list of EnvironmentVariables, optional): Environment variables to provision before running the container.
            args (list of str, optional): Command-line arguments to provide when running the container.
            resource (Server, Resource, optional): Resource requirements for the server that will be running the container. Defaults to None.
            notifications (Notifications, optional): User notification options when running the container. Defaults to None.
            max_runtime (int): The maximum runtime of the workload (in minutes). We will automatically terminate the workload if it runs for this long.

        Returns:
            Workload: A workload representing the container.
        """
        if progress != None and not progress in Workload.progress:
            raise OptumiException("Unexpected progress '" + progress + "', expected one of " + str(Workload.progress))

        nb_config = create_config(program_type="docker container", env=env, resource=resource, notifications=notifications, registry=self._registry, max_runtime=max_runtime)

        container_name = self._image

        setup = json.loads(
            optumi.core.setup_notebook(
                container_name,
                self.__utcnow(),
                {
                    "path": container_name,
                    "content": json.dumps(
                        {
                            "containerName": container_name,
                            "args": args,
                        }
                    ),
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

        try:
            optumi.core.launch_notebook(
                nb_config["upload"]["requirements"],
                [],
                [],
                [],
                [],
                [],
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
            container_name,
            container_name,
            workload_uuid,
            module_uuid,
            nb_config,
            run_num,
        )
        if wait:
            workload.wait(progress)
        return workload

    @property
    def image(self):
        """Obtain the container image name.

        Returns:
            str: The container image name.
        """
        return self._image

    @property
    def registry(self):
        """Obtain the container registry.

        Returns:
            ContainerRegistry: The container registry.
        """
        return self._registry

    def __str__(self):
        return self._registry.url + "/" + self._image if self._registry else self._image
