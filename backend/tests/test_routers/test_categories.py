import pytest
from fastapi import status

from api.schemas import categories as category_schema
from tests.factories import UserFactory, create_access_token, random_string
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestGetCategory:
    async def test_get_all_categories(self, client, login_fixture):
        user, headers = await login_fixture

        # create
        for _ in range(10):
            await client.post(
                "/categories",
                json={"name": random_string(), "user_id": user.id},
                headers=headers,
            )

        # get all
        resp = await client.get("/categories", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        resp_obj = resp.json()
        assert len(resp_obj) == 10

    async def test_get_category(self, client, login_fixture):
        _, headers = await login_fixture

        categories = []

        # create
        for _ in range(3):
            resp = await client.post("/categories", json={"name": random_string()}, headers=headers)
            categories.append(category_schema.CategoryCreateResponse(**resp.json()))

        # get one record
        for i in range(3):
            resp = await client.get(f"/categories/{categories[i].id}", headers=headers)
            assert resp.status_code == status.HTTP_200_OK
            category = category_schema.Category(**resp.json())
            assert category.id == categories[i].id
            assert category.name == categories[i].name

    async def test_get_category_which_doesnt_exist(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.get("/categories/123", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": "Category<123> Not Found"}


@pytest.mark.asyncio
class TestCreateCategory:
    async def test_post_category(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.post("/categories", json={"name": random_string()}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

    async def test_post_category_which_has_wrong_json_field(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.post("/categories", json={"my_user_name": "hoge"}, headers=headers)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
class TestUpdateCategory:
    async def test_put_category(self, client, login_fixture):
        _, headers = await login_fixture

        # create
        resp = await client.post(f"/categories", json={"name": "before"}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED
        created_id = resp.json()["id"]

        # update
        resp = await client.patch(
            f"/categories/{created_id}", json={"name": "updated :^)"}, headers=headers
        )
        assert resp.status_code == status.HTTP_200_OK

        updated_category = category_schema.CategoryCreateResponse(**resp.json())
        assert updated_category.id == created_id
        assert updated_category.name != "before"
        assert updated_category.name == "updated :^)"

    async def test_put_category_which_doesnt_exist(self, client, login_fixture):
        _, headers = await login_fixture

        resp = await client.patch("/categories/1", json={"name": "hoge"}, headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": "Category<1> Not Found"}

    async def test_put_category_by_invalid_loggedin_user(self, client, login_fixture):
        _, headers = await login_fixture

        # create category
        resp = await client.post(f"/categories", json={"name": "***"}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED
        category_id = resp.json()["id"]

        # create new user
        user = UserFactory.create_user()
        await client.post("/users", json={"name": user.name, "password": user.password})
        new_headers = await create_access_token(client, username=user.name, password=user.password)

        # update category by new user
        resp = await client.patch(
            f"/categories/{category_id}", json={"name": "updated :^)"}, headers=new_headers
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": "Not Authenticated"}


@pytest.mark.asyncio
class TestDeleteCategory:
    async def test_delete_category(self, client, login_fixture):
        _, headers = await login_fixture

        # create
        resp = await client.post(f"/categories", json={"name": "new category"}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        resp = await client.get("/categories", headers=headers)
        assert len(resp.json()) == 1

        category_id = resp.json()[0]["id"]

        # delete
        resp = await client.delete(f"/categories/{category_id}", headers=headers)
        assert resp.status_code == status.HTTP_200_OK

        resp = await client.get("/categories", headers=headers)
        assert len(resp.json()) == 0

    async def test_delete_category_which_has_wrong_id(self, client, login_fixture):
        _, headers = await login_fixture

        # create
        resp = await client.post(f"/categories", json={"name": "new category"}, headers=headers)
        assert resp.status_code == status.HTTP_201_CREATED

        resp = await client.delete("/categories/12345", headers=headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": "Category<12345> Not Found"}
