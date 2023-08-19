import responses

from gantry.applications import utils

HOST = "https://test-api"


def test_get_models_to_vendors(test_api_client):
    with responses.RequestsMock() as resp:
        resp.add(
            resp.GET,
            f"{HOST}/api/v1/sandbox/models",
            json={
                "response": "ok",
                "data": [
                    {
                        "name": "foo",
                        "vendor": "bar",
                    },
                    {
                        "name": "baz",
                        "vendor": "bar",
                    },
                    {
                        "name": "fred",
                        "vendor": "qux",
                    },
                ],
            },
            headers={"Content-Type": "application/json"},
        )

        assert utils.get_models_to_vendor(test_api_client) == {
            "foo": "bar",
            "baz": "bar",
            "fred": "qux",
        }
