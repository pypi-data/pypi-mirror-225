##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

import re, copy

from typing import List, Tuple

from contextlib import contextmanager
import sys, os


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


# Remove characters that are overwritten by newline characters
def fixCarriageReturn(txt: str):
    txt = re.compile(r"\r+\n", re.M).sub("\n", txt)  # \r followed by \n --> newline
    while not re.search(r"\r[^$]", txt) is None:
        base = re.compile(r"^(.*)\r+", re.M).match(txt)[1]
        insert = re.compile(r"\r+(.*)$", re.M).match(txt)[1]
        insert = insert + base.slice(len(insert), len(base))
        txt = re.compile(r"\r+.*$", re.M).sub("\r", txt)
        txt = re.compile(r"^.*\r", re.M).sub(insert, txt)
    return txt


# Remove characters that are overwritten by backspace characters
def fixBackspace(txt: str):
    tmp = txt
    while True:
        txt = tmp
        # Cancel out anything-but-newline followed by backspace
        tmp = re.sub(r"\n?[^\x08]\x08", "", txt)
        if len(tmp) >= len(txt):
            break
    return txt


def collapseUpdates(updates: List[Tuple[str, str]]):
    message = ""
    last_non_detail = ""
    for line, modifier in updates:
        if line != "error" and line != "stop" and line != "launched" and line != "closed" and line != "":
            if not modifier.startswith("{"):
                # Suppress duplicate update messages
                if line != last_non_detail:
                    last_non_detail = line
            message += line
            if not message.endswith("\n"):
                message += "\n"

    return fixBackspace(fixCarriageReturn(message))


def collapseNotebook(json_notebook):
    nb = copy.deepcopy(json_notebook)
    # First pass through the notebook combines multiple subsequent output streams into one
    for cell in nb["cells"]:
        if "outputs" in cell:
            last_stream = ""
            last_name = None
            new_outputs = []
            for output in cell["outputs"]:
                # Normalize the output
                if output["output_type"] == "stream":
                    if type(output["text"]) == list:
                        output["text"] = "".join(output["text"])

                # Collapse streams
                if output["output_type"] == "stream" and last_stream and output["name"] == last_name:
                    last_stream += output["text"]
                    output["text"] = last_stream
                    new_outputs.pop()
                elif output["output_type"] == "stream":
                    last_stream = output["text"]
                    last_name = output["name"]
                else:
                    last_stream = ""
                    last_name = None
                new_outputs.append(output)
            cell["outputs"] = new_outputs

    # Second pass through the notebook collapses backspaced output
    for cell in nb["cells"]:
        if "outputs" in cell:
            for output in cell["outputs"]:
                # Fix backspaces
                if output["output_type"] == "stream":
                    output["text"] = fixBackspace(output["text"])
                # Un-normalize the output
                if output["output_type"] == "stream":
                    if type(output["text"]) == list:
                        output["text"] = output["text"].split("\n")

    return nb
