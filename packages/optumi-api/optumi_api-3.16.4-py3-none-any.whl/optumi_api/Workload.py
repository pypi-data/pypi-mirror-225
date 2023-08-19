##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import optumi_core as optumi

from .CloudStorage import CloudStorage
from .CloudFile import CloudFile
from .CloudFileVersion import CloudFileVersion
from .Log import Log
from .Summary import Summary
from .Program import Program
from .Machine import Machine

# from .utils import collapseUpdates

import json, time, os, re
from sys import exit

from typing import List, Tuple


class Workload:
    """A class representing an individual workload.

    This class contains information about program execution including logs, run numbers and input/output files.
    """

    status_values = ["queued", "launching", "running", "completed"]
    progress = ["silent", "summary", "detail"]  # add "status" later

    def __init__(self, path: str, program: str, workload_uuid: str, module_uuid: str, config: dict, run_num: int):
        """Constructor for a Workload object.

        Args:
            path (str): The file path of the workload.
            program (str): Program content (script, notebook, or container info) associated with this workload.
            workload_uuid (str): Unique identifier for the workload.
            module_uuid (str): Unique identifier for the module.
            config (dict): Dictionary containing configuration related to this workload. See NotebookConfig for dictionary layout.
            run_num (int): Numerical value corresponding to which run of the given program this workload represents.
        """
        self._path = path
        self._program = program

        self._workload_uuid = workload_uuid
        self._module_uuid = module_uuid

        self._nb_config = config

        self._run_num = run_num

        self._initializing_lines = []
        self._preparing_lines = []
        self._running_lines = []
        self._input_files = CloudStorage([])

        self._update_lines = []
        self._output = []
        self._monitoring = []
        self._last_patches = 0

        self._output_files = CloudStorage([])

        self._machine = None
        self._token = None

        self._last_refresh = time.time()

    def _handle_workload_update(self, workload: str):
        updates_to_print = []

        if "uuid" in workload and workload["uuid"] != None:
            self._workload_uuid = workload["uuid"]

        if "initializing" in workload and workload["initializing"] != None:
            for i in range(len(workload["initializing"])):
                self._initializing_lines.append((workload["initializing"][i], workload["initializingmod"][i]))

        if "preparing" in workload and workload["preparing"] != None:
            for i in range(len(workload["preparing"])):
                self._preparing_lines.append((workload["preparing"][i], workload["preparingmod"][i]))
                updates_to_print.append(self._preparing_lines[-1])

        if "running" in workload and workload["running"] != None:
            for i in range(len(workload["running"])):
                self._running_lines.append((workload["running"][i], workload["runningmod"][i]))
                updates_to_print.append(self._running_lines[-1])

        if "files" in workload and workload["files"] != None:
            self._input_files = CloudStorage(
                [
                    CloudFile(
                        workload["files"][i],
                        [
                            CloudFileVersion(
                                workload["files"][i],
                                workload["hashes"][i],
                                int(workload["filessize"][i]),
                                workload["filescrt"][i],
                                workload["filesmod"][i],
                            )
                        ],
                    )
                    for i in range(len(workload["files"]))
                ]
            )

        if "modules" in workload:
            for module in workload["modules"]:
                self._handle_module_update(module)

        return updates_to_print

    def _handle_module_update(self, module: str):
        output_to_print = []

        if "uuid" in module and module["uuid"] != None:
            self._module_uuid = module["uuid"]

        if "output" in module and module["output"] != None:
            for i in range(len(module["output"])):
                self._output.append((module["output"][i], module["outputmod"][i]))
                output_to_print.append(self._output[-1])

        if "updates" in module and module["updates"] != None:
            for i in range(len(module["updates"])):
                self._update_lines.append((module["updates"][i], module["updatesmod"][i]))

        if "files" in module and module["files"] != None:
            self._output_files = CloudStorage(
                [
                    CloudFile(
                        module["files"][i],
                        [
                            CloudFileVersion(
                                module["files"][i],
                                module["hashes"][i],
                                int(module["filessize"][i]),
                                module["filescrt"][i],
                                module["filesmod"][i],
                            )
                        ],
                    )
                    for i in range(len(module["files"]))
                ]
            )

        if "monitoring" in module and module["monitoring"] != None:
            for i in range(len(module["monitoring"])):
                self._monitoring.append((module["monitoring"][i], module["monitoringmod"][i]))

        if "patches" in module and module["patches"] != None:
            self._num_patches = len(module["patches"])

        if "notebook" in module and module["notebook"] != None:
            self._program = module["notebook"]

        if "machine" in module and module["machine"] != None:
            self._machine = Machine(*Machine.reconstruct(module["machine"]))

        if "token" in module and module["token"] != None:
            self._token = module["token"]

        return output_to_print

    @classmethod
    def reconstruct(cls, workload):
        w = Workload(
            workload["name"],
            None,
            workload["uuid"],
            workload["modules"][0]["uuid"] if len(workload["modules"]) > 0 else None,
            json.loads(workload["nbConfig"]),
            workload["runNum"],
        )

        w._handle_workload_update(workload)

        return w

    def _refresh(self, force=False):
        now = time.time()
        if now - self._last_refresh > 5:
            self._last_refresh = now
            if force or self.__get_status() != "completed":
                workloads = json.loads(optumi.core.get_workloads().text)
                if not self._workload_uuid in [workload["uuid"] for workload in workloads["jobs"]]:
                    return

                updates = json.loads(
                    optumi.pull_workload_status_updates(
                        [self._workload_uuid],
                        [len(self._initializing_lines)],
                        [len(self._preparing_lines)],
                        [len(self._running_lines)],
                    ).text
                )[self._workload_uuid]

                self._handle_workload_update(updates)

                if self._module_uuid:
                    updates = json.loads(
                        optumi.pull_module_status_updates(
                            [self._workload_uuid],
                            [self._module_uuid],
                            [len(self._update_lines)],
                            [len(self._output)],
                            [len(self._monitoring)],
                            [self._last_patches],
                            True,
                        ).content
                    )[self._module_uuid]

                    self._handle_module_update(updates)

    # def __print_status(self):
    #     collapsed = collapseUpdates(
    #         self._initializing_lines + self._preparing_lines + self._running_lines
    #     ).split("\n")
    #     line = collapsed[-1] if collapsed[-1] != "" else collapsed[-2]
    #     print("\b" * self._last_line_length, end="")
    #     print(" " * self._last_line_length, end="")
    #     print("\b" * self._last_line_length, end="")
    #     self._last_line_length = len(line)
    #     print(line, end="", flush=True)
    #     time.sleep(0.3)

    def __print_output(self, progress: str, output_to_print: List[Tuple[str, str]]):
        if progress == "detail":
            for output in output_to_print:
                print(output[0], end="")

    def __print_updates(self, progress: str, updates_to_print: List[Tuple[str, str]]):
        for update in updates_to_print:
            if re.sub("[^a-zA-Z]", "", update[0]) != "" and update[0] != "\n" and update[0] != "stop" and update[0] != "error":
                if progress == "summary":
                    print(
                        update[0] if update[0].endswith("\n") else self.__adjust_message(update[0]) + "\n",
                        end="",
                        flush=True,
                    )
                # elif progress == "status":
                #     self.__print_status()

    def wait(self, progress: str = "summary"):
        """Wait for a workload to complete by regularly checking the workload status.

        Args:
            progress (str, optional): Defines the level of verbosity in reporting the workload statusas as one of "summary", "detail" or "silent". Defaults to "summary".
        """
        self._last_line_length = 0

        self.__print_output(progress, self._output)
        self.__print_updates(
            progress,
            self._initializing_lines + self._preparing_lines + self._running_lines,
        )

        while True:
            workloads = json.loads(optumi.core.get_workloads().text)
            if not self._workload_uuid in [workload["uuid"] for workload in workloads["jobs"]]:
                print("Workload removed")
                break

            updates = json.loads(
                optumi.pull_workload_status_updates(
                    [self._workload_uuid],
                    [len(self._initializing_lines)],
                    [len(self._preparing_lines)],
                    [len(self._running_lines)],
                ).text
            )[self._workload_uuid]

            self.__print_updates(progress, self._handle_workload_update(updates))

            if self._module_uuid:
                updates = json.loads(
                    optumi.pull_module_status_updates(
                        [self._workload_uuid],
                        [self._module_uuid],
                        [len(self._update_lines)],
                        [len(self._output)],
                        [len(self._monitoring)],
                        [self._last_patches],
                        progress == "detail",
                    ).content
                )[self._module_uuid]

                token = self._token

                self.__print_output(progress, self._handle_module_update(updates))

                # If we set the token, print the link for the user to access his session and stop waiting
                if token == None and self._token != None:
                    print("Session available at: https://" + self._machine.dns_name + ":54321/?token=" + self._token)
                    return

            if self.__get_status() == "completed":
                break

            time.sleep(5)

        self._refresh(force=True)

        # if progress == "status":
        #     print()

    def stop(self, wait: bool = True):
        """Stop the current workload.

        Args:
            wait (bool, optional): If set to True, the function will wait till the workload has been terminated before returning. Defaults to True.
        """
        from .Workloads import Workloads

        if optumi.utils.is_dynamic() and Workloads.current()._workload_uuid == self._workload_uuid:
            print("Stopping current workload")
            # This is for sessions
            code = os.system("jupyter lab stop 54321")
            if code > 15:  # 15 is SIGTERM
                # This is for jobs
                exit(0)
            print("...completed")
        else:
            if self.status != "completed":
                print("Stopping workload " + self.name + "...")
                optumi.core.stop_notebook(self._workload_uuid)
                if wait and self.status == "running":
                    self.wait(progress="silent")
                print("...completed")
            else:
                print("Workload not running")

    def remove(self, wait: bool = True):
        """Remove the current workload."""
        if self.status != "completed":
            self.stop(wait)
        print("Removing workload " + self.name + "...")
        optumi.core.teardown_notebook(self._workload_uuid)
        print("...completed")

    @property
    def status(self):
        """Obtain the current status of the workload.

        Returns:
            str: The current status of the workload as "launching", "running" or "completed".
        """
        self._refresh()
        return self.__get_status()

    def __get_status(self):
        if len(self._preparing_lines) == 0:
            for update in self._initializing_lines:
                if Workload.__is_error(update):
                    return "completed"

        if len(self._running_lines) == 0:
            for update in self._preparing_lines:
                if Workload.__is_error(update) or Workload.__is_terminated(update):
                    return "completed"

        if len(self._update_lines) > 0:
            running = True
            for update in self._update_lines:
                if update[1] == "stop":
                    running = False
            if running:
                return "running"

        for update in self._running_lines:
            if Workload.__is_stop(update):
                return "completed"

        for update in self._preparing_lines:
            if Workload.__is_stop(update):
                return "running"

        return "launching"

    def __adjust_message(self, message: str):
        # We will say a session is starting until we can connect to it
        if self._nb_config["interactive"] and message == "Running" and self._token == None:
            return "Connecting"
        # We call a running app 'Connected'
        if self._nb_config["interactive"] and message == "Running":
            return "Connected"
        # We call a terminated or completed app 'closed',
        if self._nb_config["interactive"] and message == "Terminating":
            return "Closing"
        if self._nb_config["interactive"] and message == "Terminated":
            return "Closed"
        if self._nb_config["interactive"] and message == "Completed":
            return "Closed"
        return message

    @property
    def detailed_status(self):
        """Obtain the detailed status of this workload.

        Returns:
            str: The detailed status of this workload.
        """
        self._refresh()

        message = ""
        if Workload.__message(self._initializing_lines) != "":
            message = Workload.__message(self._initializing_lines)
        if Workload.__message(self._preparing_lines) != "":
            message = Workload.__message(self._preparing_lines)
        if Workload.__message(self._running_lines) != "":
            message = Workload.__message(self._running_lines)

        return message

    @property
    def all_detailed_status(self):
        """Obtain all detailed status of this workload.

        Returns:
            list of str: All detailed status of this workload.
        """
        self._refresh()
        
        updates = []
        for update in self._initializing_lines + self._preparing_lines + self._running_lines:
            line = update[0]
            modifier = update[1]
            if line != "error" and line != "stop" and line != "" and not modifier.startswith("{"):
                updates.append(self.__adjust_message(line))
        return updates

    @property
    def error(self):
        """Obtain wether this workload encountered an error.

        Returns:
            bool: Wether this workload encountered an error.
        """
        self._refresh()

        for update in self._initializing_lines:
            if Workload.__is_error(update):
                return True

        for update in self._preparing_lines:
            if Workload.__is_error(update):
                return True

        for update in self._running_lines:
            if Workload.__is_error(update):
                return True

        for update in self._update_lines:
            if update[1] == "error":
                return True

        return False

    @classmethod
    def __is_error(cls, update: Tuple[str, str]):
        line = update[0]
        modifier = update[1]
        if line == "error":
            return True
        if line != "error" and line != "stop" and line != "":
            if modifier.startswith("{"):
                jsonPayload = json.loads(modifier)
                if jsonPayload["level"] == "error":
                    return True
        return False

    @classmethod
    def __is_stop(cls, update: Tuple[str, str]):
        return update[0] == "stop"

    @classmethod
    def __is_terminated(cls, update: Tuple[str, str]):
        return update[0] == "Terminated"

    @classmethod
    def __message(cls, updates: List[Tuple[str, str]]):
        for update in reversed(updates):
            line = update[0]
            modifier = update[1]
            if line != "error" and line != "stop" and line != "" and not modifier.startswith("{"):
                return line
        return ""

    @property
    def log(self):
        """Obtain the log.

        Returns:
            Log: the log
        """
        self._refresh()
        if len(self._output) == 0:
            for workload in json.loads(optumi.core.get_workload_properties(self._workload_uuid, [], ["output"]).text)["jobs"]:
                self._handle_workload_update(workload)  # There will only be one job returned and it will be the correct one
        return Log(self._path, self._output)

    @property
    def summary(self):
        """Obtain the workload summary.

        Returns:
            Summary: The status summary of this workload.
        """
        self._refresh()
        return Summary(
            self._path,
            self._initializing_lines,
            self._preparing_lines,
            self._running_lines,
        )

    @property
    def program(self):
        """Obtain the program.

        Returns:
            Program: The program represented by this workload.
        """
        self._refresh()
        if self._program == None:
            for workload in json.loads(optumi.core.get_workload_properties(self._workload_uuid, [], ["notebook"]).text)["jobs"]:
                self._handle_workload_update(workload)  # There will only be one job returned and it will be the correct one
        return Program(self._path, self._run_num, self._program)

    @property
    def input_files(self):
        """Obtain the input files specified for this workload.

        Returns:
            CloudStorage: The list of input files in Optumi cloud storage.
        """
        self._refresh()
        return self._input_files

    @property
    def output_files(self):
        """Obtain the output files generatd by this workload.

        Returns:
            CloudStorage: The list of output files in Optumi cloud storage.
        """
        self._refresh()
        if self._program == None:
            for workload in json.loads(optumi.core.get_workload_properties(self._workload_uuid, [], ["files"]).text)["jobs"]:
                self._handle_workload_update(workload)  # There will only be one job returned and it will be the correct one
        return self._output_files

    @property
    def name(self):
        """Obtain the name of this workload.

        Returns:
            str: The composed name of the workload containing the assigned name and the run number.
        """
        return self._path.split("/")[-1] + " (Run #" + str(self._run_num) + ")"

    @property
    def path(self):
        """Obtain the pathname of this workload.

        Returns:
            str: The pathname of the workload.
        """
        return optumi.utils.normalize_path(self._path, strict=False)

    @property
    def machine(self):
        """Obtain the machine this workload is or was running on.

        Returns:
            Machine: The Machine object representing the machine that the workload is or was running on.
        """
        self._refresh()
        return self._machine

    def __str__(self):
        return str(self.name)
