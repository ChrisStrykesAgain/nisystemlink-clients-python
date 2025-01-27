from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


class ResultField(str, Enum):
    """The valid ways to order a result query."""

    ID = "ID"
    STARTED_AT = "STARTED_AT"
    UPDATED_AT = "UPDATED_AT"
    PROGRAM_NAME = "PROGRAM_NAME"
    SYSTEM_ID = "SYSTEM_ID"
    HOST_NAME = "HOST_NAME"
    OPERATOR = "OPERATOR"
    SERIAL_NUMBER = "SERIAL_NUMBER"
    PART_NUMBER = "PART_NUMBER"
    PROPERTIES = "PROPERTIES"
    TOTAL_TIME_IN_SECONDS = "TOTAL_TIME_IN_SECONDS"


class ComparisonType(str, Enum):
    """The valid ways to order a result query."""

    DEFAULT = "DEFAULT"
    NUMERIC = "NUMERIC"
    LEXICOGRAPHIC = "LEXICOGRAPHIC"


class QueryResultsBase(JsonModel):
    filter: Optional[str] = None
    """
    The result query filter in Dynamic Linq format.
    Allowed properties in the filter are:
    - `id`: String for the global identifier of the result
    - `status`: String for the status of the result
    - `systemId`: String for the system identifier of the result
    - `hostName`: String for the host name of the result
    - `operator`: String for the operator of the result
    - `serialNumber`: String for the serial number of the result
    - `totalTimeInSeconds`: Float for the total time in seconds of the result
    - `partNumber`: String representing the part number of the result
    - `programName`: String of the program name
    - `startedAt`: ISO-8601 formatted UTC timestamp indicating when the result was started.
    - `updatedAt`: ISO-8601 formatted UTC timestamp indicating when the result was last updated.
    - `keywords`: A list of keyword strings
    - `properties`: A dictionary of additional string to string properties
    - `fileIds`: A list of string ids for files stored in the file service (`/nifile`)
    - `dataTableIds`: A list of string ids for data tables stored in the data frame service (`/nidataframe`)
    - `workspaceId`: String for the workspace identifier of the result
    See [Dynamic Linq](https://github.com/ni/systemlink-OpenAPI-documents/wiki/Dynamic-Linq-Query-Language)
    documentation for more details.
    `"@0"`, `"@1"` etc. can be used in conjunction with the `substitutions` parameter to keep this
    query string more simple and reusable.
    """

    substitutions: Optional[List[str]] = None
    """String substitutions into the `filter`.
    Makes substitutions in the query filter expression. Substitutions for the query expression are
    indicated by non-negative integers that are prefixed with the "at" symbol. Each substitution in
    the given expression will be replaced by the element at the corresponding index (zero-based) in
    this list. For example, "@0" in the filter expression will be replaced with the element at the
    zeroth index of the substitutions list.
    """


class QueryProductsBase(JsonModel):
    product_filter: Optional[str] = None
    """
    The product query filter in Dynamic Linq format.
    Allowed properties in the filter are:
    - `id`: String for the global identifier of the product
    - `partNumber`: String representing the part number of the product
    - `name`: String of the product name
    - `family`: String for the product family
    - `updatedAt`: ISO-8601 formatted UTC timestamp indicating when the product was last updated.
    - `keywords`: A list of keyword strings
    - `properties`: A dictionary of additional string to string properties
    - `fileIds`: A list of string ids for files stored in the file service (`/nifile`)
    See [Dynamic Linq](https://github.com/ni/systemlink-OpenAPI-documents/wiki/Dynamic-Linq-Query-Language)
    documentation for more details.
    `"@0"`, `"@1"` etc. can be used in conjunction with the `substitutions` parameter to keep this
    query string more simple and reusable.
    """

    product_substitutions: Optional[List[str]] = None
    """String substitutions into the `filter`.
    Makes substitutions in the query filter expression. Substitutions for the query expression are
    indicated by non-negative integers that are prefixed with the "at" symbol. Each substitution in
    the given expression will be replaced by the element at the corresponding index (zero-based) in
    this list. For example, "@0" in the filter expression will be replaced with the element at the
    zeroth index of the substitutions list.
    """


class QueryResultsRequest(QueryResultsBase, QueryProductsBase):

    order_by: Optional[ResultField] = Field(None, alias="orderBy")
    """Specifies the fields to use to sort the results.
    By default, results are sorted by `id`
    """
    order_by_key: Optional[str] = Field(None, alias="orderByKey")
    """Specifies the property to use to sort the results when ordering by PROPERTIES.
    Results that do not contain the orderByKey will be considered the smallest value.
    """
    order_by_comparison_type: Optional[ComparisonType] = Field(
        None, alias="orderByComparisonType"
    )
    """An enumeration of comparison types that can be used for ordered queries.
    For non-DEFAULT comparisons, values that cannot be converted will be considered the smallest value.
    """
    descending: Optional[bool] = None
    """Specifies whether to return the results in descending order.
    By default, this value is `false` and results are sorted in ascending order.
    """
    take: Optional[int] = None
    """Maximum number of results to return in the current API response.
    Uses the default if the specified value is negative. The default value is `1000` results.
    """
    continuation_token: Optional[str] = None
    """Allows users to continue the query at the next result that matches the given criteria.
    To retrieve the next page of results, pass the continuation token from the previous
    page in the next request. The service responds with the next page of data and provides a new
    continuation token. To paginate results, continue sending requests with the newest continuation
    token provided in each response.
    """
    return_count: Optional[bool] = None
    """If true, the response will include a count of all results matching the filter.
    By default, this value is `False` and count is not returned. Note that returning the count may
    incur performance penalties as the service may have to do a complete walk of the database to
    compute count. """


class QueryResultValuesRequest(QueryResultsBase):
    field: Optional[ResultField] = None
    """The result field to return for this query."""

    starts_with: Optional[str] = None
    """Only return string parameters prefixed by this value (case sensitive)."""