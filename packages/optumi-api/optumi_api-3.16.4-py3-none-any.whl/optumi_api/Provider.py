##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import json

import optumi_core as optumi
from optumi_core.exceptions import OptumiException

from typing import List


class Provider:
    """A class for capturing information about cloud providers available through the Optumi service platform."""

    def __init__(self, name: str, acronym: str = None, job_program_types: List[str] = None, session_program_types: List[str] = None):
        """Constructor to initialize the cloud provider.

        Args:
            name (str): The name of the cloud provider
            acronym (str, optional): The shorthand acronym used for the provider
            job_program_types (list of str, optional): The list of program types that are currently supported for jobs for this provider.
            session_program_types (list of str, optional): The list of program types that are currently supported for sessions for this provider.

        Raises:
            OptumiException: Raised if there is no provider matching the given name
        """

        if acronym is None or job_program_types is None or session_program_types:
            user_information = json.loads(optumi.core.get_user_information(True).text)

            for provider in user_information["providers"]:
                if provider["descriptive"].lower() == name.lower() or provider["abridged"].lower() == name.lower():
                    self._name = provider["descriptive"]
                    self._acronym = provider["abridged"]
                    self._job_program_types = provider["jobProgramTypes"]
                    self._session_program_types = provider["sessionProgramTypes"]
                    return
            raise OptumiException("Unable to find provider matching '" + str(name) + "'. use Providers.list() to see all cloud providers.")
        else:
            self._name = name
            self._acronym = acronym
            self._job_program_types = job_program_types
            self._session_program_types = session_program_types

    @classmethod
    def reconstruct(cls, provider_map):
        return (
            provider_map["descriptive"],
            provider_map["abridged"],
            provider_map["jobProgramTypes"],
            provider_map["sessionProgramTypes"],
        )

    @property
    def name(self):
        """Obtain the full provider name.

        Returns:
            str: The full provider name.
        """
        return self._name

    @property
    def acronym(self):
        """Obtain the shorthand provider acronym.

        Returns:
            str: The shorthand provider acronym.
        """
        return self._acronym

    @property
    def job_program_types(self):
        """Obtain the supported program types for jobs for the given provider.

        Returns:
            list of str: The supported program types for jobs.
        """
        return self._job_program_types

    @property
    def session_program_types(self):
        """Obtain the supported program types for sessions the given provider.

        Returns:
            list of str: The supported program types for sessions.
        """
        return self._session_program_types

    def enable(self):
        """Enable this provider so it can be used for allocating machines.

        Raises:
            OptumiException: Raised if this provider is not activated by Optumi.
        """
        user_information = json.loads(optumi.core.get_user_information(False).text)
        if self._acronym in user_information["deactivatedProviders"]:
            raise OptumiException("Cannot enable deactivated provider " + str(self))
        optumi.core.set_user_information("enableProvider", self._acronym)

    def disable(self):
        """Disable this provider so it will not used for allocating machines.

        Raises:
            OptumiException: Raised if this provider is not activated by Optumi.
        """
        user_information = json.loads(optumi.core.get_user_information(False).text)
        if self._acronym in user_information["deactivatedProviders"]:
            raise OptumiException("Cannot disable deactivated provider " + str(self))
        optumi.core.set_user_information("disableProvider", self._acronym)

    def is_activated(self):
        """Determine if this provider has been activated by Optumi.

        Returns:
            bool: True if this provider has been activated by Optumi.
        """
        user_information = json.loads(optumi.core.get_user_information(False).text)
        return not self._acronym in user_information["deactivatedProviders"]

    def is_enabled(self):
        """Determine if this provider has been enabled by the current user.

        Returns:
            bool: True if this provider has been enabled by the current user.
        """
        user_information = json.loads(optumi.core.get_user_information(False).text)
        return self._acronym in user_information["enabledProviders"]

    def __str__(self):
        return str(self._name) + " (" + self._acronym + ")"
