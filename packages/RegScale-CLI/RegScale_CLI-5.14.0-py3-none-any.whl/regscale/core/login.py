"""Provide low-level, basic login."""
import json
from os import getenv
from typing import Tuple

import requests

from regscale.core.app.logz import create_logger

logger = create_logger()


def get_regscale_token(
    username: str = getenv("REGSCALE_USER"),
    password: str = getenv("REGSCALE_PASSWORD"),
    domain: str = getenv("REGSCALE_DOMAIN"),
) -> Tuple[str, str]:
    """Authenticate with RegScale and return a token

    :param username: a string defaulting to the envar REGSCALE_USERNAME
    :param password: a string defaulting to the envar REGSCALE_PASSWORD
    :param domain: a string representing the RegScale domain,
                   checks environment REGSCALE_DOMAIN
    :raises EnvironmentError: if domain is not passed or retrieved
    :returns: a tuple of user_id and auth_token
    """
    if domain is None:
        raise EnvironmentError(
            "REGSCALE_DOMAIN must be set if not passed as parameter."
        )
    if username is None:
        raise EnvironmentError(
            "REGSCALE_USERNAME must be set if not passed as parameter."
        )
    if password is None:
        raise EnvironmentError(
            "REGSCALE_PASSWORD must be set if not passed as parameter."
        )

    auth = {  # TODO - HTTP Basic Auth an minimum
        "userName": username,
        "password": password,
        "oldPassword": "",
    }
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "authorization": "yo dawg I heard you like auth, so I put auth in your auth so you can auth while you auth",
        # FIXME -- seriously why do we need this here?
    }
    logger.info("Logging into: %s", domain)
    # suggest structuring the login paths so that they all exist in one place
    response = requests.post(
        domain + "/api/authentication/login", json=auth, headers=headers
    )
    if response.status_code == 200:
        response_dict = response.json()
    else:
        raise ValueError(
            "Unable to authenticate with RegScale.  Check your credentials."
        )
    if isinstance(response_dict, str):
        response_dict = json.loads(response_dict)
    return response_dict["id"], response_dict["auth_token"]
