import pytest
import starlette.status


# noinspection PyUnresolvedReferences
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
async def test_crete_and_read(client):
    # create
    data = {"name": "grocery"}
    resp = await client.post("/categories", json=data)
    resp_obj = resp.json()

    assert resp.status_code == starlette.status.HTTP_200_OK

    category_id = resp_obj["id"]

    # get all
    resp = await client.get("/categories")
    resp_obj = resp.json()
    assert len(resp_obj) == 1
    assert resp_obj == [{"id": category_id, "name": "grocery"}]
    assert resp_obj[0]["id"] == category_id
    assert resp_obj[0]["name"] == "grocery"
