import pytest
from fastapi import status

from api.schemas import categories as category_schema
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestGetCategory:
    async def test_get_all_categories(self, client):
        # create
        for _ in range(10):
            await client.post("/categories", json={"name": "grocery"})

        # get all
        resp = await client.get("/categories")
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert len(resp_obj) == 10

    async def test_get_category(self, client):
        categories = []

        # create
        resp = await client.post("/categories", json={"name": "hoge"})
        categories.append(category_schema.Category(**resp.json()))

        resp = await client.post("/categories", json={"name": "hige"})
        categories.append(category_schema.Category(**resp.json()))

        resp = await client.post("/categories", json={"name": "hage"})
        categories.append(category_schema.Category(**resp.json()))

        # get one record
        resp = await client.get(f"/categories/{categories[0].id}")
        assert resp.status_code == status.HTTP_200_OK
        category = category_schema.Category(**resp.json())
        assert category.id == categories[0].id
        assert category.name == categories[0].name

        resp = await client.get(f"/categories/{categories[1].id}")
        assert resp.status_code == status.HTTP_200_OK
        category = category_schema.Category(**resp.json())
        assert category.id == categories[1].id
        assert category.name == categories[1].name

        resp = await client.get(f"/categories/{categories[2].id}")
        assert resp.status_code == status.HTTP_200_OK
        category = category_schema.Category(**resp.json())
        assert category.id == categories[2].id
        assert category.name == categories[2].name

    async def test_get_category_which_doesnt_exist(self, client):
        resp = await client.get("/categories/123")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": "Category<123> Not Found"}


@pytest.mark.asyncio
class TestCreateCategory:
    async def test_post_category(self, client):
        resp = await client.post("/categories", json={"name": "hoge"})
        assert resp.status_code == status.HTTP_201_CREATED

    async def test_post_category_which_has_wrong_json_field(self, client):
        resp = await client.post("/categories", json={"my_user_name": "hoge"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
class TestUpdateCategory:
    async def test_put_category(self, client):
        # create
        resp = await client.post(f"/categories", json={"name": "before"})
        assert resp.status_code == status.HTTP_201_CREATED
        created_id = resp.json()["id"]

        # update
        resp = await client.patch(f"/categories/{created_id}", json={"name": "updated :^)"})
        updated_category = category_schema.CategoryCreateResponse(**resp.json())
        assert updated_category.id == created_id
        assert updated_category.name != "before"
        assert updated_category.name == "updated :^)"

    async def test_put_category_which_doesnt_exist(self, client):
        resp = await client.patch("/categories/1", json={"name": "hoge"})
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": "Category<1> Not Found"}


@pytest.mark.asyncio
class TestUpdateCategory:
    async def test_delete_category(self, client):
        # create
        resp = await client.post(f"/categories", json={"name": "new category"})
        assert resp.status_code == status.HTTP_201_CREATED

        resp = await client.get("/categories")
        assert len(resp.json()) == 1

        category_id = resp.json()[0]["id"]

        # delete
        resp = await client.delete(f"/categories/{category_id}")
        assert resp.status_code == status.HTTP_200_OK

        resp = await client.get("/categories")
        assert len(resp.json()) == 0

    async def test_delete_category_which_has_wrong_id(self, client):
        # create
        resp = await client.post(f"/categories", json={"name": "new category"})
        assert resp.status_code == status.HTTP_201_CREATED

        resp = await client.delete("/categories/12345")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": "Category<12345> Not Found"}
