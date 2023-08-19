##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi
from optumi_core.exceptions import OptumiException

import json, re

from typing import Dict


class EnvironmentVariables:
    """This class represents environment variables to confgure before running a program on an Optumi dynamic machine."""

    def __init__(self, name: str = "", environ: Dict[str, str] = None):
        """Constructor for defining a named set of environment variables to be configured before running a program.

        Standard environment variables are supported by Optumi through a stored configuration called an "integration". An integration can be named, unnamed, renamed, stored, retrieved and removed.

        Args:
            name (str, optional): Name of the integration. The default is indicated by the empty string ("") and will cause a name to be auto-generated.
            environ (dict of str: str, optional): A dictionary representing environment variables (key-value pairs).

        Raises:
            OptumiException: Raised if unable to load or create a set of environment variables.
        """
        self._name = name

        if environ is None:
            # Retrieve the environment variables
            # This is not the best way to do this...
            integrations = json.loads(optumi.core.get_integrations().text)["integrations"]
            for integration in integrations:
                if integration["name"] == name:
                    self._name = integration["name"]
                    self._environ = EnvironmentVariables.__format_environ(integration["keys"])
                    return
            raise OptumiException("Unable to find environment variable named '" + name + "'")
        else:
            # Make sure the env keys are not invalid
            for key in environ:
                if not bool(re.match("^[_.A-Za-z][_A-Za-z0-9]*$", key)):
                    raise OptumiException("Invalid environment variable key '" + key + "'")

            # Store the environment variables
            info = {
                "integrationType": "environment variable",
                "name": name,
                "variables": environ,
            }
            res = optumi.core.add_integration(name, json.dumps(info), False).text
            try:
                integration = json.loads(res)
                self._name = integration["name"]
                self._environ = self.__format_environ(integration["keys"])
            except json.decoder.JSONDecodeError:
                raise OptumiException(res)

    def rename(self, newName: str):
        """Rename this integration.

        Args:
            newName (str): The new integration name for this set of environment variables.
        """
        optumi.core.rename_integration(self._name, newName)
        self._name = newName

    def remove(self):
        """Remove this integration."""
        EnvironmentVariables.purge(self._name)

    @property
    def name(self):
        """Obtain the name of this integration.

        Returns:
            str: The integration name of this set of environment variables.
        """
        return self._name

    @property
    def environ(self):
        """Obtain a dictionary representing the set of environment variables.

        Returns:
            str: A dictionary representing environment variables with the values redacted (for security reasons).
        """
        return dict(zip(self._environ, ["**hidden**" for _ in self._environ]))

    @classmethod
    def __format_environ(cls, keys):
        return dict(zip(keys, ["**hidden**" for _ in keys]))

    @classmethod
    def purge(cls, name: str):
        """Remove this integration.

        Args:
            name (str): The integration name of the set of environment variables to remove.
        """
        optumi.core.remove_integration(name)

    def __str__(self):
        return str(self.environ)
