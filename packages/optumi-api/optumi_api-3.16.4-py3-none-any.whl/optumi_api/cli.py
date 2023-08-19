from .api import *

import argparse

description = """
Optumi is a cloud service that makes it easy for data scientists to develop & train ML models on powerful computing resources.

We offer a Python API library, a web application and a JupyterLab extension to launch and manage python scripts and notebooks in the cloud. We offer access to a wide variety of powerful cloud resources used for interactive sessions or batch jobs.
"""


def main():
    parser = argparse.ArgumentParser(prog="optumi-api", description=description)

    subparsers = parser.add_subparsers(title="Commands", dest="command")

    login_command = "login"
    login_parser = subparsers.add_parser(login_command, help="Log in to the Optumi platform")
    login_parser.add_argument("--token", help="A connection token (can be generated in the webapp)")
    login_parser.add_argument("--no-save-token", action="store_true", help="Whether to store the connection token on the disk")

    logout_command = "logout"
    login_parser = subparsers.add_parser(logout_command, help="Log out of the Optumi platform")
    login_parser.add_argument("--no-remove-token", action="store_true", help="Whether to remove the connection token from the disk")

    args = parser.parse_args()

    if args.command == login_command:
        login(args.token, not args.no_save_token)
    elif args.command == logout_command:
        logout(not args.no_remove_token)
