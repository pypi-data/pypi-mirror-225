##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .Packages import Packages
from .LocalStorage import LocalStorage
from .Server import Server
from .Resource import Resource
from .Notifications import Notifications
from .EnvironmentVariables import EnvironmentVariables
from .ContainerRegistry import ContainerRegistry
from .Provider import Provider

import optumi_core as optumi

from optumi_core.exceptions import OptumiException

from typing import Union, List

launch_modes = ["job", "session"]


def create_config(
    program_type: str,
    packages: Packages = Packages(),
    files: LocalStorage = LocalStorage(),
    env: Union[EnvironmentVariables, List[EnvironmentVariables]] = [],
    resource: Resource = None,
    notifications: Notifications = None,
    registry: ContainerRegistry = None,
    launch_mode: str = "job",
    max_runtime: int = -1,
):
    # Start with blank config
    nb_config = {
        "intent": 0.25,
        "compute": {
            "expertise": "component",
            "required": False,
            "rating": [-1, -1, -1],
            "score": [-1, -1, -1],
            "cores": [-1, -1, -1],
            "frequency": [-1, -1, -1],
        },
        "graphics": {
            "expertise": "simplified",
            "required": False,
            "rating": [-1, -1, -1],
            "score": [-1, -1, -1],
            "cores": [-1, -1, -1],
            "memory": [-1, -1, -1],
            "frequency": [-1, -1, -1],
            "boardType": "U",
            "memoryPerBoard": [-1, -1, -1],
            "memoryPerSystem": [-1, -1, -1],
            "boardCount": [-1, -1, -1],
        },
        "memory": {
            "expertise": "component",
            "required": False,
            "rating": [-1, -1, -1],
            "size": [-1, -1, -1],
        },
        "storage": {
            "expertise": "component",
            "required": False,
            "rating": [-1, -1, -1],
            "size": [-1, -1, -1],
            "iops": [-1, -1, -1],
            "throughput": [-1, -1, -1],
        },
        "upload": {"files": [], "requirements": ""},
        "integrations": [],
        "providers": [],
        "machineAssortment": [],
        "maxRate": -1,
        "maxRuntime": -1,
        "notifications": {
            "jobStartedSMSEnabled": False,
            "jobCompletedSMSEnabled": False,
            "jobFailedSMSEnabled": False,
            "packageReadySMSEnabled": False,
        },
        "interactive": False,
        "annotation": "",
    }

    def check_providers(providers: List[Provider]):
        for provider in providers:
            if not provider.is_activated():
                raise OptumiException("Provider " + str(provider) + " is not activated by Optumi. Contact Optumi for more information.")
            if not provider.is_enabled():
                raise OptumiException("Provider " + str(provider) + " is not enabled. Use Provider.enable() to enable it prior to launching.")
            if (launch_mode.lower() == "session") and (not program_type in provider.session_program_types):
                raise OptumiException("Provider " + str(provider) + " does not support program type '" + program_type + "' for sessions")
            if (launch_mode.lower() == "job") and (not program_type in provider.job_program_types):
                raise OptumiException("Provider " + str(provider) + " does not support program type '" + program_type + "' for jobs")

    if resource is None:
        try:
            check_providers([Provider("AZ")])
            resource = Server("AZ:Standard_NC4as_T4_v3")
        except:
            pass

    if resource is None:
        try:
            check_providers([Provider("LDL")])
            resource = Server("LDL:gpu_1x_a10")
        except:
            pass

    if resource is None:
        try:
            check_providers([Provider("AWS")])
            resource = Server("AWS:g4dn.xlarge")
        except:
            pass

    if not launch_mode.lower() in launch_modes:
        raise OptumiException("Unexpected launch mode '" + launch_mode + "', expected one of " + str(launch_modes))

    # Plug in session/job
    nb_config["interactive"] = launch_mode.lower() == "session"

    # Plug in program type
    nb_config["programType"] = program_type

    # Plug in packages
    nb_config["upload"]["requirements"] = "\n".join(packages)

    # Plug in files
    expanded = [f.path for f in files]

    # Make sure files are uploaded
    files.upload()
    nb_config["upload"]["files"] = [{"path": optumi.utils.replace_home_with_tilde(path), "enabled": True} for path in expanded]

    # Plug in environment variables
    if type(env) is EnvironmentVariables:
        nb_config["integrations"] += [
            {
                "name": env.name,
                "enabled": True,
                "integrationType": "environment variable",
            }
        ]
    else:
        nb_config["integrations"] += [
            {
                "name": e.name,
                "enabled": True,
                "integrationType": "environment variable",
            }
            for e in env
        ]

    # Plug in container registry
    if registry:
        nb_config["integrations"] += [
            {
                "name": registry.name,
                "enabled": True,
                "integrationType": "generic container registry",
            }
        ]

    # Plug in resource requirements
    if type(resource) is Server:
        check_providers([resource.provider])
        nb_config["machineAssortment"] = [resource.provider.name + ":" + resource.size]
    elif type(resource) is Resource:
        nb_config["machineAssortment"] = []

        nb_config["compute"]["cores"] = [-1, -1, -1] if resource.num_cpus == 0 else [resource.num_cpus, -1, -1]

        if resource.gpu in Resource.gpu_required_values:
            nb_config["graphics"]["cores"] = [1 if resource.gpu == "required" else -1, -1, -1]
        else:
            nb_config["graphics"]["cores"] = [1, -1, -1]
            nb_config["graphics"]["boardType"] = resource.gpu

        nb_config["graphics"]["memoryPerBoard"] = [resource.vram_per_gpu * 1024**3, -1, -1]
        nb_config["graphics"]["memoryPerSystem"] = [resource.vram_per_system * 1024**3, -1, -1]
        nb_config["graphics"]["boardCount"] = [-1, -1, -1] if resource.num_gpus == 0 else [resource.num_gpus, -1, -1]

        nb_config["memory"]["size"] = [-1, -1, -1] if resource.ram == 0 else [resource.ram * 1024**3, -1, -1]

        check_providers(resource.providers)
        nb_config["providers"] = [provider.name for provider in resource.providers]

        if resource.max_rate > 0:
            nb_config['maxRate'] = resource.max_rate / 3600 
        
    if max_runtime > 0:
        nb_config['maxRuntime'] = max_runtime * 60

    # Plug in requirements
    if notifications != None:
        nb_config["notifications"] = {
            "jobStartedSMSEnabled": notifications.job_started,
            "jobCompletedSMSEnabled": notifications.job_completed,
            "jobFailedSMSEnabled": notifications.job_failed,
            "packageReadySMSEnabled": False,
        }

    return nb_config
