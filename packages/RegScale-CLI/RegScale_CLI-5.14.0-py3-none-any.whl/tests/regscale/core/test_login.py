"""Test the login module."""
from unittest.mock import patch

from regscale.core.login import get_regscale_token


@patch("regscale.core.login.requests.post")
@patch.dict("os.environ", {"REGSCALE_DOMAIN": "example_value"})
def test_get_regscale_token(mock_post):
    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "example_id",
        "auth_token": "example_token",
    }

    result = get_regscale_token(username="example_user", password="example_password")
    result2 = get_regscale_token(
        username="example_user", password="example_password", domain="example2_domain"
    )

    assert result == ("example_id", "example_token")
    assert result2 == ("example_id", "example_token")
