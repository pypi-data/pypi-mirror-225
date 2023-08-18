#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Functions used to interact with RegScale API """

# standard imports
import mimetypes
import os
import re
import sys
from io import BytesIO
from typing import Optional

from requests import JSONDecodeError

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import (
    error_and_exit,
    get_file_name,
    get_file_type,
)
from regscale.models.regscale_models.modules import Modules

logger = create_logger()


def send_email(api: Api, domain: str, payload: dict) -> bool:
    """
    Function to use the RegScale email API and send an email, returns bool on whether API call was successful
    :param Api api: API object
    :param str domain: RegScale URL of instance
    :param dict payload: email payload
    :return: Boolean if RegScale api was successful
    :rtype: bool
    """
    # use the api to post the dict payload passed
    response = api.post(url=f"{domain}/api/email", json=payload)
    # see if api call was successful and return boolean
    return response.status_code == 200


def update_regscale_config(str_param: str, val: any, app: Application = None) -> str:
    """
    Update config in init.yaml
    :param str str_param: config parameter to update
    :param any val: config parameter value to update
    :param app: Application object
    :return: Verification message
    :rtype: str
    """
    if not app:
        app = Application()
    config = app.config
    # update config param
    # existing params will be overwritten, new params will be added
    config[str_param] = val
    # write the changes back to file
    app.save_config(config)
    logger.debug(f"Parameter '{str_param}' set to '{val}'.")
    return "Config updated"


def create_regscale_assessment(url: str, new_assessment: dict, api: Api) -> int:
    """
    Function to create a new assessment in RegScale and returns the new assessment's ID
    :param str url: RegScale instance URL to create the assessment
    :param dict new_assessment: API assessment payload
    :param Api api: API object
    :return: New RegScale assessment ID
    :rtype: int
    """
    assessment_res = api.post(url=url, json=new_assessment)
    return assessment_res.json()["id"] if assessment_res.status_code == 200 else None


def get_issues_by_integration_field(api: Api, field: str) -> list:
    """
    Function to get the RegScale issues for the provided integration field that has data populated
    :param Api api: API Object
    :param field: Integration field to filter the RegScale issues
    :raises: JSONDecodeError if API response cannot be converted to a json object
    :return: List of issues with the provided integration field populated
    :rtype: list
    """
    # set the url with the field provided
    url = f'{api.config["domain"]}/api/issues/getAllByIntegrationField/{field}'
    # get the data via API
    response = api.get(url=url)
    try:
        # try to convert the data to a json
        issues = response.json()
    except JSONDecodeError as ex:
        # unable to convert the data to a json, display error and exit
        error_and_exit(f"Unable to retrieve issues from RegScale.\n{ex}")
    # return the issues
    return issues


def verify_provided_module(module: str) -> None:
    """
    Function to check the provided module is a valid RegScale module and will display the acceptable RegScale modules
    :param str module: desired module
    :raises: General Error if the provided module is not a valid RegScale module
    :return: None
    """
    if module not in Modules().api_names():
        Modules().to_table()
        error_and_exit("Please provide an option from the Accepted Value column.")


def lookup_reg_assets_by_parent(api: Api, parent_id: int, module: str) -> list:
    """
    Function to get assets from RegScale via API with the provided System Security Plan ID
    :param Api api: API object
    :param int parent_id: RegScale System Security Plan ID
    :param str module: RegScale module
    :raises: JSONDecodeError if API response cannot be converted to a json object
    :raises: General Error if API response is not successful
    :return: List of data returned from RegScale API
    :rtype: list
    """
    # verify provided module
    verify_provided_module(module)

    config = api.config
    regscale_assets_url = (
        f"{config['domain']}/api/assets/getAllByParent/{parent_id}/{module}"
    )
    results = []

    response = api.get(url=regscale_assets_url)
    if response.ok:
        try:
            results = response.json()
        except JSONDecodeError:
            logger.warning(
                f"No assets associated with the provided ID and module: {module} #{parent_id}."
            )
    else:
        error_and_exit(
            f"Unable to get assets from RegScale. Received:{response.status_code}\n{response.text}"
        )
    return results


def get_all_from_module(api: Api, module: str, timeout: int = 300) -> list[dict]:
    """
    Function to retrieve all records for the provided Module in RegScale via API
    :param Api api: API object
    :param str module: RegScale Module
    :param int timeout: Timeout for the API call, defaults to 300 seconds
    :raises: JSONDecodeError if API response cannot be converted to a json object
    :return: list of objects from RegScale API of the provided module
    :rtype: list[dict]
    """
    # verify provided module
    verify_provided_module(module)

    # get the original timeout and update the timeout to the provided timeout
    original_timeout = api.timeout
    api.timeout = timeout

    # set URL for API call
    regscale_url = f"{api.config['domain']}/api/{module}/getAll"

    # update timeout for large datasets and get the original timeout
    original_timeout = api.timeout
    api.timeout = 300

    logger.info("Fetching full list of %s from RegScale.", module)
    # get the full list of provided module
    try:
        regscale_response = api.get(regscale_url)
        regscale_data = regscale_response.json()
        # reset the timeout to the original timeout
        api.timeout = original_timeout
    except JSONDecodeError:
        error_and_exit(f"Unable to retrieve full list of {module} from RegScale.")
    logger.info("Retrieved %s %s from RegScale.", len(regscale_data), module)
    return regscale_data


def format_control(control: str):
    """Convert a verbose control id to a regscale friendly control id,
        e.g. AC-2 (1) becomes ac-2.1
             AC-2(1) becomes ac-2.1

    :param control: Verbose Control
    :return: RegScale friendly control
    """
    # Define a regular expression pattern to match the parts of the string
    # pattern = r'^([A-Z]{2})-(\d+)\s\((\d+)\)$'
    pattern = r"^([A-Z]{2})-(\d+)\s?\((\d+)\)$"

    # Use re.sub() to replace the matched parts of the string with the desired format
    new_string = re.sub(pattern, r"\1-\2.\3", control)

    return new_string.lower()  # Output: ac-2.1


def get_user(api: Api, user_id: str) -> list:
    """
    Function to get the provided user_id from RegScale via API
    :param Api api: API Object
    :param str user_id: the RegScale user's GUID
    :raises: JSONDecodeError if API response cannot be converted to a json object
    :return: list containing the user's information
    :rtype: str
    """
    user_data = []
    url = f'{api.config["domain"]}/api/accounts/find/{user_id}'

    response = api.get(url)
    try:
        user_data = response.json()
    except JSONDecodeError:
        logger.error(
            "Unable to retrieve user from RegScale for the provided user id: %s",
            user_id,
        )
    return user_data
