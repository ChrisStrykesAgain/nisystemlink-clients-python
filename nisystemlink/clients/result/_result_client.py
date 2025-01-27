"""Implementations of the Result Client."""

from typing import List, Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import delete, get, post
from nisystemlink.clients.result.models import Result
from uplink import Field, Query, retry, returns

from . import models


@retry(when=retry.when.status(429), stop=retry.stop.after_attempt(5))
class ResultClient(BaseClient):

    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, the
                :class:`HttpConfigurationManager <nisystemlink.clients.core.HttpConfigurationManager>`
                is used to obtain the configuration.

        Raises:
            ApiException: if unable to communicate with the Result Service.
        """
        if configuration is None:
            configuration = core.HttpConfigurationManager.get_configuration()
        super().__init__(configuration, base_path="/nitestmonitor/v2/")

    @post("results", args=[Field("results")])
    def create_results(
        self, results: List[Result]
    ) -> models.CreateResultsPartialSuccess:
        """Creates one or more results and returns errors for failed creations.

        Args:
            results: A list of results to attempt to create.

        Returns: A list of created results, results that failed to create, and errors for
            failures.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` service of provided invalid
                arguments.
        """
        ...

    @get(
        "results",
        args=[Query("continuationToken"), Query("take"), Query("returnCount")],
    )
    def get_results_paged(
        self,
        continuation_token: Optional[str] = None,
        take: Optional[int] = None,
        return_count: Optional[bool] = None,
    ) -> models.PagedResults:
        """Reads a list of results.

        Args:
            continuation_token: The token used to paginate results.
            take: The number of results to get in this request.
            return_count: Whether or not to return the total number of results available.

        Returns:
            A list of results.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service
                or provided an invalid argument.
        """
        ...

    @get("results/{id}")
    def get_result(self, id: str) -> models.Result:
        """Retrieves a single result by id.

        Args:
            id (str): Unique ID of a result.

        Returns:
            The single result matching `id`

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service
                or provided an invalid argument.
        """
        ...

    @post("query-results")
    def query_results_paged(
        self, query: models.QueryResultsRequest
    ) -> models.PagedResults:
        """Queries for results that match the filter.

        Args:
            query : The query contains a DynamicLINQ query string in addition to other details
                about how to filter and return the list of results.

        Returns:
            A paged list of results with a continuation token to get the next page.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service or provided invalid
                arguments.
        """
        ...

    @returns.json  # type: ignore
    @post("query-result-values")
    def query_result_values(self, query: models.QueryResultValuesRequest) -> List[str]:
        """Queries for results that match the query and returns a list of the requested field.

        Args:
            query : The query for the fields.

        Returns:
            A list of the values of the queried field.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service or provided
            invalid arguments.
        """
        ...

    @post("update-results", args=[Field("results"), Field("replace")])
    def update_results(
        self, results: List[Result], replace: bool = False
    ) -> models.CreateResultsPartialSuccess:
        """Updates a list of results with optional field replacement.

        Args:
            `results`: A list of results to update. Results are matched for update by id.
            `replace`: Replace the existing fields instead of merging them. Defaults to `False`.
                If this is `True`, then `keywords` and `properties` for the result will be
                    replaced by what is in the `results` provided in this request.
                If this is `False`, then the `keywords` and `properties` in this request will
                    merge with what is already present in the server resource.

        Returns: A list of updates results, results that failed to update, and errors for
            failures.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service
                or provided an invalid argument.
        """
        ...

    @delete("results/{id}")
    def delete_result(self, id: str) -> None:
        """Deletes a single result by id.

        Args:
            id (str): Unique ID of a result.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service
                or provided an invalid argument.
        """
        ...

    @post("delete-results", args=[Field("ids")])
    def delete_results(
        self, ids: List[str]
    ) -> Optional[models.DeleteResultsPartialSuccess]:
        """Deletes multiple results.

        Args:
            ids (List[str]): List of unique IDs of results.

        Returns:
            A partial success if any results failed to delete, or None if all
            results were deleted successfully.

        Raises:
            ApiException: if unable to communicate with the ``/nitestmonitor`` Service
                or provided an invalid argument.
        """
        ...