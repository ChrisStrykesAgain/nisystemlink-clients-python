"""Integration tests for BaseClient."""

import pytest
from nisystemlink.clients.core._uplink._base_client import BaseClient


@pytest.fixture(scope="class")
def client(enterprise_config) -> BaseClient:
    """Fixture to create a AuthClient instance."""
    return BaseClient(enterprise_config)


@pytest.mark.enterprise
@pytest.mark.integration
class TestBaseClient:
    def test__get_single_workspace__succeeds(self, client: BaseClient):
        """Test the case of getting a single (Default) workspace."""
        response = client.get_workspaces(["Default"])
        assert response["Default"] is not None

    def test__get_all_workspaces__succeeds(self, client: BaseClient):
        """Test the case of getting all workspaces."""
        response = client.get_workspaces()
        assert response is not None
