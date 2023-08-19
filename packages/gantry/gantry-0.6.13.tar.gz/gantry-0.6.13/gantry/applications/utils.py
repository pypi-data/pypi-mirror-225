from gantry.api_client import APIClient


def get_models_to_vendor(api_client: APIClient):
    models_and_vendors = api_client.request(
        "GET",
        "/api/v1/sandbox/models",
        raise_for_status=True,
    )["data"]

    return {each["name"]: each["vendor"] for each in models_and_vendors}
