from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.result import ResultClient
from nisystemlink.clients.result.models import (
    QueryResultsRequest,
    QueryResultValuesRequest,
    Result,
    ResultField,
    StatusObject,
    StatusType,
)

program_name = "Example Name"
host_name = "Example Host"


def create_some_results():
    """Create two example results on your server."""
    new_results = [
        Result(
            part_number="Example 123 AA",
            program_name=program_name,
            host_name=host_name,
            status=StatusObject(status_type=StatusType.PASSED, status_name="Passed"),
            keywords=["original keyword"],
            properties={"original property key": "yes"},
        ),
        Result(
            part_number="Example 123 AA1",
            program_name=program_name,
            host_name=host_name,
            status=StatusObject(status_type=StatusType.FAILED, status_name="Failed"),
            keywords=["original keyword"],
            properties={"original property key": "original"},
        ),
    ]
    create_response = client.create_results(new_results)
    return create_response


# Setup the server configuration to point to your instance of SystemLink Enterprise
server_configuration = HttpConfiguration(
    server_uri="https://dev-api.lifecyclesolutions.ni.com",
    api_key="30IUOX8btHdgziA8hgya502zVH8wp2tWGEDH-yMaF6",
)
client = ResultClient(configuration=server_configuration)

# Get all the results using the continuation token in batches of 100 at a time.
response = client.get_results(take=100, return_count=True)
all_results = response.results
while response.continuation_token:
    response = client.get_results(
        take=100, continuation_token=response.continuation_token, return_count=True
    )
    all_results.extend(response.results)

create_response = create_some_results()

# use get for first result created
created_result = client.get_result(create_response.results[0].id)

# Query results without continuation
query_request = QueryResultsRequest(
    filter=f'programName="{program_name}" && hostName="{host_name}"',
    return_count=True,
    order_by=ResultField.HOST_NAME,
)
response = client.query_results(query_request)

# Update the first result that you just created and replace the keywords
updated_result = create_response.results[0]
updated_result.keywords = ["new keyword"]
updated_result.properties = {"new property key": "new value"}
update_response = client.update_results([create_response.results[0]], replace=True)

# Query for just the ids of results that match the family
values_query = QueryResultValuesRequest(
    filter=f'programName="{program_name}"', field=ResultField.ID
)
values_response = client.query_result_values(query=values_query)

# delete each created result individually by id
for result in create_response.results:
    client.delete_result(result.id)

# Create some more and delete them with a single call to delete.
create_response = create_some_results()
client.delete_results([result.id for result in create_response.results])
