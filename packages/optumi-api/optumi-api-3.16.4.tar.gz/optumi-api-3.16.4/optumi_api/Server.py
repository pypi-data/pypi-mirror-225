##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .Provider import Provider
from .Providers import Providers

import optumi_core as optumi
from optumi_core.exceptions import OptumiException

import json

_machines = None
_gpus = None


def _update_inventory_info():
    global _machines, _gpus

    user_information = json.loads(optumi.core.get_user_information(True).text)

    _machines = []
    _gpus = []

    for machine in user_information["machines"]:
        name = machine["name"]
        provider = name.split(":")[0]
        gpu = machine["graphicsCardType"]

        if not machine in _machines:
            _machines.append(name)

        if not gpu in _gpus:
            _gpus.append(gpu)

    _machines.sort()
    _gpus.sort()


# Support embedding the provider in the machine string, have no default provider argument
class Server:
    """A class specifying a server with specific machine capabilities from a given cloud provider."""

    @classmethod
    def inventory(cls):
        """Obtain a list of all cloud machines.

        Returns:
            list of string: A list of machine sizes as strings.
        """
        if _machines is None:
            _update_inventory_info()

        return _machines

    @classmethod
    def gpus(cls):
        """Obtain a list of all graphics cards in cloud machines.

        Returns:
            list of string: A list of graphics cards as strings.
        """
        if _gpus is None:
            _update_inventory_info()

        return _gpus

    def __init__(self, size: str = "Standard_NC4as_T4_v3", provider: str = "Azure"):
        """Constructor for the Server object.

        Args:
            size (str, optional): The machine size, e.g., 'Standard_NC4as_T4_v3'. If the size string contains a colon (':'), then the first part of the string is treated as the provider name and the second part of the string is treated as the size name. Available sizes can be listed using machines(). Defaults to "Standard_NC4as_T4_v3".
            provider (str, optional): The name of the provider for the server, e.g., 'Azure'. Defaults to "Azure".

        Raises:
            OptumiException: Raised if an unexpected provider or size is specified.
        """
        if ":" in size:
            s = size.split(":")
            self._provider = Provider(s[0].lower())
            self._size = s[1].lower()
        else:
            self._provider = Provider(provider.lower())
            self._size = size.lower()

        inventory = Server.inventory()
        if not self._provider.name.lower() + ":" + self._size in [x.lower() for x in inventory]:
            if len(inventory) == 0:
                if len([p for p in Providers.list() if not p.is_activated()]) == 0:
                    raise OptumiException("No activated providers. Contact Optumi for more information.")
                raise OptumiException("Machine inventory is empty. Contact Optumi for more information.")
            raise OptumiException("Unexpected machine size '" + self._provider.name + ":" + self._size + "', expected one of " + str(inventory))

        if not self._provider.is_enabled():
            raise OptumiException("Provider " + str(provider) + " is not enabled. Use Provider.enable() prior to launching.")

        if not self._provider.is_activated():
            raise OptumiException("Provider " + str(provider) + " is not activated by Optumi. Contact Optumi for more information.")

    @property
    def provider(self):
        """Obtain the cloud provider name.

        Returns:
            str: The name of the cloud provider for the allocated machine.
        """
        return self._provider

    @property
    def size(self):
        """Obtain the server size.

        Returns:
            str: The size of the allocated machine.
        """
        return self._size

    def __str__(self):
        return str(self.provider) + ":" + str(self.size)
