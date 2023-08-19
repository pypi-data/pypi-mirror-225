##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from ._version import __version__


from .LoginServer import login as oauth_login
from .HoldoverTime import HoldoverTime
from .Workloads import Workloads

import json, webbrowser
import phonenumbers
from pwinput import pwinput


# Optumi imports
import optumi_core as optumi
from optumi_core.exceptions import (
    NotLoggedInException,
    OptumiException,
)

from typing import Union

DEBUG_LOGIN = False


def docs(open: bool = True):
    """Print or open the url for full Optumi API documentation.

    Args:
        open (bool, optional): Wether to print the url or open the docs in a new browser tab. Defaults to True.
    """
    url = "https://portal.optumi.net/docs"
    if open:
        try:
            webbrowser.open_new_tab(url)
        except webbrowser.Error:
            pass
    else:
        print("Optumi API documentation is available at: " + url)


docs(False)


def login(
    connection_token: str = None,
    save_token: bool = True,
):
    """Log in to the Optumi service platform.

    If a connection token is provided - as an argument or stored on the local disk - it will be leveraged to complete the login operation otherwise a new browser tab is opened to prompt the user for credentials.

    Args:
        connection_token (str, optional): A connection token (can be generated in the webapp). Defaults to None.
        save_token (bool, optional): Whether to store the connection token on the disk. Defaults to True.

    Raises:
        NotLoggedInException: Raised if the login was not successful.
        OptumiException: Raised if the browser login could not be initiated.
    """

    def handle_login_response(login_status, message):
        if login_status == -2:  # -3 means we have a version problem
            split = message.split("-")[0].split(".")
            downgrade = __version__.split(".")[1] > split[1]
            compatible_version = ">=" + split[0] + "." + split[1] + ".0,<" + split[0] + "." + str(int(split[1]) + 1) + ".0"

            raise NotLoggedInException(
                "Sorry, we've noticed an incompatibility between this API version and our backend. To switch to a compatible extension run: pip install \"optumi-api"
                + compatible_version
                + '"'
                if downgrade
                else "We've made enhancements that require a new API version. To upgrade your extension, run:pip install \"optumi-api"
                + compatible_version
                + '"'
            )
        if login_status != 1:
            raise NotLoggedInException("Login failed: " + message)

    # On a dynamic machine we do not need to get an okta token
    if optumi.utils.is_dynamic():
        if DEBUG_LOGIN:
            print("Dynamic login")
        if not optumi.login.check_login():
            if DEBUG_LOGIN:
                print("Not logged in")
            login_status, message = optumi.login.login_rest_server(
                token="",
                login_type="dynamic",
                save_token=save_token,
            )
    else:
        if DEBUG_LOGIN:
            print("Normal login")
        if connection_token == None:
            if DEBUG_LOGIN:
                print("No connection token")
            if DEBUG_LOGIN:
                print("Trying login with disk token")
            # Try to log in with the login token from the disk
            login_status, message = optumi.login.login_rest_server(login_type="token", save_token=save_token)

            # Fall back on the browser login
            if login_status != 1:
                if DEBUG_LOGIN:
                    print("Trying browser login")

                headless = True
                try:
                    webbrowser.get()
                    headless = False
                except webbrowser.Error:
                    pass

                if headless:
                    # Prompt the user in the cli for their connection token
                    print("You can find your connection token in the settings tab here: https://portal.optumi.net")
                    connection_token = pwinput(prompt="Enter connection token: ")

                    if DEBUG_LOGIN:
                        print("Connection token")
                    login_status, message = optumi.login.login_rest_server(
                        token=connection_token,
                        login_type="token",
                        save_token=save_token,
                    )
                    handle_login_response(login_status, message)
                else:
                    # Open a new browser tab and complete the browser login
                    try:
                        login_status, message = optumi.login.login_rest_server(
                            token=oauth_login(),
                            login_type="oauth",
                            save_token=save_token,
                        )
                        handle_login_response(login_status, message)
                    except RuntimeError:
                        raise OptumiException(
                            "Unable to perform browser login from Notebook. Try logging in with a connection token as shown here: https://optumi.notion.site/Login-using-a-connection-token-710bccdeaf734cbf825aae94b79a8109"
                        )
        else:
            if DEBUG_LOGIN:
                print("Connection token")
            login_status, message = optumi.login.login_rest_server(
                token=connection_token,
                login_type="token",
                save_token=save_token,
            )
            handle_login_response(login_status, message)

    user_information = json.loads(optumi.core.get_user_information(True).text)

    print("Logged in", user_information["name"])


