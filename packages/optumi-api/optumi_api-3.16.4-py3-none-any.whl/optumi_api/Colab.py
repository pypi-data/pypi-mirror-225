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
from .Workload import Workload
from .EnvironmentVariables import EnvironmentVariables
from .Notifications import Notifications

from optumi_core.exceptions import OptumiException

import optumi_core as optumi

import os, datetime, json
from typing import Union, List


class Colab:
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
    ):
        if progress != None and not progress in Workload.progress:
            raise OptumiException("Unexpected progress '" + progress + "', expected one of " + str(Workload.progress))

        nb_config = create_config(program_type="python notebook", packages=packages, files=files, env=env, resource=resource, notifications=notifications)

        from google.colab import _message

        # Load the notebook JSON string.
        notebook = _message.blocking_request("get_ipynb")["ipynb"]

        # Remove the optumi cell
        notebook["cells"] = [cell for cell in notebook["cells"] if cell["cell_type"] == "code" and not "".join(cell["source"]).startswith("#skip@optumi")]

        program = json.dumps(notebook)

        # Get the notebook name
        import requests

        d = requests.get("http://172.28.0.2:9000/api/sessions").json()[0]
        name = d["name"]

        setup = json.loads(
            optumi.core.setup_notebook(
                name,
                self.__utcnow(),
                {"path": name, "content": program},
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

        workload = Workload(name, program, workload_uuid, module_uuid, nb_config, run_num)
        if wait:
            workload.wait(progress)
        return workload
