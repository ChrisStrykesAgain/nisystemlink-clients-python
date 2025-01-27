"""Integration tests for AuthClient."""

import pytest
from nisystemlink.clients.core._uplink._base_client import BaseClient


@pytest.fixture(scope="class")
def client(enterprise_config) -> BaseClient:
    """Fixture to create a AuthClient instance."""
    return BaseClient(enterprise_config)


@pytest.mark.enterprise
@pytest.mark.integration
class TestAuthClient:
    def test__get_auth_info__succeeds(self, client: BaseClient):
        """Test the case of getting caller information with SystemLink Credentials."""
        response = client.auth_client.get_auth_info()
        assert response is not None
