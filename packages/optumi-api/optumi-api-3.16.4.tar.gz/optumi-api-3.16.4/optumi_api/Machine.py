##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi
from optumi_core.exceptions import OptumiException

import json, time

from typing import List

class Machine:
    """A class for representing a machine. It has two constructors, one to be used when creating a new
    machine and another when reconstructing an existing Optumi dynamic machine.
    """

    status_values = ["Acquiring", "Configuring", "Busy", "Idle", "Releasing"]

    def __init__(
        self,
        uuid: str,
        size: str,
        dns_name: str,
        rate: float,
        promo: bool,
        app: str,
        state: str = None,
        gpus: List[str] = None,
        vram: int = None,
        ram: int = None,
        num_cpus: int = None,
    ):
        """Constructor for new a Machine object.

        Args:
            uuid (str): The unique machine identifier associated with this machine.
            size (str): The acronym for this machine instance that identifies its capabilities.
            dns_name (str): The DNS name assigned to this machine.
            rate (float): The hourly rate for this machine in USD.
            promo (bool): Whether this machine is being given a promotional rate or not.
            app (str): The application name of the workload being executed on this machine.
            state (str): The current state of this machine, one of "Acquiring", "Configuring", "Busy", "Idle" or "Releasing"
            gpus (list of str): The GPUs for this machine or None if this machine doesn't have any gpus.
            vram (int): The total GPU RAM for this machine in GiB or None if this machine doesn't have any gpus.
            ram (int): The amount of RAM in GiB for this machine.
            num_cpus (int): The number of cpus for this machine.
        """
        self._uuid = uuid
        self._size = size
        self._dns_name = dns_name
        self._rate = rate
        self._promo = promo
        self._app = app
        self._state = state
        self._gpus = gpus
        self._vram = vram
        self._ram = ram
        self._num_cpus = num_cpus
        self._last_refresh = time.time()

    @classmethod
    def reconstruct(cls, machine_map):
        return (
            machine_map["uuid"],
            machine_map["name"],
            machine_map["dnsName"],
            machine_map["rate"],
            machine_map["promo"],
            machine_map["app"],
            machine_map["state"],
            [machine_map["graphicsCardType"] * machine_map["graphicsNumCards"]],
            round(machine_map["graphicsMemory"] / 1024**3),
            round(machine_map["memorySize"] / 1024**3),
            machine_map["computeCores"][1],
        )

    def _refresh(self):
        now = time.time()
        if now - self._last_refresh > 5:
            self._last_refresh = now
            response = json.loads(optumi.core.get_machines().text)
            for machine in response["machines"]:
                if machine["uuid"] == self._uuid:
                    (
                        _,
                        _,
                        self._dns_name,
                        self._rate,
                        self._promo,
                        self._app,
                        self._state,
                    ) = Machine.reconstruct(machine)

    def release(self, override: bool = False):
        """Release the dynamically allocated machine.

        Args:
            override (bool, optional): Whether to allow releasing a machine with an active workload. Defaults to False.

        Raises:
            OptumiException: Raised if override is False and there is an active workload running on the machine.
        """
        if optumi.utils.is_dynamic():
            from .Workloads import Workloads

            current = Workloads.current()
            if current.machine._uuid == self._uuid:
                print("Releasing current machine")
                optumi.core.delete_machine(self._uuid)
                current.stop()
        else:
            workload = self.workload
            if workload != None:
                if override:
                    workload.stop()
                else:
                    raise OptumiException(
                        "Workload "
                        + str(workload)
                        + " is running on this machine. Stop the workload using workload.stop() or pass override=True into machine.release() to stop the workload before releasing."
                    )
            print("Releasing machine " + str(self) + "...")
            optumi.core.delete_machine(self._uuid)
            print("...completed")

    def is_visible(self):
        self._refresh()
        if (
            self._state == "requisition requested"
            or self._state == "requisition in progress"
            or self._state == "requisition completed"
            or self._state == "requisition completed"
            or self._state == "setup completed"
        ):
            return True
        return False

    @property
    def size(self):
        """Obtain the size of the machine.

        Returns:
            str: The size of this machine instance.
        """
        self._refresh()
        return self._size

    @property
    def rate(self):
        """Obtain the billing rate of the machine.

        Returns:
            float: The billing rate of this machine instance.
        """
        self._refresh()
        return self._rate

    @property
    def promo(self):
        """Determine whether a promotional rate applies to the machine.

        Returns:
            bool: Whether a promotional rate is applied to this machine instance.
        """
        self._refresh()
        return self._promo

    @property
    def dns_name(self):
        """Obtain the domain name for the machine.

        Returns:
            string: The domain name for this machine instance.
        """
        self._refresh()
        return self._dns_name

    @property
    def workload(self):
        """Obtain the workload running on the machine.

        Returns:
            Workload: The Workload object running on the machine instance, if any, otherwise None.
        """
        self._refresh()
        if self._app == None:
            return None
        from .Workloads import Workloads

        ws = Workloads.list()
        for w in ws:
            if w._workload_uuid == self._app:
                return w

    @property
    def status(self):
        """Obtain the status of the machine.

        Returns:
            string: The status of this machine instance as "Acquiring", "Configuring", "Busy", "Idle" or "Releasing".
        """
        if self._state in ["requisition requested", "requisition in progress"]:
            return "Acquiring"
        elif self._state in ["requisition completed"]:
            return "Configuring"
        elif self._state in ["setup completed"]:
            return "Busy" if self._app != None else "Idle"
        elif self._state in [
            "teardown requested",
            "sequestration requested",
            "sequestration in progress",
            "sequestration completed",
        ]:
            return "Releasing"
        else:
            return ""

    @property
    def gpus(self):
        """Obtain the gpus for this machine.

        Returns:
            list of str: The gpus for this machine instance.
        """
        self._refresh()
        return self._gpus
    
    @property
    def vram(self):
        """Obtain the VRAM for this machine.

        Returns:
            int: The VRAM for this machine instance in GiB.
        """
        self._refresh()
        return self._vram

    @property
    def ram(self):
        """Obtain the RAM for this machine.

        Returns:
            int: The RAM for this machine instance in GiB.
        """
        self._refresh()
        return self._ram

    @property
    def num_cpus(self):
        """Obtain the number of cpus for this machine.

        Returns:
            int: The number of cpus for this machine instance.
        """
        self._refresh()
        return self._num_cpus

    def __str__(self):
        return str(self._size) + " " + str(self._rate)
