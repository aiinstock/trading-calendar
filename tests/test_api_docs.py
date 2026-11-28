import pytest

from trading_calendar.main import CONTEXT_PATH


@pytest.mark.parametrize(
    "suffix",
    ["/docs", "/redoc", "/docs/oauth2-redirect", "/api/v1/openapi.json"],
)
def test_api_documentation_disabled(client, suffix):
    assert client.get(CONTEXT_PATH + suffix).status_code == 404
