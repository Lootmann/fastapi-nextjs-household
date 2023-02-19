import pytest
from fastapi import status

from api.schemas import users as user_schema
from tests.factories import UserFactory
from tests.init_async_client import async_client as client


@pytest.mark.asyncio
class TestGetUser:
    async def test_get_all_users_when_no_users(self, client):
        resp = await client.get("/users")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 0

    async def test_get_all_users(self, client):
        for _ in range(20):
            user = UserFactory.create_user()
            await client.post("/users", json={"name": user.name, "password": user.password})

        resp = await client.get("/users")
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 20

    async def test_get_user_by_id(self, client):
        user = UserFactory.create_user()
        resp = await client.post("/users", json={"name": user.name, "password": user.password})
        user_id = resp.json()["id"]

        resp = await client.get(f"/users/{user_id}")
        assert resp.status_code == status.HTTP_200_OK

        created = user_schema.UserCreateResponse(**resp.json())
        assert created.name == user.name

    async def test_get_user_by_id_which_doesnt_exist(self, client):
        resp = await client.get(f"/users/12345")
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": "User:12345 Not Found"}


@pytest.mark.asyncio
class TestPostUser:
    async def test_post_user(self, client):
        user = UserFactory.create_user()
        resp = await client.post("/users", json={"name": user.name, "password": user.password})
        assert resp.status_code == status.HTTP_201_CREATED

    async def test_post_many_users(self, client):
        user = UserFactory.create_user()
        resp = await client.post("/users", json={"name": user.name, "password": user.password})
        assert resp.status_code == status.HTTP_201_CREATED

    async def test_post_dulicate_user_name(self, client):
        user = UserFactory.create_user()

        await client.post("/users", json={"name": user.name, "password": user.password})
        resp = await client.post("/users", json={"name": user.name, "password": user.password})
        assert resp.status_code == status.HTTP_409_CONFLICT
        assert resp.json() == {"detail": f"Duplicate Username: {user.name}"}

    async def test_post_user_with_invalid_field(self, client):
        resp = await client.post("/users", json={"nama": "hoge", "password": "mogege"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        resp = await client.post("/users", json={"name": "huge", "secret": "magege"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        resp = await client.post("/users", json={"name": "magege"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        resp = await client.post("/users", json={"password": "magege"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