def logout(remove_token: bool = True):
    """Log out of the Optumi service platform, optionally removing any stored connection token.

    Args:
        remove_token (bool, optional): Whether to remove the connection token from the disk. Defaults to True.
    """
    name = None
    try:
        user_information = json.loads(optumi.core.get_user_information(True).text)
        name = user_information["name"]
    except Exception:
        pass

    try:
        optumi.login.logout(remove_token=remove_token)
    except NotLoggedInException:
        pass

    if name:
        print("Logged out", name)


def get_phone_number():
    """Obtain the user's phone number.

    Returns:
        str: The user's international phone number, starting with a plus sign ('+') and the country code.
    """
    return json.loads(optumi.core.get_user_information(False).text)["phoneNumber"]


def set_phone_number(phone_number: str):
    """Prompt the user for a verification code and store the phone number in the user's profile.

    Args:
        phone_number (str): The international phone number that the user wants to store.

    Raises:
        OptumiException: Raised if the phone number is invalid or the verification code is incorrect.
    """
    if phone_number == "":
        optumi.core.clear_phone_number()
    else:
        number = phonenumbers.parse(phone_number, "US")
        if not phonenumbers.is_valid_number(number):
            raise OptumiException("The string supplied did not seem to be a valid phone number.")

        formatted_number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)

        optumi.core.send_verification_code(formatted_number)

        while True:
            code = input("Enter code sent to " + formatted_number + ": ")
            text = optumi.core.check_verification_code(formatted_number, code).text

            if text:
                print(text)
                # This is kind of sketchy but wont break if the message changes, it will just continue prompting the user for their code
                if text == "Max check attempts reached":
                    break
            else:
                optumi.set_user_information("notificationsEnabled", True)
                break


def get_holdover_time():
    """Obtain the current holdover time.

    The holdover time is the period of time that machines are retained (provisioned) after a workload finishes. Holdover time is global and applies to all workloads.

    Returns:
        The holdover time as an HoldoverTime object.
    """
    return HoldoverTime(int(json.loads(optumi.core.get_user_information(False).text)["userHoldoverTime"]) // 60)  # Convert to minutes


def set_holdover_time(holdover_time: Union[int, HoldoverTime]):
    """Configure the holdover time.

    The holdover time is the period of time that machines are retained (provisioned) after a workload finishes. Holdover time is global and applies to all workloads.

    Args:
        holdover_time (int or HoldoverTime): The holdover time as either an integer representing minutes or a HoldoverTime object.
    """
    optumi.core.set_user_information(
        "userHoldoverTime",
        str(holdover_time.seconds if type(holdover_time) is HoldoverTime else holdover_time * 60),  # Convert to seconds
    )


def get_connection_token(forceNew: bool = False):
    """Obtain a connection token.

    Args:
        forceNew (bool, optional): If true, generate a new connection token and return it, otherwise return the existing connection token. Defaults to False.

    Returns:
        A dictionary representing the connection token in the format {'expiration': '<ISO 8601 string>', 'token': '<token string>'}
    """
    return json.loads(optumi.core.get_connection_token(forceNew).text)


def redeem_signup_code(signupCode: str):
    """Redeem a signup code used to obtain access to the Optumi service platform.

    Args:
        signupCode (str): Signup code provided by Optumi.
    """
    optumi.core.redeem_signup_code(signupCode)


def send_notification(message: str, details=True):
    """Send a notification via text message to the phone number associated with the current user.

    Optionally, additional details about the workload can be attached to the end of the message.
    If no phone number is associated with the user, a warning message will be printed to console instead.

    Args:
        message (str): The message to send as a string.
        details (bool, optional): Whether to append details about the current workload (only applies when this function is called on a machine that was dynamically allocated by Optumi). Defaults to True.
    """
    if get_phone_number():
        try:
            optumi.core.send_notification("From " + str(Workloads.current()) + ": " + message if details and optumi.utils.is_dynamic() else message)
        except:
            optumi.core.send_notification(message)
    else:
        print("Unable to send notification - no phone number specified")


def get_workload_limit():
    """Obtain the current workload limit.

    The workload limit is the maximum number of workloads that can be running in parallel.

    Returns:
        The workload limit as an integer.
    """
    return int(json.loads(optumi.core.get_user_information(False).text)["maxJobs"])
