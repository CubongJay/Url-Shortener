import json
import os
import secrets
import string

import azure.functions as func
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.data.tables import TableClient

CONN_STR = os.getenv("STORAGE_CONNECTION_STRING")
table_client = TableClient.from_connection_string(CONN_STR, table_name="shortlinks")

app = func.FunctionApp()


def generate_short_code(length: int = 6) -> str:
    alphabet = string.ascii_letters + string.digits

    return "".join(secrets.choice(alphabet) for _ in range(length))


@app.route(route="shorten", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def shorten_url(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    long_url = req_body.get("url")

    if not long_url:
        return func.HttpResponse("Missing 'url' field", status_code=400)

    if not long_url.startswith("https://"):
        return func.HttpResponse("Invalid URL", status_code=400)

    for attempt in range(3):
        code = generate_short_code()
        entity = {"PartitionKey": "url", "RowKey": code, "long_url": long_url}

        try:
            table_client.create_entity(entity=entity)
            break
        except ResourceExistsError:
            continue
    else:
        return func.HttpResponse("Could not generate unique code", status_code=500)
    base = req.url.split("/api/")[0]
    short_url = f"{base}/api/{code}"
    return func.HttpResponse(
        json.dumps({"short_url": short_url}),
        mimetype="application/json",
        status_code=200,
    )


@app.route(route="{code}", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def get_long_url(req: func.HttpRequest) -> func.HttpResponse:
    code = req.route_params.get("code")
    try:
        entity = table_client.get_entity(partition_key="url", row_key=code)

    except ResourceNotFoundError:
        return func.HttpResponse(
            f"No URL matches the given code: {code}", status_code=404
        )

    return func.HttpResponse(status_code=302, headers={"Location": entity["long_url"]})
