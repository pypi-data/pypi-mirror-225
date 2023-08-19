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

import json


class ContainerRegistry:
    """A class for managing access to a container registry with optional credentials.

    Standard Docker container registries are provided by Optumi through a stored configuration called an "integration". An integration can be named, unnamed, renamed, stored, retrieved and removed.
    """

    def __init__(
        self,
        name: str = "",
        url: str = None,
        username: str = None,
        password: str = None,
    ):
        """Constructor for logging in to a private container registry.

        A ContainerRegistry object can be created with just a name (to retrieve an existing container registry integration) or with full parameters (to create a new container registry integration).

        Args:
            name (str, optional): Name of the integration. The default is indicated by the empty string ("") and will cause a name to be auto-generated.
            url (str, optional): URL of the container registry. Defaults to None.
            username (str, optional): The username used to access the registry. Defaults to None.
            password (str, optional): The password used to access the registry. Defaults to None.

        Raises:
            OptumiException: Raised if unable to load an existing integration or create a new one.
        """
        got_url = url != None and len(username) > 0
        got_username = username != None and len(username) > 0
        got_password = password != None and len(username) > 0
        if got_url != got_username or got_url != got_password:
            raise OptumiException("Need url, username, and password to specify registry")

        self._name = name

        if url is None:
            # Retrieve the container registry
            # This is not the best way to do this...
            integrations = json.loads(optumi.core.get_integrations().text)["integrations"]
            for integration in integrations:
                if integration["name"] == name:
                    self._name = integration["name"]
                    self._url = integration["url"]
                    return
            raise OptumiException("Unable to find container registry named '" + name + "'")
        else:
            # Store the container registry
            info = {
                "integrationType": "container registry",
                "name": name,
                "registryService": "generic container registry",
                "url": url,
                "username": username,
                "password": password,
            }
            res = optumi.core.add_integration(name, json.dumps(info), False).text
            try:
                integration = json.loads(res)
                self._name = integration["name"]
                self._url = integration["url"]
            except json.decoder.JSONDecodeError:
                raise OptumiException(res)

    def rename(self, newName: str):
        """Rename this integration.

        Args:
            newName (str): The new integration name for this container registry.
        """
        optumi.core.rename_integration(self._name, newName)
        self._name = newName

    def remove(self):
        """Remove this integration."""
        ContainerRegistry.purge(self._name)

    @property
    def name(self):
        """Obtain the name of this integration.

        Returns:
            str: The integration name of this container registry.
        """
        return self._name

    @property
    def url(self):
        """Obtain the url of this container registry.

        Returns:
            str: The url of this container registry.
        """
        return self._url

    @classmethod
    def purge(cls, name: str):
        """Remove this integration.

        Args:
            name (str): The integration name of the container registry to remove.
        """
        optumi.core.remove_integration(name)

    def __str__(self):
        return str(self._url)
