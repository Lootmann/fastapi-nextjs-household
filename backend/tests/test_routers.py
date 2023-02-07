import pytest
import starlette.status


# noinspection PyUnresolvedReferences
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
async def test_create_and_read(client):
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


@pytest.mark.asyncio
async def test_create_and_read_one(client):
    models = []
    # create
    data = {"name": "hoge"}
    resp = await client.post("/categories", json=data)
    models.append(resp.json())

    data = {"name": "hige"}
    resp = await client.post("/categories", json=data)
    models.append(resp.json())

    data = {"name": "hage"}
    resp = await client.post("/categories", json=data)
    models.append(resp.json())

    # get all
    resp = await client.get("/categories")
    resp_obj = resp.json()
    assert len(resp_obj) == 3

    # get one record
    resp = await client.get(f"/categories/{models[0]['id']}")
    resp_obj = resp.json()
    assert resp_obj["id"] == models[0]["id"]
    assert resp_obj["name"] == models[0]["name"]

    resp = await client.get(f"/categories/{models[1]['id']}")
    resp_obj = resp.json()
    assert resp_obj["id"] == models[1]["id"]
    assert resp_obj["name"] == models[1]["name"]

    resp = await client.get(f"/categories/{models[2]['id']}")
    resp_obj = resp.json()
    assert resp_obj["id"] == models[2]["id"]
    assert resp_obj["name"] == models[2]["name"]

    # wrong category id
    resp = await client.get(f"/categories/123")
    resp_obj = resp.json()
    assert resp_obj is None
