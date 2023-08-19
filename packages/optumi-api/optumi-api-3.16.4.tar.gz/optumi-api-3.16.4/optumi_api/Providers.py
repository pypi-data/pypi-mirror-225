##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi

import json

from .Provider import Provider

from typing import List


class Providers(list):
    """A class for retrieving the full list of potential cloud providers."""

    def __init__(self, files: List[Provider] = []):
        """Constructor for an object that represents all providers or a specific subset of providers.

        Args:
            files (list of Provider, optional): List of Provider objects. Defaults to [].
        """
        super().__init__(files)

    @classmethod
    def list(cls):
        """Obtain the list of all cloud providers.

        Returns:
            list of Provider: The list of providers supported by Optumi.
        """

        providers = Providers()

        user_information = json.loads(optumi.core.get_user_information(True).text)

        for provider in user_information["providers"]:
            provider = Provider(*Provider.reconstruct(provider))
            providers.append(provider)

        return providers
