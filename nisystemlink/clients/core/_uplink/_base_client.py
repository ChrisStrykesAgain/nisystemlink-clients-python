# mypy: disable-error-code = misc

from typing import Dict, List, Optional

from nisystemlink.clients import core

from ._core_client import CoreClient
from ..helpers.auth._auth_client import AuthClient


class BaseClient(CoreClient):
    """Base class for SystemLink clients, which includes basic helper functions."""

    def __init__(self, configuration: core.HttpConfiguration, base_path: str = ""):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about how to connect.
            base_path: The base path for all API calls.
        """
        super().__init__(
            configuration=configuration,
            base_path=base_path,
        )
        self.auth_client = AuthClient(configuration)

    def get_workspaces(
        self, desired_workspace_names: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """Gets a list of workspaces.

        Args:
            desired_workspace_names: The specific workspaces to return. If not provided, all workspaces are returned.

        Returns:
            Dict[str, str]: A dictionary of workspace names and their corresponding IDs.
        """
        all_workspaces = self.auth_client.get_auth_info().workspaces
        if not all_workspaces:
            return {}
        if desired_workspace_names:
            return {
                workspace.name: workspace.id
                for workspace in all_workspaces
                if workspace.name in desired_workspace_names
            }
        else:
            return {workspace.name: workspace.id for workspace in all_workspaces}
