##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .Server import Server
from .Provider import Provider
from .Providers import Providers

from typing import Union, List

from optumi_core.exceptions import (
    OptumiException,
)


class Resource:
    """A class for creating resource specifications to be used when running scripts, notebooks or containers."""

    gpu_required_values = ["required", "optional"]

    def __init__(self, providers: Union[List[str], List[Provider], str, Provider] = [], gpu: str = "required", num_gpus: int = 0, vram_per_gpu: int = 0, vram_per_system: int = 0, ram: int = 0, num_cpus: int = 0, max_rate: float = -1):
        """Constructor for the Resource class.

        Args:
            providers (list of str or list of Provider): The providers that can be used. Defaults to [], which means any provider can be used.
            gpu (str): This argument specifies the type of graphics card to use. It can be set to "required" to permit any graphics card, "optional" to permit cpu only machines, or a particular value from the options in gpus(). The default option is "required".
            num_gpus (int): The minimum number of gpu cards. Defaults to 1 if gpu is specified, otherwise 0.
            vram_per_gpu (int): The minimum amount of VRAM in GiB per gpu card. Defaults to 0.
            vram_per_system (int): The minimum amount of VRAM in GiB for the machine. Defaults to 0.
            ram (int): The minimum amount of RAM in GiB for the machine. Defaults to 0.
            num_cpus (int): The minimum number of CPUs (virtual cores) for the machine. Defaults to 0.
            max_rate (float): The maximum rate in $/hr.
        Raises:
            OptumiException: Raised if an unsupported GPU card is specified.
        """
        
        # If a user passes in a singleton for provider, put it in a list
        if isinstance(providers, str) or isinstance(providers, Provider):
            providers = [providers]

        if not type(gpu) is str:
            raise OptumiException("Unexpected GPU type '" + str(gpu) + "', expected one of " + str(Resource.gpu_required_values + Server.gpus()))
        elif not gpu.lower().split('/')[0] in Resource.gpu_required_values + [x.lower() for x in Server.gpus()]:
            gpus = Server.gpus()
            if len(gpus) == 0:
                if len([p for p in Providers.list() if p.is_activated()]) == 0:
                    raise OptumiException("No activated providers. Contact Optumi for more information.")
                if len(Server.inventory()) == 0:
                    raise OptumiException("Machine inventory is empty. Contact Optumi for more information.")
                raise OptumiException("No GPU machines in inventory.")
            raise OptumiException("Unexpected GPU type '" + str(gpu) + "', expected one of " + str(Resource.gpu_required_values + gpus))

        self._providers = []
        for provider in providers:
            if type(provider) is Provider:
                self._providers.append(provider)
            else:
                self._providers.append(Provider(provider))

        if '/' in gpu:
            parts = gpu.split('/')
            self._gpu = parts[0]
            self._memory_per_gpu = int(parts[1])
        else:
            self._gpu = gpu
            self._memory_per_gpu = 0
        self._num_gpus = 1 if num_gpus == 0 and gpu != "optional" else num_gpus

        self._vram_per_gpu = vram_per_gpu
        self._vram_per_system = vram_per_system
        self._ram = ram
        self._num_cpus = num_cpus
        self._max_rate = max_rate

    @property
    def providers(self):
        """Obtain the list of the providers that can be used.

        Returns:
            list of Provider: The list of providers that can be used. Defaults to [], which means any provider.
        """
        return self._providers

    @property
    def gpu(self):
        """Obtain the type of graphics card to be used, either True for any, or a specific string value representing one of the types in gpus()

        Returns:
            str: The type of graphics card to be used, "required" to permit any graphics card, "optional" to permit cpu only machines, or a specific string value representing one of the types in gpus()
        """
        return self._gpu

    @property
    def memory_per_gpu(self):
        """Obtain the memory required per graphics card.

        Returns:
            int: The memory required per graphics card, specified in GiB.
        """
        return self._memory_per_gpu

    @property
    def num_gpus(self):
        """Obtain the number of gpu cards.

        Returns:
            int: The number of gpu cards.
        """
        return self._num_gpus
    
    @property
    def vram_per_gpu(self):
        """Obtain the minimum amount of VRAM in GiB per gpu card.

        Returns:
            int: The minimum amount of VRAM in GiB per gpu card.
        """
        return self._vram_per_gpu

    @property
    def vram_per_system(self):
        """Obtain the minimum amount of VRAM in GiB for the machine.

        Returns:
            int: The minimum amount of VRAM in GiB for the machine.
        """
        return self._vram_per_system

    @property
    def ram(self):
        """Obtain the minimum amount of RAM in GiB for the machine.

        Returns:
            int: The minimum amount of RAM in GiB for the machine.
        """
        return self._ram

    @property
    def num_cpus(self):
        """Obtain the minimum number of CPUs (virtual cores) for the machine.

        Returns:
            int: The minimum number of CPUs (virtual cores) for the machine.
        """
        return self._num_cpus

    @property
    def max_rate(self):
        """Obtain the max rate.

        Returns:
            float: The max rate.
        """
        return self._max_rate

    def __str__(self):
        ret = ""
        if len(self.providers) > 0:
            ret += "providers=" + str([str(p) for p in self.providers]) + ", "
        else:
            ret += "providers=Any, "
        ret += "gpu=" + str(self.gpu) + ", "
        if self.num_gpus > 0:
            ret += "num_gpus=" + str(self.num_gpus) + ", "
        if self.vram_per_gpu > 0:
            ret += "vram_per_gpu=" + str(self.vram_per_gpu) + "GiB, "
        if self.vram_per_system > 0:
            ret += "vram_per_system=" + str(self.vram_per_system) + "GiB, "
        if self.ram > 0:
            ret += "ram=" + str(self.ram) + "GiB, "
        if self.num_cpus > 0:
            ret += "num_cpus=" + str(self.num_cpus) + ", "
        if self.max_rate > 0:
            ret += "max_rate=$" + str(self.max_rate) + "/hr, "
        return ret[:-2]
