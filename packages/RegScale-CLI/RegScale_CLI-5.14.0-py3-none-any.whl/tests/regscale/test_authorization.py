"""Test the platform module."""
import os
from unittest.mock import MagicMock, patch

import pytest

from regscale.core.app.application import Application
from regscale.core.login import get_regscale_token
from regscale.models import platform

PATH = "regscale.models.platform"


@pytest.fixture
def env_variables():
    os.environ["REGSCALE_USER"] = "testuser"
    os.environ["REGSCALE_PASSWORD"] = "testpassword"
    os.environ["REGSCALE_DOMAIN"] = "https://testdomain.com"


@patch(f"{PATH}.get_regscale_token", return_value=("billy", "zane"))
def test_RegScaleAuth_model_behaves(mock_get_regscale_token):
    """The RegScaleAuth BaseModel class does lots of things, let's test them."""
    un = "funkenstein"
    pw = "groovin'tothewaveoftheflag"
    domain = "disinfo.org"
    model = platform.RegScaleAuth.authenticate(
        username=un,
        password=pw,
        domain=domain,
    )
    mock_get_regscale_token.assert_called_once()
    assert isinstance(model, platform.RegScaleAuth)
    assert model.token == "Bearer zane"
    assert model.user_id == "billy"
    assert model.username == un
    assert model.password.get_secret_value() == pw
    assert model.domain == domain


def test_RegScaleAuth_model():
    """The RegScaleAuth BaseModel class is based"""
    app = Application()
    domain = app.config["domain"]
    model = platform.RegScaleAuth.authenticate(
        domain=domain,
    )
    assert model.token


def test_get_regscale_token(env_variables):
    user_id, auth_token = get_regscale_token()
    print(auth_token)
    assert isinstance(user_id, str)
    assert isinstance(auth_token, str)
